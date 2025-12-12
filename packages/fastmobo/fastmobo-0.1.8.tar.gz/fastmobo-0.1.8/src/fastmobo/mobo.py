from __future__ import annotations
from botorch.utils.multi_objective.box_decompositions.non_dominated import FastNondominatedPartitioning
from botorch.utils.multi_objective.box_decompositions.dominated import DominatedPartitioning
from botorch.utils.multi_objective.scalarization import get_chebyshev_scalarization
from gpytorch.mlls.sum_marginal_log_likelihood import SumMarginalLogLikelihood
from botorch.utils.sampling import sample_simplex, draw_sobol_samples
from botorch.utils.transforms import unnormalize, normalize
from botorch.acquisition.multi_objective.logei import (
    qLogNoisyExpectedHypervolumeImprovement,
    qLogExpectedHypervolumeImprovement,
)
from botorch.optim.optimize import optimize_acqf, optimize_acqf_list
from botorch.acquisition.logei import qLogNoisyExpectedImprovement
from botorch.models.model_list_gp_regression import ModelListGP
from botorch.acquisition.objective import GenericMCObjective
from botorch.exceptions import BadInitialCandidatesWarning
from botorch.models.transforms.outcome import Standardize
from botorch.sampling.normal import SobolQMCNormalSampler
from botorch.models.gp_regression import SingleTaskGP
from botorch.models.model import Model as GPModel
from fastmobo.problems import FastMoboProblem
from botorch.sampling.base import MCSampler
from botorch import fit_gpytorch_mll
from dataclasses import dataclass
from typing import Optional, Any, TYPE_CHECKING
import matplotlib.pyplot as plt
from loguru import logger
import numpy as np
import warnings
import torch
import time

if TYPE_CHECKING:
    from botorch.models.model import Model as BotorchModel
    from gpytorch.module import Module as GPyTorchModule

warnings.filterwarnings("ignore", category=BadInitialCandidatesWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


@dataclass
class OptimizationResult:
    """Container for optimization results with comprehensive reporting"""
    hypervolumes: dict[str, list[float]]
    train_x: dict[str, torch.Tensor]
    train_obj: dict[str, torch.Tensor]
    train_obj_true: dict[str, torch.Tensor]
    n_iterations: int
    total_time: float
    n_initial: int = 0
    batch_size: int = 1
    
    def __post_init__(self):
        """Calculate batch size and n_initial if not provided"""
        if self.n_initial == 0 or self.batch_size == 1:
            first_method = list(self.train_x.keys())[0]
            total_points = len(self.train_x[first_method])
            self.n_initial = total_points // (self.n_iterations + 1)
            self.batch_size = (total_points - self.n_initial) // max(self.n_iterations, 1)
    
    def get_summary_report(self) -> dict[str, Any]:
        """Generate comprehensive summary report"""
        report = {
            "optimization_config": {
                "n_iterations": self.n_iterations,
                "n_initial": self.n_initial,
                "batch_size": self.batch_size,
                "total_time": self.total_time,
                "time_per_iteration": self.total_time / max(self.n_iterations, 1)
            },
            "methods": {},
            "comparisons": {}
        }
        
        # Per-method statistics
        for method, hvs in self.hypervolumes.items():
            final_hv = hvs[-1]
            initial_hv = hvs[0]
            improvement = final_hv - initial_hv
            improvement_pct = (improvement / abs(initial_hv) * 100) if initial_hv != 0 else 0
            
            #  convergence rate (slope of last 30% of iterations)
            n_tail = max(1, len(hvs) // 3)
            tail_hvs = hvs[-n_tail:]
            if len(tail_hvs) > 1:
                convergence_rate = (tail_hvs[-1] - tail_hvs[0]) / len(tail_hvs)
            else:
                convergence_rate = 0
            
            report["methods"][method] = {
                "final_hypervolume": float(final_hv),
                "initial_hypervolume": float(initial_hv),
                "improvement": float(improvement),
                "improvement_percent": float(improvement_pct),
                "convergence_rate": float(convergence_rate),
                "all_hypervolumes": [float(h) for h in hvs],
                "total_evaluations": len(self.train_x[method])
            }
        
        if len(self.hypervolumes) > 1:
            final_hvs = {m: hvs[-1] for m, hvs in self.hypervolumes.items()}
            best_method = max(final_hvs, key=final_hvs.get)
            worst_method = min(final_hvs, key=final_hvs.get)
            
            report["comparisons"] = {
                "best_method": best_method,
                "worst_method": worst_method,
                "best_hypervolume": float(final_hvs[best_method]),
                "worst_hypervolume": float(final_hvs[worst_method]),
                "performance_gap": float(final_hvs[best_method] - final_hvs[worst_method]),
                "rankings": sorted(final_hvs.items(), key=lambda x: x[1], reverse=True)
            }
            
            win_counts = {m: 0 for m in self.hypervolumes.keys()}
            for i in range(len(hvs)):
                iter_hvs = {m: hvs[i] for m, hvs in self.hypervolumes.items()}
                winner = max(iter_hvs, key=iter_hvs.get)
                win_counts[winner] += 1
            
            report["comparisons"]["iteration_wins"] = win_counts
        
        return report
    
    def plot_convergence(self, problem: Optional[FastMoboProblem] = None, save_path: Optional[str] = None):
        """Plot hypervolume convergence with improved visualization"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        iterations = list(range(self.n_iterations + 1))
        
        for method, hvs in self.hypervolumes.items():
            if problem and hasattr(problem, 'max_hv'):
                log_hv_diff = np.log10(np.maximum(problem.max_hv - np.asarray(hvs), 1e-10))
                ax.plot(iterations, log_hv_diff, label=method, linewidth=2, marker='o')
                ax.set_ylabel("Log Hypervolume Difference", fontsize=12)
            else:
                ax.plot(iterations, hvs, label=method, linewidth=2, marker='o')
                ax.set_ylabel("Hypervolume", fontsize=12)
        
        ax.set_xlabel("Iteration", fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_title("Optimization Convergence", fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_objectives(self, 
                        objective_names: Optional[list[str]] = None,
                        problem: Optional[FastMoboProblem] = None,
                        save_path: Optional[str] = None):
        """Plot objective space exploration with proper color mapping
        
        Args:
            objective_names: List of objective names (e.g., ['Cost', 'Accuracy'])
                            If None, tries to get from problem.objective_names, 
                            otherwise uses generic labels
            problem: FastMoboProblem instance to extract objective names from
            save_path: Path to save the figure
        """
        n_methods = len(self.train_obj_true)
        fig, axes = plt.subplots(1, n_methods, figsize=(6*n_methods, 5), 
                                sharex=True, sharey=True)
        if n_methods == 1:
            axes = [axes]

        cm = plt.get_cmap("viridis")
        norm = plt.Normalize(0, self.n_iterations)
        
        # Determine axis labels with priority: objective_names > problem.objective_names > default
        if objective_names is None:
            if problem is not None and hasattr(problem, 'objective_names'):
                objective_names = problem.objective_names
            else:
                objective_names = [f"Objective {i+1}" for i in range(2)]
        
        if len(objective_names) < 2:
            raise ValueError(f"Need at least 2 objective names, got {len(objective_names)}")

        for i, (method, train_obj) in enumerate(self.train_obj_true.items()):
            obj_np = train_obj.cpu().numpy()
            n_total = len(obj_np)
            
            iteration_labels = np.zeros(n_total)
            idx = 0
            iteration_labels[:self.n_initial] = 0  
            idx = self.n_initial
            
            for iter_num in range(1, self.n_iterations + 1):
                end_idx = min(idx + self.batch_size, n_total)
                iteration_labels[idx:end_idx] = iter_num
                idx = end_idx
            
            scatter = axes[i].scatter(
                obj_np[:, 0], obj_np[:, 1],
                c=iteration_labels,
                cmap=cm,
                norm=norm,
                s=50,
                alpha=0.6,
                edgecolors='black',
                linewidths=0.5
            )
            
            axes[i].set_title(method, fontsize=12, fontweight='bold')
            axes[i].set_xlabel(objective_names[0], fontsize=11)
            if i == 0:
                axes[i].set_ylabel(objective_names[1], fontsize=11)
            axes[i].grid(True, alpha=0.3)

        fig.subplots_adjust(right=0.9)
        cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
        cbar = fig.colorbar(scatter, cax=cbar_ax)
        cbar.ax.set_ylabel("Iteration", rotation=270, labelpad=20, fontsize=11)

        plt.suptitle("Objective Space Exploration", fontsize=14, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()

class OptimizationStorage:
    """Efficient storage for optimization data"""
    
    def __init__(self, initial_x: torch.Tensor, initial_obj: torch.Tensor):
        self.train_x = initial_x.clone()
        self.train_obj = initial_obj.clone()
        self.train_obj_true = initial_obj.clone()
    
    def append_data(self, new_x: torch.Tensor, new_obj: torch.Tensor, new_obj_true: torch.Tensor):
        """Append new optimization data"""
        self.train_x = torch.cat([self.train_x, new_x])
        self.train_obj = torch.cat([self.train_obj, new_obj])
        self.train_obj_true = torch.cat([self.train_obj_true, new_obj_true])


class FastMobo:
    """Fast Multi-Objective Bayesian Optimization"""
    
    SUPPORTED_ACQ_FUNCS = ['qEHVI', 'qNEHVI', 'qNParEGO', 'Random']

    def __init__(self, 
                 problem: FastMoboProblem,
                 train_x: Optional[torch.Tensor] = None,
                 train_y: Optional[torch.Tensor] = None,
                 acquisition_functions: Optional[list[str]] = None,
                 batch_size: int = 4,
                 num_restarts: int = 10,
                 raw_samples: int = 512,
                 mc_samples: int = 64,
                 maxiter: int = 200,
                 batch_limit: int = 5,
                 n_initial: Optional[int] = None,
                 device: str = "cpu", # Legacy
                 dtype: torch.dtype = torch.double):
        
        self.dtype = dtype
        self.tkwargs = {"device": torch.device("cuda" if torch.cuda.is_available() else "cpu") , 
                        "dtype": dtype}
        self.problem = problem
        
        if acquisition_functions is None:
            acquisition_functions = ['qEHVI', 'qNEHVI', 'qNParEGO', 'Random']
        
        invalid_acqs = set(acquisition_functions) - set(self.SUPPORTED_ACQ_FUNCS)
        if invalid_acqs:
            raise ValueError(f"Unsupported acquisition functions: {invalid_acqs}. "
                           f"Supported: {self.SUPPORTED_ACQ_FUNCS}")
        
        self.acquisition_functions = acquisition_functions
        
        self.batch_size = batch_size
        self.num_restarts = num_restarts
        self.raw_samples = raw_samples
        self.mc_samples = mc_samples
        self.maxiter = maxiter
        self.batch_limit = batch_limit
        self.n_initial = n_initial or 2 * (self.problem.dim + 1)
        
        self.standard_bounds = torch.zeros(2, self.problem.dim, **self.tkwargs)
        self.standard_bounds[1] = 1
        
        self.noise_se = self.problem.noise_std.to(**self.tkwargs)
        
        self.initial_data = None
        if train_x is not None and train_y is not None:
            self._validate_and_set_initial_data(train_x, train_y)
        
        self.result = None
    
    def _validate_and_set_initial_data(self, train_x: torch.Tensor, train_y: torch.Tensor):
        """Validate and set initial training data"""
        train_x = train_x.to(**self.tkwargs)
        train_y = train_y.to(**self.tkwargs)
        
        if train_x.shape[-1] != self.problem.dim:
            raise ValueError(f"Input dimension mismatch: expected {self.problem.dim}, got {train_x.shape[-1]}")
        
        if train_y.shape[-1] != self.problem.num_objectives:
            raise ValueError(f"Output dimension mismatch: expected {self.problem.num_objectives}, got {train_y.shape[-1]}")
        
        if train_x.shape[0] != train_y.shape[0]:
            raise ValueError(f"Batch size mismatch: train_x has {train_x.shape[0]} points, train_y has {train_y.shape[0]}")
        
        self.initial_data = (train_x, train_y)

    def generate_initial_data(self, n: Optional[int] = None) -> tuple[torch.Tensor, torch.Tensor]:
        """Generate initial training data"""
        if n is None:
            n = self.n_initial
            
        train_x = draw_sobol_samples(
            bounds=self.problem.bounds, n=n, q=1
        ).squeeze(1)
        train_y_true = self.problem(train_x)
        train_y_noisy = train_y_true + torch.randn_like(train_y_true, **self.tkwargs) * self.noise_se
        return train_x, train_y_noisy

    def get_initial_data(self) -> tuple[torch.Tensor, torch.Tensor]:
        """Get initial training data"""
        if self.initial_data is not None:
            return self.initial_data
        return self.generate_initial_data()
    
    def initialize_model(self, train_x: torch.Tensor, train_y: torch.Tensor):
        """Initialize GP model"""
        bounds = self.problem.bounds.to(train_x.device)
        train_x_normalized = normalize(train_x, bounds)
        
        models = []
        for i in range(train_y.shape[-1]):
            train_y_i = train_y[..., i:i+1]
            train_y_var = torch.full_like(train_y_i, self.noise_se[i] ** 2)
            models.append(
                SingleTaskGP(
                    train_x_normalized,
                    train_y_i,
                    train_y_var,
                    outcome_transform=Standardize(m=1),
                )
            )
        model = ModelListGP(*models)
        mll = SumMarginalLogLikelihood(model.likelihood, model)
        return mll, model

    
    def _generate_new_candidates(self, new_x: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        """Generate new objective values for candidates"""
        new_obj_true = self.problem(new_x)
        new_obj = new_obj_true + torch.randn_like(new_obj_true) * self.noise_se
        return new_obj, new_obj_true
    
    def optimize_qehvi(self, model: GPModel, train_x: torch.Tensor, train_obj: torch.Tensor, sampler: MCSampler) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Optimize qEHVI acquisition function"""
        with torch.no_grad():
            pred = model.posterior(normalize(train_x, self.problem.bounds)).mean
        
        partitioning = FastNondominatedPartitioning(
            ref_point=self.problem.ref_point,
            Y=pred,
        )
        
        acq_func = qLogExpectedHypervolumeImprovement(
            model=model,
            ref_point=self.problem.ref_point,
            partitioning=partitioning,
            sampler=sampler,
        )
        
        candidates, _ = optimize_acqf(
            acq_function=acq_func,
            bounds=self.standard_bounds,
            q=self.batch_size,
            num_restarts=self.num_restarts,
            raw_samples=self.raw_samples,
            options={"batch_limit": self.batch_limit, "maxiter": self.maxiter},
            sequential=True,
        )
        
        new_x = unnormalize(candidates.detach(), bounds=self.problem.bounds)
        new_obj, new_obj_true = self._generate_new_candidates(new_x)
        return new_x, new_obj, new_obj_true
    
    def optimize_qnehvi(self, model: GPModel, train_x: torch.Tensor, train_obj: torch.Tensor, sampler: MCSampler) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Optimize qNEHVI acquisition function"""
        acq_func = qLogNoisyExpectedHypervolumeImprovement(
            model=model,
            ref_point=self.problem.ref_point.tolist(),
            X_baseline=normalize(train_x, self.problem.bounds),
            prune_baseline=True,
            sampler=sampler,
        )
        
        candidates, _ = optimize_acqf(
            acq_function=acq_func,
            bounds=self.standard_bounds,
            q=self.batch_size,
            num_restarts=self.num_restarts,
            raw_samples=self.raw_samples,
            options={"batch_limit": self.batch_limit, "maxiter": self.maxiter},
            sequential=True,
        )
        
        new_x = unnormalize(candidates.detach(), bounds=self.problem.bounds)
        new_obj, new_obj_true = self._generate_new_candidates(new_x)
        return new_x, new_obj, new_obj_true
    
    def optimize_qnparego(self, model: GPModel, train_x: torch.Tensor, train_obj: torch.Tensor, sampler: MCSampler) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Optimize qNParEGO acquisition function"""
        train_x_norm = normalize(train_x, self.problem.bounds)
        with torch.no_grad():
            pred = model.posterior(train_x_norm).mean
        
        acq_func_list = []
        for _ in range(self.batch_size):
            weights = sample_simplex(self.problem.num_objectives, **self.tkwargs).squeeze()
            objective = GenericMCObjective(
                get_chebyshev_scalarization(weights=weights, Y=pred)
            )
            acq_func = qLogNoisyExpectedImprovement(
                model=model,
                objective=objective,
                X_baseline=train_x_norm,
                sampler=sampler,
                prune_baseline=True,
            )
            acq_func_list.append(acq_func)
        
        candidates, _ = optimize_acqf_list(
            acq_function_list=acq_func_list,
            bounds=self.standard_bounds,
            num_restarts=self.num_restarts,
            raw_samples=self.raw_samples,
            options={"batch_limit": self.batch_limit, "maxiter": self.maxiter},
        )
        
        new_x = unnormalize(candidates.detach(), bounds=self.problem.bounds)
        new_obj, new_obj_true = self._generate_new_candidates(new_x)
        return new_x, new_obj, new_obj_true
    
    def optimize_random(self) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Generate random samples"""
        train_x, train_y = self.generate_initial_data(n=self.batch_size)
        train_y_true = self.problem(train_x)
        return train_x, train_y, train_y_true
    
    def optimize(self, n_iterations: int = 5, verbose: bool = True) -> OptimizationResult:
        """Run multi-objective Bayesian optimization"""
        start_time = time.time()
        
        initial_data = self.get_initial_data()
        train_x_init, train_obj_init = initial_data
        train_obj_true_init = self.problem(train_x_init)
        
        results: dict[str, OptimizationStorage] = {}
        models = {}
        mlls = {}
        hypervolumes = {}
        
        for acq_name in self.acquisition_functions:
            results[acq_name] = OptimizationStorage(train_x_init, train_obj_init)
            results[acq_name].train_obj_true = train_obj_true_init.clone()
            
            if acq_name != 'Random':
                mll, model = self.initialize_model(train_x_init, train_obj_init)
                models[acq_name] = model
                mlls[acq_name] = mll
            
            bd = DominatedPartitioning(
                ref_point=self.problem.ref_point, 
                Y=train_obj_true_init
            )
            volume = bd.compute_hypervolume().item()
            hypervolumes[acq_name] = [volume]
        
        for iteration in range(1, n_iterations + 1):
            if verbose:
                logger.info(f"Iteration {iteration}/{n_iterations}")
            
            t0 = time.monotonic()
            
            for acq_name in self.acquisition_functions:
                if acq_name != 'Random':
                    try:
                        fit_gpytorch_mll(mlls[acq_name])
                    except Exception as e:
                        if verbose:
                            logger.error(f"Failed to fit model for {acq_name}: {e}")
            
            samplers = {
                acq_name: SobolQMCNormalSampler(sample_shape=torch.Size([self.mc_samples]))
                for acq_name in self.acquisition_functions if acq_name != 'Random'
            }
            
            for acq_name in self.acquisition_functions:
                try:
                    storage = results[acq_name]
                    
                    if acq_name == 'qEHVI':
                        new_x, new_obj, new_obj_true = self.optimize_qehvi(
                            models[acq_name], storage.train_x, storage.train_obj, samplers[acq_name]
                        )
                    elif acq_name == 'qNEHVI':
                        new_x, new_obj, new_obj_true = self.optimize_qnehvi(
                            models[acq_name], storage.train_x, storage.train_obj, samplers[acq_name]
                        )
                    elif acq_name == 'qNParEGO':
                        new_x, new_obj, new_obj_true = self.optimize_qnparego(
                            models[acq_name], storage.train_x, storage.train_obj, samplers[acq_name]
                        )
                    elif acq_name == 'Random':
                        new_x, new_obj, new_obj_true = self.optimize_random()
                    
                    storage.append_data(new_x, new_obj, new_obj_true)
                    
                    bd = DominatedPartitioning(
                        ref_point=self.problem.ref_point,
                        Y=storage.train_obj_true
                    )
                    volume = bd.compute_hypervolume().item()
                    hypervolumes[acq_name].append(volume)
                    
                    if acq_name != 'Random':
                        mll, model = self.initialize_model(storage.train_x, storage.train_obj)
                        models[acq_name] = model
                        mlls[acq_name] = mll
                        
                except Exception as e:
                    if verbose:
                        logger.error(f"Failed optimization for {acq_name}: {e}")
                    hypervolumes[acq_name].append(hypervolumes[acq_name][-1])
            
            t1 = time.monotonic()
            
            if verbose:
                hv_str = ", ".join([
                    f"{name}: {hypervolumes[name][-1]:.3f}" 
                    for name in self.acquisition_functions
                ])
                logger.info(f"HVs - {hv_str}, time: {t1-t0:.2f}s")
        
        total_time = time.time() - start_time
        
        self.result = OptimizationResult(
            hypervolumes=hypervolumes,
            train_x={name: results[name].train_x for name in self.acquisition_functions},
            train_obj={name: results[name].train_obj for name in self.acquisition_functions},
            train_obj_true={name: results[name].train_obj_true for name in self.acquisition_functions},
            n_iterations=n_iterations,
            total_time=total_time,
            n_initial=len(train_x_init),
            batch_size=self.batch_size
        )
        
        if verbose:
            logger.success(f"Optimization completed in {total_time:.2f}s")
        
        return self.result