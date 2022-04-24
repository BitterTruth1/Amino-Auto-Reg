from time import sleep
from colorama import Fore
from pyfiglet import Figlet
from secmail import SecMail
from amino import Client, device

client = Client()
secmail = SecMail()
emails = []

print(Fore.LIGHTYELLOW_EX + Figlet(font="speed").renderText("Amino\nAutoreg")+"made by @xaquake\ntelegram: https://t.me/aminoxarl\n")

password = input("password for accounts: ")
nickname = input("nickname for accounts: ")

def generate_device():
    return device.generate_device_info()["device_id"]

def get_link(email):
    return SecMail().read_message(email, SecMail().get_messages(email=email).id[0]).htmlBody.split('"')[13]

def register(email, password, nickname, deviceId, code):
    try:
        client.register(nickname=nickname, email=email, password=password, verificationCode=code, deviceId=deviceId)
        return True
    except Exception as e:
        return e

def main(email, password, nickname, deviceId):
    status = register(email=email, password=password, nickname=nickname, deviceId=deviceId, code=input(get_link(email=email)+"\nEnter the code: "))
    if status is True:
        with open("accounts.txt", "a+") as file:
            file.write(f"{email} {password} {deviceId}\n")
            print(f"{email} registered")
    else:
        print(status)

for _ in range(5):
    emails.append(secmail.generate_email())

for email in emails:
    client.request_verify_code(email=email)
    print(f"verification has been sent for {email}")

sleep(6)

for i in emails:
    main(email=i, password=password, nickname=nickname, deviceId=generate_device())
