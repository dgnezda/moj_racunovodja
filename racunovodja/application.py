import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from . import views as v
from . import models as m


class Application(tk.Tk):
    """Application root window"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = m.CSVModel()
        self.title("Moj Računovodja")
        self.columnconfigure(0, weight=1)
        
        ttk.Label(self, text="Moj Računovodja",
            font=("TkDefaultFont", 16)
            ).grid(row=0)

        self.recordform = v.DataRecordForm(self, self.model)
        self.recordform.grid(row=1, padx=10, sticky=(tk.W + tk.E))
        self.recordform.bind('<<SaveRecord>>', self._on_save)

        self.status = tk.StringVar()
        ttk.Label(self, textvariable=self.status
            ).grid(sticky=(tk.W + tk.E), row=2, padx=10)

        self._records_saved = 0

    def _on_save_pdf(self, *_):
        data = self.recordform.get()
        self.pdf.save_pdf(data)

    def _on_save(self, *_):
        """Handles save button clicks"""
        """
        errors = self.recordform.get_errors()
        if errors:
            message = "Računa ni možno shraniti."
            detail = (
                "Polja, ki imajo napake: "
                "\n  * {}".format('\n  * '.join(errors.keys()))
                )
            messagebox.showerror(
                title='Error', message=message, detail=detail)

            return False
        """
        data = self.recordform.get()
        self.model.save_record(data)
        self._records_saved += 1
        self.status.set(f"Shranjenih je bilo {self._records_saved} računov.")
        
        stevilka_racuna = self.recordform.get_stevilka_racuna()

        pdf = m.PDFModel(stevilka_racuna)

        racun_string = self.recordform.get_racun_string()
        pdf.add_page()
        pdf.set_font_size(9.5)
        pdf.ln(5)
        pdf.multi_cell(0, 4, racun_string, border = 0, align = 'L')
        #with open("pdf_ex.rst", 'r', encoding="UTF-8") as f:
        #    for line in f.readlines():
        #        pdf.cell(0, 4, line[:-1], new_x="LMARGIN", new_y="NEXT")
        pdf.image("files/podpis.png", 30, 230, 45)
        pdf.output(f"racun_st.{stevilka_racuna}.pdf")
        
        self.recordform.reset()
        