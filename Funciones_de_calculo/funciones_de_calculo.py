from tkinter import *
import tkinter.messagebox as tkmss
from math import sqrt


class ConcreteSection:
    Redondos = {6: 28.3, 8: 50.3, 10: 78.5, 12: 113.1,
                16: 201.1, 20: 314.2, 25: 490.9, 32: 804.3}
    d = 0
    fcd = 0
    fyd = 0
    y = 0
    Ast = 0     # Cuantía traccionada mm2
    Asc = 0     # Cuantía comprimida mm2
    p = 0       # Cuantía total mm2
    D_s = 0     # Diametro de redodondos traccionados
    D_c = 0     # Diametro de redondos comprimidos
    n = 0       # Número de redondos traccionados
    m = 0       # Número de redondos comprimidos

    def __init__(self, b, h, cover, Md, fck, fyk, Gc, Gs, xd):
        self.b = b
        self.h = h
        self.cover = cover
        self.Md = Md
        self.fck = fck
        self.fyk = fyk
        self.Gc = Gc
        self.Gs = Gs
        self.xd = xd

    def FlexionSimple(self):

        try:
            self.b = int(self.b)
            self.h = int(self.h)
            self.cover = int(self.cover)
            self.Md = float(self.Md)
            self.fck = int(self.fck)
            self.fyk = int(self.fyk)
            self.Gc = float(self.Gc)
            self.Gs = float(self.Gs)
            self.xd = float(self.xd)

        except TypeError:
            print("Datos no válidos")

        self.d = self.h - self.cover
        self.fcd = self.fck / self.Gc
        self.fyd = self.fyk / self.Gs
        self.y = self.xd * self.d * 0.8

        M_lim = self.b * self.y * self.fcd * (self.d - self.y / 2) / 1000000  # M_lin esta en m*kN
        if (M_lim - self.Md) < 0.01:
            increAs = (self.Md - M_lim) * 1000000 / ((self.h - 2 * self.cover) * self.fyd)  # increAs esta en mm2
        else:
            increAs = 0
            adv_cambio_x_d = tkmss.askquestion("Mlim > Md",
                                               "La capacidad a flexión de la viga es superior al momento de solicitación\n\n"
                                               "¿Desea modificar la profundidad relativa de la fibra neutra x/d?")
            if adv_cambio_x_d == "yes":
                c = self.Md * 1000000 / (self.d ** 2 * self.b * self.fcd)
                self.xd = ((1 - sqrt(1 - 2 * c)) / 0.8)
                self.FlexionSimple()
                return

        self.Ast = (self.b * self.y * self.fcd / self.fyd) + increAs
        self.Asc = increAs

        for i in ConcreteSection.Redondos:
            self.n = round(self.Ast / ConcreteSection.Redondos[i])
            esp_entre_s = (self.b - 2 * self.cover - self.n * i) / (self.n - 1)
            if esp_entre_s >= 25:
                self.D_s = i
                break

        for j in ConcreteSection.Redondos:
            m = round(self.Asc / ConcreteSection.Redondos[j])
            esp_entre_c = (self.b - 2 * self.cover - self.m * j) / (self.m - 1)
            if esp_entre_c >= 50:
                self.D_c = j
                break

        self.p = self.Ast + self.Asc

        print(round(self.Ast), round(self.Asc), round(self.p))


    def WrtResults(self, text):

        text.config(state="normal")
        text.delete(1.0, 6.0)
        text.insert(1.0, f"Armadura Traccionada: {round(self.Ast)} mm2\n")
        text.insert(2.0, f"{self.n}xØ{self.D_s}\n\n")

        if self.Asc == 0:
            text.insert(4.0, "")
            text.config(state="disable")
        else:
            text.insert(4.0, f"Armadura Comprimida: {round(self.Asc)} mm2\n")
            text.insert(5.0, f"{self.m}xØ{self.D_s}\n")
            text.config(state="disable")

    #canvas.delete("all")

class Draw(ConcreteSection):

    def __int__(self,b , h, cover, n, m , D_s, D_c, var_opc, canvas, font):
        super().__init__(b, h, cover, n, m, D_s, D_c)
        self.var_opc = var_opc
        self.canvas = canvas
        self.font = font

    def DrawFlexionPositiva(self, escala_canvas):

        x0_viga = (self.canvas.winfo_height() - self.b * escala_canvas) / 2
        y0_viga = (self.canvas.winfo_width() - self.h * escala_canvas) / 2
        x1_viga = (self.canvas.winfo_height() + self.b * escala_canvas) / 2
        y1_viga = (self.canvas.winfo_width() + self.h * escala_canvas) / 2

        x0_recubri = x0_viga + self.cover * escala_canvas
        y0_recubri = y0_viga + self.cover * escala_canvas
        x1_recubri = x1_viga - self.cover * escala_canvas
        y1_recubri = y1_viga - self.cover * escala_canvas

        D_s = self.D_s * escala_canvas
        D_c = self.D_s * escala_canvas

        x0_armar_inf = x0_recubri + D_s / 2
        y0_armar_inf = y1_recubri - D_s / 2
        x1_armar_inf = x1_recubri - D_s / 2
        y1_armar_inf = y1_recubri - D_s / 2

        x0_armar_sup = x0_recubri + D_c / 2
        y0_armar_sup = y0_recubri + D_c / 2
        x1_armar_sup = x1_recubri - D_c / 2
        y1_armar_sup = y0_recubri + D_c / 2

        len_inf = x1_armar_inf - x0_armar_inf
        len_sup = x1_armar_sup - x0_armar_sup

        self.canvas.create_rectangle(x0_viga, y0_viga, x1_viga, y1_viga, width=2)
        # canvas.create_rectangle(x0_recubri, y0_recubri, x1_recubri, y1_recubri, dash= (10,10))

        self.canvas.create_line(x0_viga - 30, y0_viga, x1_viga - self.b * escala_canvas - 30, y1_viga, arrow=BOTH)
        self.canvas.create_line(x0_viga, y0_viga + self.h * escala_canvas + 30, x1_viga, y1_viga + 30, arrow=BOTH)

        self.canvas.create_text(x1_viga - self.b / 2 * escala_canvas, y1_viga + 50, text=str(self.b), font=self.font)
        self.canvas.create_text(x0_viga - 50, y0_viga + self.h / 2 * escala_canvas, text=str(self.h), font=self.font)
        self.canvas.create_text(x1_viga + 30, y1_armar_inf, text=f"{self.n}xØ{int(D_s / escala_canvas)}", font=self.font)

        if self.m > 0:
            self.canvas.create_text(x1_viga + 30, y1_armar_sup, text=f"{self.m}xØ{int(D_c / escala_canvas)}", font=self.font)


        for a in range(self.n):
            self.canvas.create_oval(x0_armar_inf + len_inf * a / (self.n - 1) - D_s / 2, y0_armar_inf - D_s / 2,
                               x0_armar_inf + len_inf * a / (self.n - 1) + D_s / 2, y0_armar_inf + D_s / 2)

        for c in range(self.m):
            self.canvas.create_oval(x0_armar_sup + len_sup * c / (self.m - 1) - D_c / 2, y0_armar_sup - D_c / 2,
                               x0_armar_sup + len_sup * c / (self.m - 1) + D_c / 2, y0_armar_sup + D_c / 2)


    def dibujarFlexionNegativa(self, escala_canvas):
        x0_viga = (ancho_canvas - self.b * escala_canvas) / 2
        y0_viga = (alto_canvas - self.h * escala_canvas) / 2
        x1_viga = (ancho_canvas + self.b * escala_canvas) / 2
        y1_viga = (alto_canvas + self.h * escala_canvas) / 2

        x0_recubri = x0_viga + self.cover * escala_canvas
        y0_recubri = y0_viga + self.cover * escala_canvas
        x1_recubri = x1_viga - self.cover * escala_canvas
        y1_recubri = y1_viga - self.cover * escala_canvas

        D_s = self.D_s * escala_canvas
        D_c = self.D_c * escala_canvas

        x0_armar_inf = x0_recubri + D_c / 2
        y0_armar_inf = y1_recubri - D_c / 2
        x1_armar_inf = x1_recubri - D_c / 2
        y1_armar_inf = y1_recubri - D_c / 2

        x0_armar_sup = x0_recubri + D_s / 2
        y0_armar_sup = y0_recubri + D_s / 2
        x1_armar_sup = x1_recubri - D_s / 2
        y1_armar_sup = y0_recubri + D_s / 2

        len_inf = x1_armar_inf - x0_armar_inf
        len_sup = x1_armar_sup - x0_armar_sup

        canvas.create_rectangle(x0_viga, y0_viga, x1_viga, y1_viga, width=2)
        # canvas.create_rectangle(x0_recubri, y0_recubri, x1_recubri, y1_recubri, dash= (10,10))

        canvas.create_line(x0_viga - 30, y0_viga, x1_viga - b * escala_canvas - 30, y1_viga, arrow=BOTH)
        canvas.create_line(x0_viga, y0_viga + h * escala_canvas + 30, x1_viga, y1_viga + 30, arrow=BOTH)

        canvas.create_text(x1_viga - b / 2 * escala_canvas, y1_viga + 50, text=str(b), font=fuente_canvas)
        canvas.create_text(x0_viga - 50, y0_viga + h / 2 * escala_canvas, text=str(h), font=fuente_canvas)
        canvas.create_text(x1_viga + 30, y1_armar_sup, text=f"{n}xØ{int(D_s / escala_canvas)}", font=fuente_canvas)
        if m > 0:
            canvas.create_text(x1_viga + 30, y1_armar_inf, text=f"{m}xØ{int(D_c / escala_canvas)}", font=fuente_canvas)
        canvas.create_text(70, alto_canvas - 20, text=f"Escala:{escala_canvas}pixel/mm ")

        for a in range(n):
            canvas.create_oval(x0_armar_sup + len_sup * a / (n - 1) - D_s / 2, y0_armar_sup - D_s / 2,
                               x0_armar_sup + len_sup * a / (n - 1) + D_s / 2, y0_armar_sup + D_s / 2,
                               color="red", width=2)

        for c in range(m):
            canvas.create_oval(x0_armar_inf + len_inf * c / (m - 1) - D_c / 2, y0_armar_inf - D_c / 2,
                               x0_armar_inf + len_inf * c / (m - 1) + D_c / 2, y0_armar_inf + D_c / 2,
                               fg="red", width=2)
    def checkFlex(self):

        if self.var_opc.get() == 1:
            self.DrawFlexionPositiva(self, 0.5, self.font)

        elif self.var_opc.get() == 2:
            self.DrawFlexionNegativa(self, 0.5, self.font)
