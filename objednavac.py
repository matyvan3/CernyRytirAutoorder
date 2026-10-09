import requests
from time import sleep as wait
import re

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

#get user's basket UID until in-app logging into cernyrytir i implemented
basketUID = input("Basket UID?: ")

#getting the decklist either directly or via Moxfield
if int(input("Moxfield link (0) or direct list (1)? ")):
    deck = []
    deck.append(input("Enter your decklist and press Ctrl+Z: "))
    for line in sys.stdin:
        deck.append(line)
    for x in range(len(deck)):
        #check whether there's a card count on line start
        count = int(re.match(r"\d*", deck[x]).group(0))
        count = count if count else 1
        totalWanted += count
        cardsList[deck[x].split(" ", 1)[1]] = count

#user picked Moxfield as the deck source        
else:
    url = "https://api2.moxfield.com/v2/decks/all/" + input("Public ID of the deck (the string at the end of its URL)?: ")
    try:
        #we try requesting the deck data
        resp = session.get(url, timeout=20)
        json = resp.json()
        #if we succeed, we tell the user and prepare the cardslist
        if json.get("name"):
            print("Deck " + json.get("name") + "located")
        deck = json.get("mainboard")
        sideboard = json.get("sideboard")
        for part in [deck, sideboard]:
            for card in part.keys():
                qty = part[card][list(part[card].keys())[0]]
                totalWanted += qty
                cardsList[card] = qty
    except:
        #if we fail, we tell the user (and use mock data for now)
        print("Deck not found, using mock data..")
        cardsList = {"Opt":4, "Visions of Beyond":5}
        totalWanted = sum(cardsList.values())

print("\nTotal cards wanted:", totalWanted)

autoOrderCheapest = False if input("\nAutomatically order cheapest available printings? (yes/no) ").lower() != "yes" else True
orderList = {}
orderTotal = 0
missingList = {}
#once we have the cardslist, we check avilability of the cards
for card in cardsList.keys():

    #check whether the cardname is in our card data and inform user if it ain't
    if not(card in databaze):
        print("\nCard", card, "unknown, check the spelling")
        continue
    
    qty = cardsList[card]
    
    # if there's multiple versions of the card available, we check each variant for availability
    if len(databaze[card].keys()) > 1:
        
        #since people usually have Basic Lands we ask whether the user is even interested in ordering those (if not, we skip to the next card)
        if card in ["Plains", "Island", "Swamp", "Mountain", "Forest"]:
            if input("\n"+card+" is a Basic Land, are you sure you need to order those? (yes/no) ").lower() != "yes":
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
                availablePrintings[availableVersionCount] = {"pUID":pUID, "available":available, "price":price}
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
                orderList[temp["pUID"]] = amount
                amountOrdered += amount
                orderTotal += amount*temp["price"]
                
            ####add option to choose from among different printings available if not autoselect####

            #check whether we've ordered enough cards
            if total < qty:
                missingList[card] = qty - total
                print("    In total that makes", total, "available")
            print("Ordering", amountOrdered, "copies of" if amountOrdered > 1 else "copy of", card)

        #if there's exactly one printing available, we order that one
        elif total > 0:
            if total >= qty:
                amount = qty
            else:
                amount = total
                missingList[card] = qty-total
            temp = availablePrintings[next(iter(availablePrintings))]
            orderList[temp["pUID"]] = amount
            orderTotal += amount*temp["price"]
            print("Ordering", amount, "copies of" if amount > 1 else "copy of", card)
            
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
                orderList[pUID] = available
                missingList[card] = qty - available
                print("Ordering", available, "copies of" if available > 1 else "copy of", card)
            else:
                orderList[pUID] = qty
                print("\n" + card + " succesfully added to your order.")

orderURL = "https://eshop-api.cernyrytir.eu/api/public/basket/item/insert?basket_sort=INSERTED_AT"
basketTotal = 0
for pUID, qty in orderList.items():
    #send a POST request to cernyrytir api with the card uid, card uid and quantity to order
    resp = session.post(orderURL, json = {"basketUid":basketUID,"basketType":"STANDARD","productUid":pUID,"quantity":qty,"eshopLang":"CZ"})
    basket = resp.json()
    if basket.get("status") != "OK":
        print("problem ordering")
    else:
        basketTotal = basket.get("basketRecord").get("totalPrice")
    wait(0.05)

#give the user a recap
print("\n"+"-"*(19+len(str(orderTotal))))
print("Total order price calculated:", orderTotal, "\nTotal price on cernyrytir:", basketTotal)
print("Total cards ordered:", sum(list(orderList.values())), "of", totalWanted, "wanted")
#print(*orderList.items(), sep = "\n")
if len(missingList):
    print("\nMissing cards:")
for card, qty in missingList.items():
    print(card,"-", qty, "copies" if qty > 1 else "copy")

#still far from done, but it already loads cards into cart
