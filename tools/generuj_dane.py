"""Generuje przykładowy katalog specjalistów (dane zmyślone) do data/specjalisci.js.
Deterministyczny (stałe ziarno), więc każde uruchomienie daje ten sam wynik."""
import json, random
from pathlib import Path

rnd = random.Random(2026)

# zdjęcia randomuser.me pobrane do assets/img/ludzie; pominięte selfie, czapki i miny
ZLE_M = {2, 3, 6, 12, 15, 17, 23, 25, 66, 40, 54, 55, 57, 63, 68, 70, 72, 77, 84, 86, 93, 99}
ZLE_K = {5, 7, 9, 13, 15, 16, 18, 21, 22, 24, 28, 31, 32, 33, 34, 35, 38, 45, 46, 47, 50, 54, 55, 56, 57,
         66, 70, 74, 77, 80, 83, 84, 89, 92, 93, 99}
STARSI_M = [13, 21, 31, 38, 79, 82, 8, 74, 98, 29, 24, 61, 69, 11, 20, 22, 87, 88, 49, 36, 46, 76, 78, 62, 0, 1]
STARSI_K = [14, 23, 53, 41, 61, 26, 58, 4, 0, 52, 59, 39, 43, 63, 96, 65]

def kolejka(starsi, zle, prefix):
    reszta = [i for i in range(100) if i not in zle and i not in starsi]
    rnd.shuffle(reszta)
    return [f"{prefix}{i:02d}" for i in starsi + reszta]

ZDJ_M, ZDJ_K = kolejka(STARSI_M, ZLE_M, "m"), kolejka(STARSI_K, ZLE_K, "k")

IMIONA_M = ["Andrzej", "Tomasz", "Piotr", "Krzysztof", "Paweł", "Marek", "Michał", "Jan", "Grzegorz", "Jerzy",
            "Wojciech", "Adam", "Łukasz", "Marcin", "Jakub", "Bartosz", "Rafał", "Dariusz", "Mariusz", "Robert",
            "Zbigniew", "Ryszard", "Kamil", "Mateusz", "Sebastian", "Leszek", "Stanisław", "Wiesław", "Artur", "Szymon"]
IMIONA_K = ["Elżbieta", "Magdalena", "Anna", "Katarzyna", "Agnieszka", "Barbara", "Joanna", "Małgorzata", "Ewa",
            "Monika", "Aleksandra", "Dorota", "Beata", "Justyna", "Karolina", "Natalia", "Izabela", "Marta",
            "Renata", "Hanna", "Zofia", "Iwona", "Paulina", "Weronika"]
# (forma męska, forma żeńska)
NAZWISKA = [("Wawrzyniak", "Wawrzyniak"), ("Kowalczyk", "Kowalczyk"), ("Lisiecki", "Lisiecka"), ("Sowa", "Sowa"),
            ("Domański", "Domańska"), ("Kubiak", "Kubiak"), ("Nowicki", "Nowicka"), ("Zieliński", "Zielińska"),
            ("Mazur", "Mazur"), ("Pawlak", "Pawlak"), ("Michalski", "Michalska"), ("Król", "Król"),
            ("Wieczorek", "Wieczorek"), ("Jabłoński", "Jabłońska"), ("Wróbel", "Wróbel"), ("Majewski", "Majewska"),
            ("Olszewski", "Olszewska"), ("Stępień", "Stępień"), ("Malinowski", "Malinowska"), ("Jaworski", "Jaworska"),
            ("Adamczyk", "Adamczyk"), ("Dudek", "Dudek"), ("Nowakowski", "Nowakowska"), ("Pietrzak", "Pietrzak"),
            ("Wróblewski", "Wróblewska"), ("Sikora", "Sikora"), ("Baran", "Baran"), ("Rutkowski", "Rutkowska"),
            ("Michalak", "Michalak"), ("Szewczyk", "Szewczyk"), ("Ostrowski", "Ostrowska"), ("Tomaszewski", "Tomaszewska"),
            ("Pietrzyk", "Pietrzyk"), ("Duda", "Duda"), ("Zalewski", "Zalewska"), ("Wróbel", "Wróbel"),
            ("Jasiński", "Jasińska"), ("Marciniak", "Marciniak"), ("Sadowski", "Sadowska"), ("Bąk", "Bąk"),
            ("Zawadzki", "Zawadzka"), ("Jakubowski", "Jakubowska"), ("Wilk", "Wilk"), ("Chmielewski", "Chmielewska"),
            ("Włodarczyk", "Włodarczyk"), ("Borkowski", "Borkowska"), ("Czarnecki", "Czarnecka"), ("Sawicki", "Sawicka"),
            ("Sokołowski", "Sokołowska"), ("Urbański", "Urbańska"), ("Kubacki", "Kubacka"), ("Maciejewski", "Maciejewska"),
            ("Szczepański", "Szczepańska"), ("Kucharski", "Kucharska"), ("Wilczyński", "Wilczyńska"), ("Kalinowski", "Kalinowska"),
            ("Lis", "Lis"), ("Mazurek", "Mazurek"), ("Wysocki", "Wysocka"), ("Adamski", "Adamska"), ("Kaźmierczak", "Kaźmierczak"),
            ("Wasilewski", "Wasilewska"), ("Sobczak", "Sobczak"), ("Czerwiński", "Czerwińska"), ("Andrzejewski", "Andrzejewska"),
            ("Cieślak", "Cieślak"), ("Głowacki", "Głowacka"), ("Zakrzewski", "Zakrzewska"), ("Kołodziej", "Kołodziej"),
            ("Sikorski", "Sikorska"), ("Krajewski", "Krajewska"), ("Gajewski", "Gajewska"), ("Szymczak", "Szymczak"),
            ("Szulc", "Szulc"), ("Baranowski", "Baranowska"), ("Laskowski", "Laskowska"), ("Brzeziński", "Brzezińska"),
            ("Makowski", "Makowska"), ("Ziółkowski", "Ziółkowska"), ("Przybylski", "Przybylska"), ("Domagała", "Domagała"),
            ("Borowski", "Borowska"), ("Nowacki", "Nowacka"), ("Kasprzak", "Kasprzak"), ("Kurek", "Kurek"),
            ("Kaczmarczyk", "Kaczmarczyk"), ("Witkowski", "Witkowska"), ("Ryba", "Ryba"), ("Wójtowicz", "Wójtowicz"),
            ("Rogalski", "Rogalska"), ("Szczepaniak", "Szczepaniak"), ("Kowalewski", "Kowalewska"), ("Leśniak", "Leśniak"),
            ("Grabowski", "Grabowska"), ("Pawłowski", "Pawłowska"), ("Michałowski", "Michałowska"), ("Krawczyk", "Krawczyk"),
            ("Kozłowski", "Kozłowska"), ("Jankowski", "Jankowska"), ("Wojciechowski", "Wojciechowska"), ("Kwiatkowski", "Kwiatkowska"),
            ("Kaczmarek", "Kaczmarek"), ("Piotrowski", "Piotrowska"), ("Grabowiecki", "Grabowiecka"), ("Nowak", "Nowak"),
            ("Kamiński", "Kamińska"), ("Lewandowski", "Lewandowska"), ("Dąbrowski", "Dąbrowska"), ("Wiśniewski", "Wiśniewska"),
            ("Górski", "Górska"), ("Rybicki", "Rybicka"), ("Szymański", "Szymańska"), ("Woźniak", "Woźniak"),
            ("Kozieł", "Kozieł"), ("Czajkowski", "Czajkowska"), ("Bielecki", "Bielecka"), ("Kowalski", "Kowalska"),
            ("Walczak", "Walczak"), ("Stasiak", "Stasiak"), ("Tomczyk", "Tomczyk"), ("Kulesza", "Kulesza"),
            ("Mróz", "Mróz"), ("Pająk", "Pająk"), ("Wrona", "Wrona"), ("Bednarek", "Bednarek"), ("Fijałkowski", "Fijałkowska"),
            ("Konieczny", "Konieczna"), ("Gutowski", "Gutowska"), ("Maciąg", "Maciąg"), ("Rudnicki", "Rudnicka"),
            ("Socha", "Socha"), ("Kubica", "Kubica"), ("Gołębiowski", "Gołębiowska"), ("Żak", "Żak"), ("Kot", "Kot"),
            ("Skowroński", "Skowrońska"), ("Lipiński", "Lipińska"), ("Orłowski", "Orłowska"), ("Wasiak", "Wasiak"),
            ("Dziedzic", "Dziedzic"), ("Mikołajczyk", "Mikołajczyk"), ("Bielski", "Bielska"), ("Krupa", "Krupa")]

DZIEDZINY = {
    "Informatyka i AI": (38, ["uczenie maszynowe", "wizja maszynowa", "przetwarzanie języka naturalnego",
                              "systemy rekomendacyjne", "automatyzacja procesów (RPA)", "integracje z ERP",
                              "architektura systemów chmurowych", "analiza danych produkcyjnych",
                              "cyberbezpieczeństwo przemysłowe", "aplikacje mobilne", "modele predykcyjne awarii"]),
    "Automatyka i robotyka": (21, ["zrobotyzowane stanowiska spawalnicze", "sterowniki PLC", "systemy SCADA",
                                   "roboty współpracujące", "sterowanie predykcyjne", "linie montażowe",
                                   "pojazdy AGV i AMR", "napędy i serwomechanizmy"]),
    "Fizyka": (14, ["optyka i lasery", "czujniki światłowodowe", "fizyka materiałów", "akustyka i drgania",
                    "pomiary w trudnych warunkach", "fotonika", "termowizja"]),
    "Matematyka": (12, ["optymalizacja", "badania operacyjne", "statystyka przemysłowa", "symulacje Monte Carlo",
                        "planowanie produkcji", "teoria sterowania", "kryptografia"]),
    "Chemia": (11, ["polimery biodegradowalne", "recykling tworzyw", "katalizatory", "powłoki ochronne",
                    "chemia analityczna", "technologia farb i lakierów"]),
    "Inżynieria materiałowa": (9, ["kompozyty", "druk 3D z metali", "obróbka cieplna", "badania zmęczeniowe",
                                   "materiały budowlane nowej generacji"]),
    "Elektronika": (8, ["systemy wbudowane", "internet rzeczy (IoT)", "projektowanie PCB", "łączność radiowa",
                        "zasilanie i przekształtniki"]),
    "Biotechnologia": (7, ["fermentacja przemysłowa", "bioprodukty z odpadów", "diagnostyka laboratoryjna",
                           "żywność funkcjonalna"]),
    "Energetyka": (7, ["fotowoltaika i magazyny energii", "pompy ciepła", "audyty energetyczne",
                       "odzysk ciepła odpadowego", "wodór"]),
    "Mechanika i budowa maszyn": (6, ["projektowanie maszyn", "symulacje MES", "hydraulika siłowa", "tribologia"]),
    "Ekonomia i finanse": (5, ["modele finansowe projektów", "analiza kosztów i korzyści", "pomoc publiczna",
                               "wycena technologii"]),
    "Prawo i zamówienia": (4, ["prawo zamówień publicznych", "ochrona własności intelektualnej",
                               "umowy B+R", "rozliczanie dotacji"]),
}
assert sum(n for n, _ in DZIEDZINY.values()) == 142

# 31 profesorów, 27 dr hab., 44 dr, 40 mgr/mgr inż.
STOPNIE = ["prof"] * 31 + ["drhab"] * 27 + ["dr"] * 44 + ["mgr"] * 40
TECHNICZNE = {"Informatyka i AI", "Automatyka i robotyka", "Inżynieria materiałowa", "Elektronika", "Energetyka",
              "Mechanika i budowa maszyn"}
MIASTA = ["Katowice", "Gliwice", "Kraków", "Wrocław", "Warszawa", "Poznań", "Łódź", "Gdańsk", "Lublin", "Rzeszów",
          "Opole", "Bielsko-Biała"]
MIESIACE = ["stycznia", "lutego", "marca", "kwietnia", "maja", "czerwca"]

def tytul(stopien, dz):
    inz = dz in TECHNICZNE or (dz in {"Fizyka", "Chemia"} and rnd.random() < 0.4)
    return {"prof": "prof. dr hab." + (" inż." if inz else ""), "drhab": "dr hab." + (" inż." if inz else ""),
            "dr": "dr" + (" inż." if inz else ""), "mgr": "mgr inż." if inz or rnd.random() < 0.5 else "mgr"}[stopien]

def odm(n, jeden, kilka, wiele):
    """Polska odmiana po liczebniku: 1 patent, 2 patenty, 5 patentów."""
    if n == 1:
        return f"{n} {jeden}"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return f"{n} {kilka}"
    return f"{n} {wiele}"

def osiagniecia(stopien, dz):
    patenty = dz not in {"Ekonomia i finanse", "Prawo i zamówienia"}
    druga = (lambda n: odm(n, "patent", "patenty", "patentów")) if patenty else (lambda n: odm(n, "ekspertyza", "ekspertyzy", "ekspertyz"))
    if stopien == "prof":
        o = [odm(rnd.randint(60, 240), "publikacja", "publikacje", "publikacji"), druga(rnd.randint(2, 18)),
             f"kierownik {rnd.randint(3, 11)} projektów badawczych"]
    elif stopien == "drhab":
        o = [odm(rnd.randint(30, 110), "publikacja", "publikacje", "publikacji"), druga(rnd.randint(0, 7)),
             f"kierownik {rnd.randint(1, 5)} projektów badawczych".replace("kierownik 1 projektów", "kierownik 1 projektu")]
    elif stopien == "dr":
        o = [odm(rnd.randint(8, 45), "publikacja", "publikacje", "publikacji"),
             odm(rnd.randint(2, 9), "wdrożenie w przemyśle", "wdrożenia w przemyśle", "wdrożeń w przemyśle")]
    else:
        o = [odm(rnd.randint(4, 16), "rok w przemyśle", "lata w przemyśle", "lat w przemyśle"),
             odm(rnd.randint(3, 20), "zrealizowane wdrożenie", "zrealizowane wdrożenia", "zrealizowanych wdrożeń")]
    return [x for x in o if not x.startswith("0 ")]

def main():
    # kolejność: najpierw starsi stopniem, więc dostają starsze twarze z początku kolejek
    dziedziny = [d for d, (n, _) in DZIEDZINY.items() for _ in range(n)]
    rnd.shuffle(dziedziny)
    stopnie = STOPNIE[:]
    plcie = ["m" if rnd.random() < 78 / 142 else "k" for _ in range(142)]
    # wyrównaj liczbę zdjęć: 78 mężczyzn, 64 kobiety
    while plcie.count("m") > len(ZDJ_M):
        plcie[plcie.index("m")] = "k"
    while plcie.count("k") > len(ZDJ_K):
        plcie[plcie.index("k")] = "m"
    zm, zk = iter(ZDJ_M), iter(ZDJ_K)
    nazwiska = NAZWISKA[:]
    rnd.shuffle(nazwiska)
    uzyte = set()
    osoby = []
    for i in range(142):
        plec, dz, st = plcie[i], dziedziny[i], stopnie[i]
        imie = rnd.choice(IMIONA_M if plec == "m" else IMIONA_K)
        nm = nazwiska[i % len(nazwiska)][0 if plec == "m" else 1]
        if (imie, nm) in uzyte:
            imie = rnd.choice(IMIONA_M if plec == "m" else IMIONA_K)
        uzyte.add((imie, nm))
        r = rnd.random()
        if r < 0.55:
            dost, kiedy = "teraz", "Dostępn" + ("y" if plec == "m" else "a") + " teraz"
        elif r < 0.8:
            dost, kiedy = "3m", f"Wolne okno od {rnd.choice(MIESIACE[:3])} 2027"
        else:
            dost, kiedy = "pozniej", f"Wolne okno od {rnd.choice(MIESIACE[3:])} 2027"
        osoby.append({
            "id": i + 1,
            "imie": f"{imie} {nm}",
            "tytul": tytul(st, dz),
            "stopien": st,
            "dziedzina": dz,
            "spec": rnd.sample(DZIEDZINY[dz][1], 2),
            "miasto": rnd.choice(MIASTA),
            "dost": dost,
            "kiedy": kiedy,
            "osiagniecia": osiagniecia(st, dz),
            "projekty": rnd.randint(1, 9) if st in ("prof", "drhab") else rnd.randint(0, 5),
            "foto": next(zm) if plec == "m" else next(zk),
        })
    out = Path(__file__).resolve().parent.parent / "data" / "specjalisci.js"
    out.parent.mkdir(exist_ok=True)
    out.write_text("// Dane przykładowe, generowane przez tools/generuj_dane.py. Osoby są zmyślone.\n"
                   "window.SPECJALISCI = " + json.dumps(osoby, ensure_ascii=False, indent=0) + ";\n", encoding="utf-8")
    print(len(osoby), "osób,", sum(o["stopien"] == "prof" for o in osoby), "profesorów")

main()
