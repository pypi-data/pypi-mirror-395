import subprocess
import os
from rich.prompt import Prompt
from rich.text import Text
from super_pocket.video.helper import get_video

def compress_video(input_file: str, 
                   output_file: str,
                   video_codec: str = "libx264",
                   video_quality: int = 22,
                   video_preset: str = "slow",
                   audio_codec: str = "aac",
                   audio_bitrate: str = "128k") -> None:
    # Check if the file exists
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    command = [
        "ffmpeg",
        "-i", input_file,
        "-c:v", video_codec,     		# Codec (other option: libx265)
        "-crf", str(video_quality),   	# Quality (adjust if needed)
        "-preset", video_preset, 		# Compression preset	
        "-c:a", audio_codec,     		# Audio codec
        "-b:a", audio_bitrate,   		# Audio bitrate
        output_file
    ]

    try:
        print(f"Compressing {input_file}...")
        subprocess.run(command, check=True)
        print(f"Success! Video saved to: {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    input = get_video()
    output = get_video(output=True)
    compress_video(input, output)