import argparse
import copy
import re
import traceback

from bs4 import BeautifulSoup


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    with open(args.filename, "r") as fp:
        soup = BeautifulSoup(fp, "xml")

    for attr in soup.FictionBook.attrs.items():
        if attr[0].startswith("xmlns:") and attr[1].endswith("xlink"):
            xlink_ns = attr[0].removeprefix("xmlns:")
            href_attr = xlink_ns + ":href"

    try:
        description = soup.FictionBook.description
        lang = description.lang
        annotation = (copy.copy(child) for child in description.annotation.contents)

        section = soup.new_tag("section")

        title_str = "Аннотация" if lang == "ru" else "Annotation"
        title = soup.new_tag("title", string=title_str)
        section.append(title)
        section.extend(annotation)

        body = soup.FictionBook.body
        body.insert(0, section)
    except Exception:
        print("No annotation in the book")

    to_remove = set()

    for link in soup.find_all("a"):
        try:
            href = link.attrs[href_attr]
            id_ = href.removeprefix("#")
            target = soup.find("section", id=id_)
            link.replace_with(" [[ " + target.get_text() + " ]] ")
            to_remove.add(target)

        except Exception:
            print("-" * 10)
            print(f"Unable to process {link}:")
            print(traceback.format_exc())
            print("-" * 10)

    for section in to_remove:
        section.decompose()

    for body in soup.find_all("body", attrs={"name": re.compile("^(notes|comments)$")}):
        if body.find("section") is None:
            body.decompose()

    with open(args.filename.replace(".fb2", "_inlined.fb2"), "w") as fp:
        fp.write(soup.prettify())


if __name__ == "__main__":
    main()
