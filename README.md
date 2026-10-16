# CSV Merger & Cleaner

Malý nástroj v Pythone, ktorý spojí viac CSV súborov do jedného čistého súboru. Nepotrebuje žiadne ďalšie knižnice, stačí Python 3.

## Čo robí
- Automaticky rozpozná oddeľovač (čiarka, bodkočiarka, tabulátor)
- Upraví názvy stĺpcov (`Name ` sa zmení na `name`)
- Odstráni nadbytočné medzery v každej bunke
- Odstráni prázdne riadky a duplicitné riadky
- Spojí stĺpce zo všetkých súborov, chýbajúce hodnoty ostanú prázdne

## Ako ho použiť
1. Súbory CSV daj do jedného priečinka.
2. V príkazovom riadku spusti:

```
python csv_cleaner.py sample_data -o cleaned.csv
```

Voľby:
- `-o`, `--output` názov výstupného súboru (predvolene `cleaned.csv`)
- `--keep-duplicates` ponechá duplicitné riadky

Môžeš zadať aj jeden súbor namiesto priečinka:

```
python csv_cleaner.py zakaznici.csv -o vycisteny.csv
```

## Príklad
Vstup: dva súbory so zákazníkmi (`sample_data/`), ktoré majú rôzne oddeľovače, nadbytočné medzery, prázdny riadok a duplicitu.
Výstup: jeden súbor `cleaned.csv` so stĺpcami `name, email, city, phone`, bez prázdnych riadkov a duplicít.

Po spustení sa vypíše súhrn: koľko riadkov sa načítalo, koľko sa odstránilo a koľko sa uložilo.

## Poznámky
- Duplicity sa porovnávajú presne. Riadky, ktoré sa líšia aspoň v jednej bunke, ostanú oba.
- Výstupný súbor je v kódovaní UTF-8 s BOM, takže Excel správne zobrazí slovenské a české znaky.

## Autorka
Monika. Tento projekt je ukážkou mojej práce so spracovaním dát v Pythone.
