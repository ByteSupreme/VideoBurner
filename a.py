import os
import subprocess
from PIL import ImageFont
import matplotlib.font_manager as fm
import ffmpeg as ffmpeg_lib

def is_font_installed(font_name):
    # Check if the font is already installed by looking it up
    for font in fm.findSystemFonts(fontpaths=None, fontext='ttf'):
        if font_name in font:
            return True
    return False

def install_font(font_path):
    # Install the font if it's not already installed
    font_name = os.path.splitext(os.path.basename(font_path))[0]
    if not is_font_installed(font_name):
        subprocess.run(['fc-cache', '-f', '-v'], check=True)  # Update font cache
        print(f"Installed font: {font_name}")
    else:
        print(f"Font {font_name} is already installed.")
    return font_name

def find_font_name(font_path):
    # Load the font using Pillow to get its name
    font = ImageFont.truetype(font_path, size=12)
    font_name = font.getname()[0]
    return font_name

def burn_subtitles_with_font_and_size(input_video, subtitle_file, output_video, font_path, font_size, alignment, margin_vertical):
    font_name = find_font_name(font_path)  # Find the font name
    # Constructing the filter for subtitles with variable alignment and margin
    (
        ffmpeg_lib
        .input(input_video)
        .output(
            output_video, 
            vf=f"subtitles={subtitle_file}:force_style='FontName={font_name},FontSize={font_size},Alignment={alignment},MarginV={margin_vertical}'"
        )
        .run(overwrite_output=True)
    )

# Usage
font_file = 'font.ttf'  # Path to your custom .ttf font file
install_font(font_file)  # Install the font if not already installed
input_video = 'input.mp4'
subtitle_file = 'subtitles.srt'
output_video = 'output.mp4'
font_size = 24  # Desired font size

# Subtitle positioning variables
alignment = 2  # 1: Bottom left, 2: Bottom center, 3: Bottom right, etc.
margin_vertical = 35  # Pixels to adjust the vertical margin (higher values move it up)

burn_subtitles_with_font_and_size(input_video, subtitle_file, output_video, font_file, font_size, alignment, margin_vertical)