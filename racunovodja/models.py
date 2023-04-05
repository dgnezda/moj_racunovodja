import csv
from pathlib import Path
from datetime import datetime, timedelta
from fpdf import FPDF
import os

from .constants import FieldTypes as FT
from . import settings as s

class CSVModel:
    """CSV file storage"""

    fields = {
    "Št. računa": {'req': True, 'type': FT.string},
    "Naziv": {'req': True, 'type': FT.string},
    "Naslov": {'req': True, 'type': FT.string},
    "Davčna številka": {'req': True, 'type': FT.string},
    "Matična številka": {'req': False, 'type': FT.integer},
    "Opis storitve": {'req': True, 'type': FT.string},
    "Datum izdaje": {'req': True, 'type': FT.date_string},
    "Datum opravljene storitve": {'req': True, 'type': FT.date_string},
    "Datum zapadlosti": {'req': True, 'type': FT.date_string},
    "Znesek": {'req': True, 'type': FT.decimal},
    "Opomba": {'req': False, 'type': FT.long_string}
    }

    def __init__(self):

        datestring = datetime.today().strftime("%Y")
        filename = f"knjiga_racunov_{datestring}.csv"
        self.file = Path(filename)

        file_exists = os.access(self.file, os.F_OK)
        parent_writeable = os.access(self.file.parent, os.W_OK)
        file_writeable = os.access(self.file, os.W_OK)

        if (
            (not file_exists and not parent_writeable) or 
            (file_exists and not file_writeable)
            ):
            msg = f"Permission denied accessing file: {filename}"
            raise PermissionError(msg)

    def save_record(self, data):
        """Save a dict of data to the CSV file"""
        newfile = not self.file.exists()

        with open(self.file, 'a', newline='', encoding='utf-8') as fh:
            csvwriter = csv.DictWriter(fh, fieldnames=self.fields.keys())

            if newfile:
                csvwriter.writeheader()

            csvwriter.writerow(data)


class PDFModel(FPDF):
    """PDF file storage and composition"""

    def __init__(self, stevilka_racuna, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.st_racuna = stevilka_racuna

    def header(self):
        # Rendering logo:
        self.image(s.user['logo'], 10, 8, 24)
        # Setting font:
        self.add_font(fname="files/UbuntuMono-Regular.ttf")
        self.set_font("UbuntuMono-Regular", '', 14)
        title = f"Račun št. {self.get_sifra_racuna()}"
        width = len(title) + 36
        self.set_x((210 - width) / 2)
        self.set_fill_color(200, 220, 255)
        # Moving cursor to the right:
        self.cell(
            width,
            9,
            title,
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
            align="C",
            fill=True,
        )
        # Performing a line break:
        self.ln(10)

    def footer(self):
        # Position cursor at 1.5 cm from bottom:
        self.set_y(-15)
        # Setting font: helvetica italic 8
        self.set_font("helvetica", "I", 8)
        self.set_text_color(128)
        # Printing page number:
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")

    def get_racun_string(self, data):
        # Podatki o izdajatelju računa:
        naziv_i = s.user['name'] + (' ' * (68 - len(s.user['name'])))
        kraj_i = s.user['post_nr'] + ' ' + s.user['city']\
            + (' ' * (75 - len(s.user['post_nr']) - len(s.user['city'])))
        ulica_i = s.user['street'] + (' ' * (67 - len(s.user['street'])))
        ds_i = s.user['tax_nr'] + (' ' * (54 - len(s.user['tax_nr'])))
        iban_i = s.user['iban']
        banka_i = s.user['bank']
        bic_i = s.user['bic']

        # Podatki o prejemniku računa:
        naziv_p = data['Naziv']
        naslov_p = data['Naslov'].split(', ')
        ds_p = data['Davčna številka']
        ms_p = data['Matična številka']

        # Podatki o računu
        datum_storitve = data['Datum opravljene storitve']
        datum_izdaje = datetime.today().strftime("%d.%m.%Y")
        datum_zapadlosti = (datetime.today()\
            + timedelta(days=14)).strftime("%d.%m.%Y")
        opis_input = data['Opis storitve']
        znesek_input = data['Znesek']
        sklic = self.get_sifra_racuna()[2:]
        opis = opis_input + (' ' * (41 - len(opis_input)))
        znesek = znesek_input + '€' + (' ' * (9 - len(znesek_input)))
        znesek2 = znesek_input + '€' + (' ' * (14 - len(znesek_input)))
        znesek3 = znesek_input + '€' + (' ' * (17 - len(znesek_input)))

        # Konstrukcija računa
        racun_string = f"""Izdajatelj:{' ' * 53}Prejemnik: 
{naziv_i}Naziv:  {naziv_p}
{ulica_i}Naslov:  {naslov_p[0]}
{kraj_i}{naslov_p[1]}
{' ' * 71}DŠ:  {ds_p}
DAVČNA ŠTEVILKA: {ds_i}MŠ:  {ms_p}

IBAN:   {iban_i}
Banka:  {banka_i}
BIC:    {bic_i} 


Račun št. {self.get_sifra_racuna()}

{' ' * 61}Datum izdaje:  {datum_izdaje}
{' ' * 60}Način plačila:  Nakazilo na TRR
{' ' * 67}Valuta:  EUR
{' ' * 62}Kraj izdaje:  Ljutomer
{' ' * 48}Datum opravljene storitve:  {datum_storitve}
{' ' * 57}Datum zapadlosti:  {datum_zapadlosti}
{' ' * 68}Sklic:  {sklic}
{' ' * 62}Koda namena:  OTHR

{'_' * 107}
Na osnovi pogodbe/naročila vam zaračunavam avtorsko delo iz neodvisnega samostojnega opravljanja 
dejavnosti po 46. členu Zdoh-2L.
{'_' * 107}

+{'-' * 42}+{'-' * 10}+{'-' * 5}+{'-' * 11}+{'-' * 10}+{'-' * 5}+{'-' * 16}+
| Opis storitve{' ' * 28}| Količina | EM  | Cena/EM   | Popust   | DDV | Vrednost z DDV |
+{'=' * 42}+{'=' * 10}+{'=' * 5}+{'=' * 11}+{'=' * 10}+{'=' * 5}+{'=' * 16}+
| {opis}|    1     | PCE | {znesek}| 0% 0.00€ | 0%  | {znesek2}|
+{'-' * 42}+{'-' * 10}+{'-' * 5}+{'-' * 11}+{'-' * 10}+{'-' * 5}+{'-' * 16}+

DDV po 1. odstavku 94. člena ZDDV-1 ni obračunan.

{' ' * 64}+{'-' * 21}+{'-' * 19}+
{' ' * 64}| Vrednost postavk:   | {znesek3}|
{' ' * 64}+{'-' * 21}+{'-' * 19}+
{' ' * 64}| Vsota popustov:     | 0,00€{' ' * 13}|
{' ' * 64}+{'-' * 21}+{'-' * 19}+
{' ' * 64}| Osnova za DDV:      | 0.00€{' ' * 13}|
{' ' * 64}+{'-' * 21}+{'-' * 19}+
{' ' * 64}| Neobdavčeno:        | {znesek3}|
{' ' * 64}+{'-' * 21}+{'-' * 19}+
{' ' * 64}| Vsota zneskov:      | DDV: 0,00€{' ' * 8}|
{' ' * 64}+{'-' * 21}+{'-' * 19}+
{' ' * 64}| ZA PLAČILO:         | {znesek3}|
{' ' * 64}+{'-' * 21}+{'-' * 19}+


{' ' * 4}Podpis:

{'_' * 107}
"""
        return racun_string

    def get_sifra_racuna(self):
        name_split = s.user['name'].split()
        initials = name_split[0][0] + name_split[1][0]
        year = datetime.today().strftime('%y')
        code = ('0'*(3 - len(self.st_racuna))) + self.st_racuna
        return f"{initials}{year}-{code}"
