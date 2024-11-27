
Funkční prototyp pro výpočet kapacity neřízené křižovatky dle Technických podmínek 188 – Posuzování kapacit křižovatek a úseků pozemních komunikací (2018).

Na základě vstupních parametrů, jako jsou intenzity dopravy, uspořádání řadících pruhů, návrhová rychlost a typ přednosti v jízdě, program vypočítává klíčové ukazatele pro jednotlivé křižovatkové pohyby i jízdní pruhy:

        Průměrné zdržení na vozidlo,
        Délku kolony na vjezdu,
        Úroveň kvality dopravy (LOS) podle ČSN 73 6102.

Pro zajištění maximální přenositelnosti a kompatibility s prostředími používanými ve veřejné správě využívá program pouze čistý Python bez externích knihoven.

Struktura kódu je modulární a navržena s ohledem na budoucí rozšiřitelnost. Jednotlivé funkce a třídy jsou logicky odděleny do samostatných modulů, což umožňuje snadnou integraci do různých aplikací. Program je připraven pro více způsobů nasazení:

Lokální aplikace s GUI (např. Tkinter),
Webová platforma (připravuji integraci pomocí Django).

Tento prototyp představuje praktický nástroj pro projektanty dopravních staveb a specialisty na dopravní inženýrství..
