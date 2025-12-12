use crate::app::{cache, cli::Cli, external};
use anyhow::{Context, Result};
use rayon::prelude::*;
use std::fs::{self, File};
use std::io::Write;
use std::path::PathBuf;
use std::time::Instant;

pub struct RenderContext {
    pub cache_path: PathBuf,
    pub template_path: PathBuf,
    pub frames_dir: PathBuf,
    pub audio_path: Option<PathBuf>,
    pub frame_count: usize,
    pub template_width: usize,
}

pub fn run(args: &Cli) -> Result<RenderContext> {
    // 1. Calculate the unique hash for this configuration
    let hash = cache::calculate_hash(
        args.filename.to_str().unwrap(),
        args.width,
        args.height,
        args.framerate,
        &args.chafa_args,
    );

    // 2. Check if valid cache exists
    let cache_entry = cache::find_cache(&hash)?;
    let cache_path = cache::get_cache_path(&hash)?;
    let frames_dir = cache_path.join("output"); // Text frames
    let video_frames_dir = cache_path.join("video"); // PNG frames
    let template_path = cache_path.join("template.txt");

    let should_render = args.force_render || cache_entry.is_none() || !frames_dir.exists();

    let audio_path = if let Some(path) = &args.sound {
        Some(path.clone())
    } else if should_render || args.sound.is_none() {
        // If we need to render or audio wasn't explicitly provided, check cache or extract
        let ext = external::get_audio_codec(&args.filename).unwrap_or_else(|_| "mp3".to_string());
        
        // Simple mapping or default to mp3/aac. Real logic would be more robust.
        // ffmpeg is smart enough to handle most extensions, but consistency helps.
        let target_ext = if ext.contains("pcm") { "wav" } else { "mp3" }; 
        let path = cache_path.join(format!("audio.{}", target_ext));
        
        if should_render && !path.exists() {
             // Ignore error if no audio stream exists (e.g. silent video)
             let _ = external::extract_audio(&args.filename, &path); 
        }
        
        if path.exists() { Some(path) } else { None }
    } else {
        cache_entry.and_then(|e| e.sound_path.map(PathBuf::from))
    };


    if should_render {
        println!("Cache miss or forced render. Generating frames...");
        let start = Instant::now();

        // A. Clean up old directories
        if cache_path.exists() {
            fs::remove_dir_all(&cache_path).ok();
        }
        fs::create_dir_all(&video_frames_dir)?;
        fs::create_dir_all(&frames_dir)?;

        // B. Extract PNG frames from video
        println!("Extracting frames with ffmpeg...");
        external::extract_frames(&args.filename, &video_frames_dir, args.framerate)?;

        // C. Process frames with Chafa in PARALLEL (The Rayon Magic)
        println!("Converting frames to text (Multi-threaded)...");
        
        let paths: Vec<PathBuf> = fs::read_dir(&video_frames_dir)?
            .filter_map(|entry| entry.ok().map(|e| e.path()))
            .collect();
        
        // This par_iter() runs the closure on all available threads
        paths.par_iter().for_each(|img_path| {
            if let Ok(text_frame) = external::run_chafa(img_path, args.width, args.height, &args.chafa_args) {
                // Save text frame with same filename but .txt extension
                let file_name = img_path.file_stem().unwrap();
                let out_path = frames_dir.join(file_name).with_extension("txt");
                if let Ok(mut file) = File::create(out_path) {
                    let _ = file.write_all(text_frame.as_bytes());
                }
            }
        });

        // D. Cleanup PNGs to save space
        fs::remove_dir_all(&video_frames_dir)?;

        // E. Save the template (fastfetch or neofetch output)
        // We do this here so it's fresh and cached with the specific frames.
        let fetch_output = if args.fast_fetch {
            external::run_fastfetch()?
        } else {
            external::run_neofetch()?
        };
        
        fs::write(&template_path, &fetch_output)?;

        // F. Update Cache Registry
        let new_entry = cache::CacheEntry {
            hash: hash.clone(),
            filename: args.filename.to_string_lossy().to_string(),
            width: args.width,
            height: args.height,
            framerate: args.framerate,
            chafa_args: args.chafa_args.clone(),
            sound_path: audio_path.as_ref().map(|p| p.to_string_lossy().to_string()),
        };
        cache::save_cache_entry(new_entry)?;

        println!("Generation complete in {:.2?}", start.elapsed());
    } else {
        println!("Using cached animation.");
    }

    // Prepare context for the renderer
    let frame_count = fs::read_dir(&frames_dir)?.count();
    
    // Quick check to get template width for centering logic (simple version)
    let template_content = fs::read_to_string(&template_path).unwrap_or_default();
    let template_width = template_content.lines().map(|l| l.len()).max().unwrap_or(0);

    Ok(RenderContext {
        cache_path,
        template_path,
        frames_dir,
        audio_path,
        frame_count,
        template_width,
    })
}
