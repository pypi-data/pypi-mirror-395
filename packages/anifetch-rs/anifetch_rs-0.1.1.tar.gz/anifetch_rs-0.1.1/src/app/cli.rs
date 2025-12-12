use clap::Parser;
use std::path::PathBuf;

#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
pub struct Cli {
    #[arg(required = true)]
    pub filename: PathBuf,

    #[arg(short = 'W', long = "width", default_value_t = 60)]
    pub width: u32,

    #[arg(short = 'H', long = "height", default_value_t = 30)]
    pub height: u32,

    #[arg(short = 'r', long = "framerate", default_value_t = 15)]
    pub framerate: u32,

    #[arg(short = 's', long = "sound")]
    pub sound: Option<PathBuf>,

    #[arg(long = "force-render", default_value_t = false)]
    pub force_render: bool,

    #[arg(long = "fast-fetch", short = 'f', default_value_t = false)]
    pub fast_fetch: bool,

    /// Chafa arguments for rendering quality
    /// 
    /// Presets:
    ///   high: --symbols all --colors full --dither ordered --color-space din99d
    ///   medium: --symbols all --colors 256 --dither ordered
    ///   low: --symbols ascii --fg-only
    /// 
    /// Or use custom chafa arguments
    #[arg(
        short = 'c',
        long = "chafa",
        default_value = "--symbols all --colors full --dither ordered --color-space din99d"
    )]
    pub chafa_args: String,

    #[arg(short = 'l', long = "loops", default_value_t = 0)]
    pub loops: u32,

    #[arg(long = "no-buffer", default_value_t = false)]
    pub no_buffer: bool,

    /// Quality preset (overrides chafa args): high, medium, low
    #[arg(short = 'q', long = "quality")]
    pub quality: Option<String>,
}

impl Cli {
    /// Get the effective chafa arguments, considering quality presets
    pub fn effective_chafa_args(&self) -> String {
        if let Some(quality) = &self.quality {
            match quality.to_lowercase().as_str() {
                "high" | "h" => {
                    "--symbols all --colors full --dither ordered --color-space din99d".to_string()
                }
                "medium" | "m" => {
                    "--symbols all --colors 256 --dither ordered".to_string()
                }
                "low" | "l" => {
                    "--symbols ascii --fg-only".to_string()
                }
                "ultra" | "u" => {
                    // Maximum quality with all features
                    "--symbols all --colors full --dither ordered --color-space din99d --fill all".to_string()
                }
                _ => self.chafa_args.clone(),
            }
        } else {
            self.chafa_args.clone()
        }
    }
}