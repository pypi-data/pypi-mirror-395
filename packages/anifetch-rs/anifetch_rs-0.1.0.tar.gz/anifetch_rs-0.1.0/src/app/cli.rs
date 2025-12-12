use clap::Parser;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
pub struct Cli {
    #[arg(required = true)]
    pub filename: PathBuf,

    #[arg(short = 'W', long = "width", default_value_t = 40)]
    pub width: u32,

    #[arg(short = 'H', long = "height", default_value_t = 20)]
    pub height: u32,

    #[arg(short = 'r', long = "framerate", default_value_t = 10)]
    pub framerate: u32,

    #[arg(short = 's', long = "sound")]
    pub sound: Option<PathBuf>,

    #[arg(long = "force-render", default_value_t = false)]
    pub force_render: bool,

    #[arg(long = "fast-fetch", short = 'f', default_value_t = false)]
    pub fast_fetch: bool,

    #[arg(short = 'c', long = "chafa", default_value = "--symbols ascii --fg-only")]
    pub chafa_args: String,

    #[arg(short = 'l', long = "loops", default_value_t = 0)]
    pub loops: u32,

    #[arg(long = "no-buffer", default_value_t = false)]
    pub no_buffer: bool,
}