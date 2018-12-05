# secret_santa
---
This is a utility program for determining who should give a gift to who for
secret santa.

## Usage
---
`pipenv run secret_santa --email <EMAIL> --password <PASSWORD>`

The EMAIL and PASSWORD arguments are the credentials needed to log in to your
email server/email provider. The provider defaults to `smtp.gmail.com` and can
be changed in email_handler.py

The program looks for a file called `participants.csv` which should contain
participants for secret santa in the following format:
```
<NAME_1>,<EMAIL_1>,
<NAME_2>,<EMAIL_2>,
...
```
