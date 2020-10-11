"""Script that provides FLASK hooks to be a pdf to email service (and basic website)"""

import os.path
import uuid
from csv import writer
from io import StringIO
from flask import Flask, request, render_template, make_response

from pdftoemail import get_emails

# Initialize flask
APP = Flask(__name__)
APP.config['UPLOAD_PATH'] = "uploads"

# Templates
UPLOAD_TEMPLATE = "upload.jinja"

# Filename to reply with for download
RESULT_FILENAME_TEMPLATE = "{name}_emails.csv"


@APP.route('/', methods=['POST', 'GET'])
def root():
    """Main entry"""
    if request.method == "GET" or "file" not in request.files:
        return render_template(UPLOAD_TEMPLATE)

    # Check the file for the right extension
    _file = request.files['file']
    name, ext = os.path.splitext(os.path.basename(_file.filename))
    if ext.lower()[1:] not in ['pdf']:
        return render_template(UPLOAD_TEMPLATE, error="Only works on a pdf")

    # Save the file
    filename = f"{uuid.uuid4()}.pdf"
    abspath = os.path.join(APP.config['UPLOAD_PATH'], filename)
    _file.save(abspath)

    # Get the e-mails from it
    emails = get_emails(abspath)
    if not emails:
        return render_template(UPLOAD_TEMPLATE, error="No e-mails found in document")

    # Build a CSV file into memory
    string_io = StringIO()
    csv_writer = writer(string_io)
    csv_writer.writerow(["e-mail"])
    for row in emails:
        csv_writer.writerow([row])

    # Return the CSV file
    output = make_response(string_io.getvalue())
    result = RESULT_FILENAME_TEMPLATE.format(name=name)
    output.headers["Content-Disposition"] = f"attachment; filename={result}"
    output.headers["Content-type"] = "text/csv"
    return output
