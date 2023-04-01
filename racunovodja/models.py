import csv
from pathlib import Path
from datetime import datetime, timedelta
from fpdf import FPDF
import os

from .constants import FieldTypes as FT
from . import views as v

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
    def __init__(self, stevilka_racuna, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.stevilka_racuna = stevilka_racuna

    def header(self):
        # Rendering logo:
        self.image("files/logo.png", 10, 8, 24)
        # Setting font:
        self.add_font(fname="files/UbuntuMono-Regular.ttf")
        self.set_font("UbuntuMono-Regular", '', 14)
        title = f"Račun št. {self.stevilka_racuna}"
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

    