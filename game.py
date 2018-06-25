# Importando modulos
import pygame
import random

# Iniciando o pygame
pygame.init()

# Alterando a resolução do display
tela_info = pygame.display.Info()
w, h = tela_info.current_w, tela_info.current_h

if h >= 900:
	width, height = 500, 800
	escala = 1

if h < 900 and h >= 500:
	width, height = 375, 600
	escala = 0.75

if h < 500 and h >= 300:
	width, height = 300, 400
	escala = 0.5

if h < 300:
	print('As configurações de video não são suportaveis.')
	pygame.quit()

# Iniciando o display
tela = pygame.display.set_mode([width , height])
pygame.display.set_caption('Speed Py')

# Carregando imagens e sons e alterando sua escala
carro1 = pygame.transform.scale(pygame.image.load('carro1.png'), [int(80 * escala), int(150 * escala)])
carro2 = pygame.transform.scale(pygame.image.load('carro2.png'), [int(80 * escala), int(150 * escala)])
carro3 = pygame.transform.scale(pygame.image.load('carro3.png'), [int(80 * escala), int(150 * escala)])
pista1 = pygame.transform.scale(pygame.image.load('pista1.png'), [int(500 * escala), int(560 * escala)])
img001 = pygame.transform.scale(pygame.image.load('001.png'), [int(500 * escala), int(800 * escala)])

# Adicionando imagens as variaveis para seleção de veiculos
obstaculo1 = (carro1, carro2, carro3)
player = (carro1, carro2, carro3)
obstaculo1_cor = 0

# Game over
def gameover(pontos):
	tela.fill([0, 0, 0])
	font = pygame.font.Font('geo.ttf', int(20 * escala))
	text = font.render(str('Game Over'), True, [255, 255, 255])
	text2 = font.render(str(pontos), True, [255, 255, 255])
	tela.blit(text, [int(70 * escala), int(380 * escala)])
	tela.blit(text2, [int(70 * escala), int(480 * escala)])
	pygame.display.update()
	pygame.time.wait(5000)

# Introdução do game
def introducao():
	global player_cor
	intro = True
	while intro:
		tela.fill([255, 255, 255])
		font = pygame.font.Font('geo.ttf', int(20 * escala))
		text = font.render(str('Bem vindo!'), True, [0,0,0])
		text2 = font.render(str('Selecione um carro:'), True, [0,0,0])
		tela.blit(text, [int(70 * escala), int(380 * escala)])
		tela.blit(text2, [int(70 * escala), int(480 * escala)])
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					player_cor = 0
					intro = False

				if event.key == pygame.K_2:
					player_cor = 1
					intro = False

				if event.key == pygame.K_3:
					player_cor = 2
					intro = False

# Desenha a pontuação na tela
def pontuacao(pontos):
    font = pygame.font.Font('geo.ttf', 20)
    text = font.render(str(pontos), True, [255,255,255])
    text2 = font.render(str('Score:'), True, [255, 0, 255])
    tela.blit(text2, [30, 10])
    tela.blit(text, [120, 10])

# Iniciando variaveis
player_x, player_y = int(225 * escala), int(600 * escala)
obstaculo1_x, obstaculo1_y = int(20 * escala), int(-154 * escala)
x = 0
y = 0
pontos = 0

# Permitido entrada de comando com tecla pressionada
pygame.key.set_repeat(1, 1)

# Exibe logo do game
tela.blit(img001, [0, 0])
pygame.display.update()
pygame.time.wait(3000)


introducao()

# Loop principal
running = True
while running:
	# Declarando o FPS
	clock = pygame.time.Clock()
	clock.tick(60)
	velocidade = int(10 * escala)

	# Capturando movimentos
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_a:
				player_x -= int(10 * escala)

			if event.key == pygame.K_d:
				player_x += int(10 * escala)

			if event.key == pygame.K_w:
				velocidade = int(20 * escala)

	# Criando retangulos de colisão
	player_area = pygame.Rect(player_x, player_y, int(80 * escala), int(150 * escala))
	obstaculo1_area = pygame.Rect(obstaculo1_x, obstaculo1_y, int(68 * escala), int(145 * escala))

	# Detectando colisão entre carros
	if player_area.colliderect(obstaculo1_area):
		print('Game Over!')
		gameover(pontos)
		running = False

	# Limitando colisão laterais da tela
	if player_x <= int(20 * escala):
		player_x = int(20 * escala)

	if player_x >= int(400 * escala):
		player_x = int(400 * escala)

	# Desenhando na tela
	tela.fill([0, 0, 0])	
	tela.blit(pista1, [x, y - int(560 * escala)])
	tela.blit(pista1, [x, y])
	tela.blit(pista1, [x, y + int(560 * escala)])
	pontuacao(pontos)
	y += velocidade

	if y >= int(560 * escala):
		y = 0
		pontos += 1

	# Desenha carros na tela	
	tela.blit(obstaculo1[obstaculo1_cor], obstaculo1_area)
	tela.blit(player[player_cor], player_area)

	obstaculo1_y += velocidade / 2
	if obstaculo1_y >= int(800 * escala):
		obstaculo1_y = int(-154 * escala)
		obstaculo1_x = random.randint(int(20 * escala), int(400 * escala))
		obstaculo1_cor = random.randint(0, 2)

	pygame.display.update()

# Encerra o pygame
pygame.quit()