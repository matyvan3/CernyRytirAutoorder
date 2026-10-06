<h1>Automatický objednávač karet Magic: the Gathering z Černého Rytíře</h1>

<h2>Tento projek má za cíl vzít od uživatele decklist nebo odkaz na Moxfield a nahrát mu do košíku na Rytíři všechny karty z balíčku.</h2>

<h3>Aktuální stav:</h3>
  -  všechno čistě konzolové!<br>
  -  scraper (crapiabuser.py)<br>
    -  kontroluje všechna čísla od posledního záznamu (aktuálně 228068) do 999999<br>
    -  nehlídá, co se děje mezi už známými záznamy<br>
    -  bere jenom REGULAR verze karet (tj. non-foil)<br>
    -  ukládá název a číslo karty (v odkazu na stránkách rytíře)<br>
  -  objednávač (objednavac.py)<br>
    -  vyžaduje ID košíku, které je nutné manuálně vytáhnout z prohlížeče<br>
    -  pro Moxfield vyžaduje ID decku, zatím nepodporuje přímo odkaz<br>
    -  podporuje pouze jednociferné počty karet, které musí být specifikované<br>
    -  kontroluje známost karet (překlepy jsou problém)<br>
    -  vrací dostupné varianty karet - NEOBJEDNÁVÁ<br>
<br>
<br>
<h3>V plánu je:</h3>
  -  přihlašování do uživatelského účtu na Rytíři<br>
  -  výpočet celkové ceny balíčku<br>
    -  automatický výběr karet podle nelevnější varianty<br>
  -  podpora a zdůraznění různých variant karet (běžné/foil, extended/fullart atd.)<br>
  -  GUI<br>
  -  kontrola nových karet<br>
  -  změna karetních dat na JSON a formátování dle jména pro snazší práci s nimi<br>
<br>
<h3>Možná bude vytvořeno:</h3>
  -  webová verze<br>
  -  standalone exe (pravděpodobně stejně python interpreter)<br>
<br>
<h3>V plánu určitě není:</h3>
  -  offline verze (z podstaty objednávání na e-shopu)<br>
  -  built-in deck builder<br>
