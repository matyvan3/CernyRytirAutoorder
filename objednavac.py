import requests
from time import sleep as wait

#loading cards data to memory (until I turn the cards data into a usable JSON)
#currently they're ordered by a proprietary card number - not by name due to the scraping process
databaze = {}
with open("vyzranozapi.txt", "r") as file:
    for asdf in file.readlines():
        line = asdf.split(";")
        name = line[1].split(" (")[0]
        num = line[0]
        nakup = line[3][:-1]
        if not name in databaze:
            databaze[name] = {}
        databaze[name][num] = nakup

#initialize session for interacting with www
session = requests.Session()
cardsList = []

#get user's basket UID until in-app logging into cernyrytir i implemented
basketUID = input("Basket UID?: ")

#getting the decklist either directly or via Moxfield
if int(input("Moxfield link (0) or direct list (1)? ")):
    cardsList = input("Decklist?: ").split("\n")
    for x in range(len(cardsList)):
        #currently max. 9 copies of each card are supported
        cardsList[x] = [cardsList[x].split(" ", 1)[1], int(cardsList[x][0])]

#user picked Moxfield as the deck source        
else:
    url = "https://api2.moxfield.com/v2/decks/all/" + input("Public ID of the deck (the string at the end of its URL)?: ")
    try:
        #we try requesting the deck data
        resp = session.get(url, timeout=20)
        json = resp.json()
        #if we succeed, we tell the user and prepare the cardslist
        print("Deck", json.get("name"), "located")
        deck = json.get("mainboard")
        for card in deck.keys():
            cardsList.append([card, deck[card][list(deck[card].keys())[0]]])
        print(cardsList)
    except:
        #if we fail, we tell the user (and use mock data for now)
        print("Deck not found, using mock data..")
        cardsList = [["Opt", 4], ["Visions of Beyond", 3]]
        
#once we have the cardslist, we check avilability of the cards
for card in cardsList:

    #check whether the cardname is in our card data and inform user if it ain't
    if not(card[0] in databaze):
        print("Card", card[0], "unknown, check the spelling")
        continue
    
    # if there's multiple versions of the card available, we check each variant for availability
    if len(databaze[card[0]].keys()) > 1:
        print("There's", len(databaze[card[0]].keys()), "variants of", card[0], "and you want", card[1], "copies.\nAvailable ones:")
        asdf, total = 0, 0
        #for each variant check for availability and price
        for key in databaze[card[0]].keys():
            fetch = session.get("https://eshop-api.cernyrytir.eu/api/public/card/" + key + "/REGULAR?eshop_mode=STANDARD&eshop_lang=CZ")
            temp = fetch.json()
            available = temp.get("internalCards")[0]["availEshopQty"]
            edition = temp.get("cardEditionName")
            price = temp.get("internalCards")[0]["priceSell"]
            imageURL = "https://images.cernyrytir.eu/image/cernyrytir/v2?uid=" +temp.get("internalCards")[0]["imageUuid"] + "&faceType=FRONT&imageType=MTG&sizeType=BIG"
            #if available, we list it
            if available:
                total += available
                print("    Number", asdf, edition, available, "available @", price, "CZK/pc")
                asdf += 1
            wait(0.2)
        #if any printings of the card are available, we let the user know
        if total > 0 and asdf > 1:
            print("    In total that makes", total, "available")
        elif total > 0:
            ####auto-order the only one (remember which one)####
            print("    Ordering", card[1] if (total >= card[1]) else total)
        #or laugh in their face if there are none
        else:
            print("    ...None LOL")
            
    #if there's only one printing, we only check for that one
    else:
        for key in databaze[card[0]].keys():
            temp = session.get("https://eshop-api.cernyrytir.eu/api/public/card/" + key + "/REGULAR?eshop_mode=STANDARD&eshop_lang=CZ").json()
            available = temp.get("internalCards")[0]["availEshopQty"]
            edition = temp.get("cardEditionName")
            price = temp.get("internalCards")[0]["priceSell"]
            
            #if unavailable, let the user know, otherwise order the card
            if available < card[1]:
                print("Not enough", card[0], "available, there's", available, "in stock")
            else:
                ####add ordering capabilities####
                print(card[0],"succesfully added to your order.")
                
#currently far from done, but good enough as a proof of concept
