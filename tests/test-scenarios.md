# Testovací scénáře

| ID | Scénář | Postup | Očekávaný výsledek | Měřená hodnota |
|---|---|---|---|---|
| T01 | První nasazení | Nasadit čisté prostředí | Všechny komponenty jsou Ready | Doba nasazení |
| T02 | Nová verze | Změnit text frontendu a spustit pipeline | Nový obraz a úspěšné nasazení | Doba pipeline |
| T03 | Rolling update | Aktualizovat backend image | Bez výrazného výpadku | Neúspěšné HTTP požadavky |
| T04 | Selhání podu | Smazat jeden backend pod | Automatické vytvoření náhrady | Doba obnovy |
| T05 | Škálování | Zvýšit repliky backendu 2 -> 5 | Pět Ready podů | Doba škálování |
| T06 | Perzistence | Vytvořit úkol a restartovat databázi | Úkol zůstane uložen | Zachování dat ano/ne |
| T07 | Chyba testu | Úmyslně porušit backend test | Pipeline se zastaví před buildem | Správné zablokování |
| T08 | Chyba obrazu | Vložit kritickou testovací zranitelnost | Security stage selže | Správné zablokování |
| T09 | Rollback | Nasadit vadnou verzi a vrátit revizi | Obnovení poslední funkční verze | Doba rollbacku |
| T10 | Shodná verze | Nasadit stejný commit SHA do tří prostředí | Všude běží stejné tagy | Shoda digestů/tagů |

## Doporučený záznam výsledku

Pro každý běh zaznamenejte datum, prostředí, verzi obrazu, parametry infrastruktury, naměřený čas, výsledek, logy a případnou odchylku od očekávání.
