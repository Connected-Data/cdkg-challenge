import glob
import re
from pathlib import Path

output_path = Path("./data")
output_path.mkdir(parents=True, exist_ok=True)


def convert_srt_to_text(srt_content):
    # Remove timestamps and subtitle numbers
    pattern = r"\d+\n\d{2}:\d{2}:\d{2},\d{3}\s-->\s\d{2}:\d{2}:\d{2},\d{3}\n(.*?)\n\n"
    matches = re.finditer(pattern, srt_content + "\n\n", re.DOTALL)

    # Extract and join the text portions
    text_parts = [match.group(1).replace("\n", " ").strip() for match in matches]
    return " ".join(text_parts)


def process_srt_files():
    # Get all .srt files recursively
    srt_files = glob.glob("../../Transcripts/**/*.srt", recursive=True)

    for srt_path in srt_files:
        filename = Path(srt_path).stem
        # Create path for output file
        txt_path = output_path / f"{filename}.txt"
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            # Read the .srt file
            with open(srt_path, "r", encoding="utf-8") as f:
                srt_content = f.read()

            # Convert to plain text
            plain_text = convert_srt_to_text(srt_content)

            # Write the text file
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(plain_text)

            print(f"Converted {srt_path} -> {txt_path}")

        except Exception as e:
            print(f"Error processing {srt_path}: {str(e)}")


if __name__ == "__main__":
    process_srt_files()
