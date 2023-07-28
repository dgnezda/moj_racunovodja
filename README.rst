===========================================================
Moj računovodja v.1.01 - aplikacija za osebno računovodstvo
===========================================================
Opis
----
Aplikacija, ki omogoča vnos/izvoz računov v .pdf formatu in vodenje knjige 
računov v .csv formatu. Primera izvoženega računa in knjige računov se nahajata 
v mapi 'docs'.

Opombe/uporaba
--------------
* CHECK README-ENG.MD FOR ENGLISH VERSION OF README FILE
* Pri vnašanju podatkov je naslov prejemnika potrebno vnesti v sledečem formatu:

  - Ulica 12, 1000 Mesto 

* Uporabnik svoje podatke (podatke izdajatelja računa) vnese v datoteko
  'settings.py', ki se nahaja v mapi 'racunovodja'
* Datume je potrebno vnesti v formatu dd.mm.yyyy
* Ime računa se shrani v formatu 'racun_st_AB23-001_opomba.pdf', kjer sta "AB"
  inicialki izdajatelja, '23' sta zadnji stevliki leta (npr. 2023), '001' je
  številka računa, 'opomba' pa je kratka označba, ki si jo uporabnik po želji
  lahko doda za lažjo razpoznavnost posameznega računa.
* Ime knjige računov se shrani v formatu 'knjiga_racunov_2023.csv'
* Na mestu logotipa je v testnem .pdf-u emoji B-)
* Testirano s Python verzijama 3.10 in 3.11

Dependencies
------------
* fpdf2
