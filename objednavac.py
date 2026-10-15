import requests
from time import sleep as wait
import re
from sys import stdin as lines
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#loading cards data to memory (until I turn the cards data into a usable JSON)
#currently they're ordered by a proprietary card number - not by name due to the scraping process
databaze = {}
with open("vyzranozapi.txt", "r") as file:
    for availableVersionCount in file.readlines():
        line = availableVersionCount.split(";")
        name = line[1].split(" (")[0]
        num = line[0]
        nakup = line[3][:-1]
        if not name in databaze:
            databaze[name] = {}
        databaze[name][num] = nakup

#initialize session for interacting with www
session = requests.Session()
cardsList = {}
totalWanted = 0

#set up a headless browser
opts = webdriver.ChromeOptions()
opts.add_argument("--window-size=1920,1080")
opts.add_argument("--enable-javascript")
opts.add_argument("--headless=new")
driver = webdriver.Chrome(options = opts)

#keep trying to log in until successful
while driver.title != "Černý Rytíř | Magic: The Gathering – Karty, Sety, Doplňky | Praha":
       
    #get user's login details (only used for headless login, not stored locally nor in the cloud)
    username = input("Enter your cernyrytir username: ")
    password = input("Enter your cernyrytir password: ")

    #go to cernyrytir website
    driver.get("https://cernyrytir.cz")
    wait(2)

    #deny cookies to the poor bot
    try:
        cookieButton = driver.find_element(By.ID, "CybotCookiebotDialogBodyButtonDecline")
        if cookieButton:
            cookieButton.click()
    except:
        pass
        
    #jump to the login screen
    driver.find_element(By.CLASS_NAME, "profile-icon").click()
    wait(0.1)

    #fill in and submit the login form
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "kc-login").click()
    wait(0.5)
    
#after waiting for the page to fully load finally grab the basketUID (needless with the current approach)
#wait(2)
#basketUID = driver.execute_script("return window.localStorage.getItem('standard_basket_uuid');")
#print("basketUID found:", basketUID)

#getting the decklist either directly or via Moxfield
if input("Moxfield link (0) or direct list (1)? ") != "0":
    deck = []
    last = 0
    line = input("Enter your decklist and press Enter twice: ")
    while 1:
        if line != "":
            deck.append(line)
            last = 0
        elif last:
            break
        else:
            last = 1
        line = input()
    for x in range(len(deck)):
        #check whether there's a card count on line start
        count = re.match(r"\d*", deck[x]).group(0)
        if count:
            cardsList[deck[x].split(" ", 1)[1]] = int(count)
            totalWanted += int(count)
        else:
            cardsList[deck[x]] = 1
            totalWanted += 1

#user picked Moxfield as the deck source        
else:
    moxLink = input("Enter your Moxfield deck's Public ID or link: ").split("/")[-1]
    url = "https://api2.moxfield.com/v2/decks/all/" + moxLink
    try:
        #we try requesting the deck data
        resp = session.get(url, timeout=20)
        json = resp.json()
        #if we succeed, we tell the user and prepare the cardslist
        if json.get("name"):
            print("\nDeck located: " + json.get("name"))
        deck = json.get("mainboard")
        sideboard = json.get("sideboard")
        for part in [deck, sideboard]:
            for card in part.keys():
                qty = part[card][list(part[card].keys())[0]]
                totalWanted += qty
                cardsList[card] = qty
    except:
        #if we fail, we tell the user (and use mock data for now)
        print("\nDeck not found, using mock data..")
        cardsList = {"Opt":4, "Visions of Beyond":5}
        totalWanted = sum(cardsList.values())

autoOrderCheapest = True #False if input("\nAutomatically order cheapest available printings? (yes/no) ").lower() != "yes" else True
orderList, missingList, unknownList = {}, {}, []
orderTotal = 0

#define a method for ordeing the cards
def order(cardNum, qty):
    try:
        driver.get("https://cernyrytir.cz/mtg/detail/" + str(cardNum) + "/REGULAR")
        wait(1.5)
        driver.find_element(By.XPATH, "//*[@id=\"price-row\"]/div[2]/div/button").click()
        if qty > 1:
            wait(0.5)
            countField = driver.find_element(By.XPATH, "//*[@id=\"price-row\"]/div[2]/div/div[2]/div/label/div/div/div/input")
            countField.click()
            countField.send_keys(Keys.DELETE, str(qty), Keys.RETURN)
        return True
    except:
        return False

#once we have the cardslist, we check avilability of the cards
for card in cardsList.keys():

    #check whether the cardname is in our card data and inform user if it ain't
    if not(card in databaze):
        print("\nCard", card, "unknown, check the spelling")
        unknownList.append(card)
        totalWanted -= cardsList[card]
        continue
    
    qty = cardsList[card]
    
    # if there's multiple versions of the card available, we check each variant for availability
    if len(databaze[card].keys()) > 1:
        
        #since people usually have Basic Lands we ask whether the user is even interested in ordering those (if not, we skip to the next card)
        if card in ["Plains", "Island", "Swamp", "Mountain", "Forest"]:
            if input("\n"+card+" is a Basic Land, do you need to order those? (yes/no) ").lower() != "yes":
                continue
            
        #we look up how many printings the card has
        variants = len(databaze[card].keys())
        print("\nThere's", variants, "printings of" if variants > 1 else "printing of", card, "and you want", qty, "copies.\nAvailable ones:")
        availableVersionCount, total= 0, 0
        availablePrintings = {}
        
        #for each variant check for availability and price
        for cardNum, pUID in databaze[card].items():
            fetch = session.get("https://eshop-api.cernyrytir.eu/api/public/card/" + cardNum + "/REGULAR?eshop_mode=STANDARD&eshop_lang=CZ")
            temp = fetch.json()
            available = temp.get("internalCards")[0]["availEshopQty"]
            edition = temp.get("cardEditionName")
            price = temp.get("internalCards")[0]["priceSell"]
            #imageURL = "https://images.cernyrytir.eu/image/cernyrytir/v2?uid=" +temp.get("internalCards")[0]["imagepUID"] + "&faceType=FRONT&imageType=MTG&sizeType=BIG"

            #if available, we list it
            if available:
                availablePrintings[availableVersionCount] = {"pUID":pUID, "available":available, "price":price, "cardNum":cardNum}
                total += available
                print("    Number", availableVersionCount, edition, available, "available @", price, "CZK/pc")
                availableVersionCount += 1
            wait(0.05)
            
        #if multiple printings of the card are available, we let the user know (and pick eventually)
        if availableVersionCount > 1:
            amountOrdered = 0
            
            #auto-order cheapest if the user wanted to do that
            while amountOrdered < qty and amountOrdered < total and autoOrderCheapest:
                temp = availablePrintings.pop(min(availablePrintings, key=lambda x: availablePrintings[x]["price"]))
                amount = temp["available"] if temp["available"] < qty - amountOrdered else qty - amountOrdered
                orderList[temp["cardNum"]] = amount
                if order(temp["cardNum"], amount):
                    amountOrdered += amount
                    orderTotal += amount*temp["price"]
                else:
                    print("Problem ordering", amount, "copies of" if amountOrdered > 1 else "copy of", card)
                    missingList[card] = amount if not(card in missingList) else (missingList[card] + amount)
                
            ####add option to choose from among different printings available if not autoselect####

            #check whether we've ordered enough cards
            if total < qty:
                missingList[card] = qty - total
                print("    In total that makes", total, "available")
            print("Ordered", amountOrdered, "copies of" if amountOrdered > 1 else "copy of", card)

        #if there's exactly one printing available, we order that one
        elif total > 0:
            if total >= qty:
                amount = qty
            else:
                amount = total
                missingList[card] = qty-total
            temp = availablePrintings[next(iter(availablePrintings))]
            orderList[temp["cardNum"]] = amount
            if order(temp["cardNum"], amount):
                orderTotal += amount*temp["price"]
                print("Ordered", amount, "copies of" if amount > 1 else "copy of", card)
            else:
                print("Problem ordering", amount, "copies of" if amountOrdered > 1 else "copy of", card)
                missingList[card] = amount if not(card in missingList) else (missingList[card] + amount)
            
        #or laugh in their face if there are none
        else:
            missingList[card] = qty
            print("    ...None LOL\n"+card+" out of stock")

    #if there's only one printing, we only check for that one
    else:
        for cardNum, pUID in databaze[card].items():
            temp = session.get("https://eshop-api.cernyrytir.eu/api/public/card/" + cardNum + "/REGULAR?eshop_mode=STANDARD&eshop_lang=CZ").json()
            available = temp.get("internalCards")[0]["availEshopQty"]
            edition = temp.get("cardEditionName")
            price = temp.get("internalCards")[0]["priceSell"]
            
            #if unavailable, let the user know, otherwise add the card to the order list
            if not available:
                missingList[card] = qty
                print("\n"+card+" out of stock")
            elif available < qty:
                amount = available
                orderList[cardNum] = amount
                if order(cardNum, amount):
                    orderTotal += amount*price
                    print("\nOrdered", amount, "copies of" if amount > 1 else "copy of", card)
                else:
                    print("\nProblem ordering", amount, "copies of" if amount > 1 else "copy of", card)
                    missingList[card] = amount if not(card in missingList) else (missingList[card] + amount)
                missingList[card] = qty - available if not(card in missingList) else (missingList[card] + qty - available)
            else:
                amount = qty
                orderList[cardNum] = amount
                if order(cardNum, amount):
                    orderTotal += amount*price
                    print("\nOrdered", amount, "copies of" if amount > 1 else "copy of", card)
                else:
                    print("\nProblem ordering", amount, "copies of" if amount > 1 else "copy of", card)
                    missingList[card] = amount if not(card in missingList) else (missingList[card] + amount)


#print("\n-----------------------\nStarting ordering cards")
#orderURL = "https://eshop-api.cernyrytir.eu/api/public/basket/item/insert?basket_sort=INSERTED_AT"
#basketTotal = 0
#print(orderList)

"""below is a deprecated way of ordering cards - didn't work due to not having the required cookies
which would be needed in the requests.Session (and I'm currently too lazy to try to retrieve them from selenium)
technically direct POST requests to the API would be way more efficient tho (they work without logging in)"""
        
##for pUID, qty in orderList.items():
##    #send a POST request to cernyrytir api with the card uid, card uid and quantity to order
##    payload = {"basketUid":basketUID, "basketType":"STANDARD", "productUid":pUID, "quantity":qty, "eshopLang":"CZ"}
##    print(payload)
##    resp = session.post(orderURL, json = payload)
##    if resp.status_code != 200:
##        print("Status code", resp.status_code)
##    basket = resp.json()
##    print(basket)
##    if basket.get("status") != "OK":
##        print("Problem ordering - " + basket.get("status"))
##    else:
##        basketTotal = basket.get("basketRecord").get("totalPrice")
##    wait(0.1)

#give the user a recap
print("\n"+"-"*(19+len(str(orderTotal))))
print("Total order price calculated:", orderTotal)
print("Total cards ordered:", sum(list(orderList.values())), "of", totalWanted, "wanted")
#print(*orderList.items(), sep = "\n")
if len(missingList):
    print("\nMissing cards:")
for card, qty in missingList.items():
    print(card,"-", qty, "copies" if qty > 1 else "copy")

#stop the headless webdriver from running in the background
driver.quit()

#wait for the user to read the recap and confirm
input("\nTo close this window, press Enter")

#first properly working version
