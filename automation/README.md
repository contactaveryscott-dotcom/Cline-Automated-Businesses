# Content Factory Automation Pipeline

This directory contains the fully local, end-to-end automated pipeline for turning video script JSON files into finished `.mp4` videos using FFmpeg.

## Prerequisites

- Install [FFmpeg](https://ffmpeg.org/download.html) and ensure `ffmpeg` is in your PATH.
- Add a font file at `assets/font.ttf` (any TTF font).
- (Optional) Add a background video at `assets/background.mp4` if you want video backgrounds.

## Structure

- **incoming/**: Drop new video script JSON files here (see `script_schema.json` for format).
- **rendered/**: Finished `.mp4` videos are saved here.
- **logs/**: Watcher and renderer logs/errors.
- **render_config.json**: Configure FFmpeg path, resolution, font, background mode.
- **watcher.py**: Monitors `incoming/` for new scripts, validates, and triggers rendering.
- **renderer_ffmpeg.py**: Renders videos using FFmpeg (text-only style).

## How It Works

1. **Prepare Script JSON**
   - Use the schema in `incoming/script_schema.json`.
   - Example (`sample_script.json`):
     ```json
     {
       "title": "Speedy Avocado Toast",
       "script": "Mash avocado on whole grain toast, top with cherry tomatoes and a dash of pepper. Quick, nutritious, and delicious.",
       "storyboard": [
         { "timestamp": 0, "text": "Avocado, toast, tomatoes", "action": "show_ingredients", "duration": 3 },
         { "timestamp": 3, "text": "Mash avocado", "action": "mash_avocado", "duration": 3 },
         { "timestamp": 6, "text": "Top toast, add tomatoes", "action": "assemble", "duration": 3 }
       ],
       "duration": 9
     }
     ```

2. **Automatic Detection**
   - Place your JSON file in `incoming/`.
   - Run the watcher:
     ```
     python automation/watcher.py
     ```
   - Or run in a loop (default behavior):
     ```
     python automation/watcher.py
     ```
   - Watcher validates and triggers FFmpeg rendering.

3. **Rendering**
   - The renderer reads the storyboard and creates a `.mp4` video with solid color background and animated text.
   - Output is saved to `rendered/` (e.g., `rendered/sample_script.mp4`).

4. **Logs**
   - All events and errors are logged in `logs/watcher.log`.

## Example: Render the Sample Video

1. Ensure prerequisites are met.
2. Place `sample_script.json` in `incoming/`.
3. Run:
   ```
   python automation/watcher.py
   ```
4. The resulting file will appear at:
   ```
   automation/rendered/sample_script.mp4
   ```

## Customization

- Edit `render_config.json` for resolution, font, background color/video.
- Replace font or background assets as needed.

## Troubleshooting

- Check `logs/watcher.log` for errors or processing status.
- Ensure JSON files match the schema.

## End-to-End Flow

1. Drop script JSON in `incoming/`.
2. Watcher detects and validates.
3. Renderer creates `.mp4` video using FFmpeg.
4. Output saved in `rendered/`.
5. Logs written to `logs/`.

**No SaaS, no third-party dashboards. All automation is local and documented.**
