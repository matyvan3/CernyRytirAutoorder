#Automatický objednávač karet Magic: the Gathering z Černého Rytíře  
#Tento projek má za cíl vzít od uživatele decklist nebo odkaz na Moxfield a nahrát mu do košíku na Rytíři všechny karty z balíčku.  
##Aktuální stav:
&emspVšechno čistě konzolové!  
&emsp###scraper (crapiabuser.py)
&emsp&emsp-  kontroluje všechna čísla od posledního záznamu (aktuálně 228068) do 999999  
&emsp-  nehlídá, co se děje mezi už známými záznamy  
&emsp-  bere jenom REGULAR verze karet (tj. non-foil)  
&emsp-  ukládá název a číslo karty (v odkazu na stránkách rytíře)  
  
&emsp###objednávač (objednavac.py)  
&emsp-  vyžaduje ID košíku, které je nutné manuálně vytáhnout z prohlížeče  
&emsp-  pro Moxfield vyžaduje ID decku, zatím nepodporuje přímo odkaz  
&emsp-  podporuje pouze jednociferné počty karet, které musí být specifikované  
&emsp-  kontroluje známost karet (překlepy jsou problém)  
&emsp-  vrací dostupné varianty karet - NEOBJEDNÁVÁ  
  
  
##V plánu je:  
&emsp-  přihlašování do uživatelského účtu na Rytíři  
&emsp-  výpočet celkové ceny balíčku  
&emsp-  automatický výběr karet podle nelevnější varianty  
&emsp-  podpora a zdůraznění různých variant karet (běžné/foil, extended/fullart atd.)  
&emsp-  GUI  
&emsp-  kontrola nových karet  
&emsp-  změna karetních dat na JSON a formátování dle jména pro snazší práci s nimi  
  
##Možná bude vytvořeno:  
&emsp-  webová verze  
&emsp-  standalone exe (pravděpodobně stejně python interpreter)  
  
##V plánu určitě není:  
&emsp-  offline verze (z podstaty objednávání na e-shopu)  
&emsp-  built-in deck builder  
