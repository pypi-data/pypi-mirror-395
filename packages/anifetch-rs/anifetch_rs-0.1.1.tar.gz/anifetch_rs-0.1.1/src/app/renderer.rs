use crate::app::core::RenderContext;
use anyhow::Result;
use crossterm::{
    cursor::{Hide, MoveTo, Show},
    event::{self, Event, KeyCode, KeyModifiers},
    execute,
    style::Print,
    terminal::{
        disable_raw_mode, enable_raw_mode, size, Clear, ClearType, EnterAlternateScreen,
        LeaveAlternateScreen,
    },
    QueueableCommand,
};
use std::{
    fs,
    io::{stdout, Write},
    process::{Command, Stdio},
    thread,
    time::{Duration, Instant},
};

pub fn play(ctx: RenderContext, framerate: u32, width: u32, loops: u32, no_buffer: bool) -> Result<()> {
    // Handle static images differently
    if ctx.is_static {
        return play_static(ctx, width, no_buffer);
    }

    // Animated content (videos/GIFs)
    play_animated(ctx, framerate, width, loops, no_buffer)
}

fn play_static(ctx: RenderContext, width: u32, no_buffer: bool) -> Result<()> {
    let template_content = fs::read_to_string(&ctx.template_path).unwrap_or_default();
    let template_lines: Vec<&str> = template_content.lines().collect();

    // Read the single frame
    let frame_path = ctx.frames_dir.join("00001.txt");
    let frame_content = fs::read_to_string(frame_path)?;
    let frame_lines: Vec<&str> = frame_content.lines().collect();

    let padding_left = 2;
    let padding_top = 2;
    let gap = 4;

    enable_raw_mode()?;
    let mut stdout = stdout();
    
    if !no_buffer {
        execute!(stdout, EnterAlternateScreen)?;
    }
    execute!(stdout, Hide, Clear(ClearType::All))?;

    let (_term_width, term_height) = size().unwrap_or((80, 24));

    // Draw system info
    let info_x = padding_left + width as u16 + gap as u16;
    for (i, line) in template_lines.iter().enumerate() {
        let y = padding_top + i as u16;
        if y < term_height {
            stdout.queue(MoveTo(info_x, y))?;
            stdout.queue(Print(line))?;
        }
    }

    // Draw the image
    for (i, line) in frame_lines.iter().enumerate() {
        let y = padding_top + i as u16;
        if y < term_height {
            stdout.queue(MoveTo(padding_left, y))?;
            stdout.queue(Print(line))?;
        }
    }

    stdout.flush()?;

    // Wait for user to press a key to exit
    loop {
        if event::poll(Duration::from_millis(100))? {
            if let Event::Key(key) = event::read()? {
                if key.code == KeyCode::Char('q') 
                    || key.code == KeyCode::Esc
                    || (key.code == KeyCode::Char('c') && key.modifiers.contains(KeyModifiers::CONTROL))
                {
                    break;
                }
            }
        }
    }

    execute!(stdout, Show)?;
    if !no_buffer {
        execute!(stdout, LeaveAlternateScreen)?;
    } else {
        let content_height = std::cmp::max(template_lines.len(), frame_lines.len()) as u16 + padding_top;
        execute!(stdout, MoveTo(0, content_height))?;
        println!();
    }
    disable_raw_mode()?;

    Ok(())
}

fn play_animated(ctx: RenderContext, framerate: u32, width: u32, loops: u32, no_buffer: bool) -> Result<()> {
    let mut frames = Vec::new();
    let mut paths: Vec<_> = fs::read_dir(&ctx.frames_dir)?
        .filter_map(|e| e.ok())
        .collect();
    
    paths.sort_by_key(|dir| {
        dir.path().file_stem()
           .and_then(|s| s.to_str())
           .and_then(|s| s.parse::<u32>().ok())
           .unwrap_or(0)
    });

    for entry in paths {
        frames.push(fs::read_to_string(entry.path())?);
    }

    if frames.is_empty() {
        println!("No frames generated.");
        return Ok(());
    }

    let template_content = fs::read_to_string(&ctx.template_path).unwrap_or_default();
    let template_lines: Vec<&str> = template_content.lines().collect();

    let padding_left = 2;
    let padding_top = 2;
    let gap = 4;

    let template_height = template_lines.len();
    let frame_height = frames.first().map(|f| f.lines().count()).unwrap_or(0);
    let content_height = (std::cmp::max(template_height, frame_height) as u16) + padding_top;

    // Use actual framerate from context (important for GIFs)
    let actual_fps = if ctx.actual_framerate > 0.0 {
        ctx.actual_framerate
    } else {
        framerate as f64
    };

    let loop_arg = if loops == 0 { "0" } else { "1" }; 
    let audio_child = if let Some(audio_path) = &ctx.audio_path {
        Command::new("ffplay")
            .args(["-nodisp", "-autoexit", "-loop", loop_arg, "-loglevel", "quiet"])
            .arg(audio_path)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .ok()
    } else { None };

    enable_raw_mode()?;
    let mut stdout = stdout();
    
    if !no_buffer {
        execute!(stdout, EnterAlternateScreen)?;
    }
    execute!(stdout, Hide, Clear(ClearType::All))?;

    let start_time = Instant::now();
    let frame_duration = Duration::from_secs_f64(1.0 / actual_fps);
    let total_frames = frames.len();
    let mut last_size = size().unwrap_or((80, 24));
    let mut needs_redraw = true;

    loop {
        if event::poll(Duration::from_millis(5))? {
            if let Event::Key(key) = event::read()? {
                if key.code == KeyCode::Char('q') 
                    || key.code == KeyCode::Esc
                    || (key.code == KeyCode::Char('c') && key.modifiers.contains(KeyModifiers::CONTROL))
                {
                    break;
                }
            }
        }
        
        let current_size = size().unwrap_or((80, 24));
        if current_size != last_size {
            last_size = current_size;
            execute!(stdout, Clear(ClearType::All))?;
            needs_redraw = true;
        }

        if needs_redraw {
            let info_x = padding_left + width as u16 + gap as u16;
            for (i, line) in template_lines.iter().enumerate() {
                let y = padding_top + i as u16;
                if y < current_size.1 {
                    stdout.queue(MoveTo(info_x, y))?;
                    stdout.queue(Print(line))?;
                }
            }
            needs_redraw = false;
        }

        let elapsed = start_time.elapsed();
        let frame_count_f = elapsed.as_secs_f64() * actual_fps;
        let frame_idx_raw = frame_count_f as usize;
        let frame_idx = frame_idx_raw % total_frames;
        
        if loops > 0 && (frame_idx_raw / total_frames) as u32 >= loops {
            break;
        }

        let frame_lines: Vec<&str> = frames[frame_idx].lines().collect();
        for (i, line) in frame_lines.iter().enumerate() {
            let y = padding_top + i as u16;
            if y < current_size.1 {
                stdout.queue(MoveTo(padding_left, y))?;
                stdout.queue(Print(line))?;
            }
        }

        stdout.flush()?;
        
        let next_frame_time = start_time + frame_duration * (frame_count_f.floor() as u32 + 1);
        if let Some(sleep_time) = next_frame_time.checked_duration_since(Instant::now()) {
            thread::sleep(sleep_time);
        }
    }

    if let Some(mut child) = audio_child {
        let _ = child.kill();
    }
    
    execute!(stdout, Show)?;
    if !no_buffer {
        execute!(stdout, LeaveAlternateScreen)?;
    } else {
        execute!(stdout, MoveTo(0, content_height))?;
        println!();
    }
    disable_raw_mode()?;

    Ok(())
}