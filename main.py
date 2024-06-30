import time
from itertools import chain
import email, email.policy
import imaplib
import requests

imap_ssl_host = 'imap.gmail.com'
imap_ssl_port = 993
username = 'YOUR GMAIL ACCOUNT HERE'
password = 'YOUR Application Password HERE'
webhook_url = "YOUR Discord webhook URL HERE"

while 1:
    mail = imaplib.IMAP4_SSL(imap_ssl_host)
    mail.login(username, password)
    mail.select(mailbox="INBOX", readonly=False)
    result, data = mail.search(None, '(UNSEEN)')
    uids = data[0].decode().split()
    uids.reverse()

    for uid in uids:
        resp_code, mail_data = mail.fetch(uid, '(RFC822)')
        message = email.message_from_bytes(mail_data[0][1] , policy=email.policy.SMTPUTF8)

        data = {}

        data["embeds"] = [
            {
                "description": "Gmail Notification",
                "title": "",
                "color":0xfe7e06,
                "fields":[
                    {
                    "name":"Subject: {}".format(message.get("Subject")),
                    "value":"From:     {}".format(message.get("From"))
                    }
                ]
            }
        ]

        result = requests.post(webhook_url, json=data)

        try:
            result.raise_for_status()
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            print("Payload delivered successfully, code {}.".format(result.status_code))

        time.sleep(2)
        # to prevent too many requests for webhook
        
    mail.logout()
    time.sleep(120)
    # cooldown for search again
