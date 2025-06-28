import os
import re
import sys

# Get the path for fonts.txt
def get_fonts_file_path():
    if getattr(sys, 'frozen', False):  # If running as a bundled executable
        return os.path.join(sys._MEIPASS, "fonts.txt")  # Use temp path provided by PyInstaller
    else:
        return "fonts.txt"  # If running from source, look in the current directory

# Load font mapping from Fonts.txt
font_map = {}
fonts_file_path = get_fonts_file_path()  # Get the correct path for fonts.txt

if os.path.exists(fonts_file_path):  # Check if fonts.txt exists at the path
    with open(fonts_file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("=", 1)
            if len(parts) == 2:
                original, replacement = parts
                font_map[original.strip().lower()] = replacement.strip()

def convert_font_name(match):
    font_name = match.group(1).strip()
    replacement = font_map.get(font_name.lower())
    if replacement:
        return f'<font="{replacement}">'  # Apply mapped font name
    return f'<font="{font_name}">'       # Fallback to original

def convert_color(match):
    bgr = match.group(1)
    rgb = bgr[4:6] + bgr[2:4] + bgr[0:2]
    return f"<color=#{rgb}>"

def convert_alpha(match):
    hex_alpha = match.group(1)
    flipped = 255 - int(hex_alpha, 16)
    return f"<alpha=#{flipped:02X}>"

def convert_font_size(match):
    return f"<size={match.group(1)}>"

TAG_REPLACEMENTS = {
    r"\\s1": "<s>", r"\\s0": "</s>",
    r"\\b1": "<b>", r"\\b0": "</b>",
    r"\\i1": "<i>", r"\\i0": "</i>",
    r"\\u1": "<u>", r"\\u0": "</u>",
    r"\\c": "</color>",
    r"\\fs0": "</size>",
    r"\\N": "<br>",
}

def process_ass_to_rich_text(text):
    def override_replacer(match):
        override = match.group(1)
        override = re.sub(r"\\fn([^\\}]+)", convert_font_name, override, flags=re.IGNORECASE)
        override = re.sub(r"\\fs(\d+)", convert_font_size, override)
        override = re.sub(r"\\c&H([0-9A-Fa-f]{6})&", convert_color, override)
        override = re.sub(r"\\1a&H([0-9A-Fa-f]{2})&", convert_alpha, override)
        for pattern, replacement in TAG_REPLACEMENTS.items():
            override = re.sub(pattern, replacement, override)
        return override

    text = re.sub(r"{([^}]*)}", override_replacer, text)
    text = re.sub(r"\\fn([^\\}]+)", convert_font_name, text, flags=re.IGNORECASE)
    for pattern, replacement in TAG_REPLACEMENTS.items():
        text = re.sub(pattern, replacement, text)
    return text

def convert_ass_file(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    processed_lines = [process_ass_to_rich_text(line) if line.startswith("Dialogue:") else line for line in lines]

    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(processed_lines)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python script.py input.ass output.ass")
    else:
        convert_ass_file(sys.argv[1], sys.argv[2])
        print(f"✅ Converted file saved as: {sys.argv[2]}")
