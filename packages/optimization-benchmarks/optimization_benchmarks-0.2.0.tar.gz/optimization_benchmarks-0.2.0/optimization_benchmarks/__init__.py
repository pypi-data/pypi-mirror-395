"""
Optimization Benchmark Functions Package

A comprehensive collection of standard benchmark functions for evaluating
optimization algorithms. This package provides Python implementations of
classical test functions widely used in the optimization research community.

Version 0.1.1 adds metadata support for easy benchmarking with bounds,
dimensions, and known minima for all functions.

Mathematical formulations are based on well-established definitions from:
- MVF C library[1]
- Virtual Library of Simulation Experiments[2]
- Academic optimization literature[3]

References:
-----------
[1] Adorio, E. P. (2005). MVF - Multivariate Test Functions Library in C.
    University of the Philippines Diliman.
[2] Surjanovic, S. & Bingham, D. (2013). Virtual Library of Simulation Experiments.
    Simon Fraser University.
[3] Jamil, M., & Yang, X. S. (2013). A literature survey of benchmark functions
    for global optimization problems. International Journal of Mathematical
    Modelling and Numerical Optimisation, 4(2), 150-194.

License: MIT
"""

__version__ = "0.2.0"
__author__ = "AK Rahul"
__license__ = "MIT"


# Import all benchmark functions
from .functions import (
    ackley, rastrigin, rastrigin2, griewank, levy, michalewicz, schwefel2_26,
    sphere, sphere2, rosenbrock, rosenbrock_ext1, rosenbrock_ext2, sum_squares,
    hyperellipsoid, schwefel1_2, schwefel2_21, schwefel2_22, schwefel3_2,
    step, step2, maxmod, multimod, katsuura,
    beale, booth, matyas, himmelblau, easom, goldstein_price,
    branin, branin2, camel3, camel6, bohachevsky1, bohachevsky2,
    schaffer1, schaffer2, leon, trecanni, mccormick, eggholder,
    chichinadze, hosaki, zettl, holzman1, holzman2, langerman,
    stretched_v, trefethen4, box_betts, colville, corana, kowalik, exp2, gear
)

# Import metadata utilities
from .metadata import (
    BENCHMARK_SUITE,
    get_all_functions,
    get_function_info,
    get_bounds,
    get_function_list
)

# Import NEW utilities (v0.2.0)
from .utils import (
    normalize_bounds,
    generate_random_point,
    check_bounds,
    scale_to_unit,
    scale_from_unit,
    clip_to_bounds,
    get_bounds_range,
    get_bounds_center,
    generate_grid_points,
    calculate_distance_to_optimum
)

# Import NEW benchmarking tools (v0.2.0)
from .benchmarking import (
    BenchmarkRunner,
    quick_benchmark
)

# Conditional import of visualization (requires matplotlib)
try:
    from .visualization import (
        plot_function_2d,
        plot_function_3d,
        plot_convergence,
        plot_trajectory_2d,
        plot_algorithm_comparison,
        plot_benchmark_summary
    )
    __visualization_available__ = True
except ImportError:
    __visualization_available__ = False

__all__ = [
    # Version info
    '__version__',
    
    # Benchmark functions
    'ackley', 'rastrigin', 'rastrigin2', 'griewank', 'levy', 'michalewicz', 'schwefel2_26',
    'sphere', 'sphere2', 'rosenbrock', 'rosenbrock_ext1', 'rosenbrock_ext2', 'sum_squares',
    'hyperellipsoid', 'schwefel1_2', 'schwefel2_21', 'schwefel2_22', 'schwefel3_2',
    'step', 'step2', 'maxmod', 'multimod', 'katsuura',
    'beale', 'booth', 'matyas', 'himmelblau', 'easom', 'goldstein_price',
    'branin', 'branin2', 'camel3', 'camel6', 'bohachevsky1', 'bohachevsky2',
    'schaffer1', 'schaffer2', 'leon', 'trecanni', 'mccormick', 'eggholder',
    'chichinadze', 'hosaki', 'zettl', 'holzman1', 'holzman2', 'langerman',
    'stretched_v', 'trefethen4', 'box_betts', 'colville', 'corana', 'kowalik', 'exp2', 'gear',
    
    # Metadata
    'BENCHMARK_SUITE',
    'get_all_functions',
    'get_function_info',
    'get_bounds',
    'get_function_list',
    
    # Utilities (NEW in v0.2.0)
    'normalize_bounds',
    'generate_random_point',
    'check_bounds',
    'scale_to_unit',
    'scale_from_unit',
    'clip_to_bounds',
    'get_bounds_range',
    'get_bounds_center',
    'generate_grid_points',
    'calculate_distance_to_optimum',
    
    # Benchmarking (NEW in v0.2.0)
    'BenchmarkRunner',
    'quick_benchmark',
]

# Add visualization to __all__ if available
if __visualization_available__:
    __all__.extend([
        'plot_function_2d',
        'plot_function_3d',
        'plot_convergence',
        'plot_trajectory_2d',
        'plot_algorithm_comparison',
        'plot_benchmark_summary',
    ])
