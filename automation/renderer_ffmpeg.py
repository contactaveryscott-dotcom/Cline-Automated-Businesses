import json
import os
import sys
import subprocess

def load_config():
    with open("automation/render_config.json", "r") as f:
        return json.load(f)

def render_text_segment(ffmpeg_path, text, duration, output, config):
    # Render a segment with solid color background and centered text
    cmd = [
        ffmpeg_path,
        "-y",
        "-f", "lavfi",
        "-i", f"color=c={config['background_color']}:s={config['resolution']}:d={duration}",
        "-vf", f"drawtext=fontfile={config['font_path']}:text='{text}':fontcolor=white:fontsize={config['font_size']}:x=(w-text_w)/2:y=(h-text_h)/2",
        "-t", str(duration),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output
    ]
    subprocess.run(cmd, check=True)

def concat_segments(ffmpeg_path, segment_files, output):
    # Concatenate segments into final video
    with open("automation/rendered/segments.txt", "w") as f:
        for seg in segment_files:
            f.write(f"file '{os.path.abspath(seg)}'\n")
    cmd = [
        ffmpeg_path,
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", "automation/rendered/segments.txt",
        "-c", "copy",
        output
    ]
    subprocess.run(cmd, check=True)
    os.remove("automation/rendered/segments.txt")
    for seg in segment_files:
        os.remove(seg)

def render_video(script_json_path, output_path):
    config = load_config()
    ffmpeg_path = config["ffmpeg_path"]
    with open(script_json_path, "r") as f:
        data = json.load(f)
    segment_files = []
    for idx, step in enumerate(data["storyboard"]):
        seg_out = f"automation/rendered/segment_{idx}.mp4"
        text = step["text"]
        duration = step.get("duration", 3)
        render_text_segment(ffmpeg_path, text, duration, seg_out, config)
        segment_files.append(seg_out)
    concat_segments(ffmpeg_path, segment_files, output_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python automation/renderer_ffmpeg.py <script_json_path> <output_path>")
        sys.exit(1)
    render_video(sys.argv[1], sys.argv[2])
