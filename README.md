# Gloria Victis: strona koncepcyjna

Strona firmy, która prowadzi projekty z dotacji UE i PARP od pomysłu do rozliczenia i buduje technologię jako generalny wykonawca. To wersja do pokazania: firmy, kwoty, osoby i zdjęcia są przykładowe.

Podgląd: https://mcin93.github.io/gloria-victis/

## Co gdzie jest

- `index.html`: cała strona.
- `assets/css/style.css`: wygląd (czerń, złoto, biel).
- `assets/js/app.js`: menu na telefonie, katalog z filtrami, tabela realizacji, formularz (wersja demo, nic nie wysyła).
- `data/specjalisci.js`: 142 przykładowe osoby w katalogu.
- `makiety/`: wcześniejsze makiety kolorów i wersji logo.

## Jak zmienić dane

Osoby w katalogu generuje skrypt. Zmień listy w `tools/generuj_dane.py` i uruchom:

```
python tools/generuj_dane.py
```

Docelowo plik `data/specjalisci.js` zastąpią prawdziwe dane zespołu, w tym samym formacie.

Logo rysuje kod: `tools/emblemat.py` (wieniec) i `tools/emblemat_twarze.py` (twarz w środku). Po zmianie uruchom drugi skrypt i wklej nowy symbol `gv-e1` z `assets/emblemat-warianty.svg` między znaczniki `<!--EMBLEMAT-E1-->` w `index.html`.

## Źródła

- Zdjęcia: randomuser.me (do wymiany na zdjęcia zespołu przed startem).
- Flaga UE i logo PARP: Wikimedia Commons, domena publiczna. Przed startem sprawdźcie zasady oznaczania projektów z Funduszy Europejskich.
- Fonty: Newsreader, Public Sans, Marcellus (licencja SIL OFL), hostowane lokalnie.
