#Se importa la libreria de tkinter
import tkinter as tk                        #Para poder usar tkinter y los widgets
from tkinter import messagebox              #Para los mensajes desplegados en pantalla


#Para el uso de los archivos tipo json
import json

#Para generar los niveles aleatorios al inicio
import random

#Para la generación de pilas
import collections

#Para el reloj y las fechas tipo ISO
from datetime import datetime, timedelta

#Para abrir archivos en el explorador
import os

#Para la creación de pdf
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

#------------------------------------------------------------
#Creación de variables globales
#------------------------------------------------------------
INTERVALO_REFRESCO = 500  # En milisegundos

juego_borrado_numero_partida = " "

juego_cargado = False

juego_cargado_nivel = " "

nombre_jugador_cargado = " "



#------------------------------------------------------------
#Creación del documento de configuración default
#------------------------------------------------------------
nombre_archivo_config = "sudoku2026configuración.json"

#------------------------------------------------------------
#Creación del documento de para las jugadas actuales
#------------------------------------------------------------
nombre_archivo_juego_actual = "sudoku2026juegoactual.json"

#------------------------------------------------------------
#Creación del documento de para la bitacora de jugadas
#------------------------------------------------------------
nombre_archivo_bitácora_jugada = "sudoku2026_bitácora_jugadas.json"

#------------------------------------------------------------------------
#Se  definen algunos diseños que se usarán a lo largo del programa
#------------------------------------------------------------------------
FUENTE_UNIVERSAL = ("Segoe UI", 15, "bold") #Diseño para el texto de los títulos

TEXTO_UNIVERSAL = ("Segoe UI", 12, "bold") #Diseño para el texto normal

ESTILO_BOTON_MATRIZ = { 
    "bd":1,                  
    "highlightthickness":0, 
    "activebackground":"#78a5f3", # Evita que cambie de fondo gris al darle clic
    "width":5,
    "height":2
}

ESTILO_LABEL_RELOJ = {
    "bd":2,                  # Sin bordes
    "width":15,
    "height":2,
    "bg":"#ffffff",
}

ESTILO_ENTRY_RELOJ = {
    "bd":2,                  # Sin bordes
    "width":15,
    "bg":"#ffffff",
}

ESTILO_BOTONES = {
    "bd":2,                  # Sin bordes
    "width":15,
    "height":2,    
}

ESTILO_BOTON_SELECCIONA = {
    "bd": 2,
    "bg":"#ffffff",
    "width":5,
    "height":2,
}

ESTILO_BOTON_MENU = { #Estilo para los botones del menu
    "font": FUENTE_UNIVERSAL,
    "bg": "#36589b",         
    "fg": "#e5e9f0",          
    "bd": 0,
    "highlightthickness": 2,
    "highlightbackground": "#4c566a",
    "padx": 25,
    "pady": 8,
    "width": 14
}

ESTILO_OPCIONES_CONFIG = { #Estilo para las opciones de radio de la configuración
    "width": 100,
    "anchor":"w"
}

#----------------------------------------------------------------------------------------------------------------
#Se crea la ventana del menú principal, donde están las opciones para jugar, configuración, acerca, ayuda y salir
#-----------------------------------------------------------------------------------------------------------------
root = tk.Tk()
root.geometry("1000x700")
root.title("Sudoku Menú")

#sudoku-fondo
bg = tk.PhotoImage(file = "img/sudoku-fondo.png")

#Label para el fondo del menpu principal
label_fondo = tk.Label(root, image = bg)
label_fondo.place(x = 0, y = 0, relwidth=1.0, relheight=1.0)

#Muestra un label que es como un texto de tkinter
label = tk.Label(root,                   #La ventana de donde pertenece
    text="Menú Principal",               #El texto que tendrá
    font=('Segoe UI', 30, "bold"),       #El tipo de letra y tamaño
    compound="left",                     #La posición que debe tener
    fg="#0c3a95"                       #El color de la letra
)
label.pack()


#-----------------------------------------
#Funciones dentro de la ventana principal
#-----------------------------------------

#Función que despliega el manual de usuario en el browser
#E: no posee entrada
#S: se calcula la ruta del archivo y lo despliega en el browser
def desplegar_manual():
    ruta_absoluta = os.path.abspath("manual_de_usuario_sudoku.pdf")
    os.startfile(ruta_absoluta)


#------------------------------------------------------
#Función que abre la ventana de configuración
#------------------------------------------------------

#Función que emerge una ventana para la configuración del juego
#E: el usuario elige el nivel, los elementos a usar, el tipo de reloj (cronómetro, timer, ninguno), y el TOP x
#S: al finalizar y cerrar la ventana crea al archivo json para guardar los datos que el usuario eligió
def abrir_ventana_config():


    botomB.config(state="disabled")
    #------------------------------------------------------
    #Funciones dentro de la ventana secundaria del juego
    #------------------------------------------------------

    #Esta es una función para mostrar el habilitar el timer si el usuario lo selecciona, en otro caso lo deshabilita
    #E: obtiene con .get() el valor que tiene en ese momento el tiempo que se seleccionó
    #S: deshabilita los entry de las horas, minutos y segundos
    def muestra_timer():
        if root_config.reloj_seleccionado.get() == 'timer':
            estado = 'normal'
        else:
            horas.config(state='normal')
            minutos.config(state='normal')
            segundos.config(state='normal')            

            horas.delete(0, tk.END)
            horas.insert(0,0)
            minutos.delete(0, tk.END)
            minutos.insert(0,0)
            segundos.delete(0, tk.END)
            segundos.insert(0,0)
            estado = 'readonly'

        horas.config(state=estado)
        minutos.config(state=estado)
        segundos.config(state=estado)            


    #Función que guarda y cierra la configuración si el usuario lo desea
    #E: No posee entrada
    #S: Guarda los datos se configuración y cierra la ventana
    def guardar_y_cerrar():

        if messagebox.askquestion("ALTO", "¿Desea guardar la configuración dada?") == "yes":

            #Antes de salir se valida que el usuario digitara todo bien
            h = validar_timer(horas, 4, "Debe ser un número entre 0 y 4")
            m = validar_timer(minutos, 59, "Debe ser un número entre 0 y 59")
            s = validar_timer(segundos, 59, "Debe ser un número entre 0 y 59")
            topx_val = validar_topx()
            if h is None or m is None or s is None or topx_val is None:
                return  # no se cierra si hay error

            tipo_reloj = root_config.reloj_seleccionado.get()
            if h == 0 and m == 0 and s == 0 and tipo_reloj == 'timer':
                msg = 'Para el uso del timer al menos alguna de sus partes (horas, minutos, segundos) debe ser mayor a cero'
                messagebox.showinfo(message=msg, title="Aviso")
                return # no se cierra si hay error


            nombre_archivo_config = "sudoku2026configuración.json"
            configuracion_escogida = {
                "nivel": root_config.dificultad.get(), 
                "reloj": [tipo_reloj, h, m, s],
                "top x": topx_val, 
                "elementos": root_config.elementos_seleccionado.get()
            }

            # grabar datos
            f = open(nombre_archivo_config, "w")
            json.dump(configuracion_escogida, f)
            f.close()

            mensaje = "Se ha guardado la configuración"
            messagebox.showinfo(message=mensaje, title="Aviso")

            
        botomB.config(state="normal")
        # Se destruye la ventana para que efectivamente se cierre
        root_config.destroy()

    #Función que valida el timer
    #E: recibe el widget entry, el valor máximo que puede tener, y el mensaje respectivo de error
    #S: retorna el valor del contenido si es aceptado, sino, None
    def validar_timer(entry, valor_maximo, mensaje):
        try:
            contenido = int(entry.get())

        except ValueError:
            error_en_timer(entry, mensaje)
            contenido = -1

        if contenido > valor_maximo or contenido < 0:
            error_en_timer(entry, mensaje)
            return None
        
        return contenido
    
    #Función que valida el top x
    #E: obtiene el valor del entry que tiene el topx
    #S: retorna el valor del contenido si es aceptado, sino, None
    def validar_topx():
        try:
            contenido = int(entrada_topx.get())

        except ValueError: #En caso de que el usuario digitara un string
            contenido = -1

        if contenido > 10 or contenido < 0:
            entrada_topx.delete(0, tk.END)
            entrada_topx.insert(0, 0)
            messagebox.showinfo(message="Debe ser un número entre 0 y 10", title="Aviso")
            return None #Retorna None en caso de estar mal el topx
        
        return contenido #Retorna el contenido en caso de ser llamada desde guardar y cerrar
    
    #Función que valida las horas que insertó el usuario
    #E: recibe el entry de las horas
    #S: llama a la función que valida el timer y le manda el entry, el valor máximo que puede tener  y el mensaje que debe desplegar en caso de error
    def valida_horas(event):
        validar_timer(event.widget, 4, "Debe ser un número entre 0 y 4")

    #Función que valida los minutos que insertó el usuario
    #E: recibe el entry de los minutos
    #S: llama a la función que valida el timer y le manda el entry, el valor máximo que puede tener y el mensaje que debe desplegar en caso de error
    def valida_minutos(event):
        validar_timer(event.widget, 59, "Debe ser un número entre 0 y 59")

    #Función que valida los segundos que insertó el usuario
    #E: recibe el entry de los segundos
    #S: llama a la función que valida el timer y le manda el entry, el valor máximo que puede tener y el mensaje que debe desplegar en caso de error
    def valida_segundos(event):
        validar_timer(event.widget, 59, "Debe ser un número entre 0 y 59")

    #Función que solo llama a la función que valida el topx, esto para que también se pueda llamar desde guardar_cerrar
    #E: recibe el entry
    #S: llama a la función de valida topx
    def valida_topx(event):
        validar_topx() 
    
    #Función que despliega el error en caso de que el timer se haya dado en un mal rango
    #E: recibe el entry que está teniendo el error y el mensaje que debe mostrar
    #S: elimina el valor del entry y coloca 0, luego despliega el mensaje
    def error_en_timer(tipo, mensaje):

        tipo.delete(0, tk.END)
        tipo.insert(0, 0)
        messagebox.showinfo(message=mensaje, title="Aviso")

    #------------------------------------------------------
    #Se crea una ventana secundaria de configuración
    #------------------------------------------------------
    root_config = tk.Toplevel()
    root_config.title("Configuración")
    root_config.config(pady=50)

    root_config.transient(root)

    titulo_config = tk.Label(root_config, text="CONFIGURACIÓN", 
              font=('Segoe UI', 30, "bold"), 
              compound="left",
              fg="#0c3a95"
              )
    titulo_config.pack()

    #Se lee lo que hay en la cofiguración
    f = open(nombre_archivo_config, "r")
    configuracion_inicial = json.load(f)
    f.close()

    #Los frames que contienen  los distintos elementos de tkinter
    frame_a = tk.Frame(root_config, padx=10)
    frame_b = tk.Frame(root_config, padx=10)
    frame_c = tk.Frame(root_config, padx=10)
    frame_d = tk.Frame(root_config, padx=10)

    #Label para el texto del nivel
    label_a = tk.Label(master=frame_a, text="1. Nivel", font=('Segoe UI', 10, "bold"),  compound="left",  fg="#0c3a95", **ESTILO_OPCIONES_CONFIG)
    label_a.pack(pady=30, padx=10)

    #En esta parte se definen los radio buttons para el nivel
    root_config.dificultad = tk.StringVar(value=configuracion_inicial["nivel"])

    radio_facil = tk.Radiobutton(frame_a, text="Fácil", variable=root_config.dificultad, value='fácil', **ESTILO_OPCIONES_CONFIG)
    radio_facil.pack(pady=10, padx=5)

    radio_inter = tk.Radiobutton(frame_a, text="Intermedio", variable=root_config.dificultad, value='intermedio', **ESTILO_OPCIONES_CONFIG)
    radio_inter.pack(pady=10, padx=5)

    radio_dificil = tk.Radiobutton(frame_a, text="Difícil", variable=root_config.dificultad, value='difícil', **ESTILO_OPCIONES_CONFIG)
    radio_dificil.pack(pady=10, padx=5)

    #Label para el titulo del reloj
    label_b = tk.Label(master=frame_b, text="2. Reloj", font=('Segoe UI', 10, "bold"),  compound="left",  fg="#0c3a95", **ESTILO_OPCIONES_CONFIG)
    label_b.pack(pady=30, padx=10)

    #Los radio buttons para selecionar el reloj
    root_config.reloj_seleccionado = tk.StringVar(value=configuracion_inicial["reloj"][0])

    radio_cron = tk.Radiobutton(frame_b, text="Cronómetro", variable=root_config.reloj_seleccionado, value='cronometro', **ESTILO_OPCIONES_CONFIG, command=muestra_timer)
    radio_cron.pack(pady=10, padx=5)

    radio_timer = tk.Radiobutton(frame_b, text="Timer", variable=root_config.reloj_seleccionado, value='timer', **ESTILO_OPCIONES_CONFIG, command=muestra_timer)
    radio_timer.pack(pady=10, padx=5)

    radio_no_reloj = tk.Radiobutton(frame_b, text="No usar reloj", variable=root_config.reloj_seleccionado, value='ninguno', **ESTILO_OPCIONES_CONFIG, command=muestra_timer)
    radio_no_reloj.pack(pady=10, padx=5)

    #Frame auxiliar para el timer, este muestra el cuadro de las horas minutos y segundos
    frame_b_aux = tk.Frame(frame_b)

    lista_timer = ['Horas', 'Minutos', 'Segundos']

    for j,nombre_timer in enumerate(lista_timer): #Este cógdigo es para generar las tres columnas de horas, minutos y segundos de la tabla timer
        e = tk.Entry(frame_b_aux, justify="center", relief=tk.GROOVE)
        e.grid(row=1, column=j, sticky=tk.NSEW, ipady=5)
        e.insert(0,nombre_timer)
        e.config(fg="black",state='readonly')

    horas = tk.Entry(frame_b_aux,width=3, justify="center",  relief=tk.GROOVE) #El entry para las horas
    horas.bind("<FocusOut>", valida_horas) #Si el entry pierde el foco entonces valida los datos
    horas.bind("<Return>", valida_horas)

    minutos = tk.Entry(frame_b_aux,width=3, justify="center",  relief=tk.GROOVE) #El entry para los minutos
    minutos.bind("<FocusOut>", valida_minutos) #Si el entry pierde el foco entonces valida los datos
    minutos.bind("<Return>", valida_minutos)

    segundos = tk.Entry(frame_b_aux,width=3, justify="center",  relief=tk.GROOVE) #El entry para los segundos
    segundos.bind("<FocusOut>", valida_segundos) #Si el entry pierde el foco entonces valida los datos
    segundos.bind("<Return>", valida_segundos)

    #Para colocarlos con grid en columnas y filas
    horas.grid(row=2, column=0, sticky=tk.NSEW, ipady=5)
    minutos.grid(row=2, column=1, sticky=tk.NSEW, ipady=5)
    segundos.grid(row=2, column=2, sticky=tk.NSEW, ipady=5)

    #Se les inseertan los datos iniciales para que no queden sin valor predeterminado
    horas.insert(0,configuracion_inicial["reloj"][1])
    minutos.insert(0,configuracion_inicial["reloj"][2])
    segundos.insert(0,configuracion_inicial["reloj"][3])

    #Se les cambia el estado a readonlyu al inicio para que el usuario no lo pueda modificar hasta que escoga el reloj del timer
    horas.config(fg="black", state='readonly')
    minutos.config(fg="black", state='readonly')
    segundos.config(fg="black", state='readonly')

    frame_b_aux.pack()

    #El label para el texto del top x
    label_c = tk.Label(master=frame_c, text="3. Cantidad de jugadas desplegadas en el TOP X:", font=('Segoe UI', 10, "bold"),  compound="left",  fg="#0c3a95", **ESTILO_OPCIONES_CONFIG)
    label_c.pack(pady=30, padx=10)

    entrada_topx = tk.Entry(frame_c, width=80)
    entrada_topx.insert(0, configuracion_inicial["top x"]) #Valor por defecto se inserta al inicio
    entrada_topx.bind("<Return>", valida_topx) #Si el usuario da entener se validan los datos
    entrada_topx.bind("<FocusOut>", valida_topx) #Si el entry pierde el foco se validan los datos
    
    entrada_topx.pack()

    #El label del titulo del panel de elementos
    label_d = tk.Label(master=frame_d, text="4. Panel de elementos para llenar la cuadrícula:", font=('Segoe UI', 10, "bold"),  compound="left",  fg="#0c3a95", **ESTILO_OPCIONES_CONFIG)
    label_d.pack(pady=30, padx=10)

    #Se preparan los entry con el valor de elemento seleccionado y se selecciona el que tiene por valor 'numeros'
    root_config.elementos_seleccionado = tk.StringVar(value=configuracion_inicial["elementos"])

    frame_d_aux = tk.Frame(frame_d)

    radio_num = tk.Radiobutton(frame_d_aux, text="Números", variable=root_config.elementos_seleccionado, value='numeros')
    radio_num.grid(row=1, column=1)

    #Esta parte es para crear los labels de los números, en cascada
    fila_num = 2
    for i in range(1,10):
        label_num = tk.Label(frame_d_aux, text=i)
        label_num.grid(row=fila_num, column=1)
        fila_num += 1

    radio_letra = tk.Radiobutton(frame_d_aux, text="Letras", variable=root_config.elementos_seleccionado, value='letras')
    radio_letra.grid(row=1, column=2)

    #Esta parte es para crear las letras en cascada
    fila_letra = 2
    lista_letras = ['A','B','C','D','E','F','G','H','I']
    for i in lista_letras:
        label_num = tk.Label(frame_d_aux, text=i)
        label_num.grid(row=fila_letra, column=2)
        fila_letra += 1

    frame_d_aux.pack()

    #Se usa pack para insertar los frames ya hechos con todos los valores
    frame_a.pack()
    frame_b.pack()
    frame_c.pack()
    frame_d.pack()

    #Si el usuario le da a la equis de la ventana primero llamará a la función de guardar_cerrar
    root_config.protocol("WM_DELETE_WINDOW", guardar_y_cerrar)


#------------------------------------------------------
#Función que abre la ventana para jugar
#------------------------------------------------------

#Función que emerge una ventana para la configuración del juego
#E: el usuario elige el nivel, los elementos a usar, el tipo de reloj (cronómetro, timer, ninguno), y el TOP x
#S: al finalizar y cerrar la ventana crea al archivo json para guardar los datos que el usuario eligió
def abrir_ventana_jugar():

    botonA.config(state="disabled")

    #Variable para saber si el usuario borro el juego pero desea la misma partida que tenía
    global juego_borrado_numero_partida
    global juego_cargado
    global nombre_jugador_cargado
    global juego_cargado_nivel
    global juego_cargado_elementos

    #-------------------------------------------------------------------------------------
    #Código para traer los datos del json que contiene la configuración que dió el usuario
    #--------------------------------------------------------------------------------------
    
    # leer datos
    f = open(nombre_archivo_config, "r")
    configuracion = json.load(f)
    f.close()


    #-------------------------------------------------------------------------------------
    #Funciones aparte para la ventana de jugar
    #--------------------------------------------------------------------------------------

    def ir_menu_principal():
        if messagebox.askquestion("ALTO", "¿Desea salir y perder el progreso?") == "yes":
            global juego_borrado_numero_partida
            global juego_cargado
            global nombre_jugador_cargado
            global juego_cargado_nivel
            global juego_cargado_elementos

            juego_borrado_numero_partida = " "
            juego_cargado = False
            nombre_jugador_cargado = " "
            juego_cargado_nivel = " "
            juego_cargado_elementos = " "

            #Se vuelve a habilitar el botón
            botonA.config(state="normal")

            root_juego.destroy()



    #Función que se encarga de cerrar la ventana del juego y la vuelve a abrir
    #E:
    #S: cambia los valores de algunas variables
    def cerrar_ventana_juego():
        global juego_borrado_numero_partida
        global juego_cargado
        global nombre_jugador_cargado
        global juego_cargado_nivel
        global juego_cargado_elementos

        juego_borrado_numero_partida = " "
        juego_cargado = False
        nombre_jugador_cargado = " "
        juego_cargado_nivel = " "
        juego_cargado_elementos = " "

        root_juego.destroy()
        abrir_ventana_jugar()


    #Función que crea la matriz inicial del juego
    #E: recibe un valor booleando si debe buscar una matriz y cargarla o solamente la de las partidas
    #S: crea la matriz y la depsliega
    def crear_matriz(matriz_dada):

        frame_matriz = tk.Frame(frame_principal)

        #Se crea la matriz vacía
        root_juego.matriz_sudoku_vacia = [] 

        for i in range(9):

            fila = []

            for j in range(9):
                fila.append(None)

            root_juego.matriz_sudoku_vacia.append(fila)


        #Se crean cada cuadrante
        matriz_cuadrante_vacio = [] 

        for i in range(3):

            fila = []

            for j in range(3):
                fila.append(None)

            matriz_cuadrante_vacio.append(fila)

        for filaC in range(3):
            for colC in range(3):

                cuadrante = tk.Frame(frame_matriz, bd=1, relief="solid")
                cuadrante.grid(row=filaC, column=colC)
                matriz_cuadrante_vacio[filaC][colC] = cuadrante


        for cuad_f in range(3):        
            for cuad_c in range(3):   

                cuadrante_actual = matriz_cuadrante_vacio[cuad_f][cuad_c]

                for f_interna in range(3):
                    for c_interna in range(3):

                        fila_real = (cuad_f * 3) + f_interna
                        columna_real = (cuad_c * 3) + c_interna

                        celda = tk.Entry(cuadrante_actual, width=3, font=FUENTE_UNIVERSAL, justify="center")
                        celda.grid(row=f_interna, column=c_interna, ipady=5) 
                        celda.fila = fila_real
                        celda.columna = columna_real

                        root_juego.matriz_sudoku_vacia[fila_real][columna_real] = celda

                        coordenada_texto = f"{fila_real},{columna_real}"

                        if coordenada_texto in partida_actual:

                            valor_pista = partida_actual[coordenada_texto]

                            if root_juego.elementos == 'letras':
                                valor_pista = cambia_a_letra(valor_pista)

                            celda.insert(0, str(valor_pista))
                            celda.config(fg="black", state="disabled", bg="red")
                            celda.bind("<ButtonPress-1>", jugada_invalida)

                        else:
                            celda.bind("<ButtonPress-1>", digitar_numero)
                            celda.config(fg="black", state="readonly", cursor="hand2")

        frame_matriz.grid(row=1, column=1)

    #Funcion que formatea los segundos y los vuelve a horas minutos y segundos
    #E: recibe los segundos totales
    #S: devuelve los segundos ya formateados
    def formatear_segundos(segundos_totales):

        horas = segundos_totales // 3600
        segundos_restantes = segundos_totales % 3600
        minutos = segundos_restantes // 60
        segundos = segundos_restantes % 60

        # El :02d le dice a Python: "Muestra este número con 2 dígitos, rellenando con ceros a la izquierda si falta"
        tiempo_formateado = f"{horas:02d}:{minutos:02d}:{segundos:02d}"
        return tiempo_formateado
    
    #Función que recibe horas, minutos y segundos y los convierte a segundos totales
    #E: recibe las horas, minutos y segundos (pueden ser enteros o strings numéricos)
    #S: devuelve un entero con los segundos totales
    def calcular_segundos_totales(horas, minutos, segundos):

        #Se convierten a enteros
        h = int(horas)
        m = int(minutos)
        s = int(segundos)
        segundos_totales = (h * 3600) + (m * 60) + s
        
        return segundos_totales

    #Función que calcula los segundos durados según el timer, en caso de guardar la partida usnando el timer
    #E: no posee entradas
    #S: retorna los segundos que duro el usuario
    def obtener_duracion_timer():
        tiempo_inicial = calcular_segundos_totales(root_juego.horas_reloj, root_juego.minutos_reloj, root_juego.segundos_reloj)

        tiempo_restante = root_juego.segundos_restantes

        segundos_durados = tiempo_inicial - tiempo_restante

        #Código por seguridad
        if segundos_durados < 0:
            segundos_durados = 0

        return segundos_durados

    #Función que genera el PDF con el informe del TopX
    #E: trae del archivo json de bitacora jugadas las mejores
    #S: abre el archivo en el navegador
    def generar_topx_pdf():

        documento = SimpleDocTemplate('Informe_Top_X.pdf')  #Se crea el archivo PDF, con la función de reportla
        flowables = []
        sample_style_sheet = getSampleStyleSheet()
      
        titulo = Paragraph("Informe del Top X", sample_style_sheet['Heading1']) #Se crea el título del PDF, y se le da el estilo de un encabezado #1
        flowables.append(titulo) #Se inserta dentro de los flowables
      
        subtitulo =  [["", 'Jugador', 'Tiempo', 'Jugado el']] #Se crea el subtitulo del PDF
        tabla_subtitulo = Table(subtitulo, colWidths=[130, 80, 80, 80], hAlign='LEFT')     
        flowables.append(tabla_subtitulo)  #Se inserta dentro de los flowables


        #Código para leer los datos del json bitacora jugadas que contiene las partidas terminadas
        f = open(nombre_archivo_bitácora_jugada, "r")
        bitacora_jugada = json.load(f)
        f.close()

        # diccionario para agrupar los tiempos por dificultad
        tiempos_por_dificultad = {
            "difícil": [],
            "intermedio": [],
            "fácil": []
        }

        # se recorrer el diccionario para sacar los tiempos y la información de la jugada
        for jugador in bitacora_jugada:
            lista_partidas = bitacora_jugada[jugador]

            for partida in lista_partidas: #Se recorre la lista de partidas de cada jugador
                dificultad = partida["dificultad"]
                tiempo = partida["tiempo"]
                fecha_hora = partida["fecha_hora"]

                #Se crea un diccionario con los datos necesarios
                dic_tiempo = {"jugador": jugador, "tiempo": tiempo, "fecha_hora": fecha_hora}

                #Se agrega el diccionario a la lista correspondiente
                tiempos_por_dificultad[dificultad].append(dic_tiempo)

        #Se crea el diccionario de mejores tiempos para guardar los mejores de cada dificultad segun el Top x
        mejores_tiempos = {
            "difícil": [],
            "intermedio": [],
            "fácil": []
        }

        #Se ordena en mejor tiempo
        for dificultad in tiempos_por_dificultad:
            lista = tiempos_por_dificultad[dificultad]
            n = len(lista)

            #Para ordenar del menor al mayor
            for i in range(n):
                for j in range(0, n - i - 1):
                    if lista[j]["tiempo"] > lista[j + 1]["tiempo"]:
                        # Intercambio de posiciones
                        temporal = lista[j]
                        lista[j] = lista[j + 1]
                        lista[j + 1] = temporal

            #Se calcula el máximo del topx
            if root_juego.topx == 0:
                    limite = len(lista)
            else:
                limite = root_juego.topx
                
                if len(lista) < limite:
                    limite = len(lista)

            for k in range(limite):
                mejores_tiempos[dificultad].append(lista[k])

        #Esta parte es para generar ya el informe y la información que tendrá dentro
        for i, dificultad in enumerate(mejores_tiempos):

            titulo2 = Paragraph("Nivel "+dificultad+":") #Se crea el título del PDF, y se le da el estilo de un encabezado #1
            flowables.append(titulo2) #Se inserta dentro de los flowables

            top = 1 #El top para los puestos de tiempo
            for jugador_dic in mejores_tiempos[dificultad]:

                jugador = jugador_dic["jugador"]
                tiempo = jugador_dic["tiempo"]
                fecha_hora = jugador_dic["fecha_hora"]
                tiempo_formateado = formatear_segundos(tiempo)

                jugador = str(top) + "- " + jugador

                #Se llena la informacion del horario
                jugador_top =  [["",jugador,tiempo_formateado,fecha_hora]]
                tabla_estadistica = Table(jugador_top, colWidths=[130, 80, 80, 80], hAlign='LEFT')     
                flowables.append(tabla_estadistica)
                
                top += 1 #Se incrementa el top al final
      
        documento.build(flowables)
        try:
          ruta_absoluta = os.path.abspath("Informe_Top_X.pdf")
          os.startfile(ruta_absoluta) #Línea para que el archivo se abra en el buscador
        except:
          return

    #Esta función entra cada vez que el usuario inserta un elemento, es para saber si terminó el juego
    #E: np recibe nada
    #S: si es la jugada final, llama a guardar la bitácora, es decir guardar la jugada
    def valida_ultima_jugada():
        lista = []
        for fila in root_juego.matriz_sudoku_vacia: #Se crea una lista que tiene todos los valores de la matriz
            for col in fila:
                
                valor = col.get()
                lista.append(valor)
        
        if '' not in lista: #Si todos los espacios están completados, lanza el mensaje de felicitación y guarda la jugada
            pausar_reloj() #Se pausa el reloj
            mensaje = "¡EXCELENTE! JUEGO COMPLETADO"
            messagebox.showinfo(message=mensaje, title="Aviso")

            guardar_bitacora_jugada() #Se guarda la jugada

    #Función que guarda la partida en la bitácora
    #E: no recibe parámetros
    #S: graba la jugada en el archivo json de bitácora
    def guardar_bitacora_jugada():

        if root_juego.reloj != 'ninguno':
            ahora = datetime.now() #obtiene el tiempo actual
            ahora = ahora.strftime("%Y%m%dT%H:%M:%S") #lo transforma a la forma estandar

            jugador_actual = entry_nombre.get() #obtiene el nombre que el usuario digitó

            #Se traen los datos del json para buscar al jugador entre ellos
            f = open(nombre_archivo_bitácora_jugada, "r")
            bitacora_partidas = json.load(f)
            f.close()

            #En caso de sel cronómetro se calculan los segundos totales sin restar
            if root_juego.reloj == 'cronometro':
                tiempo_segundos = calcular_segundos_totales(root_juego.horas_entry.get(), root_juego.minutos_entry.get(), root_juego.segundos_entry.get())

            #En el caso del timer, se calcula el tiempo basandose en el que el usuario había dado al inicio y restando
            elif root_juego.reloj == 'timer':
                tiempo_segundos = obtener_duracion_timer()

            #Si no hay reloj los segundos son nulos
            else:
                tiempo_segundos = None

            #Se crea un diccionario para la partida actual
            dic_partida_actual = {
                'dificultad': root_juego.nivel,
                'tiempo': tiempo_segundos,
                'fecha_hora': ahora
            }

            if jugador_actual not in bitacora_partidas: #Si el jugador no tiene una partida ya, se crea y se le pone la partida en la lista
                lista_niveles = [dic_partida_actual]
                bitacora_partidas[jugador_actual] = lista_niveles

            else: #En caso de que el usuario si este, se inserta la jugada en la lista de partidas
                lista_niveles_actuales = bitacora_partidas[jugador_actual]
                lista_niveles_actuales.append(dic_partida_actual)
                bitacora_partidas[jugador_actual] = lista_niveles_actuales

            #Se graban los datos del archivo de configuración por default
            f = open(nombre_archivo_bitácora_jugada, "w")
            json.dump(bitacora_partidas, f)
            f.close()

        cerrar_ventana_juego()
            
    #Función que cambia los digitos de la matriz por las letras correpondientes si el usuario lo indicó
    #E: la entrada es el digito a cambiar
    #S: la salida es el la letra
    def cambia_a_letra(digito):
        lista_letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'] #Se crea una lista con las letras
        posicion = digito - 1 #Se le resta uno al número ya que empiezan en 1
        valor = lista_letras[posicion]
        return valor
    
    #Función que cambia de letra a numerp
    #E: el caracter
    #S: el numero requerido
    def cambia_a_numero(caracter):
        lista_letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I'] #Se crea una lista con las letras

        for i,c in enumerate(lista_letras):
            if c == caracter:
                return i+1

    #Función que valida el timer
    #E: recibe el widget entry, el valor máximo que puede tener, y el mensaje respectivo de error
    #S: retorna el valor del contenido si es aceptado, sino, None
    def validar_timer(entry, valor_maximo, mensaje):
        try:
            contenido = int(entry.get())

        except ValueError:
            error_en_timer(entry, mensaje)
            contenido = -1

        if contenido > valor_maximo or contenido < 0:
            error_en_timer(entry, mensaje)
            return None
        
        return contenido
        
    #Función que valida las horas que insertó el usuario
    #E: recibe el entry de las horas
    #S: llama a la función que valida el timer y le manda el entry, el valor máximo que puede tener  y el mensaje que debe desplegar en caso de error
    def valida_horas(event):
        validar_timer(event.widget, 4, "Debe ser un número entre 0 y 4")

    #Función que valida los minutos que insertó el usuario
    #E: recibe el entry de los minutos
    #S: llama a la función que valida el timer y le manda el entry, el valor máximo que puede tener y el mensaje que debe desplegar en caso de error
    def valida_minutos(event):
        validar_timer(event.widget, 59, "Debe ser un número entre 0 y 59")

    #Función que valida los segundos que insertó el usuario
    #E: recibe el entry de los segundos
    #S: llama a la función que valida el timer y le manda el entry, el valor máximo que puede tener y el mensaje que debe desplegar en caso de error
    def valida_segundos(event):
        validar_timer(event.widget, 59, "Debe ser un número entre 0 y 59")
    
    #Función que despliega el error en caso de que el timer se haya dado en un mal rango
    #E: recibe el entry que está teniendo el error y el mensaje que debe mostrar
    #S: elimina el valor del entry y coloca 0, luego despliega el mensaje
    def error_en_timer(tipo, mensaje):

        tipo.delete(0, tk.END)
        tipo.insert(0, 0)
        messagebox.showinfo(message=mensaje, title="Aviso")


    #Actualiza los entry del reloj cuando va sumando el tiempo
    #E: reecibe el entry a cambiar y el nuevo valor
    #S: cambia los valores
    def actualizar_entrada_readonly(input_entry, nuevo_texto):
        input_entry.config(state='normal') #Cambia el estado del entry para poder modificarlo
        input_entry.delete(0, tk.END) #Elimina el valor que tenía antes
        input_entry.insert(0, nuevo_texto) #Le inserta el nuevo valor
        input_entry.config(state='readonly') #Lo devuelve al estado readonly para que no se pueda modificar

    #Función que va a calcular el tiempo transcurrido para el cronómetro
    #E: no recibe parámetros
    #S: retorna lo que venga de la llamada a la función que formatea los segundos
    def obtener_tiempo_transcurrido_formateado():
        segundos_transcurridos= (datetime.now() - root_juego.hora_inicio).total_seconds()
        return segundos_a_segundos_minutos_y_horas(int(segundos_transcurridos))
    
    #Función que formatea los segundos
    #E: recibe los segundos
    #S: retorna un string con las horas minutos y segundos con el formato de relleno 00
    def segundos_a_segundos_minutos_y_horas(segundos):
        horas = int(segundos / 60 / 60)
        segundos -= horas*60*60
        minutos = int(segundos/60)
        segundos -= minutos*60
        return f"{horas:02d}", f"{minutos:02d}", f"{segundos:02d}"

    #Función que se refresca cada milisegundo para contar el tiempo
    #E: no recibe parámetros
    #S: refresca el reloj
    def refrescar_tiempo_transcurrido():
        if getattr(root_juego, 'juego_iniciado', False) and not getattr(root_juego, 'reloj_pausado', False):
            h, m, s = obtener_tiempo_transcurrido_formateado()
            actualizar_entrada_readonly(root_juego.horas_entry, h)
            actualizar_entrada_readonly(root_juego.minutos_entry, m)
            actualizar_entrada_readonly(root_juego.segundos_entry, s)

            root_juego.after_reloj_id = root_juego.after(INTERVALO_REFRESCO, refrescar_tiempo_transcurrido)

    #Función que prerara los segundos totales a ir restando
    #E: no recibe parámetros
    #S: calcula los segundos totales y llama al modificador de timer
    def preparar_timer():
        try:
            #Se convierte el tiempo dado por el usuario a entero
            hours = int(root_juego.horas_reloj)
            minutes = int(root_juego.minutos_reloj)
            seconds = int(root_juego.segundos_reloj)

            #Calcula los segundos totales para ir contando hacia atras
            root_juego.segundos_restantes = (hours * 3600) + (minutes * 60) + seconds

            modificar_timer()

        except ValueError:
            pass
    
    #Funció que va modificando el timer
    #E: no recibe parámetros
    #S: si el reloj está en pausa retorna
    def modificar_timer():
        if getattr(root_juego, 'reloj_pausado', False):
            return
    
        #Modo de conteo regresivo
        if root_juego.segundos_restantes > 0 and not getattr(root_juego, 'modo_cronometro_extra', False):
            root_juego.segundos_restantes -= 1 #Va restando

        #Se está usando el tiempo extra
        elif getattr(root_juego, 'modo_cronometro_extra', False):
            root_juego.segundos_restantes += 1 #Va sumando

        #Se llegó a cero en el timer
        else:
            #Se pone marcador en cero visualmente
            actualizar_entrada_readonly(root_juego.horas_entry, "00")
            actualizar_entrada_readonly(root_juego.minutos_entry, "00")
            actualizar_entrada_readonly(root_juego.segundos_entry, "00")

            #Se pregunta si se desea seguir jugando
            if messagebox.askquestion("ALTO", "Tiempo expirado, ¿Desea continuar el mismo juego?") == "yes":
                root_juego.modo_cronometro_extra = True
                root_juego.reloj = 'cronometro'
                titulo_reloj.config(text='Cronómetro')

                horas = int(root_juego.horas_reloj)
                minutos = int(root_juego.minutos_reloj)
                segundos = int(root_juego.segundos_reloj)
                root_juego.segundos_restantes = (horas * 3600) + (minutos * 60) + segundos

                # Creamos la hora de inicio artificial para que la función de PAUSA no se rompa
                root_juego.hora_inicio = datetime.now() - timedelta(seconds=root_juego.segundos_restantes)

                root_juego.after_reloj_id = root_juego.after(1000, modificar_timer)
                return 

            else:
                cerrar_ventana_juego()
                return

        h_str, m_str, s_str = segundos_a_segundos_minutos_y_horas(root_juego.segundos_restantes)

        #Se actualizan los segundos
        actualizar_entrada_readonly(root_juego.horas_entry, h_str)
        actualizar_entrada_readonly(root_juego.minutos_entry, m_str)
        actualizar_entrada_readonly(root_juego.segundos_entry, s_str)
        root_juego.after_reloj_id = root_juego.after(1000, modificar_timer)

    #Función que pausa el reloj
    #E: no recibe parámetros
    #S: retorna si el juego no ha inciado o estaba pausado
    def pausar_reloj():
        #si el juego no ha iniciado no hace nada, si esta pausado tampoco
        if not getattr(root_juego, 'juego_iniciado', False) or getattr(root_juego, 'reloj_pausado', False):
            return

        root_juego.reloj_pausado = True #Se marca como pausado

        #Se cancela el after
        if root_juego.after_reloj_id:
            root_juego.after_cancel(root_juego.after_reloj_id)
            root_juego.after_reloj_id = None

        if root_juego.reloj == 'cronometro':
            root_juego.segundos_transcurridos = int((datetime.now() - root_juego.hora_inicio).total_seconds())

    #Función para reanudar el reloj
    #E: no recibe parámetros
    #S: retorna si el juego no ha iniciado
    def reanudar_reloj():
        #si el juego no ha iniciado no hace nada, si no estaba pausado tampoco
        if not getattr(root_juego, 'juego_iniciado', False) or not getattr(root_juego, 'reloj_pausado', False):
            return

        root_juego.reloj_pausado = False #Se quita el estado de pausado

        if root_juego.reloj == 'cronometro': #Si era el cronómetro el vuelve a prender
            # Reajustamos la hora de inicio con el tiempo que se quedó congelado en la pausa
            root_juego.hora_inicio = datetime.now() - timedelta(seconds=root_juego.segundos_transcurridos)
            refrescar_tiempo_transcurrido()

        elif root_juego.reloj == 'timer': #Si era el timer se llama a modificar
            modificar_timer()

    #Valida que la jugada este bien colocada, que no interrumpa las demás casillas ni las reglas
    #E: el entry que se está tratando de cambiar y el valor a insertar
    #S: el mensaje respectivo o None si todo salió bien
    def valida_jugada(entry_actual, valor):

        fila = entry_actual.fila #Se obtiene la fila donde está el entry
        columna = entry_actual.columna #Se obtiene la columna donde está el entry

        #Se verifica la fila
        for c in range(9):
            if c != columna: #Cada columna sin verificar en la que se inserta el número
                celda_vecina = root_juego.matriz_sudoku_vacia[fila][c]
                if celda_vecina.get() == valor:
                    mensaje = f"¡Error! El {valor} ya está en la fila {fila}"
                    return mensaje

        #Se verifica la columna
        for f in range(9):
            if f != fila:  #Cada fila sin verificar en la que se inserta el número
                celda_vecina = root_juego.matriz_sudoku_vacia[f][columna]
                if celda_vecina.get() == valor:
                    mensaje = f"¡Error! El {valor} ya está en la columna {columna}"
                    return mensaje

        inicio_f = (fila // 3) * 3
        inicio_c = (columna // 3) * 3

        for f in range(inicio_f, inicio_f + 3):
            for c in range(inicio_c, inicio_c + 3):

                if f != fila or c != columna:
                    celda_vecina = root_juego.matriz_sudoku_vacia[f][c]
                    if celda_vecina.get() == valor:
                        mensaje = f"¡Error! El {valor} ya está en este cuadrante"
                        return mensaje

        #Retornar None en caso de que todo haya salido bien
        tupla_jugada = (fila,columna,valor)
        root_juego.jugadas_realizadas.append(tupla_jugada)
        return 

    #Valida el nombre del jugador, que no exceda el límite
    #E: recibe el nombre del jugador, un string
    #S: si excede despliega el mensaje respectivo
    def valida_nombre(value):
        if len(entry_nombre.get()) > 30 and len(entry_nombre.get()) < 1:
            msg = "Debe ser un string de menos de 30"
            entry_nombre.delete(0, tk.END)
            messagebox.showinfo(message=msg, title="Aviso")
        #elif entry_nombre.get() != "" and entry_nombre.get() != "String de 1 a 30 caracteres..":
         #   msg = "Se guardó el nombre"
         #   messagebox.showinfo(message=msg, title="Correcto")
        
        if entry_nombre.get() == "":
            entry_nombre.insert(0, "String de 1 a 30 caracteres..")
    
    #Función que quita el placeholder de un entry
    #E: recibe value
    #S: si excede despliega el mensaje respectivo
    def quita_texto(value):
        if entry_nombre.get() == "String de 1 a 30 caracteres...":
            entry_nombre.delete(0, tk.END)

    #Función para seleccionar el elemento que se desea insertar en las casillas
    #E: recibe el entry es decir el elemento que tiene el elemento a insertar
    #S: retorna en caso de que el boton actual sea el mismo al activo
    def seleccionar_boton_elemento(event):
        boton_actual = event.widget

        if root_juego.boton_activo is not None: #Si había un boton ya activo se cambia de color al predeterminado
            root_juego.boton_activo.config(bg="#ffffff", fg="#000000")

        if root_juego.boton_activo == boton_actual: #Si el botón actual es el mismo que el activo se retorna
            root_juego.boton_activo = None 
            return

        #Si el boton erá diferente entonces lo selecciona
        boton_actual.config(bg="#88c0d0", fg="#2e3440")
        root_juego.boton_activo = boton_actual

    #Función que indica que entry está teniendo una jugada invalida, que va fuera de las reglas
    #E: el entry
    #S: despliega el mensaje respectivo
    def jugada_invalida(event):
        casilla = event.widget
        casilla.config(state="normal")
        casilla.config(bg="#e55699")

        msg = "Esta casilla ya tiene un elemento fijo"
        messagebox.showinfo(message=msg, title="Error")

        casilla.config(bg="SystemButtonFace") #Le devuleve el color original del sistema
        casilla.config(state="disabled")

    #Función para insertar un elemento en la celda seleccionada
    #E: el entry a insertar
    #S: despliega un mensaje respectivo de error o inserta el elemento en el entry
    def digitar_numero(event):
        if root_juego.juego_iniciado: #verifica que el juego haya inciado
            if root_juego.boton_activo != None: #verifica que haya un elemento seleeccioando

                boton_actual = event.widget
                estado = boton_actual.cget("state") #obtiene el estado del entry a modificar
                if estado != "disabled": #Si es diferente a deshabilitado no tiene ningún elemento insertado
                    valor_actual = root_juego.boton_activo.cget("text")

                    validador = valida_jugada(boton_actual, valor_actual) #valida la jugada según las reglas

                    if validador == None:

                        boton_actual.config(state="normal")
                        boton_actual.insert(0,valor_actual )
                        boton_actual.config(state="disabled")
                        valida_ultima_jugada()

                    else:
                        boton_actual.config(state="normal", bg="#e55699")
                        msg = validador
                        messagebox.showinfo(message=msg, title="Error")
                        boton_actual.config(state="readonly", bg="SystemButtonFace")

                #Si la casilla ya tiene un dígito
                else:
                    jugada_invalida(event)
            else:
                msg = "Debe seleccionar un elemento para insertar"
                messagebox.showinfo(message=msg, title="Error")
        else:
            msg = "Error: primero debe iniciar el juego"
            messagebox.showinfo(message=msg, title="Error")

    #Crea el reloj al inicio del juego si se necesita
    #E: no recibe parámetros
    #S: crea el reloj
    def crea_reloj(cargado):
        root_juego.frame_reloj = tk.Frame(frame_reloj_principal)

        lista_timer = ['Horas', 'Minutos', 'Segundos']

        for j,nombre_timer in enumerate(lista_timer): #Este cógdigo es para generar las tres columnas de horas, minutos y segundos de la tabla timer
            e = tk.Entry(root_juego.frame_reloj, justify="center", relief=tk.GROOVE)
            e.grid(row=1, column=j, sticky=tk.NSEW, ipady=5)
            e.insert(0,nombre_timer)
            e.config(fg="black",state='readonly')


        root_juego.horas_entry = tk.Entry(root_juego.frame_reloj, width=3, justify="center", relief=tk.GROOVE)
        root_juego.horas_entry.bind("<FocusOut>", valida_horas)

        root_juego.minutos_entry = tk.Entry(root_juego.frame_reloj, width=3, justify="center", relief=tk.GROOVE)
        root_juego.minutos_entry.bind("<FocusOut>", valida_minutos)

        root_juego.segundos_entry = tk.Entry(root_juego.frame_reloj, width=3, justify="center", relief=tk.GROOVE)
        root_juego.segundos_entry.bind("<FocusOut>", valida_segundos)

        # Los posicionas igual usando el grid
        root_juego.horas_entry.grid(row=2, column=0, sticky=tk.NSEW, ipady=5)
        root_juego.minutos_entry.grid(row=2, column=1, sticky=tk.NSEW, ipady=5)
        root_juego.segundos_entry.grid(row=2, column=2, sticky=tk.NSEW, ipady=5)

        # Insertar valores iniciales
        root_juego.horas_entry.insert(0, root_juego.horas_reloj)
        root_juego.minutos_entry.insert(0, root_juego.minutos_reloj)
        root_juego.segundos_entry.insert(0, root_juego.segundos_reloj)

        if root_juego.reloj == 'cronometro':
            root_juego.horas_entry.config(fg="black", state='readonly')
            root_juego.minutos_entry.config(fg="black", state='readonly')
            root_juego.segundos_entry.config(fg="black", state='readonly')

        root_juego.frame_reloj.pack(pady=10)

    #Función que valida que el juego haya iniciado
    #E: no recibe parámetros
    #S: retorna True si esta inciado, sino retorna None
    def valida_inicio_juego():
        if root_juego.juego_iniciado:
            return True

        else:
            msg = "NO SE HA INICIADO EL JUEGO"
            messagebox.showinfo(message=msg, title="Error")
            return
        
    #Función que identifica si un nombre ya está en el topx
    #E: recibe el nombre, un string
    #S: retorna True si está, False en otro caso
    def busca_jugador(nombre):

        f = open(nombre_archivo_bitácora_jugada, "r")
        bitacora_jugadas = json.load(f)
        f.close()

        if nombre in bitacora_jugadas:
            return True
        
        return False
    #----------------------------------------------------------------------------------------------------------------
    #Funciones para los botones de opciones
    #-----------------------------------------------------------------------------------------------------------------

    #Función que termina el juego, lo devuelve a jugar de nuevo con una nueva partida
    #E: no recibe parámetros
    #S: si el juego no ha iniciado despliega el mensaje respectivo, sino cierra la ventana y crea otra
    def terminar_juego():
        if valida_inicio_juego():
            if messagebox.askquestion("Terminar Juego", "¿Está seguro de terminar el juego?") == "yes":
                cerrar_ventana_juego()
                

    #Función que borra el juego, lo devuelve a jugar pero con al misma partida
    #E: no recibe parámetros
    #S: si el juego no ha iniciado despliega el mensaje respectivo, sino cierra la ventana y crea otra
    def borrar_juego():

        if valida_inicio_juego():
            if messagebox.askquestion("Borrar Juego", "¿Está seguro de borrar el juego?") == "yes":
                global juego_borrado_numero_partida 
                juego_borrado_numero_partida = root_juego.numero_partida #Guarda el número de partida que tenía el usuario
                root_juego.destroy()
                abrir_ventana_jugar()

    #Función para rehacer una jugada
    #E: no recibe parámetros
    #S:
    def rehacer_jugada():

        if valida_inicio_juego():
            if len(root_juego.jugadas_eliminadas) != 0: #Valida que hayan jugadas para rehacer
                tupla_eliminada = root_juego.jugadas_eliminadas.pop() #Saca la jugada de las jugadas eliminadas y obtiene su valor

                fila = tupla_eliminada[0]
                columna = tupla_eliminada[1]
                valor = tupla_eliminada[2]

                celda_rehacer = root_juego.matriz_sudoku_vacia[fila][columna] #Se obtiene el entry donde estaba la jugada

                if celda_rehacer.cget("state") != "disabled" : #Se valida que no haya un elemento ya insertado

                    celda_rehacer.config(state='normal')
                    celda_rehacer.insert(0, valor)
                    celda_rehacer.config(state='disabled')
                    #se inserta la jugada que se va a rehacer a la pila de jugadas realizadas
                    root_juego.jugadas_realizadas.append(tupla_eliminada)
            else:
                msg = "NO HAY JUGADAS PARA REHACER"
                messagebox.showinfo(message=msg, title="Error")

    #Función para deshacer una jugada
    #E: no recibe parámetros
    #S: en caso de no haber jugadas despliega el mensaje respectivo
    def deshacer_jugada():

        if valida_inicio_juego():
            if len(root_juego.jugadas_realizadas) != 0: #Valida que hayan jugadas para deshacer
                tupla_jugada = root_juego.jugadas_realizadas.pop() #Saca la jugada de las jugadas realizadas y obtiene su valor

                #se inserta la jugada que se va a deshacer a la pila de jugadas eliminadas
                root_juego.jugadas_eliminadas.append(tupla_jugada)

                fila = tupla_jugada[0]
                columna = tupla_jugada[1]

                celda_deshacer = root_juego.matriz_sudoku_vacia[fila][columna] #Se obtiene el entry donde estaba la jugada
                celda_deshacer.config(state='normal')
                celda_deshacer.delete(0, tk.END) #Se elimina lo que había
                celda_deshacer.config(state='readonly')

            else:
                msg = "NO HAY JUGADAS PARA DESHACER"
                messagebox.showinfo(message=msg, title="Error")
            
    #Función para iniciar el juego
    #E: no recibe parámetros
    #S: retorna si el nombre existe y el usuario no desea usarlo
    def iniciar_juego():

        if root_juego.reloj == 'timer':
            
            #Antes de salir se valida que el usuario digitara todo bien
            h = validar_timer(root_juego.horas_entry, 4, "Debe ser un número entre 0 y 4")
            m = validar_timer(root_juego.minutos_entry, 59, "Debe ser un número entre 0 y 59")
            s = validar_timer(root_juego.segundos_entry, 59, "Debe ser un número entre 0 y 59")

            if h is None or m is None or s is None:
                return  # no inicia el juego

            if h == 0 and m == 0 and s == 0:
                msg = 'Para el uso del timer al menos alguna de sus partes (horas, minutos, segundos) debe ser mayor a cero'
                messagebox.showinfo(message=msg, title="Aviso")
                return # no se cierra si hay error


        jugador_actual = entry_nombre.get()
        if jugador_actual != '' and jugador_actual != "String de 1 a 30 caracteres...": #Se valida que el jugador haya insertado su nombre
            
            if busca_jugador(jugador_actual):
                if messagebox.askquestion("ALTO", "Este nombre ya tiene partidas, ¿desea seguir con el nombre?") == "no":
                    entry_nombre.delete(0, tk.END)
                    return             
    
            if root_juego.reloj == 'cronometro':
                #Se recuperan los segundos precargados. Si es partida nueva, por defecto será 0.
                segundos_ya_jugados = getattr(root_juego, 'segundos_transcurridos', 0)

                root_juego.hora_inicio = datetime.now() - timedelta(seconds=segundos_ya_jugados)
                refrescar_tiempo_transcurrido()

            elif root_juego.reloj == 'timer':

                root_juego.horas_entry.config(fg="black", state='readonly')
                root_juego.minutos_entry.config(fg="black", state='readonly')
                root_juego.segundos_entry.config(fg="black", state='readonly')

                root_juego.horas_reloj = root_juego.horas_entry.get()
                root_juego.minutos_reloj = root_juego.minutos_entry.get()
                root_juego.segundos_reloj = root_juego.segundos_entry.get()

                root_juego.juego_iniciado = True
                root_juego.reloj_pausado = False 
                boton_iniciar_juego.config(state='disabled') #deshabilita el boton de iniciar juego
                entry_nombre.config(state="disabled") #deshabilita el nombre

                #Se verifica si ya hay un tiempo guardado en memoria por la carga de la partida
                tiempo_guardado = getattr(root_juego, 'segundos_restantes', 0)

                if tiempo_guardado > 0:
                    modificar_timer()
                else:
                    preparar_timer()
            
            else:
                root_juego.juego_iniciado = True
                boton_iniciar_juego.config(state='disabled') #deshabilita el boton de iniciar juego
                entry_nombre.config(state="disabled") #deshabilita el nombre


        else:
            msg = "ERROR: no se puede iniciar el juego, debe digitar su nombre"
            messagebox.showinfo(message=msg, title="Error")

    #Función para mostrar el top x
    #E: no recibe parámetros
    #S: pausa el reloj, llama la función que genera el pdf y lueego muestra el mensaje para continuar y reanudar el reloj
    def mostrar_topx():

        if root_juego.reloj != 'ninguno':
            pausar_reloj()
            generar_topx_pdf()

            messagebox.showinfo(
                "Top X",
                "Cuando termine de ver el ranking, pulse Aceptar para continuar."
            )
            reanudar_reloj()
        
        else:
            generar_topx_pdf()


    #Función para guardar la jugada
    #E: no recibe parámetros
    #S: guarda el juego, o muestra el mensaje respectivo
    def guardar_juego():

        if valida_inicio_juego():

            jugador_actual = entry_nombre.get()
            if jugador_actual != '':

                f = open(nombre_archivo_juego_actual, "r")
                partidas_actuales = json.load(f)
                f.close()
                
                #Esta parte guarda en un diccionario la información de la matriz en el momento de guardar la partida
                dic_matriz_actual = {} 
                for i,fila in enumerate(root_juego.matriz_sudoku_vacia):
                    for j, col in enumerate(root_juego.matriz_sudoku_vacia[i]):
                        posicion = f"{i},{j}"

                        valor = root_juego.matriz_sudoku_vacia[i][j].get()
                        if valor != '': #Guarda solamente los que tienen elementos insertados
                            try:
                                dic_matriz_actual[posicion] = int(valor)
                            except ValueError:

                                valor = cambia_a_numero(valor)
                                dic_matriz_actual[posicion] = valor
                try:
                    #Crea una lista que contiene la información del reloj y las horas, minutos y segundos
                    lista_reloj = [root_juego.reloj, root_juego.horas_entry.get(), root_juego.minutos_entry.get(), root_juego.segundos_entry.get()]

                except AttributeError: #Entra aquí en caso de no estar usando un reloj
                    lista_reloj = [root_juego.reloj, 0, 0, 0]

                dic_nivel_jugador = {
                    'cuadricula': dic_matriz_actual,
                    'reloj': lista_reloj,
                    'elementos': root_juego.elementos
                }

                if jugador_actual not in partidas_actuales:
                    dic_jugador_actual = {}

                    dic_jugador_actual[root_juego.nivel] = dic_nivel_jugador
                    partidas_actuales[jugador_actual] = dic_jugador_actual
    
                else:
                    dic_jugador_actual = partidas_actuales[jugador_actual]
                    dic_jugador_actual[root_juego.nivel] = dic_nivel_jugador
                    partidas_actuales[jugador_actual] = dic_jugador_actual

                #Se graban los datos del archivo de configuración por default
                f = open(nombre_archivo_juego_actual, "w")
                json.dump(partidas_actuales, f)
                f.close()

                msg = "¡Se guardó el juego correctamente!"
                messagebox.showinfo(message=msg, title="Error")

            else:
                msg = "ERROR: debe digitar primero su nombre"
                messagebox.showinfo(message=msg, title="Error")
            
    #Función para cargar una jugada
    #E: no recibe parámetros
    #S: despliega el mensaje respectivo si ya empezó el juego o carga la partida
    def cargar_juego():
        global juego_cargado
        global nombre_jugador_cargado
        global juego_cargado_nivel
        global juego_cargado_elementos
        global juego_borrado_numero_partida

        if root_juego.juego_iniciado == False: #Verifica que el usuario no haya iniciado ya el juego

            jugador_actual = entry_nombre.get()
            if jugador_actual != '': #Verifica que el nombre no esté vac+io

                # leer datos
                f = open(nombre_archivo_juego_actual, "r")
                jugada_actual = json.load(f)
                f.close()

                if jugador_actual not in jugada_actual:
                    msg = "NO TIENE NINGUNA PARTIDA GUARDADA CON ESE NOMBRE"
                    messagebox.showinfo(message=msg, title="Error")
                    return
                
                dic_niveles_jugador = jugada_actual[jugador_actual]
                
                if root_juego.nivel not in dic_niveles_jugador:
                    msg = "NO TIENE UN JUEGO GUARDADO CON ESTA DIFICULTAD"
                    messagebox.showinfo(message=msg, title="Error")
                    

                    juego_borrado_numero_partida = " "
                    juego_cargado = False
                    nombre_jugador_cargado = " "
                    juego_cargado_nivel = " "
                    juego_cargado_elementos = " "

                    root_juego.destroy()
                    return

                juego_cargado = True

                juego_cargado_nivel = root_juego.nivel

                nombre_jugador_cargado = jugador_actual

                juego_cargado_elementos = root_juego.elementos

                root_juego.destroy()
                abrir_ventana_jugar()


            else:
                msg = "ERROR: debe digitar primero su nombre"
                messagebox.showinfo(message=msg, title="Error")
        else:
            msg = "ERROR: no se puede cargar partida, ya se inició el juego"
            messagebox.showinfo(message=msg, title="Error")


    #------------------------------------------------------------
    #Se crea la ventana para la jugada
    #------------------------------------------------------------
    root_juego = tk.Toplevel() 
    root_juego.title("Jugando Sudoku :o")
    root_juego.config( pady=50)

    root_juego.transient(root)

    #Si el usuario no había borrado la partida antes genera una partida al azar
    if juego_borrado_numero_partida == " ":
        root_juego.numero_partida = str(random.randint(1, 3))
    else:
        root_juego.numero_partida = juego_borrado_numero_partida #Sino, agarra la que había dado el usuario
    
    #Se crean las pilas para las jugadas
    root_juego.jugadas_realizadas = collections.deque()
    root_juego.jugadas_eliminadas = collections.deque()

    #Valores predeterminados antes de jugar
    root_juego.boton_activo = None
    root_juego.juego_iniciado = False
    root_juego.nivel = configuracion["nivel"]
    root_juego.elementos = configuracion["elementos"]
    root_juego.topx = configuracion["top x"]

    #Información para el reloj
    root_juego.reloj = configuracion["reloj"][0]
    root_juego.horas_reloj = configuracion["reloj"][1]
    root_juego.minutos_reloj = configuracion["reloj"][2]
    root_juego.segundos_reloj = configuracion["reloj"][3]

    root_juego.reloj_pausado = False
    root_juego.after_reloj_id = None
    root_juego.modo_cronometro_extra = False
    root_juego.segundos_restantes = 0

    #------------------------------------------------------------
    #Se leen las partidas ya hechas
    #------------------------------------------------------------

    if juego_cargado:
        f = open(nombre_archivo_juego_actual, "r")
        juego_actual = json.load(f)
        f.close()

        dic_jugador = juego_actual[nombre_jugador_cargado]

        dic_nivel_jugador = dic_jugador[juego_cargado_nivel]

        partida_actual = dic_nivel_jugador["cuadricula"]

        root_juego.reloj = dic_nivel_jugador["reloj"][0]

        root_juego.elementos = dic_nivel_jugador["elementos"]

        root_juego.horas_reloj = dic_nivel_jugador["reloj"][1]
        root_juego.minutos_reloj = dic_nivel_jugador["reloj"][2]
        root_juego.segundos_reloj = dic_nivel_jugador["reloj"][3]

        h_int = int(root_juego.horas_reloj)
        m_int = int(root_juego.minutos_reloj)
        s_int = int(root_juego.segundos_reloj)

        root_juego.segundos_restantes = (h_int * 3600) + (m_int * 60) + s_int
        root_juego.segundos_transcurridos = (h_int * 3600) + (m_int * 60) + s_int

    else:
        nombre_archivo = "sudoku2026partidas.json"

        # leer datos
        f = open(nombre_archivo, "r")
        partidas = json.load(f)
        f.close()

        partida_actual = partidas[root_juego.nivel][root_juego.numero_partida] #Es un diccionario


    titulo_juego = tk.Label(root_juego, text="SUDOKU", 
              font=('Segoe UI', 30, "bold"), 
              compound="left",
              fg="#0c3a95"
              )
    titulo_juego.pack()

    frame_jugador = tk.Frame(root_juego,pady=20)

    nombre = tk.Label(frame_jugador, text="Jugador", 
                  font=('Segoe UI', 12, "bold"),
                  compound="left",
                  )
    nombre.grid(row=1, column=1)

    entry_nombre = tk.Entry(frame_jugador, width=80)


    
    entry_nombre.bind("<FocusIn>", quita_texto) 
    entry_nombre.bind("<FocusOut>", valida_nombre)
    entry_nombre.bind("<Return>", valida_nombre) #Para el nombre del jugador
    
    if juego_cargado:
        entry_nombre.insert(0, nombre_jugador_cargado)
        entry_nombre.config(state='disabled')
    else:
        entry_nombre.insert(0, "String de 1 a 30 caracteres...")
    
    entry_nombre.grid(row=2, column=1)

    frame_jugador.pack()

    #------------------------------------------------------------
    #Parte para la creación de la matriz
    #------------------------------------------------------------
    
    frame_principal = tk.Frame(root_juego)

    if juego_cargado:
        crear_matriz(True)
    else:
        crear_matriz(False)
    
    #------------------------------------------------------------
    #Parte para la creación de los botones cde opciones
    #------------------------------------------------------------
    frame_principal_botones = tk.Frame(frame_principal)
    frame_botones = tk.Frame(frame_principal_botones, padx=20)

    count = 1
    for row in range(3):
        for col in range(3):

            valor = count
            if root_juego.elementos == 'letras':
                valor = cambia_a_letra(count)

            boton_selecciona = tk.Button(
                frame_botones,
                text=f"{valor}",
                font=TEXTO_UNIVERSAL,
                **ESTILO_BOTON_SELECCIONA

            )

            boton_selecciona.bind("<Button-1>", seleccionar_boton_elemento)

            boton_selecciona.grid(row=row, column=col, padx=10, pady=10)

            count += 1

    frame_botones.pack()

    frame_principal_botones.grid(row=1, column=2)

    frame_reloj_principal = tk.Frame(frame_principal)

    reloj_titulo = 'Sin reloj'
    if root_juego.reloj == 'cronometro':
        reloj_titulo = 'Cronómetro'
    elif root_juego.reloj == 'timer':
        reloj_titulo = 'Timer'

    titulo_reloj = tk.Label(frame_reloj_principal, 
                  font=TEXTO_UNIVERSAL,
                  text=reloj_titulo,
                  compound="left",
                  )
    titulo_reloj.pack()

    if root_juego.reloj != 'ninguno':
        if juego_cargado:
            crea_reloj(True)
        else:
            crea_reloj(False)

    label_nivel = tk.Label(frame_reloj_principal,
                           font=TEXTO_UNIVERSAL,
                           text="Nivel de dificultad: "+root_juego.nivel,
                           )
    label_nivel.pack(pady=10)

    frame_reloj_principal.grid(row=3, column=1,pady=25)


    #*****************************************************

    frame_botones_partida = tk.Frame(frame_principal)

    boton_guardar = tk.Button(frame_botones_partida,
                font=TEXTO_UNIVERSAL,
                text=f"Guardar Juego",
                bg="#ffffff",
                activebackground="#e3e3e3",
                **ESTILO_BOTONES,
                command=guardar_juego)

    boton_guardar.grid(row=1, column=1,padx=10)

    boton_cargar = tk.Button(frame_botones_partida,
                font=TEXTO_UNIVERSAL,
                bg="#ffffff",
                text=f"Cargar Juego",
                activebackground="#e3e3e3",
                **ESTILO_BOTONES,
                command=cargar_juego)

    boton_cargar.grid(row=1, column=2,padx=10)

    frame_botones_partida.grid(row=3, column=2,pady=25)

    #*****************************************************

    frame_botones_jugada =  tk.Frame(frame_principal)

    #Tres botones****************************************
    boton_iniciar_juego = tk.Button(frame_botones_jugada,
                font=TEXTO_UNIVERSAL,
                text=f"Iniciar Juego",
                bg="#ffa5ea",
                activebackground="#f580d9",
                **ESTILO_BOTONES,
                command=iniciar_juego)

    boton_iniciar_juego.grid(row=1, column=1,padx=10)

    boton_deshacer_jugada = tk.Button(frame_botones_jugada,
                font=TEXTO_UNIVERSAL,
                text=f"Deshacer Jugada",
                bg="#a1e9ff",
                activebackground="#7dcbe3",
                **ESTILO_BOTONES,
                command=deshacer_jugada)

    boton_deshacer_jugada.grid(row=1, column=2,padx=10)

    boton_rehacer_jugada = tk.Button(frame_botones_jugada,
                font=TEXTO_UNIVERSAL,
                bg="#a1e9ff",
                text=f"Rehacer Jugada",
                activebackground="#7dcbe3",
                **ESTILO_BOTONES,
                command=rehacer_jugada)

    boton_rehacer_jugada.grid(row=1, column=3,padx=10)

    frame_botones_jugada.grid(row=4,column=1,pady=25)



    frame_botones_jugada2 =  tk.Frame(frame_principal)

    #Tres botones****************************************
    boton_borrar_juego = tk.Button(frame_botones_jugada2,
                font=TEXTO_UNIVERSAL,
                text=f"Borrar Juego",
                bg="#90beff",
                activebackground="#6d9cdd",
                **ESTILO_BOTONES,
                command=borrar_juego)

    boton_borrar_juego.grid(row=1, column=1,padx=10)

    boton_terminar_juego = tk.Button(frame_botones_jugada2,
                font=TEXTO_UNIVERSAL,
                text=f"Terminar Juego",
                bg="#a7deb2",
                activebackground="#86c893",
                **ESTILO_BOTONES,
                command=terminar_juego)

    boton_terminar_juego.grid(row=1, column=2,padx=10)

    boton_top_x = tk.Button(frame_botones_jugada2,
                font = TEXTO_UNIVERSAL,
                text = f"Top X",
                bg = "#fffddd",
                activebackground = "#eeeab1",
                **ESTILO_BOTONES,
                command=mostrar_topx)

    boton_top_x.grid(row=1, column=3, padx=10)

    frame_botones_jugada2.grid(row=4,column=2,pady=25)

    frame_principal.pack()

    root_juego.protocol("WM_DELETE_WINDOW", ir_menu_principal)

#Función que abre la ventana de acerca de
#E: no posee entradas
#S: despliega el acerca
def abrir_ventana_acerca():

    botonD.config(state="disabled")

    root_acerca = tk.Toplevel()
    root_acerca.title("Acerca del Sudoku")
    root_acerca.geometry("700x700")
    root_acerca.config(padx=100, pady=100, bg="#cddeff")

    frame_acerca = tk.Frame(root_acerca, padx= 100, pady=50)

    tk.Label(frame_acerca, text="ACERCA DEL \nPROGRAMA", 
              font=('Segoe UI', 30, "bold"), 
              compound="left",
              fg="#0c3a95",
              pady=50
              ).pack()

    

    tk.Label(frame_acerca, font=('Segoe UI', 15), text="SUDOKU").pack()
    tk.Label(frame_acerca, font=('Segoe UI', 15), text="18 de Mayo del 2026").pack()
    tk.Label(frame_acerca, font=('Segoe UI', 15), text="v1.0").pack()
    tk.Label(frame_acerca, font=('Segoe UI', 15), text="Sofía Rivera Vanegas").pack()

    def activa_boton():
        botonD.config(state="normal")
        root_acerca.destroy()

    frame_acerca.pack()

    root_acerca.protocol("WM_DELETE_WINDOW", activa_boton)


botonA = tk.Button(root, text="Jugar",  command=abrir_ventana_jugar, **ESTILO_BOTON_MENU)
botonA.pack(pady=15)  # Add some padding

botomB = tk.Button(root, text="Configurar", command=abrir_ventana_config, **ESTILO_BOTON_MENU)
botomB.pack(pady=15)  # Add some padding

botonC = tk.Button(root, text="Ayuda", command=desplegar_manual, **ESTILO_BOTON_MENU)
botonC.pack(pady=15)  # Add some padding

botonD = tk.Button(root, text="Acerca de", command=abrir_ventana_acerca, **ESTILO_BOTON_MENU)
botonD.pack(pady=15)  # Add some padding

botonE = tk.Button(root, text="Salir", command=quit, **ESTILO_BOTON_MENU)
botonE.pack(pady=15)  # Add some padding


#Para cambiar el ícono de la ventana
icono_chico = tk.PhotoImage(file="img/sudoku.png")
# Establecerlo como ícono de la ventana.
root.iconphoto(True, icono_chico)

root.mainloop() 
