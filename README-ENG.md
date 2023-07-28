============================================================
Moj računovodja v.1.01 - application for personal accounting
============================================================
Description
-----------
Appliction for exporting .pdf invoices and automatic logging of accounting book 
in .csv format. Examples of invoices and accounting book can be found in the 
folder 'docs'.

Notes/usage
--------------
* The address needs to be entered in the following format:

  - Street 12, 1000 City 

* The user needs to enter personal info (payment info) into the file
  'settings.py', wich can be found in the 'racunovodja' folder
* Dates need to be entered in the following format: dd.mm.yyyy
* The name of the invoice will be saved as 'racun_st_AB23-001_opomba.pdf', where
  "AB" are the inicials of the user, '23' stands for year (eg. 2023), '001' is the 
  number of the invoice, 'opomba' is short note, that can be added to the end
  (but is not required)
* The name of the accounting book, that holds entries of all invoices is saved as
  'knjiga_racunov_2023.csv'
* The test .pdf of invoice includes a B-) emoji instead of a logo
* Tested with Python versions 3.10 and 3.11

Dependencies
------------
* fpdf2
