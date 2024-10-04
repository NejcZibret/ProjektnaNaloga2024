# PROJEKTNA NALOGA: SMUČIŠČA

Avtor: Nejc Žibret

# Opis
Moja projektna naloga pri predmetu UVP, program finančna matematika, študijsko leto 2023/24, zajema dva dela: zajemanje podatkov in analizo podatkov o svetovnih smučiščih. Zanjo sem uporabil programski jezik Python, svoje podatke pa sem vzel iz spletne strani Skiresorts.info. Pobral sem podatke o 3850 smučiščih. Ostala smučišča se mi niso zdela analize vredna, ker so se mi zdela prekratka. Za vsako smučišče sem zajel:
- podatek o njegovem položaju na lestvici velikosti smučišč,
- ime smučišča,
- celino,
- državo,
- oceno,
- višinsko razliko,
- dolžine prog (skupno ter dolžine modrih, rdečih in črnih posamično),
- skupno število žičnic.
Ker je bilo nekaj smučišč, ki niso imela podanega katerega izmed podatkov, sem manjkajoče številske podatke nadomestil z 'NaN', če ni bilo podatka o državi pa sem dodelil vrednost 'no data'.

# Navodila za uporabo
Uporabnik si lahko ogleda analizo podatkov tako, da preprosto odpre dokument analiza.ipynb. Podatki so iz csv datoteke, ki je vključena v repozitorij. Analiza podatkov je predstavljena v Jupyter Notebook-u.

Če hoče uporabnik sam zagnati program, enostavno le zažene main.py. Ta bo najprej pobral spletne strani (v primeru, da te še niso), nato izluščil podatke s pomočjo regularnih izrazov in na koncu še vse skupaj zapisal v json in csv. Nato uporabnik požene še vse celice v datoteki analiza.ipynb.

# Ključne knjižnice
Tukaj so uporabljene knjižnice in njihove naloge:
- csv: delo s CSV datotekami,
- json: delo z JSON datotekami,
- os: interakcija z operacijskim sistemom,
- requests: za pridobivanje podatkov s spleta,
- sys: za dostop do sistemskih funkcij,
- html: delo s HTML,
- re: delo z regularnimi izrazi,
- numpy (np): za učinkovito delo z velikimi nizi in matrikami numeričnih podatkov,
- pandas (pd): delo z razpredelnicami,
- matplotlib.pyplot: risanje grafov,
- seaborn (sns): napredne vizualizacije.