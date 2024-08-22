import pygame
import math
import constantes

class Weapon:
    def __init__(self, image, imagen_bala):
        self.imagen_bala = imagen_bala
        self.imagen_original = image
        self.angulo = 0
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.forma = self.image.get_rect()
        self.disparada = False
        self.ultimo_disparo = 0  # Inicialización de la variable

    def update(self, personaje):
        disparo_cooldown = constantes.COOLDOWN
        # Centrar el arma en el personaje
        self.forma.center = personaje.forma.center

        # Ajustar posición del arma basado en el flip del personaje
        if personaje.flip:
            self.forma.x -= personaje.forma.width / 5
        else:
            self.forma.x += personaje.forma.width / 5

        # Rotar el arma hacia el mouse
        self.angulo = self.calcular_angulo()
        self.rotar_arma(personaje.flip)

        # Inicializar la bala como None
        bala = None

        # Detectar click del mouse y crear bala
        if pygame.mouse.get_pressed()[0] and not self.disparada:
            angulo_disparo = self.angulo
            if personaje.flip:
                angulo_disparo = 180 - self.angulo  # Ajuste del ángulo si el personaje está volteado

            bala = Bullet(self.imagen_bala, self.forma.centerx, self.forma.centery, angulo_disparo)
            self.disparada = True
            self.ultimo_disparo = pygame.time.get_ticks()  # Actualización del tiempo de disparo

        # Resetear el click del mouse después de un cooldown
        if not pygame.mouse.get_pressed()[0] and (pygame.time.get_ticks() - self.ultimo_disparo >= disparo_cooldown):
            self.disparada = False
        
        return bala
            
    def dibujar(self, interfaz):
        interfaz.blit(self.image, self.forma)

    def calcular_angulo(self):
        # Obtener la posición del mouse
        mouse_pos = pygame.mouse.get_pos()
        diferencia_x = mouse_pos[0] - self.forma.centerx
        diferencia_y = -(mouse_pos[1] - self.forma.centery)
        
        # Calcular el ángulo en grados
        angulo = math.degrees(math.atan2(diferencia_y, diferencia_x))
        return angulo

    def rotar_arma(self, flip):
        # Rotar y voltear la imagen del arma
        imagen_flip = pygame.transform.flip(self.imagen_original, flip, False)
        self.image = pygame.transform.rotate(imagen_flip, self.angulo)
        self.forma = self.image.get_rect(center=self.forma.center)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.imagen_original = image
        self.angulo = angle
        self.image = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Calcular el vector de movimiento
        self.delta_x = math.cos(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA
        self.delta_y = -math.sin(math.radians(self.angulo)) * constantes.VELOCIDAD_BALA

    def update(self):
        # Mover la bala
        self.rect.x += self.delta_x
        self.rect.y += self.delta_y
        
        # Verificar si la bala sale de la pantalla
        if self.rect.right < 0 or self.rect.left > constantes.ANCHO_VENTANA or \
           self.rect.bottom < 0 or self.rect.top > constantes.ALTO_VENTANA:
            self.kill()  # Eliminar la bala del grupo de sprites

    def dibujar(self, interfaz):
        interfaz.blit(self.image, (self.rect.centerx, self.rect.centery - int(self.image.get_height() / 2)))
