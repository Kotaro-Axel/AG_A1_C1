import tkinter as tk
from tkinter.constants import DISABLED, RIGHT
import tkinter.font as font
from tkinter.messagebox import showinfo
from tkinter.constants import END, INSERT


import math
import random
# from random import *
import random as rand
from Individuo import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


class View(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.set_window_format()
        self.create_stage()

    def set_window_format(self):
        self.master.title("ALGORITMOS GENETICOS")
        #self.master.tk.call('wm', 'iconphoto', self.master._w,tk.PhotoImage(file='assets/mysql.png'))
        self.master.configure(width=1000, height=600)
        self.master.resizable(0, 0)
        self.place(relwidth=1, relheight=1)

    def create_stage(self):

        # Background
        self.bg = tk.PhotoImage(file="assets/bg.png")
        self.bgI = tk.Label(self, image=self.bg, text="BG")
        self.bgI.place(x=0, y=0, relwidth=1, relheight=1)

        self.fontStyleTitle = font.Font(family="Lucida Grande", size=20)
        self.fontStyleText = font.Font(family="Luicda Grande", size=14)

        self.title = tk.Label(self, font=self.fontStyleTitle, text = "ALGORITMOS GENETICOS C1A1")
        self.title.place(x = 290, y = 15)


        self.Label_po = tk.Label(self, font=self.fontStyleText, text="Poblacion : ")
        self.input_po = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_po.place(x=100, y=100)
        self.input_po.place(x=210, y=100)

        self.Label_pm = tk.Label(self, font=self.fontStyleText, text="Población  máxima : ")
        self.input_pm = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_pm.place(x=100, y=150)
        self.input_pm.place(x=290, y=150)

        self.Label_cantidad_genes = tk.Label(self, font=self.fontStyleText, text="Cantidad de genes : ")
        self.input_cantidad_genes = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_cantidad_genes.place(x=100, y=200)
        self.input_cantidad_genes.place(x=290, y=200)

        self.Label_rango_min = tk.Label(self, font=self.fontStyleText, text="Rango  min : ")
        self.input_rango_min = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_rango_min.place(x=100, y=250)
        self.input_rango_min.place(x=290, y=250)

        self.Label_rango_max = tk.Label(self, font=self.fontStyleText, text="Rango max : ")
        self.input_rango_max = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_rango_max.place(x=100, y=300)
        self.input_rango_max.place(x=290, y=300)

        self.Label_intervalo = tk.Label(self, font=self.fontStyleText, text="Intervalo : ")
        self.input_intervalo = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_intervalo.place(x=100, y=350)
        self.input_intervalo.place(x=290, y=350)

        self.Label_pmi = tk.Label(self, font=self.fontStyleText, text="PMI : ")
        self.input_pmi = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_pmi.place(x=500, y=100)
        self.input_pmi.place(x=580, y=100)

        self.Label_pmg = tk.Label(self, font=self.fontStyleText, text="PMG : ")
        self.input_pmg = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_pmg.place(x=500, y=150)
        self.input_pmg.place(x=580, y=150)

        self.Label_pc = tk.Label(self, font=self.fontStyleText, text="PC : ")
        self.input_pc = tk.Entry (self, width=10, font='Helvetica 12')
        self.Label_pc.place(x=500, y=200)
        self.input_pc.place(x=580, y=200)

        self.buttonAGS = tk.Button(self, text="Run AGS" ,command=self.AGS)
        self.buttonAGS.place(x=500, y=235)


    def AGS(self):

        # RECORDATORIO // DEBES REINICIAR EL CONTADOR DE NUM_DECEND
        self.num_generacion = 0
        self.pob_cruza = []
        self.pob_muta = []
        self.poblacion_init = []
        self.poblacion_max = []
        self.poblacion_min = []
        self.poblacion_final = []
        self.poblacion_generacion = []

        self.pc = float(self.input_pc.get())
        self.pmi = float(self.input_pmi.get())
        self.pmg = float(self.input_pmg.get())
        self.po = int(self.input_po.get())
        self.p_Max = int(self.input_pm.get())
        self.rango_min = float(self.input_rango_min.get())
        self.rango_max = float(self.input_rango_max.get())
        self.interv = float(self.input_intervalo.get())
        self.cantidad_gene = int(self.input_cantidad_genes.get())

        # CALCULAR EL RANGO
        self.rango = self.rango_max - self.rango_min

        # CALCULA LOS PUNTOS DE BITS
        self.puntos = (self.rango / self.interv) + 1

        # CALCULA LOS BITS
        self.exponente = 1
        while True:
            self.exponente += 1
            self.bits = 2 ** self.exponente
            if self.bits >= self.puntos:
                break


        # EJECUCION DE LAS GENERACIONES SEGUN EL NUMERO ASIGNADO POR EL USUARIO
        self.resultSet = tk.Text(self, font='Helvetica 11', width=52,  
                                height=10, highlightbackground='BLUE', 
                                bg='cornflowerblue')

        while True:
            self.pob_cruza.clear()
            self.pob_muta.clear()
            self.poblacion_init.clear()
            self.poblacion_max.clear()
            self.poblacion_min.clear()
            self.poblacion_final.clear()

            # LLAMADA DE FUNCION CREACION DE INDIVIDUOS y SELECCION
            self.fun_poblacion_init(self.exponente, self.rango, self.interv, self.po)
            # LLAMADA DE METODO PARA CRUZA
            self.cruza(self.pc, self.po, self.exponente, self.rango, self.interv)
            # LLAMADA A LA MUTACION
            self.mutacion(self.pmi, self.pmg, self.exponente, self.rango, self.interv)
            # LLAMADA A PODA
            self.poda(self.p_Max, self.rango_max, self.rango_min)
            self.num_generacion += 1
            if self.num_generacion == self.cantidad_gene:
                break
        
        #Interfaz
        self.resultSet.place(x=500, y=320)
        #GRAFICAMOS LAS GENERACIONES X APTITUD
        print(self.poblacion_generacion)
        x = [0,1,2]
        y = [31,23,23]
        plt.plot(x,y)
        plt.show()


    def fun_poblacion_init(self, exponente, rango, interv, po):
        # CREACION DE LOS INDIVIDUOS
        for i in range(po):
            alelo_c = ""
            for o in range(exponente):
                alelo_c = alelo_c + str(rand.choice(["0", "1", "0", "1", "0"]))

            self.poblacion_init.append(self.creacion_indiv(alelo_c, rango, interv))

    def creacion_indiv(self, alelo_c, rango, interv):
        valor_c = 0
        for posicion, digito_string in enumerate(alelo_c[::-1]):
            valor_c += int(digito_string) * 2 ** posicion

        # CUALCULO DE FENO Y APTITUD POR INDIVIDUO
        feno = self.fenotipo(rango, interv, valor_c)
        apti = self.aptitud(feno)
        # CREACION DEL INDIVIDUO
        individuo = Individuo(alelo_c, valor_c, feno, apti)
        individuo.alelo = alelo_c
        # SE AGREGA A LA POBLACION INICIAL
        # print("generacion interna creacion_ind",num_decend)
        # self.poblacion_init[num_decend].append(individuo)
        return individuo

    def cruza(self, pc, po, exponente, rango, interv):
        pob_cruza = []
        # IMPLEMENTACION DE PROBABILIDADES DE CRUZA
        num_ind = round(pc * po)
        while True:
            cont_cruza = 0
            list_value = []
            for i in range(po):
                value = random.uniform(0, 0.9)
                list_value.append(value)
                # print("test -- valor de pc")
                # print(float(value))
                # print('{:.2f},'.format(value))
                if list_value[i] <= pc:
                    cont_cruza += 1
                    indv = self.poblacion_init[i]
                    pob_cruza.append(indv)
            if cont_cruza == num_ind:
                break
            else:
                pob_cruza.clear()

        # PROCESO DE CRUZA Y CREACION DE NUEVOS NUEVOS INDIVIDUOS
        tam_pob_cruce = len(pob_cruza)
        punto_cruce = random.randint(0, exponente)

        # NUEVA ACTUALIZACION PARA SALVAR LA GENERACION NUEVA DE LA LIST() POBLACION INICIAL
        # self.num_decend = self.num_decend + 1
        for i in range(tam_pob_cruce - 1):
            parent1 = pob_cruza[i].alelo
            parent2 = pob_cruza[i + 1].alelo

            children_rest1 = parent2[:punto_cruce] + parent1[punto_cruce:]
            children_rest2 = parent1[:punto_cruce] + parent2[punto_cruce:]

            children1 = "".join(children_rest1)
            children2 = "".join(children_rest2)

            self.poblacion_init.append(self.creacion_indiv(children1, rango, interv))
            self.poblacion_init.append(self.creacion_indiv(children2, rango, interv))

        for i in range(len(pob_cruza)):
            print("PROSPECTOS A CRUZA: ", pob_cruza[i].alelo)
            self.resultSet.insert(INSERT,'PROSPECTOS A CRUZA:'+ pob_cruza[i].alelo + '\n')
        # COPIA DE LA LISTA POB_CRUZA PARA USAR UNA LISTA GLOBAL
        self.pob_cruza = pob_cruza

    def aptitud(self, fenotipo):
        termino_1 = (fenotipo ** 2) / 20

        termino_2 = math.tanh(fenotipo ** 2)

        termino_3 = math.cos(10 * fenotipo)

        aptitud = termino_1 + termino_2 * termino_3
        return aptitud

    def poda(self,num_pobmax,rango_max,rango_min):
        #MUESTRA DATOS IMPORTANTES Y GUARDA POBLACION
        self.test_print()
        #ORDENA POBLACION DE MAYOR A MENOR
        pob_total = sorted(self.poblacion_final, key=lambda indiv: indiv.aptitud, reverse=True)
        print("POBLACION TOTAL ORDENADA:")
        self.resultSet.insert(INSERT,'Poblacion Total :' + '\n')

        cont_max = 0
        #DESCARGA INDIVIDUOS YA SEA POR REPETIDOS O FUERA DE RANGO O POR LIMITE DE POBLACION FINAL
        for i in range(len(pob_total)):
            print("aptitud : fenotipo: ", pob_total[i].aptitud, pob_total[i].fenotipo)
            self.resultSet.insert(INSERT,'Aptitud: ' + str(pob_total[i].aptitud) + " Fenotipo: "+ str(pob_total[i].fenotipo) + '\n')
            if pob_total[i].fenotipo <= rango_max and pob_total[i].fenotipo >= rango_min:
                if cont_max < num_pobmax and pob_total[i].fenotipo != pob_total[i-1].fenotipo:

                    self.poblacion_max.append(pob_total[i])
                    cont_max += 1
                else:
                    if cont_max == num_pobmax:
                        break
        self.poblacion_generacion.append([])
        print("-----------POBLACION FINAL MAXIMA-------------")
        self.resultSet.insert(INSERT,'Poblacion Final Maxima :' + '\n')
        for m in range(len(self.poblacion_max)):
            print("Aptitud:", self.poblacion_max[m].aptitud)
            print("generacion: ", self.num_generacion)
            self.poblacion_generacion[self.num_generacion].append(self.poblacion_max[m].aptitud)
            self.resultSet.insert(INSERT,'Aptitud: ' + str(self.poblacion_max[m].aptitud) + " Generacion: "
                                    + str(pob_total[i].fenotipo) + '\n')

    def mutacion(self, pmi, pmg, exponente, rango, interv):
        pc = pmi * pmg
        pob_muta = []
        # IMPLEMENTACION DE PROBABILIDADES DE MUTA
        while True:
            cont_muta = 0
            list_value = []
            for i in range(len(self.pob_cruza)):
                value = random.uniform(0, (0.9 + pc))
                list_value.append(value)
                if list_value[i] <= pc:
                    cont_muta += 1
                    # MUTACION DE LOS INDIVIOS
                    print("INDIVIDUO ACEPTADOS PARA MUTA :" + str(self.pob_cruza[i].alelo))
                    #self.resultSet.insert(INSERT,'INDIVIDUO ACEPTADOS PARA MUTA :' + str(self.pob_cruza[i].alelo) + '\n')
                    valor_m = self.pob_cruza[i].alelo
                    l_valor_m = list(valor_m)
                    # MUTACION DE LOS INDIVIDUOS
                    ale = random.randint(0, (exponente - 1))

                    if valor_m[ale] == '0':
                        l_valor_m[ale] = '1'
                    else:
                        l_valor_m[ale] = '0'
                    valor_m = "".join(l_valor_m)

                    pob_muta.append(self.creacion_indiv(valor_m, rango, interv))
            if cont_muta > 1:
                break
            else:
                pob_muta.clear()
        print("cantidad que mutaron: ", len(pob_muta))
        self.resultSet.insert(INSERT,'cantidad que mutaron :' + str(len(pob_muta)) + '\n')
        self.pob_muta = pob_muta

    def fenotipo(self, rango, interv, indv_valor):
        fenotipo = 0.0
        fenotipo = (rango + indv_valor) * interv
        return fenotipo

    # FUNCION DE TEST DE INVIDUOS POR DESCENDIA DE UNA GENERACION
    def test_print(self):
        print("------------POB INICIAL--------------")
        for i in range(len(self.poblacion_init)):
            p_alelo = self.poblacion_init[i].alelo
            p_fenotipo = self.poblacion_init[i].fenotipo
            p_aptitud = self.poblacion_init[i].aptitud
            # AÑADIR INDIVIDUOS A LA POBLACION FINAL
            self.poblacion_final.append(self.poblacion_init[i])
            print("DESCENDENCIA:", len(self.poblacion_init))
            print("alelo: ", p_alelo)
            print("feno: ", p_fenotipo)
            print("aptitud: ", p_aptitud)
            print("----")

        print("----------POB--CRUZA----------------")
        for i in range(len(self.pob_cruza)):
            p_alelo = self.pob_cruza[i].alelo
            p_fenotipo = self.pob_cruza[i].fenotipo
            p_aptitud = self.pob_cruza[i].aptitud
            # AÑADIR INDIVIDUOS A LA POBLACION FINAL
            self.poblacion_final.append(self.pob_cruza[i])
            print("DESCENDENCIA:", len(self.pob_cruza))
            print("alelo: ", p_alelo)
            print("feno: ", p_fenotipo)
            print("aptitud: ", p_aptitud)
            print("----")

        print("----------POB--MUTA----------------")
        for i in range(len(self.pob_muta)):
            p_alelo = self.pob_muta[i].alelo
            p_fenotipo = self.pob_muta[i].fenotipo
            p_aptitud = self.pob_muta[i].aptitud
            # AÑADIR INDIVIDUOS A LA POBLACION FINAL
            self.poblacion_final.append(self.pob_muta[i])
            print("DESCENDENCIA:", len(self.pob_muta))
            print("alelo: ", p_alelo)
            print("feno: ", p_fenotipo)
            print("aptitud: ", p_aptitud)
            print("----")
