import argparse
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file-name", default="fb2_inline_plaintext.py")
    args = parser.parse_args()

    if os.path.isfile(args.file_name):
        print(
            f"{args.file_name} already exists in current directory. Run it like './{args.file_name} or remove if want to start from scratch"
        )
        exit(1)

    with open(args.file_name, "w") as f:
        f.write(
            r"""\
#!/usr/bin/env python3

import os
import re
import sys
import zipfile


def is_fb2(x: str):
    return x.endswith(".fb2")


def process_file(contents: str) -> str:
    while (link := re.search(r"\[(\d+)\]", contents)) is not None:
        num = link.group(1)
        target = re.search(r"<p>" + str(num) + r". (.+?)<\/p>", contents)

        if target is None:
            print(f"Dangling link [{num}]")
            exit(1)

        text = target.group(1)

        contents = (
            contents[: link.start()] + f" [[{num}: {text}]] " + contents[link.end() :]
        )

    return contents


if len(sys.argv) != 2:
    print("Supply book file as the only argument")
    exit(1)

filename = sys.argv[1]

print(
    f"Make shure the script has correct regexes for {filename}. Process (y/N):",
    end=" ",
)
if input()[:1].lower() != "y":
    exit(0)

if filename.endswith(".zip"):
    new_contents: dict[str, str] = {}

    with zipfile.ZipFile(filename, "r") as zip_ref:
        files = zip_ref.namelist()
        for file in files:
            if file.endswith(".fb2"):
                print(f"Processing {file}")
                with zip_ref.open(file, "r") as file_ref:
                    contents = file_ref.read().decode()

                new_contents[file] = process_file(contents)

        base_name = os.path.splitext(filename)[0]

        match len(new_contents.values()):
            case 0:
                print("No fb2 book found")
                exit(1)
            case 1:
                new_file = (
                    os.path.join(
                        os.path.dirname(base_name),
                        os.path.splitext(list(new_contents.keys())[0])[0],
                    )
                    + "_notes.fb2"
                )
                with open(new_file, "w") as f:
                    f.write(list(new_contents.values())[0])
            case _:
                os.makedirs(base_name, exist_ok=True)
                for file, contents in new_contents.items():
                    new_file = os.path.join(
                        base_name, os.path.splitext(file)[0] + "_notes.fb2"
                    )
                    with open(new_file, "w") as f:
                        f.write(contents)
                pass
elif filename.endswith(".fb2"):
    with open(filename, "r") as f:
        contents = f.read()

    new_content = process_file(contents)

    with open(os.path.splitext(filename)[0] + "_notes.fb2", "w") as f:
        f.write(new_content)
else:
    print("Unsupported file type")
    exit(1)
"""
        )

    print(
        f"./{args.file_name} was created. Edit it to properly handle specific book. Then run like an ordinary executable `./{args.file_name}`"
    )


if __name__ == "__main__":
    main()
