use crate::app::{cache, cli::Cli, external, file_type};
use anyhow::Result;
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
    pub is_static: bool,  // True for static images
    pub actual_framerate: f64,  // Actual framerate (for GIFs)
}

pub fn run(args: &Cli) -> Result<RenderContext> {
    // Detect media type
    let media_type = file_type::detect_media_type(&args.filename)?;
    
    // Get effective chafa arguments (considering quality preset)
    let chafa_args = args.effective_chafa_args();
    
    match media_type {
        file_type::MediaType::Image => run_static_image(args, &chafa_args),
        file_type::MediaType::Gif => run_animated(args, true, &chafa_args),
        file_type::MediaType::Video => run_animated(args, false, &chafa_args),
    }
}

/// Handle static images
fn run_static_image(args: &Cli, chafa_args: &str) -> Result<RenderContext> {
    // For static images, we don't need caching complexity
    // Just render once and display
    let hash = cache::calculate_hash(
        args.filename.to_str().unwrap(),
        args.width,
        args.height,
        0, // No framerate for static images
        chafa_args,
    );

    let cache_path = cache::get_cache_path(&hash)?;
    let frames_dir = cache_path.join("output");
    let template_path = cache_path.join("template.txt");

    let should_render = args.force_render || !template_path.exists();

    if should_render {
        println!("Rendering static image...");
        fs::create_dir_all(&frames_dir)?;

        // Generate the ASCII art
        let ascii_art = external::run_chafa(&args.filename, args.width, args.height, chafa_args)?;
        
        // Save as a single "frame"
        let frame_path = frames_dir.join("00001.txt");
        let mut file = File::create(frame_path)?;
        file.write_all(ascii_art.as_bytes())?;

        // Save the fetch output
        let fetch_output = if args.fast_fetch {
            external::run_fastfetch()?
        } else {
            external::run_neofetch()?
        };
        fs::write(&template_path, &fetch_output)?;

        // Save cache entry
        let entry = cache::CacheEntry {
            hash: hash.clone(),
            filename: args.filename.to_string_lossy().to_string(),
            width: args.width,
            height: args.height,
            framerate: 0,
            chafa_args: chafa_args.to_string(),
            sound_path: None,
        };
        cache::save_cache_entry(entry)?;
    }

    let template_content = fs::read_to_string(&template_path).unwrap_or_default();
    let template_width = template_content.lines().map(|l| l.len()).max().unwrap_or(0);

    Ok(RenderContext {
        cache_path,
        template_path,
        frames_dir,
        audio_path: None,
        frame_count: 1,
        template_width,
        is_static: true,
        actual_framerate: 0.0,
    })
}

/// Handle animated content (videos and GIFs)
fn run_animated(args: &Cli, is_gif: bool, chafa_args: &str) -> Result<RenderContext> {
    // Determine actual framerate for GIFs
    let actual_framerate = if is_gif {
        let detected = external::get_gif_framerate(&args.filename)?;
        if args.framerate == 10 {  // User didn't specify, use detected
            detected
        } else {
            args.framerate as f64  // User specified, use that
        }
    } else {
        args.framerate as f64
    };

    let hash = cache::calculate_hash(
        args.filename.to_str().unwrap(),
        args.width,
        args.height,
        actual_framerate as u32,
        chafa_args,
    );

    let cache_entry = cache::find_cache(&hash)?;
    let cache_path = cache::get_cache_path(&hash)?;
    let frames_dir = cache_path.join("output");
    let video_frames_dir = cache_path.join("video");
    let template_path = cache_path.join("template.txt");

    let should_render = args.force_render || cache_entry.is_none() || !frames_dir.exists();

    let audio_path = if let Some(path) = &args.sound {
        Some(path.clone())
    } else if should_render || args.sound.is_none() {
        let ext = external::get_audio_codec(&args.filename).unwrap_or_else(|_| "mp3".to_string());
        let target_ext = if ext.contains("pcm") { "wav" } else { "mp3" };
        let path = cache_path.join(format!("audio.{}", target_ext));
        
        if should_render && !path.exists() {
            let _ = external::extract_audio(&args.filename, &path);
        }
        
        if path.exists() { Some(path) } else { None }
    } else {
        cache_entry.and_then(|e| e.sound_path.map(PathBuf::from))
    };

    if should_render {
        println!("Cache miss or forced render. Generating frames...");
        let start = Instant::now();

        if cache_path.exists() {
            fs::remove_dir_all(&cache_path).ok();
        }
        fs::create_dir_all(&video_frames_dir)?;
        fs::create_dir_all(&frames_dir)?;

        // Extract frames
        println!("Extracting frames with ffmpeg...");
        if is_gif {
            external::extract_gif_frames(&args.filename, &video_frames_dir)?;
        } else {
            external::extract_frames(&args.filename, &video_frames_dir, actual_framerate as u32)?;
        }

        // Convert to ASCII in parallel
        println!("Converting frames to text (Multi-threaded)...");
        let paths: Vec<PathBuf> = fs::read_dir(&video_frames_dir)?
            .filter_map(|entry| entry.ok().map(|e| e.path()))
            .collect();
        
        paths.par_iter().for_each(|img_path| {
            if let Ok(text_frame) = external::run_chafa(img_path, args.width, args.height, chafa_args) {
                let file_name = img_path.file_stem().unwrap();
                let out_path = frames_dir.join(file_name).with_extension("txt");
                if let Ok(mut file) = File::create(out_path) {
                    let _ = file.write_all(text_frame.as_bytes());
                }
            }
        });

        // Cleanup
        fs::remove_dir_all(&video_frames_dir)?;

        // Save fetch output
        let fetch_output = if args.fast_fetch {
            external::run_fastfetch()?
        } else {
            external::run_neofetch()?
        };
        fs::write(&template_path, &fetch_output)?;

        // Update cache
        let new_entry = cache::CacheEntry {
            hash: hash.clone(),
            filename: args.filename.to_string_lossy().to_string(),
            width: args.width,
            height: args.height,
            framerate: actual_framerate as u32,
            chafa_args: chafa_args.to_string(),
            sound_path: audio_path.as_ref().map(|p| p.to_string_lossy().to_string()),
        };
        cache::save_cache_entry(new_entry)?;

        println!("Generation complete in {:.2?}", start.elapsed());
    } else {
        println!("Using cached animation.");
    }

    let frame_count = fs::read_dir(&frames_dir)?.count();
    let template_content = fs::read_to_string(&template_path).unwrap_or_default();
    let template_width = template_content.lines().map(|l| l.len()).max().unwrap_or(0);

    Ok(RenderContext {
        cache_path,
        template_path,
        frames_dir,
        audio_path,
        frame_count,
        template_width,
        is_static: false,
        actual_framerate,
    })
}