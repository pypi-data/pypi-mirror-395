use anyhow::{Context, Result};
use directories::ProjectDirs;
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Path, PathBuf};

const ORG: &str = "Notenlish"; // Keeping original credit
const APP: &str = "anifetch-rs";

#[derive(Serialize, Deserialize, Debug, Clone)]
pub struct CacheEntry {
    pub hash: String,
    pub filename: String,
    pub width: u32,
    pub height: u32,
    pub framerate: u32,
    pub chafa_args: String,
    pub sound_path: Option<String>,
}

/// Locates the data directory (e.g., ~/.local/share/anifetch-rs)
pub fn get_data_dir() -> Result<PathBuf> {
    if let Some(proj_dirs) = ProjectDirs::from(ORG, ORG, APP) {
        let data_dir = proj_dirs.data_dir();
        fs::create_dir_all(data_dir).context("Failed to create data directory")?;
        Ok(data_dir.to_path_buf())
    } else {
        // Fallback to current directory if system dirs are weird
        Ok(PathBuf::from("."))
    }
}

/// Generates a unique SHA256 hash based on the render parameters.
pub fn calculate_hash(
    filename: &str,
    width: u32,
    height: u32,
    framerate: u32,
    chafa_args: &str,
) -> String {
    let mut hasher = Sha256::new();
    hasher.update(filename);
    hasher.update(width.to_be_bytes());
    hasher.update(height.to_be_bytes());
    hasher.update(framerate.to_be_bytes());
    hasher.update(chafa_args);
    let result = hasher.finalize();
    hex::encode(result)
}

/// Loads the caches.json file.
pub fn load_caches() -> Result<Vec<CacheEntry>> {
    let data_dir = get_data_dir()?;
    let cache_file = data_dir.join("caches.json");

    if !cache_file.exists() {
        return Ok(Vec::new());
    }

    let content = fs::read_to_string(cache_file).context("Failed to read caches.json")?;
    let caches: Vec<CacheEntry> = serde_json::from_str(&content).unwrap_or_default();
    Ok(caches)
}

/// Saves the cache list back to caches.json.
pub fn save_cache_entry(entry: CacheEntry) -> Result<()> {
    let mut caches = load_caches()?;
    
    // Remove old entry with same hash if it exists (update it)
    caches.retain(|c| c.hash != entry.hash);
    caches.push(entry);

    let data_dir = get_data_dir()?;
    let cache_file = data_dir.join("caches.json");
    let json = serde_json::to_string_pretty(&caches)?;
    
    fs::write(cache_file, json).context("Failed to write caches.json")?;
    Ok(())
}

/// Finds a matching cache entry for the current arguments.
pub fn find_cache(hash: &str) -> Result<Option<CacheEntry>> {
    let caches = load_caches()?;
    Ok(caches.into_iter().find(|c| c.hash == hash))
}

/// Returns the path where frames for a specific hash should be stored.
pub fn get_cache_path(hash: &str) -> Result<PathBuf> {
    let data_dir = get_data_dir()?;
    let path = data_dir.join(hash);
    fs::create_dir_all(&path)?;
    Ok(path)
}
