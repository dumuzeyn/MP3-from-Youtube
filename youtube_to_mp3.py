import argparse
import os
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
    parser.add_argument(
        "--cookies-from-browser",
        choices=["brave", "chrome", "chromium", "edge", "firefox", "opera", "vivaldi"],
        help="Use cookies from a browser where YouTube is already signed in.",
    )
    parser.add_argument(
        "--cookies",
        help="Path to an exported cookies.txt file.",
    )
    return parser.parse_args()


def resource_path(relative_path):
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative_path


def bundled_ffmpeg_dir():
    ffmpeg_dir = resource_path("ffmpeg")
    if (ffmpeg_dir / "ffmpeg.exe").exists():
        return ffmpeg_dir
    return None


def bundled_deno_path():
    deno_path = resource_path("deno/deno.exe")
    if deno_path.exists():
        return deno_path
    return None


def configure_bundled_ffmpeg():
    ffmpeg_dir = bundled_ffmpeg_dir()
    if ffmpeg_dir is not None:
        os.environ["PATH"] = str(ffmpeg_dir) + os.pathsep + os.environ.get("PATH", "")
    return ffmpeg_dir


def download_mp3(
    urls,
    output_dir,
    quality,
    progress_hooks=None,
    logger=None,
    cookies_from_browser=None,
    cookies_file=None,
    cancel_event=None,
):
    output_path = Path(output_dir).expanduser().resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    ffmpeg_dir = configure_bundled_ffmpeg()
    deno_path = bundled_deno_path()

    options = {
        "format": "bestaudio/best",
        "outtmpl": str(output_path / "%(title).200B.%(ext)s"),
        "windowsfilenames": True,
        "ignoreerrors": True,
        "remote_components": ["ejs:github"],
        "noplaylist": False,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
    }
    if ffmpeg_dir is not None:
        options["ffmpeg_location"] = str(ffmpeg_dir)
    if deno_path is not None:
        options["js_runtimes"] = {"deno": {"path": str(deno_path)}}
    hooks = list(progress_hooks or [])
    if cancel_event is not None:
        def cancel_hook(_info):
            if cancel_event.is_set():
                raise DownloadError("Cancelled by user.")

        hooks.insert(0, cancel_hook)
    if hooks:
        options["progress_hooks"] = hooks
    if logger:
        options["logger"] = logger
    if cookies_file:
        options["cookiefile"] = str(Path(cookies_file).expanduser().resolve())
    if cookies_from_browser:
        options["cookiesfrombrowser"] = (cookies_from_browser,)

    with YoutubeDL(options) as ydl:
        failures = ydl.download(urls)
        return failures


def main():
    args = parse_args()

    try:
        failures = download_mp3(
            args.urls,
            args.output_dir,
            args.quality,
            cookies_from_browser=args.cookies_from_browser,
            cookies_file=args.cookies,
        )
        if failures:
            print(f"Completed with {failures} failed item(s).", file=sys.stderr)
            return 1
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
