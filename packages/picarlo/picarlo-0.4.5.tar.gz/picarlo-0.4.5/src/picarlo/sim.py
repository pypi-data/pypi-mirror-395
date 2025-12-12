import functools
import multiprocessing
import random
import time
from dataclasses import dataclass

from loguru import logger


def monte_carlo_pi_python(num_samples: int) -> tuple[float, float]:
    """
    Estimate the value of Pi using the Monte Carlo method (Python implementation).

    This function generates random points within a unit square and counts how many fall within the unit circle.
    The ratio of points inside the circle to the total number of points is used to estimate Pi.

    Args:
        num_samples (int): The number of random points to generate.

    Returns:
        tuple[float, float]: A tuple containing:
            - The estimated value of Pi.
            - The runtime of the calculation in seconds.
    """  # noqa: E501

    start = time.time()

    in_circle_count = 0
    in_square_count = 0

    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            in_circle_count += 1
        in_square_count += 1

    end = time.time()

    return (4 * in_circle_count / in_square_count, end - start)


try:
    print("importing rust lib")
    from picarlo._picarlo_rust import monte_carlo_pi as _monte_carlo_pi_rust
except ImportError:
    print("importing rust lib failed")
    logger.warning("Falling back to Python implementation.")
    _monte_carlo_pi_rust = None


# 2. Define the public function explicitly (picklable)
def monte_carlo_pi(num_samples: int, force_python: bool = False) -> tuple[float, float]:
    """
    Estimate Pi using the available backend (Rust or Python).

    Args:
        num_samples (int): The number of random samples to generate.
        force_python (bool, optional): Whether to force the use of the Python
        implementation.
                                       Defaults to False.

    Returns:
        tuple[float, float]: A tuple containing:
            - The estimated value of Pi.
            - The total runtime (including overhead) in seconds.
    """
    start = time.time()

    # Use Rust if available AND not forced to use Python
    if _monte_carlo_pi_rust and not force_python:
        result, runtime = _monte_carlo_pi_rust(num_samples)
        print("rust run done.")
    else:
        result, runtime = monte_carlo_pi_python(num_samples)
        print("python run done.")

    end = time.time()
    logger.info(f"Runtime: outer {end - start:.2f} s, inner {runtime:.2f} s")
    return (result, end - start)


def monte_carlo_pi_parallel(
    num_samples: int, num_proc: int, force_python: bool = False
) -> tuple[float, float]:
    """
    Estimate the value of Pi using the Monte Carlo method in parallel.

    This function divides the task of estimating Pi into multiple processes
    to take advantage of multiple CPU cores, thereby speeding up the computation.

    Args:
        num_samples (int): The number of random samples to generate in each process.
        num_proc (int): The number of processes to use for parallel computation.
        force_python (bool, optional): Whether to force the use of the Python
        implementation.
                                       Defaults to False.

    Returns:
        tuple[float, float]: A tuple containing:
            - The estimated value of Pi.
            - The runtime of the parallel execution in seconds.
    """
    # TODO: get # of core and other info about mutliprocessing
    num_cores = multiprocessing.cpu_count()

    logger.info(
        f"# of avail. cores: {num_cores} | {num_proc} procs spawned.",
    )

    start = time.time()

    # Prepare the worker with the frozen argument
    worker = functools.partial(monte_carlo_pi, force_python=force_python)

    pool = multiprocessing.Pool(processes=num_proc)
    # map passes the iterable items as the first argument to 'worker'
    results = pool.map(worker, [num_samples] * num_proc)
    pool.close()
    pool.join()

    end = time.time()

    # Extract just the Pi estimates from the results (which are (pi, runtime) tuples)
    pi_estimates = [res[0] for res in results]

    return (sum(pi_estimates) / num_proc, end - start)


@dataclass
class Config:
    """
    Configuration class for simulation parameters.

    Attributes:
        num_samples (int): The number of samples to be used in the simulation.
        Default is 10,000,000.
    """

    num_samples: int = 10000


def hello() -> str:
    print("inside hello!")
    return "hello"


def goodbye() -> str:
    print("inside goodbye!")
    return "goodbye"


def stringify_the_float(value: float) -> str:
    return f"{int(value):d} dot {int((value-int(value))*100):d}"
