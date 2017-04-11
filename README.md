# imeil.py
A python script to test smtp/email servers.  Accepts multiple arguments from command line.

## Pre requisites
* Python 3.4+
* python-magic --> pip3 install python-magic

## Usage
```sh
usage: Imeil [-h] [-f address [Full Name ...]] [-m SMTPHOST] [-s SUBJECT]
             [-b BODY] [-l HTML] [-r address [Full Name ...]]
             [-c address [Full Name ...]] [-o address [Full Name ...]] [-u]
             [-d] [-i] [-a ATTACHMENTS [ATTACHMENTS ...]] [-p] [-t] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -f address [Full Name ...], --mailfrom address [Full Name ...]
                        Mail From:
  -m SMTPHOST, --smtphost SMTPHOST
                        SMTP server where to send feed
  -s SUBJECT, --subject SUBJECT
                        Subject
  -b BODY, --body BODY  text/plain body - String or path to the file
                        containing the body
  -l HTML, --htmlbody HTML
                        text/html body - String or path to the file containing
                        the html body
  -r address [Full Name ...], --rcptto address [Full Name ...]
                        RCPT TO:
  -c address [Full Name ...], --cc address [Full Name ...]
                        CC:
  -o address [Full Name ...], --bcc address [Full Name ...]
                        BCC:
  -u, --success         Success Notification to be sent from the server
  -d, --delay           Delay Notification to be sent from the server
  -i, --failure         Failure Notification to be sent from the server
  -a ATTACHMENTS [ATTACHMENTS ...], --attach ATTACHMENTS [ATTACHMENTS ...]
                        Path to files to attach
  -p, --print           Prints the message instead of sending it
  -t, --notls           Disables TLS
  -v, --verbose         Verbose
```