import tkinter.messagebox
from tkinter import *
from tkinter.ttk import Combobox
import datetime
import controller


def generate():
    print("test")
    startY = cb_period_year.get()
    startM = cb_period_mth.get()
    startD = "01"
    endY = cb_period_year.get()
    endM = cb_period_mth.get()
    endD = controller.last_day(endY, endM)
    finY = cb_enddate_year.get()
    finM = cb_enddate_mth.get()
    finD = controller.last_day(finY, finM)


    if check_pl_val.get():
        data = controller.xl_input(controller.rates_pl("EUR", startY, startM, startD, endY, endM, endD),finY, finM, finD)
        controller.create_file(data, f"PL_{startM}{startY}")
    if check_cz_val.get():
        data = controller.xl_input(controller.rates_cz("EUR", startY, startM, startD, endY, endM, endD),finY, finM, finD)

        controller.create_file(data, f"CZ_{startM}{startY}")
    if check_bg_val.get():
        data = controller.xl_input(controller.rates_bg("PLN", startY, startM, startD, endY, endM, endD),finY, finM, finD)
        controller.create_file(data, f"BG_{startM}{startY}")
    if check_hr_val.get():
        data = controller.xl_input(controller.rates_hr("EUR", startY, startM, startD, endY, endM, endD),finY, finM, finD)
        controller.create_file(data, f"HR_{startM}{startY}")

    tkinter.messagebox.showinfo(title="Done", message="Files has been saved")

root = Tk()
root.title("MyLease FX")
root.geometry("300x500")

frm_date = Frame(root)
frm_date.grid(row=0, column=0, pady=5, padx=5)


lbl_period = Label(frm_date, text="Period:")
lbl_period.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="W")

lbl_year = Label(frm_date, text="year:")
lbl_year.grid(row=1, column=0, pady=5, padx=5, sticky="E")


cb_period_year = Combobox(frm_date)
cb_period_year['values'] = ["2021","2022","2023"]
cb_period_year['state'] = "readonly"
cb_period_year.grid(row=1, column=1, pady=5, padx=0)

lbl_mth = Label(frm_date, text="month:")
lbl_mth.grid(row=2, column=0, pady=5, padx=5, sticky="E")

cb_period_mth = Combobox(frm_date)
cb_period_mth['values'] = ["01","02","03","04", "05", "06", "07", "08", "09", "10", "11", "12"]
cb_period_mth['state'] = "readonly"
cb_period_mth.grid(row=2, column=1, pady=5, padx=0)

frm_ent = Frame(root)
frm_ent.grid(row=1, column=0, pady=5, padx=5)

lbl_ent = Label(frm_ent, text="Choose entity: ")
lbl_ent.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="W")

check_pl_val = BooleanVar()
check_pl = Checkbutton(frm_ent, text="PL", variable=check_pl_val, onvalue=True, offvalue=False)
check_pl.grid(row=1, column=1, pady=2, padx=2, sticky="W")
check_pl.select()
check_cz_val = BooleanVar()
check_cz = Checkbutton(frm_ent, text="CZ", variable=check_cz_val, onvalue=True, offvalue=False)
check_cz.grid(row=2, column=1, pady=2, padx=2, sticky="W")
check_cz.select()
check_bg_val = BooleanVar()
check_bg = Checkbutton(frm_ent, text="BG", variable=check_bg_val, onvalue=True, offvalue=False)
check_bg.grid(row=3, column=1, pady=2, padx=2, sticky="W")
check_bg.select()
check_hr_val = BooleanVar()
check_hr = Checkbutton(frm_ent, text="HR", variable=check_hr_val, onvalue=True, offvalue=False)
check_hr.grid(row=4, column=1, pady=2, padx=2, sticky="W")
check_hr.select()

frm_enddate = Frame(root)
frm_enddate.grid(row=2, column=0, pady=5, padx=5,)

lbl_enddate = Label(frm_enddate, text="Choose extrapolation date:")
lbl_enddate.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="W")

lbl_endyear = Label(frm_enddate, text="year:")
lbl_endyear.grid(row=1, column=0, pady=5, padx=5, sticky="E")


cb_enddate_year = Combobox(frm_enddate)
cb_enddate_year['values'] = ["2021","2022","2023","2024","2025","2026","2027","2028","2029"]
cb_enddate_year['state'] = "readonly"
cb_enddate_year.grid(row=1, column=1, pady=5, padx=0)

lbl_endmth = Label(frm_enddate, text="month:")
lbl_endmth.grid(row=2, column=0, pady=5, padx=5, sticky="E")

cb_enddate_mth = Combobox(frm_enddate)
cb_enddate_mth['values'] = ["01","02","03","04", "05", "06", "07", "08", "09", "10", "11", "12"]
cb_enddate_mth['state'] = "readonly"
cb_enddate_mth.grid(row=2, column=1, pady=5, padx=0)

frm_buttons = Frame(root)
frm_buttons.grid(row=3, column=0, pady=20, padx=5)

btn_run = Button(frm_buttons, text="Run", command=generate, width=20)
btn_run.grid(row=0, column=0, sticky="E")

current_date = datetime.date.today()
delta = datetime.timedelta(days=20)

cb_period_year.set((current_date - delta).strftime("%Y"))
cb_period_mth.set((current_date - delta).strftime("%m"))
cb_enddate_year.set((current_date - delta).strftime("%Y"))
cb_enddate_mth.set("12")

root.mainloop()
