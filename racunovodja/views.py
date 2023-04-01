import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from pathlib import Path
import os

from . import widgets as w


class DataRecordForm(ttk.Frame):
    """The input form for our widgets"""

    def _add_frame(self, label, cols=2):
        """Add a LabelFrame to the form"""
        frame = ttk.LabelFrame(self, text=label)
        frame.grid(sticky=tk.W + tk.E)
        for i in range(cols):
            frame.columnconfigure(i, weight=1)
        return frame

    def _on_save(self):
        self.event_generate('<<SaveRecord>>')

    def __init__(self, parent, model, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.model = model
        fields = self.model.fields

        self._vars = {
        'Št. računa': tk.StringVar(),
        'Naziv': tk.StringVar(),
        'Naslov': tk.StringVar(),
        'Davčna številka': tk.StringVar(),
        'Matična številka': tk.IntVar(),
        'Opis storitve': tk.StringVar(),
        'Datum izdaje': tk.StringVar(),
        'Datum opravljene storitve': tk.StringVar(),
        'Datum zapadlosti': tk.StringVar(),
        'Znesek': tk.StringVar(),
        'Opomba': tk.StringVar(),
        }

        p_info = self._add_frame("Prejemnik:")

        w.LabelInput(p_info, "Naziv", field_spec=fields['Naziv'], 
            var=self._vars['Naziv']
            ).grid(row=0, column=0)
        w.LabelInput(p_info, "Naslov", field_spec=fields['Naslov'],
            var=self._vars['Naslov']
            ).grid(row=0, column=1)
        w.LabelInput(p_info, "Davčna številka", 
            field_spec=fields['Davčna številka'], 
            var=self._vars['Davčna številka'] 
            ).grid(row=1, column=0)
        w.LabelInput(p_info, "Matična številka", 
            field_spec=fields['Matična številka'], 
            var=self._vars['Matična številka']
            ).grid(row=1, column=1)

        r_info = self._add_frame("Podatki o računu:")

        w.LabelInput(r_info, "Št. računa", field_spec=fields['Št. računa'], 
            var=self._vars['Št. računa'], 
            ).grid(row=0, column=0)
        w.LabelInput(r_info, "Datum izdaje", field_spec=fields['Datum izdaje'], 
            var=self._vars['Datum izdaje'], 
            ).grid(row=0, column=1)
        w.LabelInput(r_info, "Znesek", field_spec=fields['Znesek'], 
            var=self._vars['Znesek']
            ).grid(row=1, column=0)
        w.LabelInput(r_info, "Datum zapadlosti", 
            field_spec=fields['Datum zapadlosti'], 
            var=self._vars['Datum zapadlosti'],
            ).grid(row=1, column=1)
        w.LabelInput(r_info, "Opis storitve", field_spec=fields['Opis storitve'], 
            var=self._vars['Opis storitve'],
            ).grid(row=2, column=0)
        w.LabelInput(r_info, "Datum opravljene storitve", 
            field_spec=fields['Datum opravljene storitve'], 
            var=self._vars['Datum opravljene storitve'],
            ).grid(row=2, column=1)

        o_info = self._add_frame("Drugo:")
        w.LabelInput(o_info, "Opomba", field_spec=fields['Opomba'],
            var=self._vars['Opomba'],
            ).grid(row=3, column=0, columnspan=2)

        buttons = tk.Frame(self)
        buttons.grid(sticky=tk.W + tk.E, row=4)
        self.savebutton = ttk.Button(buttons, text='Shrani', command=self._on_save)
        self.savebutton.pack(side=tk.RIGHT)

        self.resetbutton = ttk.Button(buttons, text='Ponastavi', command=self.reset)
        self.resetbutton.pack(side=tk.RIGHT)
        self.reset()

    def reset(self):
        """Resets the form entries"""

        for var in self._vars.values():
            var.set('')

        datum_izdaje = datetime.today().strftime('%d.%m.%Y')
        datum_zapadlosti = (datetime.today() + timedelta(days=14)).strftime("%d.%m.%Y")
        self._vars['Datum izdaje'].set(datum_izdaje)
        self._vars['Datum zapadlosti'].set(datum_zapadlosti)
        self._vars['Št. računa'].set('001')

        """FOR TESTING PURPOUSES:
        self._vars['Datum opravljene storitve'].set(datum_izdaje)
        self._vars['Znesek'].set('123,45')
        self._vars['Davčna številka'].set('12344123')
        self._vars['Matična številka'].set('12121212')
        self._vars['Naziv'].set('Mr. Kakakakak')
        self._vars['Naslov'].set('Kakoslavska 12, 9240 Blatunovci')
        self._vars['Opis storitve'].set('Kakovanje')
        """

    def get(self):
        data = dict()
        
        for key, variable in self._vars.items():
            try:
                data[key] = variable.get()
            except tk.TclError:
                message = f"Error in field: {key}. Data was not saved!"
                raise ValueError(message)

        return data

    def get_errors(self):
        """Get a list of field errors in the form"""

        errors = {}
        for key, var in self._vars.items():
            inp = var.label_widget.input
            error = var.label_widget.error

            if hasattr(inp, 'trigger_focusout_validation'):
                inp.trigger_focusout_validation()
            if error.get():
                errors[key] = error.get()

        return errors

    def get_racun_string(self):
        naziv = self._vars['Naziv'].get()
        naslov = self._vars['Naslov'].get()
        ds = self._vars['Davčna številka'].get()
        ms = self._vars['Matična številka'].get()
        datum_storitve = self._vars['Datum opravljene storitve'].get()
        stevilka_racuna_input = self._vars['Št. računa'].get()
        opis_input = self._vars['Opis storitve'].get()
        znesek_input = self._vars['Znesek'].get()

        stevilka_racuna = f"JN{datetime.today().strftime('%y')}-{('0' * (3 - len(stevilka_racuna_input))) + stevilka_racuna_input}"
        naslov_split = naslov.split(', ')
        sklic = f'{stevilka_racuna[2:]}'
        opis = opis_input + (' ' * (41 - len(opis_input)))
        znesek = znesek_input + '€' + (' ' * (9 - len(znesek_input)))
        znesek2 = znesek_input + '€' + (' ' * (14 - len(znesek_input)))
        znesek3 = znesek_input + '€' + (' ' * (17 - len(znesek_input)))

        racun_string = f"""Izdajatelj:                                                     Prejemnik: 
JANEZ NOVAK                                                         Naziv:  {naziv}
PREŠERNOVA 2                                                       Naslov:  {naslov_split[0]}
1000 LJUBLJANA                                                              {naslov_split[1]}
                                                                       DŠ:  {ds}
DAVČNA ŠTEVILKA: 32133211                                              MŠ:  {ms}

IBAN:   SI56 0123 4567 8901 234
Banka:  Nova Ljubljanska Banka
BIC:    LJBASI2XXXX 


Račun št. {stevilka_racuna}

                                                             Datum izdaje:  {datetime.today().strftime("%d.%m.%Y")}
                                                            Način plačila:  Nakazilo na TRR
                                                                   Valuta:  EUR
                                                              Kraj izdaje:  Ljubljana
                                                Datum opravljene storitve:  {datum_storitve}
                                                         Datum zapadlosti:  {(datetime.today() + timedelta(days=14)).strftime("%d.%m.%Y")}
                                                                    Sklic:  {sklic}
                                                              Koda namena:  OTHR

___________________________________________________________________________________________________________
Na osnovi pogodbe/naročila vam zaračunavam avtorsko delo iz neodvisnega samostojnega opravljanja 
dejavnosti po 46. členu Zdoh-2L.
___________________________________________________________________________________________________________

+------------------------------------------+----------+-----+-----------+----------+-----+----------------+
| Opis storitve                            | Količina | EM  | Cena/EM   | Popust   | DDV | Vrednost z DDV |
+==========================================+==========+=====+===========+==========+=====+================+
| {opis}|    1     | PCE | {znesek}| 0% 0.00€ | 0%  | {znesek2}|
+------------------------------------------+----------+-----+-----------+----------+-----+----------------+

DDV po 1. odstavku 94. člena ZDDV-1 ni obračunan.

                                                                +---------------------+-------------------+
                                                                | Vrednost postavk:   | {znesek3}|
                                                                +---------------------+-------------------+
                                                                | Vsota popustov:     | 0,00€             |
                                                                +---------------------+-------------------+
                                                                | Osnova za DDV:      | 0.00€             |
                                                                +---------------------+-------------------+
                                                                | Neobdavčeno:        | {znesek3}|
                                                                +---------------------+-------------------+
                                                                | Vsota zneskov:      | DDV: 0,00€        |
                                                                +---------------------+-------------------+
                                                                | ZA PLAČILO:         | {znesek3}|
                                                                +---------------------+-------------------+


    Podpis:

___________________________________________________________________________________________________________
"""
        return racun_string

    def get_stevilka_racuna(self):
        return self._vars['Št. računa'].get()
