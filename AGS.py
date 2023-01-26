import math
import random
# from random import *
import random as rand
from Individuo import *
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

class AGS(object):
    # RECORDATORIO // DEBES REINICIAR EL CONTADOR DE NUM_DECEND
    num_generacion = 0
    pob_cruza = []
    pob_muta = []
    poblacion_init = []
    poblacion_max = []
    poblacion_min = []
    poblacion_final = []
    poblacion_generacion = []

    def __init__(self, pc, pmi, pmg, po, p_Max, rango_min, rango_max, interv, cantidad_gene):
        self.pc = pc
        self.pmi = pmi
        self.pmg = pmg
        self.po = po
        self.p_Max = p_Max
        self.rango_min = rango_min
        self.rango_max = rango_max
        self.interv = interv
        self.cantidad_gene = cantidad_gene

        # CALCULAR EL RANGO
        rango = rango_max - rango_min

        # CALCULA LOS PUNTOS DE BITS
        puntos = (rango / interv) + 1

        # CALCULA LOS BITS
        exponente = 1
        while True:
            exponente += 1
            bits = 2 ** exponente
            if bits >= puntos:
                break


        # EJECUCION DE LAS GENERACIONES SEGUN EL NUMERO ASIGNADO POR EL USUARIO
        while True:
            self.pob_cruza.clear()
            self.pob_muta.clear()
            self.poblacion_init.clear()
            self.poblacion_max.clear()
            self.poblacion_min.clear()
            self.poblacion_final.clear()

            # LLAMADA DE FUNCION CREACION DE INDIVIDUOS y SELECCION
            self.fun_poblacion_init(exponente, rango, interv, po)
            # LLAMADA DE METODO PARA CRUZA
            self.cruza(pc, po, exponente, rango, interv)
            # LLAMADA A LA MUTACION
            self.mutacion(pmi, pmg, exponente, rango, interv)
            # LLAMADA A PODA
            self.poda(p_Max, rango_max, rango_min)
            self.num_generacion += 1
            if self.num_generacion == self.cantidad_gene:
                break
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
        cont_max = 0
        #DESCARGA INDIVIDUOS YA SEA POR REPETIDOS O FUERA DE RANGO O POR LIMITE DE POBLACION FINAL
        for i in range(len(pob_total)):
            print("aptitud : fenotipo: ", pob_total[i].aptitud, pob_total[i].fenotipo)

            if pob_total[i].fenotipo <= rango_max and pob_total[i].fenotipo >= rango_min:
                if cont_max < num_pobmax and pob_total[i].fenotipo != pob_total[i-1].fenotipo:

                    self.poblacion_max.append(pob_total[i])
                    cont_max += 1
                else:
                    if cont_max == num_pobmax:
                        break
        self.poblacion_generacion.append([])
        print("-----------POBLACION FINAL MAXIMA-------------")
        for m in range(len(self.poblacion_max)):
            print("Aptitud:", self.poblacion_max[m].aptitud)
            print("generacion: ", self.num_generacion)
            self.poblacion_generacion[self.num_generacion].append(self.poblacion_max[m].aptitud)

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
                    print("INDIVIDUPS ACEPTADOS PARA MUTA")
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
        print("cantidad que mutaron; ", len(pob_muta))
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
