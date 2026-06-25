from tkinter import *
from tkinter import messagebox
import random
import time
import json
import os


def cargarImagen(nombre):
    """carga imagenes"""
    ruta = os.path.join("imagenes", nombre)
    imagen = PhotoImage(file=ruta)
    return imagen


# ==================== mapa ====================

class CrazySnackRushGame:
    """ventana principal"""
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 700
    WINDOW_TITLE = "Crazy Snack Rush"
    IMAGE_PATH = "imagenes"
    BACKGROUND_IMAGE = "fondo.gif"
    
    def __init__(self):
        self.window = None
        self.background_image = None
        self.background_label = None
        self.name_entry = None
        
        self._setup_window()#crear la ventana 
        self._load_background()#carga el imagen de fondo
        self._create_widgets()#crea los componentes de pantalla
     #crear la ventana    
    def _setup_window(self):
        self.window = Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.window.resizable(width=False, height=False)
    #carga el fondo
    def _load_background(self):
        image_path = os.path.join(self.IMAGE_PATH, self.BACKGROUND_IMAGE)
        self.background_image = PhotoImage(file=image_path)
        self.background_label = Label(self.window, image=self.background_image)
        self.background_label.place(x=0, y=0)
    #crear los widgets
    def _create_widgets(self):
        self._create_info_button()
        self._create_name_input_section()
        self._create_play_button()
       #crea el boton de informacion 
    def _create_info_button(self):
        info_button = Button(self.window,text="Informacion",command=self._show_game_info,padx=15,pady=5)
        info_button.place(x=self.WINDOW_WIDTH - 120, y=20)
    #crea   espacio para ingresar nombre
    def _create_name_input_section(self):
        name_label = Label(self.window,text="Ingrese su nombre：")
        name_label.place(x=self.WINDOW_WIDTH//2 - 150, y=self.WINDOW_HEIGHT - 200)
        
        self.name_entry = Entry(self.window)
        self.name_entry.place(x=self.WINDOW_WIDTH//2 + 30, y=self.WINDOW_HEIGHT - 200)
        self.name_entry.bind("<Return>", self._on_play_clicked)
    #crea boton para iniciar    
    def _create_play_button(self):
        play_button = Button(self.window,text="Start the game",command=self._on_play_clicked)
        play_button.place(x=self.WINDOW_WIDTH//2 - 80, y=self.WINDOW_HEIGHT - 100)
    #funcion de boton de informacion  
    def _show_game_info(self):
        info_window = Toplevel(self.window)
        info_window.title("Informacion de juego")
        info_window.geometry("300x150")
        info_window.resizable(width=False, height=False)
        
        info_text = ("🎮 Crazy Snack Rush\n\n"
                     "👨‍💻 Creador：\n"
                     "   • Anderson Lu Lu\n"
                     "   • Sebastian Solano Porras")
        
        info_label = Label(info_window,text=info_text)
        info_label.pack(expand=True, fill=BOTH, padx=20, pady=20)
    #funcion de boton play    
    def _on_play_clicked(self, event=None):
        player_name = self.name_entry.get().strip()
        
        if not player_name:
            messagebox.showwarning("Error", "Por favor escriba su nombre")
            self.name_entry.focus_set()
            return
            
        try:
            # crear informacion de personaje
            jugador = InforPlayer(player_name)
            # pasa a ventana de selecionar nivel
            self.window.destroy()
            mapa = MapaSeleccion(jugador)
            mapa.run()
        except Exception as e:
            messagebox.showerror("Error", f"Error al iniciar: {str(e)}")
        
    def run(self):
        self.window.mainloop()
class MapaSeleccion:
    """ventana de selecciona nivel"""
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 700
    WINDOW_TITLE = "Seleccionar Mapa - Crazy Snack Rush"
    BACKGROUND_IMAGE = "FondoMapa.png"
    IMAGE_PATH = "imagenes"

    COLOR_BLUE = "#3498db"
       
    def __init__(self, player_info):
        self.player_info = player_info
        self.window = None
        self.per_frame = None
        self.score_label = None
        self.rank_label = None
        
        self._setup_window()#crea el window
        self._load_background()#carga la imagen de fondo
        self._create_info_bar()#muestra los informaciones de jugador en la ventana
        self._create_ranking_button()#crea un boton de raking 
        self._create_title()#un label 
        self._create_level_buttons()#crear botones de entrar nivel
        self._create_bottom_bar()#crear boton donde guarda los puntos obtenidos
        
        self._update_score_display()
        self._update_rank_display()
    ##crea el window
    def _setup_window(self):
        self.window = Tk()
        self.window.title(self.WINDOW_TITLE)
        self.window.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")
        self.window.resizable(width=False,height=False)
        self.per_frame = Frame(self.window)
        self.per_frame.pack(fill=BOTH,expand=True)
    #carga la imagen de fondo
    def _load_background(self):
        try:
            ruta = os.path.join(self.IMAGE_PATH, self.BACKGROUND_IMAGE)
            foto_fondo = PhotoImage(file=ruta)
            foto_fondo = foto_fondo.zoom(2, 1)
            label_fondo = Label(self.per_frame, image=foto_fondo)
            label_fondo.place(relx=0.5, rely=0.5, anchor="center")
            label_fondo.lower()
            label_fondo.image = foto_fondo
        except Exception as e:
            print(f"⚠️ Error cargando fondo: {e}")
    #muestra los informaciones de jugador en la ventana
    def _create_info_bar(self):
        info_frame = Frame(self.per_frame, height=80)
        info_frame.place(relx=0, rely=0, relwidth=1, height=80)

        name_label = Label(info_frame,text=f"🎮 Jugador: {self.player_info.name}")
        name_label.place(x=30, y=25)

        self.score_label = Label(info_frame,text=f"⭐ Puntos: {self.player_info.get_points()}")
        self.score_label.place(x=350, y=25)

        self.rank_label = Label(info_frame,text="🏆 Ranking: -")
        self.rank_label.place(x=600, y=25)
    
    def _update_score_display(self):
        if self.score_label:
            self.score_label.config(text=f"⭐ Puntos: {self.player_info.get_points()}")
    
    def _update_rank_display(self):
        if self.rank_label:
            rank = self.player_info.get_rank()
            rank_text = f"🏆 Ranking: #{rank}" if rank > 0 else "🏆 Ranking: -"
            self.rank_label.config(text=rank_text)
    #crea el boton de ranking 
    def _create_ranking_button(self):
        btn_ranking = Button(self.per_frame,text="📊 Ranking",command=self._mostrar_ranking,
        padx=20,pady=10,cursor="hand2")
        btn_ranking.place(relx=0.88, rely=0.05, anchor="center")
    #funcion de boton ranking
    def _mostrar_ranking(self):
        ranking_window = Toplevel(self.window)
        ranking_window.title("🏆 Ranking")
        ranking_window.geometry("500x600")
        ranking_window.resizable(width=False, height=False)
        ranking_window.transient(self.window)
        ranking_window.grab_set()
        
        Label(ranking_window,text="🏆 RANKING").pack(pady=20)
        
        ranking_data = RankingManager.get_ranking_data(15)
        
        if not ranking_data:
            Label(ranking_window,text="📋 Sin datos",).pack(pady=50)
        else:
            self._crear_tabla_ranking(ranking_window, ranking_data)
        
    
    def _crear_tabla_ranking(self, parent, ranking_data):
        table_frame = Frame(parent, bg="white")
        table_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)
        
        # Header
        header_frame = Frame(table_frame, bg="#34495e", height=40)
        header_frame.pack(fill=X)
        header_frame.pack_propagate(False)
        
        Label(header_frame, text="#", width=6, bg="#34495e", fg="white",
              font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
        Label(header_frame, text="Jugador", width=15, bg="#34495e", fg="white",
              font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
        Label(header_frame, text="Puntos", width=10, bg="#34495e", fg="white",
              font=("Arial", 12, "bold")).pack(side=LEFT, padx=5)
        
        # List
        list_frame = Frame(table_frame, bg="white")
        list_frame.pack(fill=BOTH, expand=True)
        
        scrollbar = Scrollbar(list_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        
        canvas = Canvas(list_frame, yscrollcommand=scrollbar.set, bg="white")
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.config(command=canvas.yview)
        
        content_frame = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=content_frame, anchor=NW)
        
        for i, player in enumerate(ranking_data, 1):
            self._crear_fila_ranking(content_frame, i, player)
        
        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    
    def _crear_fila_ranking(self, parent, position, player):
        row = Frame(parent, bg="white", height=35)
        row.pack(fill=X, pady=2)
        row.pack_propagate(False)
        
        if position == 1:
            rank_text = "🥇"
            bg_color = "#FFD700"
        elif position == 2:
            rank_text = "🥈"
            bg_color = "#C0C0C0"
        elif position == 3:
            rank_text = "🥉"
            bg_color = "#CD7F32"
        else:
            rank_text = str(position)
            bg_color = "white"
        
        if player['name'] == self.player_info.name:
            bg_color = self.COLOR_BLUE
            fg_color = "white"
        else:
            fg_color = "#2c3e50"
        
        Label(row, text=rank_text, width=6, bg=bg_color, fg=fg_color,
              font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
        Label(row, text=player['name'], width=15, bg=bg_color, fg=fg_color,
              font=("Arial", 10)).pack(side=LEFT, padx=5)
        Label(row, text=str(player['points']), width=10, bg=bg_color, fg=fg_color,
              font=("Arial", 10, "bold")).pack(side=LEFT, padx=5)
    
    def _create_title(self):
        title_label = Label(self.per_frame,text="🌍 Selecciona tu nivel",padx=30,pady=15)
        title_label.place(relx=0.5, rely=0.12, anchor="center")
    
    def _create_level_buttons(self):
        #nivel1     
        nivel1button=Button(self.per_frame,text="✈️ Restaurante Volador",
        command=self._nivel_1,)
        nivel1button.place(relx=0.25, rely=0.3, anchor="center")
        
        # Nivel 2
        nivel2button=Button(self.per_frame,text="✈️ Restaurante En La Costa",
        command=self._nivel_2,)
        nivel2button.place(relx=0.75, rely=0.3, anchor="center")
        
        # Nivel 3
        nivel3button=Button(self.per_frame,text="✈️ Restaurante Frances",
        command=self._nivel_3,)
        nivel3button.place(relx=0.5, rely=0.55, anchor="center")
    
    def _nivel_1(self):

        self.window.withdraw()

        Cocina(self.window,300,10,20,"Restaurante Volador",self.player_info,1,recetasVolador)
    
    def _nivel_2(self):

        self.window.withdraw()
        Cocina(self.window,300,10,20,"Restaurante Frances",self.player_info,2,recetasFrances)
    
    def _nivel_3(self):

        self.window.withdraw()

        Cocina(self.window,300,10,20,"Restaurante Costa",self.player_info,3,recetasLaCosta)
    
    def _create_bottom_bar(self):
        bottom_frame = Frame(self.per_frame,height=60)
        bottom_frame.place(relx=0,rely=0.93,relwidth=1,height=60)

        Button(bottom_frame,text="💾 Guardar Puntos",command=self._guardar_puntos,
        padx=25,pady=8,cursor="hand2").place(relx=0.5,rely=0.5,anchor="center")
    
    def _guardar_puntos(self):
        if messagebox.askyesno(
            "Guardar",
            f"¿Guardar puntuación?\n"
            f"Jugador: {self.player_info.name}\n"
            f"Puntos: {self.player_info.get_points()}"
        ):
            if self.player_info.save_data():
                messagebox.showinfo(
                    "✅ Éxito",
                    f"¡Guardado!\n"
                    f"Ranking: #{self.player_info.get_rank()}"
                )
                self._update_score_display()
                self._update_rank_display()
            else:
                messagebox.showerror("❌ Error", "Error al guardar")
    
    def run(self):
        self.window.mainloop()


class Cocina:

    TAM_CELDA = 50

    def __init__(self,parent,tiempo,filas,columnas,escenario,inforplayer,espacio,recetas):
        self.tiempo = tiempo
        self.escenario = escenario
        self.inforplayer = inforplayer
        self.recetas = recetas
        self.filas = filas
        self.columnas = columnas
        self.espacio=espacio
        self.window = Toplevel(parent)
        self.window.title(self.escenario)
        self.window.geometry("1200x800")
        self.imagenes = []
        self.matriz = [[None for _ in range(columnas)]for _ in range(filas)]
        self.matriz[0][9] = Dispensador(0,9,Proteinas("pollo"))
        self.matriz[0][8] = Dispensador(0,5,Proteinas("vaca"))
        self.matriz[1][9] = Dispensador(1,9,Proteinas("cerdo"))
        self.matriz[2][9] = Dispensador(2,9,Proteinas("oreja"))
        self.matriz[3][9] = Dispensador(3,9,Vegetales_Y_Frutas("zanahoria"))
        self.matriz[4][9] = Dispensador(4,9,Vegetales_Y_Frutas("papa"))
        self.matriz[5][9] = Dispensador(5,9,Vegetales_Y_Frutas("remolacha"))
        self.matriz[7][9] = EstacionProcesamiento(7,9,"calentar",Proteinas)
        self.matriz[8][9] = EstacionProcesamiento(8,9,"picar",Vegetales_Y_Frutas)
        self.matriz[9][9] = Plato(9,9,self)

        self.crearVentana()#crea la ventana
        #elementos de matrices
        self.player1 = Player(self.frameMapa,self,5,5,1)
        self.player2 = Player(self.frameMapa,self,7,5,2)
        self.jugadorActual = self.player1
        self.actualizarBolsos()
        #vincula el teclado
        self.window.bind("<Key>",self.teclado)
        self.window.focus_force()
        self.actualizarTiempo()

    def actualizarBolsos(self):

        if self.player1.bag is None:

            self.labelBag1.config(
                image="",
                text="None"
            )

        else:

            foto = cargarImagen(
            self.player1.bag.getImagen()
            )

            self.labelBag1.config(
                image=foto,
                text=""
            )

            self.labelBag1.image = foto

        if self.player2.bag is None:

            self.labelBag2.config(
                image="",
                text="None"
            )

        else:

            foto = cargarImagen(self.player2.bag.getImagen())

            self.labelBag2.config(
                image=foto,
                text=""
            )

            self.labelBag2.image = foto

    def crearVentana(self):
        self.top_frame = Frame(self.window)
        self.top_frame.pack(fill=X)
        Label(self.top_frame,text=self.escenario).pack(side=LEFT,padx=20)
        self.labelBag1 = Label(self.top_frame)

        self.labelBag1.pack(side=LEFT,padx=20)

        self.labelBag2 = Label(self.top_frame)

        self.labelBag2.pack(side=LEFT,padx=20)
        #label de tiempo
        self.labelTiempo = Label(self.top_frame,text=f"Tiempo: {self.tiempo}")
        self.labelTiempo.pack(side=RIGHT,padx=20)

        #tamano de matriz
        ancho = self.columnas * self.TAM_CELDA
        alto = self.filas * self.TAM_CELDA
        #crea el frame para ser contenedor principal de matriz del juego 
        self.frameMapa = Frame(self.window,width=ancho,height=alto)
        self.frameMapa.pack(pady=20)
        self.frameMapa.pack_propagate(False)
        self.dibujarMatriz()#crea la matriz 
        print(ancho, alto)
        print(self.frameMapa.winfo_width())
        print(self.frameMapa.winfo_height())

    def dibujarMatriz(self):
        print("dibujando matriz")

        for fila in range(self.filas):

            for columna in range(self.columnas):
                #determine tamano de cada casilla
                casilla = Frame(self.frameMapa,width=50,height=50,relief="solid",bd=1)
                casilla.grid(row=fila,column=columna)
                casilla.grid_propagate(False)

                obj = self.matriz[fila][columna]
                
                if obj is not None:

                    if isinstance(obj, Dispensador):

                        nombre = obj.ingrediente.nombre

                        foto = cargarImagen(f"zonade{nombre}.gif")
                        self.imagenes.append(foto)
                        casilla = Label(self.frameMapa,image=foto,relief="solid")

                        casilla.image = foto
                    elif isinstance(obj, Plato):

                        foto = cargarImagen("plato.gif")

                        self.imagenes.append(foto)

                        casilla = Label(self.frameMapa,image=foto)

                        casilla.image = foto
                    elif isinstance(obj, EstacionProcesamiento):

                        foto = cargarImagen(f"estacionde{obj.nombre}.gif")
                        self.imagenes.append(foto)

                        casilla = Label(self.frameMapa,image=foto)

                        casilla.image = foto
                    else:

                        casilla = Label(self.frameMapa,width=50,height=50,relief="solid")
                else:
                    fotovacio=cargarImagen(f"espacio{self.espacio}.gif")
                    self.imagenes.append(fotovacio)
                    casilla = Label(self.frameMapa,image=fotovacio,width=50,height=50,relief="solid")
                    casilla.image=fotovacio

                casilla.grid(row=fila,column=columna)
        print("matriz terminada")

    def teclado(self,event):

        tecla = event.keysym.lower()

        if tecla == "q":

            if self.jugadorActual == self.player1:

                self.jugadorActual = self.player2

                print("Controlando Jugador 2")

            else:

                self.jugadorActual = self.player1

                print("Controlando Jugador 1")

        elif tecla in ["w","a","s","d"]:

            self.jugadorActual.mover(tecla)

        elif tecla == "e":

            self.jugadorActual.interactuar()

    def actualizarTiempo(self):

        self.labelTiempo.config(
            text=f"Tiempo: {self.tiempo}"
        )

        if self.tiempo > 0:

            self.tiempo -= 1

            self.window.after(
                1000,
                self.actualizarTiempo
            )

# ==================== informacion de jugador ====================

class InforPlayer:
    """guardar informacion de jugador"""
    SAVE_DIR = "saves"
    RANKING_FILE = "ranking.json"
    
    def __init__(self, name):
        self.name = name
        self.level1 = 0
        self.level2 = 0
        self.level3 = 10
        self.points = self.level1+self.level2+self.level3
        self._load_data()
    
    def setpointlevel1(self, point):
        self.level1 = point
        self._update_total_points()
    
    def setpointlevel2(self, point):
        self.level2 = point
        self._update_total_points()
    
    def setpointlevel3(self, point):
        self.level3 = point
        self._update_total_points()
    
    def _update_total_points(self):
        self.points = self.level1 + self.level2 + self.level3
    
    def get_points(self):
        return self.points
    
    def save_data(self):
        try:
            if not os.path.exists(self.SAVE_DIR):
                os.makedirs(self.SAVE_DIR)
            
            # guarda informacion de jugador
            filename = f"{self.name.lower().replace(' ', '_')}.json"
            filepath = os.path.join(self.SAVE_DIR, filename)
            
            data = {
                "name": self.name,
                "level1": self.level1,
                "level2": self.level2,
                "level3": self.level3,
                "points": self.points
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            
            # actualizar
            self._update_ranking()
            print(f" Puntos de {self.name} guardados: {self.points}")
            return True
            
        except Exception as e:
            print(f" Error al guardar: {str(e)}")
            return False
    
    def _load_data(self):
        try:
            filename = f"{self.name.lower().replace(' ', '_')}.json"
            filepath = os.path.join(self.SAVE_DIR, filename)
            
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.level1 = data.get('level1', 0)
                self.level2 = data.get('level2', 0)
                self.level3 = data.get('level3', 0)
                self.points = data.get('points', 0)
                print(f"📂 Cargado: {self.name} - {self.points} pts")
                return True
            else:
                print(f"📝 Nuevo jugador: {self.name}")
                return False
        except Exception as e:
            print(f"⚠️ Error al cargar: {str(e)}")
            return False
    
    def _update_ranking(self):
        try:
            all_players = []
            if os.path.exists(self.SAVE_DIR):
                for filename in os.listdir(self.SAVE_DIR):
                    if filename.endswith('.json') and filename != self.RANKING_FILE:
                        filepath = os.path.join(self.SAVE_DIR, filename)
                        with open(filepath, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            # 确保有 points 字段
                            if 'points' in data:
                                all_players.append({
                                    "name": data['name'],
                                    "points": data['points']
                                })
            
            # 
            sorted_players = sorted(all_players, key=lambda x: x['points'], reverse=True)
            
            ranking_path = os.path.join(self.SAVE_DIR, self.RANKING_FILE)
            with open(ranking_path, 'w', encoding='utf-8') as f:
                json.dump(sorted_players, f, ensure_ascii=False, indent=4)
            
        except Exception as e:
            print(f"⚠️ Error al actualizar ranking: {str(e)}")
    
    def get_ranking(self, top_n=None):
        try:
            ranking_path = os.path.join(self.SAVE_DIR, self.RANKING_FILE)
            
            if os.path.exists(ranking_path):
                with open(ranking_path, 'r', encoding='utf-8') as f:
                    ranking = json.load(f)
                
                if top_n:
                    return ranking[:top_n]
                return ranking
            else:
                self._update_ranking()
                return self.get_ranking(top_n)
        except Exception as e:
            print(f"⚠️ Error al leer ranking: {str(e)}")
            return []
    
    def get_rank(self):
        ranking = self.get_ranking()
        for i, player in enumerate(ranking, 1):
            if player['name'] == self.name:
                return i
        return -1
class RankingManager:
    """coordinar ranking"""
    
    @staticmethod
    def get_ranking_data(top_n=None):
        temp_player = InforPlayer("_temp_")
        return temp_player.get_ranking(top_n)
    
    @staticmethod
    def display_ranking(top_n=10):
        ranking = RankingManager.get_ranking_data(top_n)
        if not ranking:
            print("📋 No hay datos")
            return
        
        print("\n" + "=" * 50)
        print("🏆 RANKING")
        print("=" * 50)
        for i, player in enumerate(ranking, 1):
            medal = "🥇 " if i == 1 else "🥈 " if i == 2 else "🥉 " if i == 3 else f"{i}. "
            print(f"{medal}{player['name']}: {player['points']} pts")
        print("=" * 50)
    
    @staticmethod
    def get_top_player():
        ranking = RankingManager.get_ranking_data(1)
        return ranking[0] if ranking else None

# ==================== ingredientes ====================

class Ingrediente:
    def __init__(self, nombre):
        self.nombre = nombre
        self.estado = False
    def interactuar(self):
        self.estado=True
    def getImagen(self):

        if self.estado:

            return f"{self.nombre}procesado.gif"

        else:

            return f"{self.nombre}.gif"    
class Granos(Ingrediente):

    def __init__(self,nombre):

        super().__init__(nombre)

    def interactuar(self):

        self.estado = True
class Vegetales_Y_Frutas(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
    def interactuar(self):
        self.estado = True
class Panes_Y_Bases(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
    def interactuar(self):
        self.estado = True
class Proteinas(Ingrediente):
    def __init__(self, nombre):
        super().__init__(nombre)
    def interactuar(self):
        self.estado = True
class Receta:

    def __init__(self,nombre,
                 listaIngredientes,
                 puntosReceta,
                 maxTimeReceta):

        self.listaIngredientes = listaIngredientes
        self.nombre=nombre
        self.puntosReceta = puntosReceta
        self.maxTimeReceta = maxTimeReceta

    def comparaReceta(self, listaIngredientes):

        if len(listaIngredientes) != len(self.listaIngredientes):
            return False

        for i in range(len(listaIngredientes)):

            if listaIngredientes[i].nombre != self.listaIngredientes[i].nombre:
                return False

            if listaIngredientes[i].estado != self.listaIngredientes[i].estado:
                return False

        return True

    def TiempoLimite(self, tiempo):

        if tiempo <= self.maxTimeReceta:

            self.puntosReceta //= 2

            if self.puntosReceta < 0:
                self.puntosReceta = 0

#estaciones
class Estacion:
    def __init__(self,nombre,x,y):

        self.nombre = nombre

        self.x = x
        self.y = y
class Dispensador(Estacion):

    def __init__(self,x,y,ingrediente):

        super().__init__("dispensador",x,y)

        self.ingrediente = ingrediente

    def interactuar(self,jugador):

        jugador.bag=self.ingrediente

        print("Bag =", jugador.bag)
        print("Nombre =", jugador.bag.nombre)
class EstacionProcesamiento(Estacion):

    def __init__(self,x,y,tipo,aceptado):

        super().__init__(tipo,x,y)
        self.aceptado = aceptado

    def interactuar(self,jugador):

        print("Estacion activada")

        print("Bag:", jugador.bag)

        print("Aceptado:", self.aceptado)

        if jugador.bag is None:

            print("No tienes ingrediente")

            return

        if isinstance(jugador.bag,self.aceptado):

            print("Ingrediente correcto")

            jugador.bag.estado = True

            print(
                jugador.bag.nombre,
                "procesado"
            )

        else:

            print("Ingrediente incorrecto")

class Plato(Estacion):

    def __init__(self,x,y):

        super().__init__(
            "plato",
            x,
            y
        )

        self.ingredientes = []

class Plato(Estacion):

    def __init__(self,x,y,cocina):

        super().__init__("plato",x,y)

        self.cocina = cocina

        self.ingredientesDelPlato = []

        self.platoPreparado = None

    def interactuar(self,jugador):
        if jugador.bag is None and self.platoPreparado:

            jugador.bag = self.platoPreparado

            self.platoPreparado = None

            self.ingredientesDelPlato.clear()

            jugador.kitchen.actualizarBolsos()

            return

        if jugador.bag is None:

            print("No tiene ingrediente")

            return

        if jugador.bag.estado == False:

            print("Ingrediente no procesado")

            return

        self.ingredientesDelPlato.append(
            jugador.bag
        )

        print(
            jugador.bag.nombre,
            "agregado al plato"
        )
        print("Contenido del plato:")

        for ingrediente in self.ingredientesDelPlato:

            print(
                ingrediente.nombre
            )


        jugador.bag = None

        jugador.kitchen.actualizarBolsos()

    def limpiarPlato(self):

        self.ingredientes = []
class Mostrador(Estacion):

    def __init__(self,x,y):
        super().__init__("mostrador",x,y)

    def entregar(self,plato,recetas):

        for receta in recetas:

            if receta.comparaReceta(plato.ingredientes):

                puntos = receta.puntosReceta

                plato.limpiarPlato()

                return puntos

        return 0


class Player:

    TAM_CELDA = 50

    def __init__(self,root,kitchen,fila,columna,personaje):

        self.root = root
        self.kitchen = kitchen
        self.personaje=personaje
        self.bag=None
        self.face="abajo"
        self.photo=cargarImagen(f"personaje{self.personaje}{self.face}.gif")
        self.fila = fila
        self.columna = columna

        self.photo = cargarImagen(f"personaje{self.personaje}{self.face}.gif")

        self.label = Label(root,image=self.photo,bd=0)
        self.label.config(image=self.photo)

        self.label.image = self.photo

        self.actualizarPosicion()

    def actualizarPosicion(self):

        ancho_img = self.photo.width()
        alto_img = self.photo.height()

        x = self.columna * self.TAM_CELDA + (self.TAM_CELDA - ancho_img)//2

        y = self.fila * self.TAM_CELDA + (self.TAM_CELDA - alto_img)//2

        self.label.place(x=x,y=y)


    def mover(self, direccion):

        nuevaFila = self.fila
        nuevaColumna = self.columna

        if direccion == "w":

            nuevaFila -= 1
            self.face = "arriba"

        elif direccion == "s":

            nuevaFila += 1
            self.face = "abajo"

        elif direccion == "a":

            nuevaColumna -= 1
            self.face = "izquierda"

        elif direccion == "d":

            nuevaColumna += 1
            self.face = "derecha"

        if 0 <= nuevaFila < self.kitchen.filas:
            self.fila = nuevaFila

        if 0 <= nuevaColumna < self.kitchen.columnas:
            self.columna = nuevaColumna
        
        self.photo = cargarImagen(f"personaje{self.personaje}{self.face}.gif")
        self.label.config(image=self.photo)
        self.label.image = self.photo
        self.actualizarPosicion()

    def interactuar(self):

        fila = self.fila
        columna = self.columna

        if self.face == "arriba":
            fila -= 1

        elif self.face == "abajo":
            fila += 1

        elif self.face == "izquierda":
            columna -= 1

        elif self.face == "derecha":
            columna += 1

        if (
            0 <= fila < self.kitchen.filas
            and
            0 <= columna < self.kitchen.columnas
        ):

            obj = self.kitchen.matriz[fila][columna]

            if obj is not None:
                obj.interactuar(self)
                self.kitchen.actualizarBolsos()






# ==================== Recetas ====================

recetasFrances = [Receta("Estofado Francés",[Proteinas("res"),Vegetales_Y_Frutas("papa"),Vegetales_Y_Frutas("zanahoria")],100,60),
                  Receta("Sopa de Remolacha",[Vegetales_Y_Frutas("remolacha")],50,30)]

recetasVolador = [Receta("Pollo con Arroz Volador",[Granos("arroz"),Proteinas("pollo")],80,50),
                  Receta("Cerdo con Zanahoria",[Proteinas("cerdo"),Vegetales_Y_Frutas("zanahoria")],90,50),
                  Receta("Carne con Papas",[Proteinas("vaca"),Vegetales_Y_Frutas("papa")],120,60)]

recetasLaCosta = [Receta("Parrillada de la Costa",[Proteinas("cerdo"),Proteinas("vaca"),Proteinas("res"),Proteinas("pollo")],250,90),
                  Receta("Ensalada de Raices",[Vegetales_Y_Frutas("zanahoria"),Vegetales_Y_Frutas("remolacha"),Vegetales_Y_Frutas("papa")],150,60),
                  Receta("Arroz con Fideos",[Granos("arroz"),Granos("fideos")],120,50),
                  Receta("Arroz con Cerdo Costeño",[Granos("arroz"),Proteinas("cerdo"),Vegetales_Y_Frutas("zanahoria")],180,70)]





def main():
    game = CrazySnackRushGame()
    game.run()
main()