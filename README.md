# PROJEKTNA NALOGA: SMUČIŠČA

# Opis
Avtor: Nejc Žibret

Moja projektna naloga pri predmetu UVP, program finančna matematika, zajema dva dela: zajemanje podatkov in analizo podatkov o smučiščih. Zanjo sem uporabil programski jezik Python, svoje podatke pa sem vzel iz spletne strani [Skiresorts.info](https://www.skiresort.info/). Pobral sem podatke o 3850 smučiščih. Ostala smučišča se mi niso zdela analize vredna, ker so se mi zdela prekratka. Za vsako smučišče sem zajel:
- podatek o njegovem položaju na lestvici velikosti smučišč,
- ime smučišča,
- celino,
- državo,
- oceno,
- višinsko razliko,
- dolžine prog (skupno ter dolžine modrih, rdečih in črnih posamično),
- skupno število žičnic.

Ker je bilo nekaj smučišč, ki niso imela podanega katerega izmed podatkov, sem manjkajoče številske podatke nadomestil z 'NaN', če ni bilo podatka o državi, pa sem dodelil vrednost 'no data'.

# Navodila za uporabo
Uporabnik si lahko ogleda analizo podatkov tako, da preprosto odpre dokument analiza.ipynb. Podatki so iz csv datoteke, ki je vključena v repozitorij. Analiza podatkov je predstavljena v Jupyter Notebook-u. Ta je sestavljen iz štirih sklopov. Vsak ima na začetku splošne podatke, nato pa še moje hipoteze. Te sem s pomočjo podatkov potrdil ali ovrgel.

Če hoče uporabnik sam zagnati program, enostavno le zažene main.py. Ta bo najprej pobral spletne strani (v primeru, da te še niso), nato izluščil podatke s pomočjo regularnih izrazov in na koncu še vse skupaj zapisal v csv. 

# Ključne knjižnice
Na začetku obeh datotek (main.py ter analiza.ipynb) so prikazane knjižnice, ki sem jih uporabil za pisanje projektne naloge.