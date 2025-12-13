import argparse
import os
import re
import shutil

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("-i", "--preserve-images", action="store_true")
    args = parser.parse_args()

    filename = args.filename
    out_dir = filename.removesuffix(".fb2")
    if os.path.exists(out_dir):
        if input("Output path exists. Remove it? (y/N): ").lower() == "y":
            shutil.rmtree(out_dir)
        else:
            exit(0)

    os.mkdir(out_dir)

    with open(filename, "r") as fp:
        soup = BeautifulSoup(fp, "xml")

    if args.preserve_images:
        for attr in soup.FictionBook.attrs.items():
            if attr[0].startswith("xmlns:") and attr[1].endswith("xlink"):
                xlink_ns = attr[0].removeprefix("xmlns:")
                href_attr = xlink_ns + ":href"
    else:
        coverpage = soup.FictionBook.description.find("coverpage")
        if coverpage is not None:
            coverpage.decompose()

    title_info = soup.description.find("title-info")

    book_title = title_info.find("book-title").string

    body = soup.body

    if args.preserve_images:
        binaries = {
            binary["id"]: binary.extract() for binary in body.find_all_next("binary")
        }
    else:
        for binary in body.find_all_next("binary"):
            binary.decompose()
        for image in body.find_all("image"):
            image.decompose()

    sections = [
        section.extract() for section in body.find_all("section", recursive=False)
    ]

    for i, section in enumerate(sections):
        try:
            body.append(section)

            title = section.title.text
            title = title.replace("\n", " ")
            title = title.replace("\t", " ")
            title = re.sub(r"\s\s+", " ", title)
            title = re.sub(r"\[\[.*?\]\]", "", title)
            title = title.strip()

            if args.preserve_images:
                for image in soup.find_all("image"):
                    href = image[href_attr]
                    id_ = href.removeprefix("#")

                    binary = binaries[id_]
                    soup.FictionBook.append(binary)

            title_info.find("book-title").string = f"{title} from {book_title}"

            with open(os.path.join(out_dir, f"{i + 1:02}.{title}.fb2"), "w") as fp:
                fp.write(soup.prettify())

            body.clear(
                decompose=True
            )  # necessary to run after the first run to remove titles and epigraphs
            section.decompose()

            if args.preserve_images:
                for binary in body.find_all_next("binary"):
                    binary.extract()
        except Exception as e:
            terminal_width = shutil.get_terminal_size(fallback=(80, 1))[0]
            print("-" * terminal_width)
            print(f"Error while processing {i + 1:02}")
            print(repr(e))
            print(section)
            print("-" * terminal_width)


if __name__ == "__main__":
    main()
