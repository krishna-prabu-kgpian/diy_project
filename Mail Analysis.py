import os
from imbox import Imbox 
import traceback
import time
from FunctionsLibrary import ContentFromJSON
from FunctionsLibrary import ImageAnalysis
from FunctionsLibrary import NumberToBeFed
import serial

host = "imap.gmail.com"
username = "yourusername@gmail.com"
password = 'password'
download_folder = "path/to/download/folder"

isEmailDownloaded = 0

isImageAnalysed = 0

arduino = serial.Serial(port='COM12', baudrate=115200, timeout=0.1)

if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)

while True:
    print()
    try:
        mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
        messages = mail.messages(unread=True, subject='Please Check')

        print("Defined imbox for downloading the mail.")

        for (uid, message) in messages:
            mail.mark_seen(uid)
            print("Marked message as read.")

            for idx, attachment in enumerate(message.attachments):
                try:
                    att_fn = attachment.get('filename')
                    download_path = f"{download_folder}/{att_fn}"
                    print(download_path)
                    with open(download_path, "wb") as fp:
                        fp.write(attachment.get('content').read())
                    isEmailDownloaded = 1
                    print("Image Downloaded.")
                except:
                    print(traceback.print_exc())

        mail.logout()
        print("Mail ended.")

    except Exception as e:
        print("An error occured", e)

    if (isEmailDownloaded == 1):
        print("Analyzing image...")
        data = ImageAnalysis()

        output = ContentFromJSON(data)

        print(output)

        number = NumberToBeFed(output)

        print(number)
        stringnumber = str(number)

        print("Image Analyzed, output transmitting...")

        isEmailDownloaded = 0

        isImageAnalysed = 1

    if (isImageAnalysed == 1):
        arduino.write(bytes(stringnumber, 'utf-8'))
        time.sleep(0.05)
        print("Output transmitted. Have a good day.")
        isImageAnalysed = 0

    time.sleep(5)

    print("Scanning....")