from super_pocket.settings import click, CONTEXT_SETTINGS
from super_pocket.video.video import compress_video
from super_pocket.video.helper import get_video


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-i', '--input', type=str, help='Input video file path.')
@click.option('-o', '--output', type=str, help='Output video file path.')
@click.option('-c', '--codec', type=str, default="libx264", help='Video codec.')
@click.option('-q', '--quality', type=int, default=22, help='Video quality.')
@click.option('-p', '--preset', type=str, default="slow", help='Video preset.')
@click.option('-a', '--audio-codec', type=str, default="aac", help='Audio codec.')
@click.option('-b', '--audio-bitrate', type=str, default="128k", help='Audio bitrate.')
def video_cli(input: str, output: str, codec: str, quality: int, preset: str, audio_codec: str, audio_bitrate: str):
    """Video compression commands."""
    if not input:
        input = get_video()
    if not output:
        output = get_video(output=True)
    compress_video(input, output, codec, quality, preset, audio_codec, audio_bitrate)


if __name__ == "__main__":
    video_cli()
