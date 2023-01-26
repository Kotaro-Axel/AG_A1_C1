# This is a sample Python scrip
import View
import streamlit as ts
from View import *
from Individuo import *
from AGS import *

import tkinter as tk

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':



    root = tk.Tk()
    app = View(master=root)
    app.mainloop()  


    print('PyCharm')

    #PARAMETROS MIENTRAS NO ESTA LA INTERFAZ
    a = """po = 10
    pmi = 0.5
    pmg = 0.5
    pc = 0.5
    p_max = 5
    rango_min = 10
    rango_max = 25
    interv = 1
    cantidad_gene = 3
    #CREACION DE INDIVIDUO
    algoritmo_g = AGS(pc,pmi,pmg,po,p_max,rango_min,rango_max,interv,cantidad_gene)"""
    # LLAMADA A LA INTERFAZ GRAFICA
    # #View.vista
    # st.write("""" """)

# See PyCharm help at htt#ps://www.jetbrains.com/help/pycharm/
