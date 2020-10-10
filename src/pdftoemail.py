"""Script that extracts e-mail addresses from a pdf (using pdftotext). Also provides FLASK hooks"""

from flask import Flask, request, render_template, make_response, redirect, url_for
import os.path
import uuid
from subprocess import call
from re import findall
import argparse
from csv import writer
from io import StringIO

# Initialize flask
APP = Flask(__name__)
APP.config['UPLOAD_PATH'] = "uploads"

# Templates
UPLOAD_TEMPLATE = "upload.html"

# Conversion settings
BINARY = '/usr/local/bin/pdftotext'

# Pattern to match an e-mail address
E_MAIL_PATTERN = "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}"


def convert_to_text(pdf_path):
    """Converts a pdf to txt"""
    # Convert to .txt
    command = [BINARY, "-enc", "UTF-8"]
    command.append(pdf_path)
    print(command)
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


@APP.route('/')
def root():
    """Simple root entry"""
    return render_template(UPLOAD_TEMPLATE)


@APP.route('/upload', methods=['POST'])
def endpoint_upload():
    """Upload"""
    if "file" not in request.files:
        return redirect(url_for(''))

    _file = request.files['file']
    filename = f"{uuid.uuid4()}.pdf"
    abspath = os.path.join(APP.config['UPLOAD_PATH'], filename)
    _file.save(abspath)
    emails = get_emails(abspath)
    if not emails:
        return "None found"
    string_io = StringIO()
    csv_writer = writer(string_io)
    csv_writer.writerow(["e-mail"])
    for row in emails:
        csv_writer.writerow([row])
    output = make_response(string_io.getvalue())
    name = os.path.splitext(os.path.basename(_file.filename))[0]
    output.headers["Content-Disposition"] = f"attachment; filename={name}_emails.csv"
    output.headers["Content-type"] = "text/csv"
    return output


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
