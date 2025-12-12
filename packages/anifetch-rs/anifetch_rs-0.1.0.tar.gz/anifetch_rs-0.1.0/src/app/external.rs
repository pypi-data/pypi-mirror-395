use anyhow::{Context, Result, bail};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::str;

/// Runs fastfetch to get the system info text.
pub fn run_fastfetch() -> Result<String> {
    let output = Command::new("fastfetch")
        .args(["--logo", "none", "--pipe", "false"])
        .output()
        .context("Failed to execute fastfetch. Is it installed?")?;

    if !output.status.success() {
        let stderr = str::from_utf8(&output.stderr).unwrap_or("Unknown error");
        bail!("fastfetch failed: {}", stderr);
    }

    Ok(str::from_utf8(&output.stdout)?.to_string())
}

/// Runs neofetch to get the system info text.
pub fn run_neofetch() -> Result<String> {
    // Neofetch often outputs color codes that might need stripping or handling,
    // but for now let's just run it standard.
    // We use --off to turn off the image backend since we handle that.
    let output = Command::new("neofetch")
        .arg("--off")
        .arg("--color_blocks")
        .arg("off") // clean output
        .output()
        .context("Failed to execute neofetch. Is it installed?")?;

    if !output.status.success() {
        let stderr = str::from_utf8(&output.stderr).unwrap_or("Unknown error");
        bail!("neofetch failed: {}", stderr);
    }

    Ok(str::from_utf8(&output.stdout)?.to_string())
}

/// Uses ffprobe to get the video width and height.
pub fn get_video_dimensions(path: &Path) -> Result<(u32, u32)> {
    let output = Command::new("ffprobe")
        .args([
            "-v", "error",
            "-select_streams", "v:0",
            "-show_entries", "stream=width,height",
            "-of", "csv=s=x:p=0",
        ])
        .arg(path)
        .output()
        .context("Failed to run ffprobe. Is ffmpeg installed?")?;

    if !output.status.success() {
        bail!("ffprobe failed to read video dimensions");
    }

    let output_str = str::from_utf8(&output.stdout)?.trim();
    let parts: Vec<&str> = output_str.split('x').collect();

    if parts.len() != 2 {
        bail!("Invalid ffprobe output format: {}", output_str);
    }

    let width = parts[0].parse::<u32>().context("Failed to parse width")?;
    let height = parts[1].parse::<u32>().context("Failed to parse height")?;

    Ok((width, height))
}

/// Extract all frames from the video into the output directory as PNGs.
pub fn extract_frames(input: &Path, output_dir: &Path, framerate: u32) -> Result<()> {
    // pattern for ffmpeg output: video/%05d.png
    let output_pattern = output_dir.join("%05d.png");

    let output = Command::new("ffmpeg")
        .args([
            "-i", input.to_str().unwrap(),
            "-vf", &format!("fps={},format=rgba", framerate),
            output_pattern.to_str().unwrap(),
        ])
        .stdout(Stdio::null())
        .stderr(Stdio::piped()) // Actually capture it for errors
        .output()
        .context("Failed to run ffmpeg extraction")?;

    if !output.status.success() {
        let stderr = str::from_utf8(&output.stderr).unwrap_or("Unknown ffmpeg error");
        bail!("ffmpeg failed to extract frames:\n{}", stderr);
    }

    Ok(())
}

/// Helper to check the audio codec so we can decide the file extension.
pub fn get_audio_codec(path: &Path) -> Result<String> {
    let output = Command::new("ffprobe")
        .args([
            "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=codec_name",
            "-of", "default=nokey=1:noprint_wrappers=1",
        ])
        .arg(path)
        .output()
        .context("Failed to run ffprobe for audio codec")?;

    Ok(str::from_utf8(&output.stdout)?.trim().to_string())
}

/// Extract audio track from the video.
pub fn extract_audio(input: &Path, output_path: &Path) -> Result<()> {
    let status = Command::new("ffmpeg")
        .args([
            "-i", input.to_str().unwrap(),
            "-y", // overwrite
            "-vn", // no video
            "-c:a", "copy", // copy stream (fastest)
            "-loglevel", "quiet",
            output_path.to_str().unwrap(),
        ])
        .status()
        .context("Failed to run ffmpeg audio extraction")?;

    if !status.success() {
        bail!("ffmpeg audio extraction failed");
    }

    Ok(())
}

/// Run chafa on a single image file to get the string representation.
pub fn run_chafa(image_path: &Path, width: u32, height: u32, extra_args: &str) -> Result<String> {
    // extra_args comes in as a string like "--symbols ascii --fg-only"
    // We need to split it for Command::args
    let split_args: Vec<&str> = extra_args.split_whitespace().collect();

    let output = Command::new("chafa")
        .args(split_args)
        .args([
            "--format", "symbols",
            &format!("--size={}x{}", width, height),
        ])
        .arg(image_path)
        .output()
        .context("Failed to run chafa")?;

    if !output.status.success() {
        let stderr = str::from_utf8(&output.stderr).unwrap_or("Unknown error");
        bail!("chafa failed: {}", stderr);
    }

    Ok(str::from_utf8(&output.stdout)?.to_string())
}
