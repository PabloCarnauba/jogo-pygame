import pygame
import random
import time

pygame.init()

# Definindo as dimensões da tela
x = 1280
y = 720

screen = pygame.display.set_mode((x, y))
pygame.display.set_caption("Meu primeiro jogo em Pygame")

# Carregando as imagens
img = pygame.image.load('JogoPygame/cenário.jpg').convert_alpha()
img = pygame.transform.scale(img, (x, y))

alien = pygame.image.load('JogoPygame/naveY.png').convert_alpha()
alien = pygame.transform.scale(alien, (50, 50))

player = pygame.image.load('JogoPygame/naveX.png').convert_alpha()
player = pygame.transform.scale(player, (50, 50))
player = pygame.transform.rotate(player, -90)

missilPNG = pygame.image.load('JogoPygame/míssil.png').convert_alpha()
missilPNG = pygame.transform.scale(missilPNG, (25, 25))

# Posições iniciais
PosAlienX = 1280
PosAlienY = random.randint(1, 640)

PosPlayerX = 200
PosPlayerY = 300

missilList = []

# Variáveis de pontuação
pontos = 1
font = pygame.font.Font(None, 36)

# Função respawn para alienígena
def respawn():
    x = 1280
    y = random.randint(1, 640)
    return [x, y]

backgroundX = 0
rodando = True
velocidadeAlien = 5  # Velocidade inicial do alien

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not missilList:
                # Adiciona um míssil na posição do jogador
                missilList.append([PosPlayerX + 50, PosPlayerY + 25])

    screen.blit(img, (0, 0))

    realX = backgroundX % img.get_rect().width
    screen.blit(img, (realX - img.get_rect().width, 0))  # cria background
    if realX < 1200:
        screen.blit(img, (realX, 0))

    # Teclas
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_UP] and PosPlayerY > 1:
        PosPlayerY -= 5
    if tecla[pygame.K_DOWN] and PosPlayerY < 665:
        PosPlayerY += 5

    # Respawn alienígena
    if PosAlienX < -50:
        pontos -= 1
        PosAlienX, PosAlienY = respawn()

    # Movimento
    backgroundX -= 2
    PosAlienX -= velocidadeAlien

    # Movimento dos mísseis
    for missil in missilList:
        missil[0] += 10  # Velocidade do míssil
        if missil[0] > x:
            missilList.remove(missil)

    # Colisões
    playerRect = pygame.Rect(PosPlayerX, PosPlayerY, player.get_width(), player.get_height())
    alienRect = pygame.Rect(PosAlienX, PosAlienY, alien.get_width(), alien.get_height())

    for missil in missilList:
        missilRect = pygame.Rect(missil[0], missil[1], missilPNG.get_width(), missilPNG.get_height())
        if missilRect.colliderect(alienRect):
            missilList.remove(missil)
            PosAlienX, PosAlienY = respawn()
            pontos += 1
            velocidadeAlien += 0.5  # Aumenta a velocidade do alien a cada ponto

    if playerRect.colliderect(alienRect):
        pontos -= 1
        PosAlienX, PosAlienY = respawn()

    # Exibir pontuação
    textoPontos = font.render(f"Pontos: {pontos}", True, (255, 255, 255))
    screen.blit(textoPontos, (10, 10))

    # Condições de vitória/derrota
    if pontos >= 10:
        textoVitoria = font.render("You Win", True, (0, 0, 0))  # Preto
        screen.blit(textoVitoria, (x // 2 - textoVitoria.get_width() // 2, y // 2 - textoVitoria.get_height() // 2))
        pygame.display.update()
        time.sleep(3)
        rodando = False
    elif pontos <= 0:
        textoDerrota = font.render("Game Over", True, (255, 0, 0))  # Vermelho
        screen.blit(textoDerrota, (x // 2 - textoDerrota.get_width() // 2, y // 2 - textoDerrota.get_height() // 2))
        pygame.display.update()
        time.sleep(3)
        rodando = False

    # Criar imagens
    screen.blit(alien, (PosAlienX, PosAlienY))
    screen.blit(player, (PosPlayerX, PosPlayerY))

    for missil in missilList:
        screen.blit(missilPNG, (missil[0], missil[1]))

    pygame.display.update()

pygame.quit()