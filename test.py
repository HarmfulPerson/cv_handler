import imaplib
import smtplib, ssl
import email
import sys
from email.header import decode_header
import webbrowser
import re
import os
import pathlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

username = input('Podaj swój e-mail:')
password = input('Podaj swoje hasło:')
attachment_dir = pathlib.Path().absolute()
attachments_to_delete = []

def send_answer(message, receiver):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = receiver
        msg['Subject'] = Temat

        body = message
        msg.attach(MIMEText(body, text_type))
        text = msg.as_string()
        server.login(username, password)
        print(username, receiver)
        server.sendmail(username, receiver, text)
        server.quit()

imap = imaplib.IMAP4_SSL("imap.gmail.com")
try:
    imap.login(username, password)
    print ("Zalogowano pomyślnie jako %r !" % username)
except:
    var = imap.error
    print ("Coś poszło nie tak :( %r." % var)
    sys.exit(1)
status, messages = imap.select("INBOX")

ilosc_mejli_w_tyl = 100
zostan = 1
port = 465
text_type = 'plain'

cv_ok = """Witamy, Twoje CV się nam spodobało, niedługo się z Tobą skontaktujemy!"""
Temat = "Rekrutacja u Marcina!"
cv_not_ok = """Witamy, Twoje CV nam się nie spodobało, powodzenia!"""

subjects_to_select = ['praca', 'CV']

messages = int(messages[0])
for i in range(messages, messages-ilosc_mejli_w_tyl, -1):
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode()
            from_ = msg.get("From")
            if subject in subjects_to_select:
                print("Temat:", subject)
                print("Od kogo:", from_)
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        if part.get_content_maintype() == 'multipart':
                            continue
                        if part.get('Content-Disposition') is None:
                            continue
                        filename = part.get_filename()
                        if bool(filename):
                            from_ = re.sub(r"\s+", "", from_, flags=re.UNICODE)
                            if ('<' in from_):
                                start_index = from_.find('<')
                                end_index = from_.find('>')
                                from_ = from_[start_index+1: end_index]
                            filePath = os.path.join(attachment_dir, from_+'.pdf')
                            with open(filePath, 'wb') as f:
                                f.write(part.get_payload(decode=True))
                                webbrowser.open_new(r'C://Users\marci\PycharmProjects\untitled' + '/' + from_+'.pdf')
                                zostan = input('Czy CV sie spodobalo? 1-tak, 2-nie\nOpcja:')
                                zostan = int(zostan)
                                if (zostan == 1):
                                    send_answer(cv_ok, from_)
                                if (zostan == 2):
                                    send_answer(cv_not_ok, from_)
                                    attachments_to_delete.append(from_)
for attachment in attachments_to_delete:
    os.remove(attachment + '.pdf')
imap.close()
imap.logout()