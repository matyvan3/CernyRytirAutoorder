from time import sleep as wait
from random import random as rng
import requests
from os import fsync as zapis

#start from last scraped card (or 0 if none have been scraped yet)
filename = "vyzranozapi.txt"
session = requests.Session()
with open(filename, "r+") as file:
    try:
        lastnum = int(file.readlines()[-1].split(";")[0]) + 1
    except:
        lastnum = 0
    print("starting at", lastnum)
    toCheck = range(lastnum, 999999)

#check whether a card exists for each number above the starting one
with open(filename, "a+", encoding = "utf8") as file:
    for cardnum in toCheck:
        #timeout prevention
        wait(0.3+rng()*0.4)
        #every 100 tries note down where we are and fully write into the file
        if (not cardnum%100) and (cardnum != lastnum):
            zapis(file.fileno())
            print("trying number: " + str(cardnum))
        url = "https://eshop-api.cernyrytir.eu/api/public/card/" + str(cardnum) + "/REGULAR?eshop_mode=STANDARD&eshop_lang=CZ"
        try:
            resp = session.get(url, timeout = 20)
        except requests.RequestException as error:
            raise error
        if resp.status_code != 200:
            continue
        if resp.text == "":
            continue
        #if the card exists, note down its number and name
        json = resp.json()
        name = json.get("name")
        #save it into the I/O stream
        if len(name):
            file.write(str(cardnum) + ";" + str(name) + "\n")
            file.flush()
    
