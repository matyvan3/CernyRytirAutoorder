# Automatický objednávač karet Magic: the Gathering z Černého Rytíře

Tento projekt má za cíl zpohodlnit objednávání karet z Černého Rytíře, když uživatel má již sestavený decklist k objednání

Je postavený na čistě na Pythonu (3.13.5) a vyžaduje dvě externí knihovny pro komunikaci s internetem (Requests, selenium)

## 

## Jak používat

1. Stáhněte repozitář
2. Extrahujte soubory
3. V terminálu dojděte do složky, kam byly soubory extrahovány
4. Spusťte příkaz "pip install -r requirements.txt"
5. UJISTĚTE SE, ŽE VÁŠ KOŠÍK NA ČERNÉM RYTÍŘI JE PRÁZDNÝ, nebo alespoň neobsahuje žádnou z karet ve chtěném decklistu
6. Spusťte objednavac.py
7. Zadejte přihlašovací údaje do svého účtu na Černém Rytíři
8. Vyberte, zda chcete decklist dodat manuálně, nebo přes Moxfield
9. Počkejte na doběhnutí programu
10. Pro zavření okna stiskněte Enter
11. PŘED OBJEDNÁNÍM ZKONTROLUJTE OBSAH KOŠÍKU, NERUČÍM ZA PŘÍPADNÉ CHYBY



Přibližná doba běhu: 10s + 5s na kartu - ca 100s na Standard deck, ca 300s na EDH deck (mírně ovlivněno výkonem počítače)

## 

## Aktuální stav:

Všechno čistě konzolové!

Poslední obsažený set: Reality Fracture

### scraper (crapiabuser.py)

* kontroluje všechna čísla od posledního záznamu (aktuálně 228068) do 999999
* nehlídá, co se děje mezi už známými záznamy
* bere jenom REGULAR verze karet (tj. non-foil)
* ukládá název a číslo karty (v odkazu na stránkách rytíře)

### objednávač (objednavac.py)

* vyžaduje uživatelské přihlašovací údaje pro přístup do košíku (nejsou nikde ukládány)
* podporuje odkazy na Moxfield i manuální vložení decklistu
* kontroluje známost karet (překlepy či špatný zápis oboustranných karet jsou problém)
* vrací dostupné varianty karet
* automaticky objednává nejlevnější varianty karet pro naplnění požadovaného počtu
* Neodesílá objednávku - je nutné dokončit ji externě, a to do hodiny od nahrání karet do košíku

## V plánu je:

* podpora a zdůraznění různých variant karet (běžné/foil, extended/fullart atd.)
* GUI
* kontrola nových karet
* změna karetních dat na JSON a formátování dle jména pro snazší práci s nimi

## Možná bude vytvořeno:

* webová verze
* standalone exe

## V plánu určitě není:

* offline verze (z podstaty objednávání na e-shopu)
* built-in deck builder

