import pygame
import constantes

class Personaje:
    def __init__(self, x, y, animaciones):
        self.flip = False 
        self.animaciones = animaciones

        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]

        self.forma = self.image.get_rect()

        self.forma.center = (x, y)
        
    def movimiento(self, delta_x, delta_y):
        # Ajustar el flip basado en la dirección del movimiento
        if delta_x > 0: 
            self.flip = False  # No invertir la imagen cuando se mueve a la derecha
        elif delta_x < 0:
            self.flip = True  # Invertir la imagen cuando se mueve a la izquierda

        self.forma.x += delta_x
        self.forma.y += delta_y

    def update(self):
        cooldown_animacion = 100  # Ajusta el tiempo de espera entre cuadros de animación
        # Actualizar imagen según el índice actual del cuadro
        self.image = self.animaciones[self.frame_index]
        # Cambiar el cuadro si ha pasado suficiente tiempo
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = (self.frame_index + 1) % len(self.animaciones)  # Reinicia el índice si alcanza el final
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len (self.animaciones):
            self.frame_index= 0

    def dibujar(self, interfaz):
        # Crear una imagen invertida si flip es True
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        # Dibujar la imagen del personaje (invertida si es necesario)
        interfaz.blit(imagen_flip, self.forma.topleft)  # Usar self.forma.topleft para la posición correcta
        # Opcional: Dibujar el rectángulo alrededor del personaje (para debug)
        #pygame.draw.rect(interfaz, constantes.COLOR_PERSONAJE, self.forma, 1)  # Añadir un grosor al rectángulo para que sea visible
