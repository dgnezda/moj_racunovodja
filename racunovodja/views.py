import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from pathlib import Path
import os

from . import widgets as w
from . import settings as s


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
        #self._vars['Št. računa'].set('1')

        #"""FOR TESTING PURPOUSES:
        self._vars['Datum opravljene storitve'].set(datum_izdaje)
        self._vars['Znesek'].set('123,45')
        self._vars['Davčna številka'].set('SI12344123')
        self._vars['Matična številka'].set('12121212')
        self._vars['Naziv'].set('Mr. Kakos Blatunos')
        self._vars['Naslov'].set('Kakoslavska 12, 9240 Blatunovci')
        self._vars['Opis storitve'].set('Delo na črno')
        #"""

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

    def get_stevilka_racuna(self):
        return self._vars['Št. računa'].get()

    def get_naslov_racuna(self):
        return self._vars['Opomba'].get()
