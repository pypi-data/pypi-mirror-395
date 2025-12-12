use pyo3::prelude::*;
use clap::Parser;

pub mod app;
use app::cli::Cli;

#[pymodule]
fn anifetch_rs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(run_cli, m)?)?;
    m.add_function(wrap_pyfunction!(main, m)?)?;  // Add a main function
    Ok(())
}

#[pyfunction]
fn main() -> PyResult<()> {
    // Get args from Python's sys.argv via pyo3
    Python::with_gil(|py| {
        let sys = py.import("sys")?;
        let argv: Vec<String> = sys.getattr("argv")?.extract()?;
        run_cli(argv)
    })
}

#[pyfunction]
fn run_cli(py_args: Vec<String>) -> PyResult<()> {
    // Parse arguments using Rust's Clap
    let args = match Cli::try_parse_from(py_args) {
        Ok(a) => a,
        Err(e) => {
            e.print().unwrap();
            return Ok(());
        }
    };

    // Run the app core
    let context = app::core::run(&args).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string())
    })?;

    // Play animation
    app::renderer::play(
        context, 
        args.framerate, 
        args.width, 
        args.loops, 
        args.no_buffer
    ).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(e.to_string())
    })?;

    Ok(())
}