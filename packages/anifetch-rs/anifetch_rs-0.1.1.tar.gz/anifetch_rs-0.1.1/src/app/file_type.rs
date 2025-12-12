use anyhow::{bail, Result};
use std::path::Path;

#[derive(Debug, Clone, Copy, PartialEq)]
pub enum MediaType {
    Video,
    Image,
    Gif,
}

/// Detects the media type based on file extension
pub fn detect_media_type(path: &Path) -> Result<MediaType> {
    let extension = path
        .extension()
        .and_then(|e| e.to_str())
        .map(|e| e.to_lowercase())
        .unwrap_or_default();

    match extension.as_str() {
        // Video formats
        "mp4" | "mkv" | "avi" | "mov" | "webm" | "flv" | "wmv" | "m4v" | "mpg" | "mpeg" => {
            Ok(MediaType::Video)
        }
        // GIF (animated)
        "gif" => Ok(MediaType::Gif),
        // Static image formats
        "png" | "jpg" | "jpeg" | "bmp" | "webp" | "tiff" | "tif" | "ico" | "svg" => {
            Ok(MediaType::Image)
        }
        _ => bail!("Unsupported file format: {}", extension),
    }
}