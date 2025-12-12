from botorch.test_functions.base import MultiObjectiveTestProblem
from botorch.utils.multi_objective.hypervolume import Hypervolume
from botorch.utils.multi_objective.pareto import is_non_dominated
from typing import Callable, Optional
from torch import Tensor
import torch 


class FastMoboProblem(MultiObjectiveTestProblem):
    """Custom multi-objective problem wrapper with CUDA support"""

    def __init__(self, 
                 objective_func: Callable[[Tensor], Tensor],
                 bounds: torch.Tensor,
                 ref_point: torch.Tensor,
                 num_objectives: int,
                 noise_std: Optional[torch.Tensor] = None,
                 negate: bool = True,
                 max_hv: Optional[float] = None,
                 device: Optional[str] = None,
                 dtype: torch.dtype = torch.double):
        """
        Args:
            objective_func: Function that takes x (n_points x dim) and returns objectives (n_points x num_obj)
            bounds: 2 x dim tensor with [lower_bounds, upper_bounds]
            ref_point: Reference point for hypervolume calculation
            num_objectives: Number of objectives
            noise_std: Standard deviation of observation noise
            negate: Whether to negate objectives (for maximization)
            max_hv: Maximum achievable hypervolume (for plotting)
            device: Device to use ('cuda' or 'cpu'). If None, auto-detects CUDA availability
            dtype: Data type for tensors
        """
        # Auto-detect device if not specified
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.device = torch.device(device)
        self.dtype = dtype
        self.tkwargs = {"device": self.device, "dtype": dtype}
        
        self.objective_func = objective_func
        self.num_objectives = num_objectives
        self.negate = negate
        self._max_hv = max_hv
        
        # Move all tensors to the correct device
        self.bounds = bounds.to(**self.tkwargs)
        self.ref_point = ref_point.to(**self.tkwargs)
        
        if noise_std is not None:
            self.noise_std = noise_std.to(**self.tkwargs)
        else:
            self.noise_std = torch.zeros(num_objectives, **self.tkwargs)
        
        self.dim = bounds.shape[1]
    
    @property
    def max_hv(self) -> float:
        """Get maximum hypervolume (estimated or provided)"""
        if self._max_hv is not None:
            return self._max_hv
        else:
            return self._estimate_max_hv(
                self.objective_func, 
                self.bounds, 
                self.ref_point,
                device=self.device,
                dtype=self.dtype
            )
    
    @staticmethod
    def _estimate_max_hv(
        objective_func: Callable, 
        bounds: torch.Tensor, 
        ref_point: torch.Tensor, 
        n_samples: int = 10000,
        device: Optional[torch.device] = None,
        dtype: torch.dtype = torch.double
    ) -> float:
        """Estimate maximum hypervolume using random sampling"""
        if device is None:
            device = bounds.device
        
        tkwargs = {"device": device, "dtype": dtype}
        
        # Ensure bounds and ref_point are on the correct device
        bounds = bounds.to(**tkwargs)
        ref_point = ref_point.to(**tkwargs)
        
        # Uniform random samples in input space
        X = torch.rand(n_samples, bounds.shape[1], **tkwargs)
        X = X * (bounds[1] - bounds[0]) + bounds[0]
        
        Y = objective_func(X)
        
        # Keep only non-dominated solutions
        mask = is_non_dominated(Y)
        pareto_Y = Y[mask]
        
        if pareto_Y.shape[0] == 0:
            return 0.0
        
        # Compute HV of Pareto front
        hv = Hypervolume(ref_point=ref_point)
        return hv.compute(pareto_Y).item()

    def __call__(self, X: Tensor) -> Tensor:
        """Evaluate the objective function"""
        return self._evaluate_true(X)
    
    def _evaluate_true(self, X: Tensor) -> Tensor:
        """Evaluate true objective values"""
        # Ensure X is on the correct device
        X = X.to(**self.tkwargs)
        
        obj = self.objective_func(X)
        
        # Ensure output is on the correct device
        obj = obj.to(**self.tkwargs)
        
        return -obj if self.negate else obj
    
    def gen_pareto_front(self, n: int) -> Tensor:
        """Generate Pareto front approximation
        
        Args:
            n: Number of points to return
            
        Returns:
            Tensor of shape (n, num_objectives) representing the Pareto front
        """
        # Generate random samples on the correct device
        X = torch.rand(5000, self.dim, **self.tkwargs)
        X = X * (self.bounds[1] - self.bounds[0]) + self.bounds[0]
        
        Y = self.objective_func(X)
        Y = Y.to(**self.tkwargs)
        
        # Find non-dominated points
        mask = is_non_dominated(Y)
        pareto_Y = Y[mask]
        
        if pareto_Y.shape[0] == 0:
            # If no non-dominated points found, return random points
            return torch.rand(n, self.num_objectives, **self.tkwargs)
        
        # If too many points, downsample to n evenly spaced points
        if pareto_Y.shape[0] > n:
            # Sort by first objective for more even spacing
            sorted_indices = torch.argsort(pareto_Y[:, 0])
            pareto_Y = pareto_Y[sorted_indices]
            
            # Select n evenly spaced points
            idx = torch.linspace(0, pareto_Y.shape[0] - 1, n, **self.tkwargs).long()
            pareto_Y = pareto_Y[idx]
        elif pareto_Y.shape[0] < n:
            # If too few points, pad with duplicates of the last point
            num_to_pad = n - pareto_Y.shape[0]
            padding = pareto_Y[-1].unsqueeze(0).repeat(num_to_pad, 1)
            pareto_Y = torch.cat([pareto_Y, padding], dim=0)
        
        return pareto_Y
    
    def to(self, device: torch.device) -> 'FastMoboProblem':
        """Move problem to a different device"""
        self.device = device
        self.tkwargs = {"device": device, "dtype": self.dtype}
        self.bounds = self.bounds.to(**self.tkwargs)
        self.ref_point = self.ref_point.to(**self.tkwargs)
        self.noise_std = self.noise_std.to(**self.tkwargs)
        return self
    
    def set_bounds(self, bounds: torch.Tensor):
        """Update problem bounds"""
        self.bounds = bounds.to(**self.tkwargs)
        self.dim = bounds.shape[1]
    
    def set_ref_point(self, ref_point: torch.Tensor):
        """Update reference point"""
        self.ref_point = ref_point.to(**self.tkwargs)
    
    def set_noise_std(self, noise_std: torch.Tensor):
        """Update noise standard deviation"""
        self.noise_std = noise_std.to(**self.tkwargs)
