"""Script that extracts e-mail addresses from a pdf (using pdftotext)."""
import os.path
from subprocess import call
from re import findall
import argparse


# Conversion settings
BINARY = 'pdftotext'

# Pattern to match an e-mail address
E_MAIL_PATTERN = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}"


def convert_to_text(pdf_path):
    """Converts a pdf to txt"""
    # Convert to .txt
    command = [BINARY, "-enc", "UTF-8"]
    command.append(pdf_path)
    call(command)
    txt_path = "{base}.txt".format(base=os.path.splitext(pdf_path)[0])
    if os.path.exists(txt_path):
        return txt_path
    return None


def get_emails(pdf_path):
    """Returns all the e-mails in a file"""
    txt_path = convert_to_text(pdf_path)

    if not txt_path:
        return None

    with open(txt_path, 'r') as handle:
        return findall(E_MAIL_PATTERN, handle.read())


def parse_args():
    """Parse args"""
    parser = argparse.ArgumentParser(description="Extract e-mail addresses from a pdf file")
    parser.add_argument("path", help="Path to pdf")
    args = parser.parse_args()
    return args


def main():
    """Main method"""
    args = parse_args()
    emails = get_emails(args.path)
    if emails:
        print("\n".join(emails))
    else:
        print("Could not process file")


if __name__ == "__main__":
    main()
