from rich.prompt import Prompt
from rich.text import Text

def get_video(output=False):
    destination = "Input" if not output else "Output"
    default = "input.mov" if not output else "video_legere.mp4"
    video = Prompt.ask(
        Text(f"{destination} video file path ?", style="bold orange_red1"),
        default=default
    )
    return video