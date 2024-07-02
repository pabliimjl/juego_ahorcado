import pygame
from biblioteca import *
from idioma import BOTONES

class PantallaPuntaje():
    def __init__(self,window,running,idioma, play_music):
        self.window = window
        self.running = running
        self.idioma = idioma
        self.cargar_json()
        self.ordenar_lista()
        self.play_music = play_music
        self.inicializar_variables()
        self.iniciar_bucle_principal()


    def iniciar_bucle_principal(self):
        while self.running:
            self.window.blit(self.fondo,self.window.get_rect())
            self.window.blit(self.imagen_home,(720,40))
            self.window.blit(self.imagen_sonido,(375,40)) if self.play_music else self.window.blit(self.imagen_mute,(375,40))
            self.dibujar_texto_puntaje()
            self.dibujar_tabla()
            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.boton_sonido.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        self.pausar_musica() if self.play_music else self.reanudar_musica()

                    if self.boton_menu.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        self.running = False
                        
            pygame.display.update()
            pygame.display.flip()

    def dibujar_texto_puntaje(self):
        """Dibuja el encabezado de la pantalla de puntaje
        """        
        self.texto_puntaje = self.font.render(f"{BOTONES[1][self.idioma]}",True,(232, 234, 237))
        self.box_texto_puntaje = pygame.draw.rect(self.window,(232, 234, 237),(400,150,0,0))
        self.rect_texto_puntaje = self.texto_puntaje.get_rect()
        self.rect_texto_puntaje.center = self.box_texto_puntaje.center
        self.window.blit(self.texto_puntaje,self.rect_texto_puntaje)

    def inicializar_variables(self):
        """Inicializacion de variables y apertura de imagenes a utilizar en el juego
        """        
        self.fondo = pygame.image.load('imagenes_ahorcado\\fondo_inicio.jpg')
        self.fondo = pygame.transform.scale(self.fondo,(800,600))
        self.font = pygame.font.SysFont("Bradley Hand ITC", 40)
        self.sonido_boton = pygame.mixer.Sound("musica_ahorcado\\sonido_boton.mp3")
        self.imagen_mute = pygame.image.load("imagenes_ahorcado\\volume_off.png")
        self.imagen_mute = pygame.transform.scale(self.imagen_mute,(50,50))
        self.imagen_sonido = pygame.image.load("imagenes_ahorcado\\volume_on.png")
        self.imagen_sonido = pygame.transform.scale(self.imagen_sonido,(50,50))
        self.boton_sonido = pygame.draw.rect(self.window,(232, 234, 237),(375,40,50,50))
        self.imagen_home = pygame.image.load("imagenes_ahorcado\\home.png")
        self.imagen_home = pygame.transform.scale(self.imagen_home,(50,50))
        self.boton_menu = pygame.draw.rect(self.window, (232, 234, 237), (720, 40, 50, 50))

    def dibujar_tabla(self):
        """Dibuja la tabla con los nombres y puntajes de los jugadores
        """        
        self.interlineado = 80
        if len(self.lista_jugadores) >= 5:
            self.cantidad_elementos = 5
        else: 
            self.cantidad_elementos = len(self.lista_jugadores)
        for i in range(self.cantidad_elementos):
            self.texto_nombre_jugador = self.font.render(f"{self.lista_jugadores[i]['nombre']}",True,(232, 234, 237))
            self.texto_puntaje_jugador = self.font.render(f"{self.lista_jugadores[i]['puntaje']}",True,(232, 234, 237))
            self.window.blit(self.texto_nombre_jugador,(250,100+self.interlineado))
            self.window.blit(self.texto_puntaje_jugador,(500,100+self.interlineado))
            self.interlineado += 40

    def reproducir_sonido_boton(self):
        """Reproduce un sonido de click
        """      
        self.sonido_boton.play()

    def cargar_json(self):
        """Carga el archivo con el historial de jugadores
        """        
        self.lista_jugadores = abrir_json('puntaje.json','jugadores')

    def ordenar_lista(self):
        """Ordena la lista de jugadores de forma descendente por puntaje
        """        
        for i in range (len(self.lista_jugadores)-1):
            for j in range (i+1,len(self.lista_jugadores)):
                if int(self.lista_jugadores[i]['puntaje']) < int(self.lista_jugadores[j]['puntaje']):
                    auxiliar = self.lista_jugadores[i]
                    self.lista_jugadores[i] = self.lista_jugadores[j]
                    self.lista_jugadores[j] = auxiliar
    
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
