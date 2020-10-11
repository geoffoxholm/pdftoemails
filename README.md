# pdftoemails

Extracts e-mail addresses from pdfs

## Web page usage

1. Click "Choose File"
2. Select the `pdf` on your computer
3. Click "Get emails"
4. If successful, you will start to download a `csv` file with the e-mails. If unsuccessful, you will see an error message.

## Usage

### Output a list of e-mail

```sh
python3 src/pdftoemail.py my_resume_book.pdf
```

### Copy the list to clipboard (Mac)

```sh
python3 src/pdftoemail.py my_resume_book.pdf | pbcopy
```

### Run a web server

```sh
cd src
./run_service.sh
```
