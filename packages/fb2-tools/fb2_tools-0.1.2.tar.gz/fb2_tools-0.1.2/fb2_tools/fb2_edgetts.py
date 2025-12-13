import argparse
import os
import re
import subprocess
import time
import zipfile
from collections import deque
from pathlib import Path
from typing import Literal

from selenium import webdriver
from splinter import Browser


def init_browser(download_dir: Path):
    options = webdriver.firefox.options.Options()
    options.binary_location = "/usr/bin/librewolf"

    options.set_preference("browser.download.folderList", 2)  # use custom download path
    options.set_preference("browser.download.dir", str(download_dir.absolute()))
    options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "audio/mpeg")

    browser = Browser("firefox", options=options)

    return browser


def set_value(id_: str, value, browser: Browser):
    browser.execute_script(f"document.getElementById('{id_}').value = {value}")
    browser.execute_script(
        f"document.getElementById('{id_}').dispatchEvent(new Event('input'))"
    )


def set_expanding(id_: str, value, browser: Browser):
    if not browser.find_by_id(id_).visible:
        browser.find_by_id("dop-settings-label").click()
    set_value(id_, value, browser)


def display_block(id_: str, browser: Browser):
    browser.evaluate_script(f"document.getElementById('{id_}').style.display = 'block'")


def set_up_browser(
    browser: Browser,
    pointstype: Literal["V1", "V2", "V3"],
    rate: int,
    pitch: int,
    max_threads: int,
    mergefiles: int,
):
    browser.visit("https://edgetts.github.io")

    while browser.find_by_id("pointstype").value != pointstype:
        browser.find_by_id("pointstype").click()

    set_value("rate", rate, browser)

    set_expanding("pitch", pitch, browser)
    set_expanding("max-threads", max_threads, browser)
    set_expanding("mergefiles", mergefiles, browser)

    display_block('file-input', browser)
    browser.evaluate_script("document.getElementById('file-input').name = 'file-input'")

    display_block("stat-area", browser)

pieces_regex = re.compile(r"(\d+) / (\d+)")


def get_stats(index: int, browser: Browser):
    assert index == 1 or index == 2

    return pieces_regex.search(browser.find_by_id("stat-str").value).group(index)


def finished_downloading(path: Path):
    part_path = path.with_name(path.name + ".part")

    return path.exists() and not part_path.exists()


def zip_dir(dir_path: Path, target: Path):
    with zipfile.ZipFile(target, "w", zipfile.ZIP_STORED) as zipf:
        for file_path in dir_path.rglob("*"):
            if file_path.is_file():
                arcname = file_path.relative_to(dir_path)
                zipf.write(file_path, arcname)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="*", default=[Path(".")], type=Path)
    parser.add_argument(
        "-o", "--output", default=Path("~/Music/tmp").expanduser(), type=Path
    )

    parser.add_argument("--pointstype", choices=["V1", "V2", "V3"], default="V3")
    parser.add_argument("--rate", type=int, choices=range(-50, 100 + 1), default=75)
    parser.add_argument("--pitch", type=int, choices=range(-50, 50 + 1), default=0)
    parser.add_argument("--max-threads", type=int, choices=range(1, 30 + 1), default=20)
    parser.add_argument(
        "--mergefiles",
        type=int,
        choices=range(1, 100 + 1),
        default=100,
        help="100 means merge all pieces",
    )

    parser.add_argument("--skip-downrate", action="store_true")
    parser.add_argument("--skip-archive", action="store_true")
    args = parser.parse_args()

    if len(args.source) == 1:
        source = args.source[0]
        if source.is_dir():
            out_name = source.name
        else:
            out_name = source.stem.removesuffix(".fb2")

        output_dir = args.output / out_name
    else:
        output_dir = args.output

    if not output_dir.exists():
        os.makedirs(output_dir)
    elif not output_dir.is_dir():
        print(f"Output must be a directory: '{output_dir}'")
        exit(1)
    elif len(list(output_dir.iterdir())) != 0 and not args.skip_downrate:
        print(
            f"Output directory '{output_dir}' is not empty."
            f" Running downrate.sh on it may cause unwanted files changed and messed up statistics."
        )
        if input("Continue? (y/N): ").lower() != "y":
            exit(0)

    browser = init_browser(output_dir)
    set_up_browser(
        browser,
        args.pointstype,
        args.rate,
        args.pitch,
        args.max_threads,
        args.mergefiles,
    )

    to_process: deque[Path] = deque(args.source)
    outputs = set()
    while to_process:
        path = to_process.popleft()

        if path.is_dir():
            to_process.extend(path.iterdir())
        else:
            if path.exists():
                browser.attach_file("file-input", str(path))
                outputs.add(output_dir / path.with_suffix(".mp3").name)

    if browser.is_text_present("Открыты"):
        overall_pieces = get_stats(2, browser)
        browser.find_by_id("savebutton").click()

        processed_pieces = get_stats(1, browser)
        while any(
            status in browser.find_by_id("stat-area").value
            for status in ("Открыта", "Запущена", "Обработка", "ПЕРЕЗАПУСК")
        ):
            print(
                f"Processing {processed_pieces}/{overall_pieces}",
                end="\r",
                flush=True,
            )
            time.sleep(0.5)
            processed_pieces = get_stats(1, browser)
        print(
            f"Processed {get_stats(1, browser)}/{overall_pieces}   "
        )  # spaces to flush remainings of previous line contents

        i = 0
        while outputs:
            print(f"Downloading{'.' * i}", end="\r", flush=True)
            for path in outputs.copy():
                if finished_downloading(path):
                    outputs.remove(path)
                    print(f"Produced '{path}'")

            time.sleep(0.5)
            i += 1

    browser.quit()

    if not args.skip_downrate:
        print("Downrating")
        try:
            res = subprocess.run(
                ["downrate.sh"],
                capture_output=True,
                check=True,
                cwd=output_dir,
                text=True,
            )

            print(res.stdout.strip())
        except subprocess.CalledProcessError as e:
            print("Failed to downrate output directory:")
            print(e.stderr)

    if not args.skip_archive:
        zip_path = Path(output_dir.with_name(output_dir.name + ".zip"))
        if zip_path.exists():
            print(f"'{zip_path}' already exists. Do you want to recreate it? (y/N): ")
            if input().lower() == "y":
                zip_dir(output_dir, zip_path)
        else:
            zip_dir(output_dir, zip_path)
        print(f"Compressed to '{zip_path}")


if __name__ == "__main__":
    main()
