from picarlo.sim import monte_carlo_pi

# Number of samples for benchmarking
N_SAMPLES = 1_000_000


def test_benchmark_rust(benchmark):
    """Benchmark the Rust implementation of Monte Carlo Pi."""
    result, _ = benchmark(monte_carlo_pi, N_SAMPLES)
    assert 3.1 < result < 3.2


def test_benchmark_python(benchmark):
    """Benchmark the Python implementation of Monte Carlo Pi."""
    # We access the Python implementation directly if exposed,
    # or force it via the wrapper if possible.
    # Assuming 'monte_carlo_pi' has a 'force_python' kwarg based on previous files.
    result, _ = benchmark(monte_carlo_pi, N_SAMPLES, force_python=True)
    assert 3.1 < result < 3.2
