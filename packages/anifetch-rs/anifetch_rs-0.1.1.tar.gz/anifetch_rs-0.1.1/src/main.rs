mod app;

use anyhow::Result;
use clap::Parser;
use app::cli::Cli;

fn main() -> Result<()> {
    let args = Cli::parse();

    let context = app::core::run(&args)?;

    app::renderer::play(
        context, 
        args.framerate, 
        args.width,
        args.loops,
        args.no_buffer
    )?;
    
    Ok(())
}