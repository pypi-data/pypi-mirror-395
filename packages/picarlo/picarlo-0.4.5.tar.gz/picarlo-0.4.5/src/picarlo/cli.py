import typer

from picarlo.sim import monte_carlo_pi, monte_carlo_pi_parallel

app = typer.Typer(help="Monte Carlo π estimator")


@app.command()
def run(
    iterations: int = typer.Option(
        10_000, "--iterations", "-i", help="Samples per process"
    ),
    cores: int = typer.Option(
        1, "--cores", "-c", help="Number of processes (defaults to CPU count)"
    ),
    use_python: bool = typer.Option(
        False, "--use-python", help="Force use of Python implementation"
    ),
):
    if cores == 1:
        pi = monte_carlo_pi(iterations, force_python=use_python)
    else:
        pi = monte_carlo_pi_parallel(iterations, cores, force_python=use_python)

    typer.echo(f"π ≈ {pi}")


def main():
    app()


if __name__ == "__main__":
    main()
