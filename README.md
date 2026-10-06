<h1>Automatický objednávač karet Magic: the Gathering z Černého Rytíře</h1>

<h2>Tento projek má za cíl vzít od uživatele decklist nebo odkaz na Moxfield a nahrát mu do košíku na Rytíři všechny karty z balíčku.</h2>

<h3>Aktuální stav:</h3>
  -  všechno čistě konzolové!
  -  scraper (crapiabuser.py)
    -  kontroluje všechna čísla od posledního záznamu (aktuálně 228068) do 999999
    -  nehlídá, co se děje mezi už známými záznamy
    -  bere jenom REGULAR verze karet (tj. non-foil)
    -  ukládá název a číslo karty (v odkazu na stránkách rytíře)
  -  objednávač (objednavac.py)
    -  vyžaduje ID košíku, které je nutné manuálně vytáhnout z prohlížeče
    -  pro Moxfield vyžaduje ID decku, zatím nepodporuje přímo odkaz
    -  podporuje pouze jednociferné počty karet, které musí být specifikované
    -  kontroluje známost karet (překlepy jsou problém)
    -  vrací dostupné varianty karet - NEOBJEDNÁVÁ


<h3>V plánu je:</h3>
  -  přihlašování do uživatelského účtu na Rytíři
  -  výpočet celkové ceny balíčku
    -  automatický výběr karet podle nelevnější varianty
  -  podpora a zdůraznění různých variant karet (běžné/foil, extended/fullart atd.)
  -  GUI
  -  kontrola nových karet
  -  změna karetních dat na JSON a formátování dle jména pro snazší práci s nimi

<h3>Možná bude vytvořeno:</h3>
  -  webová verze
  -  standalone exe (pravděpodobně stejně python interpreter)

<h3>V plánu určitě není:</h3>
  -  offline verze (z podstaty objednávání na e-shopu)
  -  built-in deck builder
