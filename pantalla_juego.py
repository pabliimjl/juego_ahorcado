import pygame
import pygame_textinput
from biblioteca import *
import time
import random
from idioma import BOTONES

class PantallaJuego():
    def __init__(self, window, running, idioma, play_music):
        self.window = window
        self.running = running
        self.idioma = idioma
        self.play_music = play_music
        self.cargar_sonidos()        
        self.inicializar_variables()
        self.abrir_imagenes()
        self.abrir_archivo()
        self.obtener_palabra()
        self.iniciar_bucle_principal()

    def iniciar_bucle_principal(self):
        """Bucle principal del juego
        """        
        while self.running:
            self.window.blit(self.fondo_ahorcado, self.window.get_rect())
            
            self.events = pygame.event.get()
            if len(self.textinput.value) < 1 or self.bandera_juego_en_curso == False:
                self.textinput.update(self.events)

            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_sonido.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        self.pausar_musica() if self.play_music else self.reanudar_musica()
                    if self.boton_menu.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        self.running = False
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.textinput.update(self.events)
                if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.KSCAN_RETURN) and self.textinput.value != "":

                    if self.bandera_juego_en_curso == False:
                        self.nombre_a_guardar = self.textinput.value
                        self.running = False
                    else:    
                        self.validacion = self.verificar_letra_en_palabra(self.palabra, self.textinput.value,self.palabra_secreta)

                        if self.validacion != False:
                            self.palabra_secreta = self.validacion
                        else:
                            self.reproducir_tiza_corto()
                            self.contador_errores += 1
                        if self.validacion == self.palabra and self.bandera_juego_en_curso:
                            self.procesar_ganaste()
                        if self.contador_errores == 6:
                            self.procesar_perdiste()
                        self.textinput.value = ""

            if self.palabra == False:
                self.finalizar_juego()

            if self.bandera_juego_en_curso:
                self.dibujar_pantalla_juego_en_curso()
                
            self.dibujar_palabra_secreta()

            pygame.display.update()

            pygame.display.flip()

        if not self.bandera_juego_en_curso:
            self.guardar_json_puntaje()

    def cargar_sonidos(self):
        """Carga los sonidos a utilizarse en la pantalla
        """        
        self.sonido_boton = pygame.mixer.Sound("musica_ahorcado\\sonido_boton.mp3")
        self.sonido_ganador = pygame.mixer.Sound("musica_ahorcado\\sonido_ganador.mp3")
        self.sonido_perdedor = pygame.mixer.Sound("musica_ahorcado\\sonido_perdedor.mp3")
        self.sonido_tiza_corto = pygame.mixer.Sound("musica_ahorcado\\sonido_tiza_corto.mp3")

    def abrir_archivo(self):
        """Abre el archivo con las soluciones y crea la lista de palabras
        """        
        self.ahorcado = abrir_json('datos.json','ahorcado')
    
    def abrir_imagenes(self):
        """Abre las imagenes e iconos a utilizarse en la pantalla
        """        
        self.imagen_mute = pygame.image.load("imagenes_ahorcado\\volume_off.png")
        self.imagen_mute = pygame.transform.scale(self.imagen_mute,(50,50))
        self.imagen_sonido = pygame.image.load("imagenes_ahorcado\\volume_on.png")
        self.imagen_sonido = pygame.transform.scale(self.imagen_sonido,(50,50))
        self.boton_sonido = pygame.draw.rect(self.window,(232, 234, 237),(375,0,50,50))
        self.imagen_home = pygame.image.load("imagenes_ahorcado\\home.png")
        self.imagen_home = pygame.transform.scale(self.imagen_home,(50,50))
        self.boton_menu = pygame.draw.rect(self.window, (232, 234, 237), (720, 40, 50, 50))
        self.fondo_ahorcado = pygame.image.load('imagenes_ahorcado\\fondo_inicio.jpg')
        self.fondo_ahorcado = pygame.transform.scale(self.fondo_ahorcado,(800,600))
    
    def reproducir_sonido_boton(self):
        """Reproduce un sonido de click
        """        
        self.sonido_boton.play()

    def reproducir_sonido_ganador(self):
        """Reproduce sonido predefinido para cuando se gana
        """        
        self.sonido_ganador.play()

    def reproducir_sonido_perdedor(self):
        """Reproduce sonido predefinido cuando se pierde
        """        
        self.sonido_perdedor.play()

    def inicializar_variables(self):
        """Inicializacion de variables
        """        
        self.palabra_secreta = ""
        self.bandera_nombre = True
        self.posicion_text_input = (130, 52)
        self.contador_errores = 0
        self.puntaje = 0
        self.letra = ""
        self.bandera_juego_en_curso = True
        self.lista_palabras_usadas = []  
        self.font = pygame.font.SysFont("Arial Narrow", 40)
        self.font1 = pygame.font.SysFont("Arial Narrow", 80)    
        self.textinput = pygame_textinput.TextInputVisualizer(font_color=(232, 234, 237), cursor_color=(232, 234, 237))

    def dibujar_palabra_secreta(self):
        """Dibuja la palabra secreta
        """        
        self.texto_palabra_secreta = self.font1.render(f"{self.palabra_secreta}", True, (255, 255, 255))
        self.rect_texto_palabra_secreta = self.texto_palabra_secreta.get_rect()
        self.rect_texto_palabra_secreta.center = self.box_palabra_secreta.center
        self.window.blit(self.texto_palabra_secreta,self.rect_texto_palabra_secreta)

    def dibujar_pantalla_juego_en_curso(self):
        """Dibuja la pantalla del juego mientras se esta en curso
        """
        self.window.blit(self.textinput.surface, self.posicion_text_input)
        self.window.blit(self.imagen_sonido,(375,40)) if self.play_music else self.window.blit(self.imagen_mute,(375,40)) 
        self.window.blit(self.imagen_home,(720,40))
        self.texto_puntaje = self.font.render(f"{BOTONES[5][self.idioma]} {self.puntaje}", True, (255, 255, 255))
        self.box_palabra_secreta = pygame.draw.rect(self.window,('white'),(225,390,0,0))
        self.texto_letra = self.font.render(f"{BOTONES[6][self.idioma]} {self.letra}", True, (255, 255, 255))
        self.window.blit(self.texto_puntaje,(500,50))
        self.window.blit(self.texto_letra,(30,50))
        self.imagen_ahorcado = pygame.image.load(f'imagenes_ahorcado\\ahorcado_{self.contador_errores}.png')
        self.imagen_ahorcado = pygame.transform.scale(self.imagen_ahorcado,(150,150))
        self.window.blit(self.imagen_ahorcado,(550,250))

    def finalizar_juego(self):
        """Dibuja la pantalla al finalizar todas las palabras
        """
        self.bandera_juego_en_curso = False
        self.texto_ingrese_nombre = self.font.render(f'{BOTONES[13][self.idioma]}',True,(232, 234, 237))
        self.box_texto_ingrese_nombre = pygame.draw.rect(self.window,('white'),(400,200,0,0))
        self.rect_texto_ingrese_nombre = self.texto_ingrese_nombre.get_rect()
        self.rect_texto_ingrese_nombre.center = self.box_texto_ingrese_nombre.center
        self.window.blit(self.texto_ingrese_nombre, self.rect_texto_ingrese_nombre)
        self.box_palabra_secreta = pygame.draw.rect(self.window,('white'),(400,300,0,0))
        self.box_textinput = pygame.draw.rect(self.window,('white'),(400,230,0,0))
        self.rect_textinput = self.textinput.surface.get_rect()
        self.rect_textinput.center = self.box_textinput.center
        self.window.blit(self.textinput.surface,self.rect_textinput)

    def procesar_ganaste(self):
        """Serie de ejecuciones que se realizan cuando se acierta una palabra
        """
        self.reproducir_sonido_ganador()
        self.puntaje += len(self.palabra)
        self.texto_ganaste = self.font.render(f'{BOTONES[8][self.idioma]}',True,(232, 234, 237))
        self.box_ganaste = pygame.draw.rect(self.window,(232, 234, 237),(400,300,0,0))
        self.rect_texto_ganaste = self.texto_ganaste.get_rect()
        self.rect_texto_ganaste.center = self.box_ganaste.center
        self.window.blit(self.texto_ganaste,self.rect_texto_ganaste)
        pygame.display.flip()
        time.sleep(2)
        self.obtener_palabra()
        self.contador_errores = 0

    def procesar_perdiste(self):
        """Serie de ejecuciones que se realizan cuando te quedaste sin intentos para adivinar la palabra
        """        

        self.imagen_ahorcado = pygame.image.load(f'imagenes_ahorcado\\ahorcado_{6}.png')
        self.imagen_ahorcado = pygame.transform.scale(self.imagen_ahorcado,(150,150))
        self.window.blit(self.imagen_ahorcado,(550,250))
        self.reproducir_sonido_perdedor()
        self.texto_perdiste = self.font.render(f'{BOTONES[9][self.idioma]}',True,(232, 234, 237))
        self.box_perdiste = pygame.draw.rect(self.window,(232, 234, 237),(400,300,0,0))
        self.rect_texto_perdiste = self.texto_perdiste.get_rect()
        self.rect_texto_perdiste.center = self.box_perdiste.center
        self.window.blit(self.texto_perdiste,self.rect_texto_perdiste)
        pygame.display.flip()
        time.sleep(2)                
        self.obtener_palabra()
        self.contador_errores = 0
        self.bandera_perder = False
        self.bandera_perder = True

    def guardar_json_puntaje(self):
        """Agrega el nombre y el puntaje del jugador al archivo con el historial de jugadores
        """        
        self.lista_jugadores = abrir_json('puntaje.json','jugadores')
        self.lista_jugadores.append({'nombre':self.nombre_a_guardar,'puntaje':self.puntaje})
        guardar_json('puntaje.json','jugadores',self.lista_jugadores)

    def obtener_palabra(self):
        """Obtiene una palabra random
        """        
        self.palabra = self.obtener_palabra_random(self.ahorcado, self.idioma)
        self.palabra_secreta = self.slot_palabra(self.palabra)
    
    def reproducir_tiza_corto(self):
        """Reproduce sonido predefinido para cuando se dibuja una parte del cuerpo del ahorcado
        """        
        self.sonido_tiza_corto.play()

    def obtener_palabra_random(self, lista:list, idioma:list)->str:
        """Obtiene una palabra random de una lista de diccionarios de palabras

        Args:
            lista (list): lista de palabras
            idioma (str): clave del idioma en el que esta el juego

        Returns:
            str: palabra random obtenida
        """        
        palabra = random.choice(lista)

        if len(self.lista_palabras_usadas) == len(lista):
            palabra = False

        else:
            while palabra["id"] in self.lista_palabras_usadas:
                palabra = random.choice(lista)

            self.lista_palabras_usadas.append(palabra["id"])

            palabra = palabra[idioma]
        
        return palabra

    def slot_palabra(self, palabra:str)->str:
        """Genera la palabra codificada en guiones para el juego. EJ: Ahorcado -> --------

        Args:
            palabra (str): palabra a codificar

        Returns:
            str: palabra codificada
        """        
        retorno = ""

        if palabra == False:
            retorno = "Juego Terminado"
        else:
            for letra in palabra:
                retorno += "-"

        return retorno

    def verificar_letra_en_palabra(self, palabra:str, ingreso:str ,palabra_secreta:str):
        """Comprueba si la letra ingresada esta en la palabra a adivinar, y en caso de estar reemplaza el guion correspondiente de la palabra codificada con la letra adivinada.

        Args:
            palabra (str): palabra a adivinar
            ingreso (str): letra ingresada
            palabra_secreta (str): palabra codificada

        Returns:
            _type_: palabra codificada con la letra reemplazada. En caso de no estar la letra devuelve falso
        """        
        
        bandera_cambio = False

        lista_palabra_secreta = []

        for letra in palabra_secreta:
            lista_palabra_secreta.append(letra)

        if len(ingreso) == 1:
            for i in range(len(palabra)):
                if palabra[i] == ingreso:
                    lista_palabra_secreta[i] = ingreso
                    bandera_cambio = True

        palabra_final = ""
        for letra in lista_palabra_secreta:
            palabra_final += letra


        return palabra_final if bandera_cambio == True else False

    def pausar_musica(self):
        """Pausa la musica de fondo
        """        
        self.play_music = False
        pygame.mixer.music.pause()

    def reanudar_musica(self):
        """Reanuda la musica de fondo
        """        
        self.play_music = True
        pygame.mixer.music.unpause()
