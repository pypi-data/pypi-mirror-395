import yt_dlp
import argparse
import os
import shutil
import sys

def main():
    parser = argparse.ArgumentParser(description="rob - file and YouTube downloader")
    parser.add_argument("url", nargs="?", help="File URL or YouTube video URL")
    parser.add_argument("-q", "--quality", help="Video quality (e.g., 720, 480, best, worst)(to be used with -v)", default="best")
    parser.add_argument("-f", "--file", help="Download a normal file instead of a video", action="store_true")
    parser.add_argument("-v", "--video", help="Download a Youtube video", action="store_true")
    parser.add_argument("-u", "--update", help="Updates rob", action="store_true")

    args = parser.parse_args()

    def has_ffmpeg():
        return shutil.which("ffmpeg") is not None

    ####################
    # File flag
    ####################

    if args.file:
        if not args.url:
            print("no url provided")
            sys.exit(1)

        output_filename = args.url.split("/")[-1]
        os.system(f'curl -L -o "{output_filename}" "{args.url}"')
        print(f"file downloaded as: {output_filename}")

    ####################
    # Video flag
    ####################

    elif args.video:
        if not args.url:
            print("no url provided")
            sys.exit(1)

        ffmpeg_installed = has_ffmpeg()

        if args.quality.isdigit():
            if ffmpeg_installed:
                format_string = f"bestvideo[height<={args.quality}]+bestaudio/best"
            else:
                format_string = f"best[height<={args.quality}]"
        else:
            format_string = args.quality if ffmpeg_installed else "best"

        ydl_opts = {
            "format": format_string,
            "merge_output_format": "mp4",
            "noplaylist": True
        }

        if not ffmpeg_installed:
            print("ffmpeg not found — downloading single file without merging")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([args.url])
        except Exception as error:
            print("download failed:", error)

    ####################
    # Update rob flag
    ####################

    elif args.update:
        pm = input("Update using (1) pip or (2) uv?")
        if pm == "1":
            print("Updating rob using pip")
            os.system("pip install rob-dl")
        elif pm == "2":
            os.system("uv pip install rob-dl")
        else:
            print("Please input (1) pip or (2) uv")

    ####################
    # No flags
    ####################

    else:
        print("Please provide a flag; -v for video, -f for file, or -u for updating rob")

if __name__ == "__main__":
    main()