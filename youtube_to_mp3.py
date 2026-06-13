import argparse
import sys
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError


def parse_args():
    parser = argparse.ArgumentParser(
        description="Download one or more YouTube videos as MP3 files."
    )
    parser.add_argument(
        "output_dir",
        help="Folder where MP3 files will be saved.",
    )
    parser.add_argument(
        "urls",
        nargs="+",
        help="One or more YouTube video or playlist links.",
    )
    parser.add_argument(
        "--quality",
        default="192",
        choices=["128", "192", "256", "320"],
        help="MP3 bitrate in kbps. Default: 192.",
    )
    return parser.parse_args()


def download_mp3(urls, output_dir, quality):
    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)

    options = {
        "format": "bestaudio/best",
        "outtmpl": str(output_path / "%(title).200B.%(ext)s"),
        "windowsfilenames": True,
        "ignoreerrors": True,
        "noplaylist": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
    }

    with YoutubeDL(options) as ydl:
        ydl.download(urls)


def main():
    args = parse_args()

    try:
        download_mp3(args.urls, args.output_dir, args.quality)
    except KeyboardInterrupt:
        print("\nDownload cancelled.", file=sys.stderr)
        return 130
    except DownloadError as error:
        message = str(error)
        print(f"Download error: {message}", file=sys.stderr)

        if "playlist does not exist" in message.lower():
            print(
                "YouTube says this playlist does not exist. Check that the link is correct, "
                "the playlist is public, and it opens in your browser.",
                file=sys.stderr,
            )
        else:
            print(
                "Check the YouTube link and try updating yt-dlp: "
                "python -m pip install -U yt-dlp",
                file=sys.stderr,
            )

        return 1
    except Exception as error:
        print(f"Error: {error}", file=sys.stderr)
        print(
            "If this happened during MP3 conversion, make sure ffmpeg is available in PATH.",
            file=sys.stderr,
        )
        return 1

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
