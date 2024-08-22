import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
import os 

# Escalar imagen 
def escalar_img(image, scale):
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (int(w * scale), int(h * scale)))
    return nueva_imagen

# Función para contar elementos
def contar_elementos(directorio):
    return len(os.listdir(directorio))

# Función listar nombres de carpetas 
def nombres_carpetas(directorio):
    return os.listdir(directorio)

print(contar_elementos("juego_pygamee/assets/images/characters/enemies/"))

pygame.init()

# Creación de la ventana del juego
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA, constantes.ALTO_VENTANA))
pygame.display.set_caption("Jueguito kokoa")

# Arma
imagen_pistola = pygame.image.load("juego_pygamee/assets/images/characters/weapons/gun.png").convert_alpha()
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARM)

# Balas
imagen_balas = pygame.image.load("juego_pygamee/assets/images/characters/weapons/bullet.png").convert_alpha()
imagen_balas = escalar_img(imagen_balas, constantes.SCALA_ARM)

# Cargar animaciones del personaje principal
animaciones = []
for i in range(7):
    img = pygame.image.load(f"C:\\Users\\Home\\Desktop\\ejemplo\\juego_pygamee\\assets\\images\\characters\\personaje\\Player_{i}.png").convert_alpha()
    img = escalar_img(img, constantes.SCALA_PER)
    animaciones.append(img)

# Enemigos
directorio_enemigos = "juego_pygamee/assets/images/characters/enemies/"
tipo_enemigos = nombres_carpetas(directorio_enemigos)
print(f"enemigos: {tipo_enemigos}")
animaciones_enemigos = []
for eni in tipo_enemigos:
    lista_temp = []
    ruta_temp = f"juego_pygamee/assets/images/characters/enemies/{eni}"
    num_animaciones = contar_elementos(ruta_temp)
    for i in range(num_animaciones):
        img_enemigo = pygame.image.load(os.path.join(ruta_temp, f"{eni}_{i+1}.png")).convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.ENEMIGOS)
        lista_temp.append(img_enemigo)
    animaciones_enemigos.append(lista_temp)

print(animaciones_enemigos)

# Creación del personaje
jugador = Personaje(50, 50, animaciones)

# Crear enemigos
demonio = Personaje(400, 300, animaciones_enemigos[0])
hongo = Personaje(200, 200, animaciones_enemigos[1])
demonio_2 = Personaje(100, 250, animaciones_enemigos[0])

# Crear lista de enemigos
lista_enemigos = [demonio, demonio_2, hongo]
print(lista_enemigos)

# Creación del arma
arma = Weapon(imagen_pistola, imagen_balas)

# Crear un grupo de sprites para las balas
grupo_balas = pygame.sprite.Group()

# Variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

# Crear un objeto de reloj para controlar el FPS
reloj = pygame.time.Clock()

# Bucle principal del juego
run = True
while run:
    # Controla el número de FPS
    reloj.tick(constantes.FPS)
    # Rellena el fondo de la ventana
    ventana.fill(constantes.COLOR_BG)

    # Calcular el movimiento del jugador
    delta_x = 0
    delta_y = 0

    # Mover el jugador en la dirección deseada
    if mover_derecha:
        delta_x = constantes.VELOCIDAD
    if mover_izquierda:
        delta_x = -constantes.VELOCIDAD
    if mover_arriba:
        delta_y = -constantes.VELOCIDAD
    if mover_abajo:
        delta_y = constantes.VELOCIDAD

    # Actualizar la posición del jugador
    jugador.movimiento(delta_x, delta_y)

    # Actualizar el jugador (animaciones, etc.)
    jugador.update()

    # Actualizar y dibujar los enemigos
    for enemigo in lista_enemigos:
        enemigo.update()
        enemigo.dibujar(ventana)

    # Actualizar el arma y manejar las balas
    bala = arma.update(jugador)
    if bala:
        grupo_balas.add(bala)

    # Actualizar todas las balas en el grupo
    grupo_balas.update()

    # Dibujar el jugador en la ventana
    jugador.dibujar(ventana)

    # Dibujar el arma
    arma.dibujar(ventana)

    # Dibujar las balas
    for bala in grupo_balas:
        bala.dibujar(ventana)

    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False

    # Actualizar la pantalla
    pygame.display.update()

pygame.quit()
