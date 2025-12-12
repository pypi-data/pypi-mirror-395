use pyo3::prelude::*;
use rand::prelude::*;
use std::time::Instant;

/// Estimate the value of Pi using the Monte Carlo method.
///
/// # Arguments
///
/// * `num_samples` - The number of random points to generate.
///
/// # Returns
///
/// A tuple containing:
/// - The estimated value of Pi (`f64`).
/// - The runtime of the calculation in seconds (`f64`).
#[pyfunction]
fn monte_carlo_pi(num_samples: usize) -> (f64, f64) {
    let start = Instant::now();

    let mut in_circle_count = 0;
    let mut rng = SmallRng::from_entropy();

    for _ in 0..num_samples {
        let x: f64 = rng.gen();
        let y: f64 = rng.gen();
        if x * x + y * y <= 1.0 {
            in_circle_count += 1;
        }
    }

    let duration = start.elapsed();
    println!("Rust Runtime: {:.2?}", duration);

    // Return both Pi estimate and timing as a tuple
    (
        4.0 * (in_circle_count as f64) / (num_samples as f64),
        duration.as_secs_f64(),
    )
}

/// A Python module implemented in Rust.
#[pymodule]
fn _picarlo_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    println!("adding function to Python module");
    m.add_function(wrap_pyfunction!(monte_carlo_pi, m)?)?;
    Ok(())
}
