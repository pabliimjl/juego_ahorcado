import pygame
from idioma import *
from pantalla_juego import PantallaJuego
from pantalla_puntaje import PantallaPuntaje

class PantallaInicio():
    def __init__(self, window, running):
        self.window = window
        self.running = running
        self.inicializar_variables()
        self.iniciar_bucle_principal()

    def iniciar_bucle_principal(self):
        while self.running:
            self.window.blit(self.fondo,self.window.get_rect())
            self.window.blit(self.imagen_ahorcado,(520,150))
            self.window.blit(self.imagen_sonido,(375,40)) if self.play_music else self.window.blit(self.imagen_mute,(375,40))
            

            self.crear_botones()
            self.actualizar_pantalla()
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if self.boton_iniciar.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        PantallaJuego(self.window,running = True, idioma=self.idioma,play_music=self.play_music)
                    if self.boton_salir.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        self.running = False
                    if self.boton_idioma.collidepoint(event.pos):
                        self.cambiar_idioma()
                        self.reproducir_sonido_boton()
                    if self.boton_puntaje.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        PantallaPuntaje(self.window,running=True,idioma=self.idioma,play_music=self.play_music)
                    if self.boton_sonido.collidepoint(event.pos):
                        self.reproducir_sonido_boton()
                        self.pausar_musica() if self.play_music else self.reanudar_musica()
                            

    def inicializar_variables(self):
        """Inicializacion de variables y carga de imagenes
        """        
        self.play_music = True
        self.idioma = 'ES'
        self.font = pygame.font.SysFont("Arial Narrow", 30)
        self.font_title = pygame.font.SysFont("Bradley Hand ITC", 80)

        self.fondo = pygame.image.load('imagenes_ahorcado\\fondo_inicio.jpg')
        self.fondo = pygame.transform.scale(self.fondo,(800,600))

        self.imagen_ahorcado = pygame.image.load('imagenes_ahorcado\\ahorcado_blanco.png')
        self.imagen_ahorcado = pygame.transform.scale(self.imagen_ahorcado,(150,150))

        self.imagen_mute = pygame.image.load("imagenes_ahorcado\\volume_off.png")
        self.imagen_mute = pygame.transform.scale(self.imagen_mute,(50,50))

        self.imagen_sonido = pygame.image.load("imagenes_ahorcado\\volume_on.png")
        self.imagen_sonido = pygame.transform.scale(self.imagen_sonido,(50,50))

        self.boton_sonido = pygame.draw.rect(self.window,(232, 234, 237),(375,40,50,50))
        self.boton_iniciar = pygame.draw.rect(self.window,(232, 234, 237), (142, 400, 50, 50))
        self.boton_puntaje = pygame.draw.rect(self.window,(232, 234, 237), (375, 400, 50, 50))
        self.boton_salir = pygame.draw.rect(self.window,(232, 234, 237), (609, 400, 50, 50))


        self.logo_iniciar = pygame.image.load("imagenes_ahorcado\\logo_jugar.png")
        self.logo_iniciar = pygame.transform.scale(self.logo_iniciar,(50,50))

        self.logo_puntaje_social = pygame.image.load("imagenes_ahorcado\\logo_puntaje_social.png")
        self.logo_puntaje_social = pygame.transform.scale(self.logo_puntaje_social,(50,50))

        self.logo_puntaje = pygame.image.load("imagenes_ahorcado\\logo_puntaje.png")
        self.logo_puntaje = pygame.transform.scale(self.logo_puntaje_social,(50,50))

        self.logo_salir = pygame.image.load("imagenes_ahorcado\\logo_salir.png")
        self.logo_salir = pygame.transform.scale(self.logo_salir,(50,50))
        

        pygame.mixer.music.load("musica_ahorcado\\background.mp3")
        pygame.mixer.music.set_volume(0.45)
        pygame.mixer.music.play(-1)

        self.sonido_boton = pygame.mixer.Sound("musica_ahorcado\\sonido_boton.mp3")

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

    def reproducir_sonido_boton(self):
        """Reproduce un sonido de click
        """         
        self.sonido_boton.play()

    def cambiar_idioma(self):
        """Cambia el idioma en que se muestra el juego
        """        
        if self.idioma == 'ES':
            self.idioma = 'EN'
        elif self.idioma == 'EN':
            self.idioma = 'BR'
        else:
            self.idioma = 'ES'

    def crear_botones(self):
        """Crea los botones y texto de la pantalla de inicio
        """        
        self.texto_el = self.font_title.render(f'{BOTONES[10][self.idioma]}',True,(232, 234, 237))
        self.texto_ahorcado = self.font_title.render(f'{BOTONES[11][self.idioma]}',True,(232, 234, 237))
        self.window.blit(self.texto_el,(160,130))
        self.window.blit(self.texto_ahorcado,(160,230))
        

        self.rect_logo_iniciar = self.logo_iniciar.get_rect()
        self.rect_logo_iniciar.center = self.boton_iniciar.center
        self.window.blit(self.logo_iniciar,self.rect_logo_iniciar)

        self.rect_logo_puntaje = self.logo_puntaje.get_rect()
        self.rect_logo_puntaje.center = self.boton_puntaje.center
        self.window.blit(self.logo_puntaje,self.rect_logo_puntaje)

        self.rect_logo_salir = self.logo_salir.get_rect()
        self.rect_logo_salir.center = self.boton_salir.center
        self.window.blit(self.logo_salir,self.rect_logo_salir)


        self.box_texto_iniciar = pygame.draw.rect(self.window,(232, 234, 237), (167, 470, 0, 0))
        self.box_texto_puntaje = pygame.draw.rect(self.window,(232, 234, 237), (400, 470, 0, 0))
        self.box_texto_salir = pygame.draw.rect(self.window,(232, 234, 237), (634, 470, 0, 0))

        self.texto_iniciar = self.font.render(f"{BOTONES[0][self.idioma]}", True, (232, 234, 237))
        self.boton_volumen = self.imagen_sonido.get_rect()

        self.rect_texto_iniciar = self.texto_iniciar.get_rect()
        self.rect_texto_iniciar.center = self.box_texto_iniciar.center
        self.window.blit(self.texto_iniciar,self.rect_texto_iniciar)

        self.texto_puntaje = self.font.render(f"{BOTONES[1][self.idioma]}", True, (232, 234, 237))

        self.rect_texto_puntaje = self.texto_puntaje.get_rect()
        self.rect_texto_puntaje.center = self.box_texto_puntaje.center

        self.window.blit(self.texto_puntaje,self.rect_texto_puntaje)

        self.texto_salir = self.font.render(f"{BOTONES[2][self.idioma]}", True, (232, 234, 237))
        self.rect_texto_salir = self.texto_salir.get_rect()
        self.rect_texto_salir.center = self.box_texto_salir.center
        self.window.blit(self.texto_salir,self.rect_texto_salir) #(650, 10, 50, 50)
        self.boton_idioma = pygame.draw.rect(self.window, (6, 27, 30), (724, 45, 42, 40),border_radius=8)
        self.texto_boton_idioma = self.font.render(f"{BOTONES[4][self.idioma]}",True,(232, 234, 237))
        self.rect_texto_boton_idioma = self.texto_boton_idioma.get_rect()
        self.rect_texto_boton_idioma.center = self.boton_idioma.center
        self.window.blit(self.texto_boton_idioma,self.rect_texto_boton_idioma)
        self.texto_idioma = self.font.render(f"{BOTONES[3][self.idioma]}",True,(232, 234, 237))
        self.window.blit(self.texto_idioma,(570,55))

    def actualizar_pantalla(self):
        """Actualiza la pantalla
        """        
        pygame.display.update()
        pygame.display.flip()