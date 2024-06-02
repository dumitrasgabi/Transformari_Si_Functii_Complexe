import numpy as np
from tkinter import *
import tkinter.messagebox
from math import *
from cmath import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
Figura = []  # folosita pt a putea stora o figura dupa ce o desenam. Ne ajuta la transformari si functia e4
Umplere = np.array([])  # folosit pentru a stora figuri cu gradient
z_global = 0+0j  # pentru a putea schimba Umplerea in aplicarea unor functii semicercului
regiune_prezenta = 0
semidisk_prezent = 0
disk_prezent = 0


class Class:
    def __init__(self, rot):
        # ======================================================================== Functii ==========================================================================

        def focus_next_entry(event):  # down arrow ca sa manevram mai usor printre textboxuri
            event.widget.tk_focusNext().focus()
            return "break"

        def focus_previous_entry(event):  # up arrow la fel
            event.widget.tk_focusPrev().focus()
            return "break"

        def on_enter_pressed(event):  # enter in loc de go
            go(Figura)

        def on_escape_pressed(event):  # escape in loc de iesire
            Iesire()

        def on_r_pressed(event):  # pt reset r
            Reset()

        def Trig_To_Cart(modul, arg):  # conversie de la trigonometric la cartezian
            x = modul * cos(arg)
            y = modul * sin(arg)
            z = x + 1j * y
            return z

        def Paint1(y):  # Desi canvas poate fi dat ca parametru, cu ax e mai greu
            ax1.clear()
            ax1.set_xlim(-10, 10)
            ax1.set_ylim(-10, 10)
            x_points = np.real(y)
            y_points = np.imag(y)
            x_points = np.append(x_points, x_points[0])
            y_points = np.append(y_points, y_points[0])
            ax1.plot(x_points, y_points)
            ax1.spines['left'].set_position('zero')
            ax1.spines['bottom'].set_position('zero')
            ax1.xaxis.set_ticks_position('bottom')
            ax1.yaxis.set_ticks_position('left')
            ax1.spines['top'].set_color('none')
            ax1.spines['right'].set_color('none')
            canvas1.draw()
            desen = list(zip(x_points, y_points))
            return desen

        def Paint2(y):
            ax2.clear()
            ax2.set_xlim(-10, 10)
            ax2.set_ylim(-10, 10)
            x_points = np.real(y)
            y_points = np.imag(y)
            x_points = np.append(x_points, x_points[0])
            y_points = np.append(y_points, y_points[0])
            ax2.plot(x_points, y_points)
            ax2.spines['left'].set_position('zero')
            ax2.spines['bottom'].set_position('zero')
            ax2.xaxis.set_ticks_position('bottom')
            ax2.yaxis.set_ticks_position('left')
            ax2.spines['top'].set_color('none')
            ax2.spines['right'].set_color('none')
            canvas2.draw()
            desen = list(zip(x_points, y_points))
            return desen

        def Mesh(x, y, z):
            ax1.clear()
            ax1.set_xlim(-5, 5)
            ax1.set_ylim(0, np.pi)
            ax1.pcolormesh(x, y, np.angle(z), shading='auto')
            ax1.spines['left'].set_position('zero')
            ax1.spines['bottom'].set_position('zero')
            ax1.xaxis.set_ticks_position('bottom')
            ax1.yaxis.set_ticks_position('left')
            ax1.spines['top'].set_color('none')
            ax1.spines['right'].set_color('none')
            canvas1.draw()
            m = list(zip(x.flatten(), y.flatten(), np.angle(z).flatten()))
            return m

        def deseneaza_la_apasare(lista):
            global Figura
            Figura = Paint1(lista)

    # ======================================================== Functii pt desen ========================================================================
        def drseg(z1, z2):  # << draws segments >>
            ZL = []
            for k in range(100):
                t = k / 100
                z = (1 - t) * z1 + t * z2
                ZL.append(z)
            return ZL

        def drcir():  # << draws circles >>
            ZL = []
            for k in range(200):
                theta = 2 * pi * k / 200
                z = 0 + Trig_To_Cart(4, theta)
                ZL.append(z)
            return ZL

        def drsq():  # << draws squares >>
            square = drseg(0, 4) + drseg(4, 4+4j) + drseg(4+4j, 4j) + drseg(4j, 0)
            return square

        def drtra():  # << draws trapezoids >>
            trapezoid = drseg(0, 4) + drseg(4, 3+2j) + drseg(3+2j, 1+2j) + drseg(1+2j, 0)
            return trapezoid

        def drrect():  # << draws rectangles >>
            rectangle = drseg(0, 4) + drseg(4, 4+2j) + drseg(4+2j, 2j) + drseg(2j, 0)
            return rectangle

        def drpar():  # << draws parallelograms >>
            parallelogram = drseg(0, 4) + drseg(4, 6 + 3j) + drseg(6 + 3j, 2 + 3j) + drseg(2 + 3j, 0)
            return parallelogram

        def drpol(num):  # << draws polygons >>
            marime = 4.0
            theta = np.linspace(0, 2 * np.pi, num + 1)
            polygon = marime * np.exp(1j * theta)
            return polygon

        def drkite():  # << draws kites >>
            kite = drseg(0, 2+2j) + drseg(2+2j, 4) + drseg(4, 2-4j) + drseg(2-4j, 0)
            return kite

        def drreg():  # << draws regions >>
            global Umplere, regiune_prezenta
            x = np.linspace(-5, 5, 400)
            y = np.linspace(0, pi, 400)
            xx, yy = np.meshgrid(x, y)
            z = xx + 1j * yy
            Umplere = np.exp(z)
            m = Mesh(xx, yy, z)
            regiune_prezenta = 1
            return m

        def drsemidisk():  # << draws semi-disks >>
            global Umplere, semidisk_prezent
            theta = np.linspace(0, np.pi, 400)
            r = np.linspace(0, 1, 200)
            theta, r = np.meshgrid(theta, r)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = x + 1j * y
            Umplere = np.exp(z)
            m = Mesh(x, y, z)
            semidisk_prezent = 1
            return m

        def drdisk():  # << draws disks >>
            global Umplere, disk_prezent
            theta = np.linspace(0, 2 * np.pi, 400)
            r = np.linspace(0, 1, 200)
            theta, r = np.meshgrid(theta, r)
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            z = x + 1j * y
            Umplere = np.exp(z)
            m = Mesh(x, y, z)
            disk_prezent = 1
            return m

        # ======================================= Transformari si functii complexe ===========================================================
        def tr(lista, t):  # prescurtare de la << translation >>
            w = []
            for z in lista:
                complex_z = complex(z[0], z[1])
                w.append(complex_z + t)
            return w

        def hom(lista, alfa):  # prescurtare de la << homothety >>
            w = []
            for z in lista:
                w.append(z * alfa)
            return w

        def rotation(lista, r):  # prescurtare de la << rotation >>
            w = []
            for z in lista:
                Elait = Trig_To_Cart(1, r)
                w.append(z * Elait)
            return w

        def sym(lista, vert):  # prescurtare de la << symmetry >>
            w = []
            for z in lista:
                if vert is True:
                    w.append(z.conjugate())
                else:
                    w.append(z.conjugate()*(-1))
            return w

        def e5():
            global Umplere
            if disk_prezent == 0 and semidisk_prezent == 0 and regiune_prezenta == 0:
                tkinter.messagebox.showwarning("Eroare", "Invalid!")
                Reset()
                return
            else:
                ax2.clear()
                x_edges = np.linspace(-np.exp(5), np.exp(5), Umplere.shape[1] + 1)
                y_edges = np.linspace(0, np.exp(5), Umplere.shape[0] + 1)
                ax2.set_xlim(-np.exp(5), np.exp(5))
                ax2.set_ylim(0, np.exp(5))
                ax2.pcolormesh(x_edges, y_edges, np.angle(Umplere), shading='auto')
                ax2.spines['left'].set_position('zero')
                ax2.spines['bottom'].set_position('zero')
                ax2.xaxis.set_ticks_position('bottom')
                ax2.yaxis.set_ticks_position('left')
                ax2.spines['top'].set_color('none')
                ax2.spines['right'].set_color('none')
                canvas2.draw()
                m = list(zip(np.real(Umplere).flatten(), np.imag(Umplere).flatten(), np.angle(Umplere).flatten()))
                return m

        def e10():
            if disk_prezent == 1:
                global Umplere
                ax2.clear()
                z = Umplere
                w = 1j * (1 - z) / (1 + z)
                x_new = np.real(w)
                y_new = np.imag(w)
                x_edges = np.linspace(-5, 5, x_new.shape[1] + 1)
                y_edges = np.linspace(0, 5, y_new.shape[0] + 1)
                ax2.set_xlim(-5, 5)
                ax2.set_ylim(-5, 5)
                ax2.pcolormesh(x_edges, y_edges, np.angle(w), shading='auto')
                ax2.spines['left'].set_position('zero')
                ax2.spines['bottom'].set_position('zero')
                ax2.xaxis.set_ticks_position('bottom')
                ax2.yaxis.set_ticks_position('left')
                ax2.spines['top'].set_color('none')
                ax2.spines['right'].set_color('none')
                canvas2.draw()
                m = list(zip(np.real(w).flatten(), np.imag(w).flatten(), np.angle(w).flatten()))
                return m
            else:
                tkinter.messagebox.showwarning("Eroare", "Invalid!")
                Reset()

        # ================== Optiuni ========================
        def go(lista):
            global Figura
            t = T.get()
            h = H.get()
            r = R.get()
            s = S.get()
            v = vertical.get()
            try:
                t = complex(t)
                h = complex(h)
                r = complex(r)
                s = complex(s)
                if h == 0:
                    tkinter.messagebox.showwarning("Eroare", "Valoarea lui H nu poate fi zero!")
                    Reset()
                    return
                if s != 0 and s != 1:
                    tkinter.messagebox.showwarning("Eroare", "Valoarea lui S poate fi numai 1 (DA) sau 0 (NU)!")
                    Reset()
                    return
                t1 = tr(lista, t)
                h1 = hom(t1, h)
                r1 = rotation(h1, r)
                if s == 1:
                    r1 = sym(r1, v)
                Figura = Paint2(r1)
                T.set("0")
                H.set("1")
                R.set("0")
                S.set("0")

                return r1
            except ValueError:
                tkinter.messagebox.showwarning("Eroare", "Valorile introduse nu sunt corecte!")
                T.set("0")
                H.set("1")
                R.set("0")
                return True

        def Reset():
            global regiune_prezenta, semidisk_prezent
            T.set("0")
            H.set("1")
            R.set("0")
            S.set("0")
            regiune_prezenta = 0
            semidisk_prezent = 0
            vertical.set(True)
            ax1.clear()
            ax1.plot(0, 0)
            ax1.spines['left'].set_position('zero')
            ax1.spines['bottom'].set_position('zero')
            ax1.xaxis.set_ticks_position('bottom')
            ax1.yaxis.set_ticks_position('left')
            ax1.spines['top'].set_color('none')
            ax1.spines['right'].set_color('none')
            canvas1.draw()
            ax2.clear()
            ax2.plot(0, 0)
            ax2.spines['left'].set_position('zero')
            ax2.spines['bottom'].set_position('zero')
            ax2.xaxis.set_ticks_position('bottom')
            ax2.yaxis.set_ticks_position('left')
            ax2.spines['top'].set_color('none')
            ax2.spines['right'].set_color('none')
            canvas2.draw()
            return

        def Iesire():
            q = tkinter.messagebox.askyesno("Validate Entry Widget", "Sunteti sigur ca doriti sa parasiti aplicatia?")
            if q > 0:
                rot.destroy()
                return

        # ================= Frame-uri =======================
        self.root = rot
        self.root.title("Transformari & functii complexe")
        self.root.geometry("1495x690+0+0")
        self.root.configure(bg="#d9c0de")
        frmPrincipal = Frame(self.root, bd=10, width=700)
        frmPrincipal.grid()
        frmTitlu = Frame(frmPrincipal, bd=10, width=700, relief=RIDGE)
        frmTitlu.pack(side=TOP)
        frmBefore = Frame(frmPrincipal, bd=10, width=300, relief=RIDGE)
        frmBefore.pack(side=LEFT, anchor='nw')
        frmAfter = Frame(frmPrincipal, bd=10, width=300, relief=RIDGE)
        frmAfter.pack(side=RIGHT, anchor='ne')
        frmFunctii = Frame(frmPrincipal, bd=10, width=600, relief=RIDGE)
        frmFunctii.pack(side=BOTTOM)

        # ================= Variabile =======================
        T = StringVar(value="0")
        H = StringVar(value="1")
        R = StringVar(value="0")
        S = StringVar(value="0")
        vertical = BooleanVar(value=True)

        # ================= Widget-uri ======================
        lblInfo = Label(frmTitlu, font=('Helvetica', 25, 'bold'), text="Transformari & functii complexe", justify=LEFT, bg="#d9c0de")
        lblInfo.pack(side=TOP)
        lblDate = LabelFrame(frmPrincipal, bd=10, width=500, height=200, font=('Helvetica', 12, 'bold'), text='Figuri', relief=RIDGE)
        lblDate.pack(side=TOP)
        lblTransformari = LabelFrame(frmPrincipal, bd=10, width=350, height=220, font=('Helvetica', 12, 'bold'), text='Transformari', relief=RIDGE)
        lblTransformari.pack(side=TOP, fill=Y)
        lblOptiuni = LabelFrame(frmPrincipal, bd=10, width=620, height=100, font=('Helvetica', 12, 'bold'), text='Optiuni', relief=RIDGE)
        lblOptiuni.pack(side=BOTTOM)
        lblBefore = LabelFrame(frmBefore, bd=10, width=200, height=200, font=('Helvetica', 12, 'bold'), text='Before', relief=RIDGE)
        lblBefore.pack(anchor='nw')
        lblAfter = LabelFrame(frmAfter, bd=10, width=200, height=200, font=('Helvetica', 12, 'bold'), text='After', relief=RIDGE)
        lblAfter.pack(anchor='ne')
        cnvPanza1 = Canvas(lblBefore, width=200, height=300)
        cnvPanza1.pack()
        cnvPanza2 = Canvas(lblAfter, width=200, height=300)
        cnvPanza2.pack()
        lblFunctii = LabelFrame(frmFunctii, bd=10, width=400, height=300, font=('Helvetica', 12, 'bold'), text='Functii', relief=RIDGE)
        lblFunctii.pack(fill=X)

        fig1 = Figure(figsize=(4, 3), dpi=100)
        ax1 = fig1.add_subplot(111)
        canvas1 = FigureCanvasTkAgg(fig1, master=cnvPanza1)
        canvas_widget = canvas1.get_tk_widget()
        canvas_widget.pack()
        ax1.plot(0, 0)
        ax1.spines['left'].set_position('zero')
        ax1.spines['bottom'].set_position('zero')
        ax1.xaxis.set_ticks_position('bottom')
        ax1.yaxis.set_ticks_position('left')
        ax1.spines['top'].set_color('none')
        ax1.spines['right'].set_color('none')
        canvas1.draw()

        fig2 = Figure(figsize=(4, 3), dpi=100)
        ax2 = fig2.add_subplot(111)
        canvas2 = FigureCanvasTkAgg(fig2, master=cnvPanza2)
        canvas_widget = canvas2.get_tk_widget()
        canvas_widget.pack()
        ax2.plot(0, 0)
        ax2.spines['left'].set_position('zero')
        ax2.spines['bottom'].set_position('zero')
        ax2.xaxis.set_ticks_position('bottom')
        ax2.yaxis.set_ticks_position('left')
        ax2.spines['top'].set_color('none')
        ax2.spines['right'].set_color('none')
        canvas2.draw()

        # ================================= Toolbar ========================================
        toolbar1 = NavigationToolbar2Tk(canvas1, pack_toolbar=False)
        toolbar1.update()
        toolbar1.pack(side=BOTTOM, fill=X)

        toolbar2 = NavigationToolbar2Tk(canvas2, pack_toolbar=False)
        toolbar2.update()
        toolbar2.pack(side=BOTTOM, fill=X)

        # ================================= Butoane Figuri =================================
        btnSq = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drsq()), text="Patrat", bg="#c75858")
        btnSq.grid(row=0, column=0, pady=12)
        btnCir = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drcir()), text="Cerc", bg="#c78058")
        btnCir.grid(row=0, column=1, pady=12)
        btnTri = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drpol(3)), text="Triun.", bg="#c79858")
        btnTri.grid(row=0, column=2, pady=12)
        btnTra = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drtra()), text="Trapez", bg="#c7af58")
        btnTra.grid(row=0, column=3, pady=12)
        btnRect = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drrect()), text="Drept.", bg="#c7c758")
        btnRect.grid(row=0, column=4, pady=12)
        btnRho = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drpol(4)), text="Romb", bg="#a5c758")
        btnRho.grid(row=0, column=5, pady=12)
        btnSeg = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drseg(0+0j, 2+2j)), text="Segm.", bg="#58c75d")
        btnSeg.grid(row=0, column=6, pady=12)
        btnKite = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drkite()), text="Zmeu", bg="#62d98b")
        btnKite.grid(row=0, column=7, pady=12)
        btnPent = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drpol(5)), text="5-gon", bg="#58c788")
        btnPent.grid(row=1, column=0, pady=12)
        btnHex = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drpol(6)), text="6-gon", bg="#58a9c7")
        btnHex.grid(row=1, column=1, pady=12)
        btnHept = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drpol(7)), text="7-gon", bg="#5880c7")
        btnHept.grid(row=1, column=2, pady=12)
        btnOct = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drpol(8)), text="8-gon", bg="#6658c7")
        btnOct.grid(row=1, column=3, pady=12)
        btnPar = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=lambda: deseneaza_la_apasare(drpar()), text="Paral.", bg="#a958c7")
        btnPar.grid(row=1, column=4, pady=12)
        btnReg = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=drreg, text="Dr.Gr.", bg="#cbc3f7")
        btnReg.grid(row=1, column=5, pady=12)
        btnDisk = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=drdisk, text="Disc", bg="#cbc3f7")
        btnDisk.grid(row=1, column=6, pady=12)
        btnSem = Button(lblDate, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=3, command=drsemidisk, text="Smdisc", bg="#cbc3f7")
        btnSem.grid(row=1, column=7, pady=12)

        # ================================ TextBoxuri Transformari ==============================================
        lblT = Label(lblTransformari, font=('Helvetica', 12, 'bold'), text="Translatie: T = ", bd=7)
        lblT.grid(row=2, column=0, sticky=W)
        txtT = Entry(lblTransformari, font=('Helvetica', 12, 'bold'), bd=7, textvariable=T, width=40)
        txtT.grid(row=2, column=1)
        lblH = Label(lblTransformari, font=('Helvetica', 12, 'bold'), text="Omotetie: H = ", bd=7)
        lblH.grid(row=3, column=0, sticky=W)
        txtH = Entry(lblTransformari, font=('Helvetica', 12, 'bold'), bd=7, textvariable=H, width=40)
        txtH.grid(row=3, column=1)
        lblR = Label(lblTransformari, font=('Helvetica', 12, 'bold'), text="Rotatie: R = ", bd=7)
        lblR.grid(row=4, column=0, sticky=W)
        txtR = Entry(lblTransformari, font=('Helvetica', 12, 'bold'), bd=7, textvariable=R, width=40)
        txtR.grid(row=4, column=1)
        lblS = Label(lblTransformari, font=('Helvetica', 12, 'bold'), text="Simetrie (1:DA, 0:NU) ", bd=7)
        lblS.grid(row=5, column=0, sticky=W)
        txtS = Entry(lblTransformari, font=('Helvetica', 12, 'bold'), bd=7, textvariable=S, width=40)
        txtS.grid(row=5, column=1)
        radioV = Radiobutton(lblTransformari, text="Vertical", variable=vertical, value=True, font=('Helvetica', 15), padx=20, pady=13)
        radioV.grid(row=6, column=0)
        radioO = Radiobutton(lblTransformari, text="Orizontal", variable=vertical, value=False, font=('Helvetica', 15), padx=20, pady=13)
        radioO.grid(row=6, column=1)

        # ================================= Butoane Optiuni ====================================================
        txtT.bind("<Down>", focus_next_entry)
        txtH.bind("<Down>", focus_next_entry)
        txtR.bind("<Down>", focus_next_entry)
        txtS.bind("<Up>", focus_previous_entry)
        txtH.bind("<Up>", focus_previous_entry)
        txtR.bind("<Up>", focus_previous_entry)

        btnGo = Button(lblOptiuni, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=15, command=lambda: go(Figura), text="Go (Enter)", bg="#414ce8")
        btnGo.grid(row=7, column=0, pady=12)
        root.bind('<Return>', on_enter_pressed)

        btnReset = Button(lblOptiuni, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=14, command=Reset, text="Reset (R)", bg="#a8323e")
        btnReset.grid(row=7, column=1, pady=12)
        root.bind('<KeyPress-r>', on_r_pressed)

        btnIesire = Button(lblOptiuni, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=14, command=Iesire, text="Iesire (Esc)", bg="#32a891")
        btnIesire.grid(row=7, column=2, pady=12)
        root.bind('<Escape>', on_escape_pressed)

        # ======================================== Butoane Functii Complexe ====================================================
        btnE5 = Button(lblFunctii, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=9, command=e5, text="E5", bg="#cbc3f7")
        btnE5.grid(row=9, column=1, pady=12, sticky=W)
        btnE10 = Button(lblFunctii, padx=12, bd=7, font=('Helvetica', 12, 'bold'), width=9, command=e10, text="E10", bg="#c3d3f7")
        btnE10.grid(row=9, column=2, pady=12, sticky=W)


if __name__ == '__main__':
    root = Tk()
    root.iconbitmap("tr.ico")
    application = Class(root)
    root.resizable(False, False)
    root.mainloop()
