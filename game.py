# Importando modulos
import pygame
import random
import os.path

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
img002 = pygame.transform.scale(pygame.image.load('002.png'), [int(500 * escala), int(800 * escala)])
img002b = pygame.transform.scale(pygame.image.load('002b.png'), [int(100 * escala), int(200 * escala)])
img003 = pygame.transform.scale(pygame.image.load('003.png'), [int(500 * escala), int(800 * escala)])

# Adicionando imagens as variaveis para seleção de veiculos
obstaculo1 = (carro1, carro2, carro3)
obstaculo2 = (carro1, carro2, carro3)
player = (carro1, carro2, carro3)
obstaculo1_cor, obstaculo2_cor = 0, 0

# Gerando historico de pontuação, Rank
def rank(score_new):
	global score_max
	# Criando o arquivo rank.txt
	e = os.path.isfile('rank.txt')
	if e == False:
		rank = open('rank.txt', 'w')
		rank.write('1')
		rank.close()

	# Lendo maior pontuação
	rank = open('rank.txt', 'r')
	score_file = rank.read()
	rank.close()

	# Comparando pontuação
	score_file = int(score_file)
	if score_new > score_file:
		score_max = score_new
	else:
		score_max = score_file

	# Escrevendo maior pontuação
	rank = open('rank.txt', 'w')
	rank.write(str(score_max))
	rank.close()

# Game over
def gameover(pontos):
	rank(pontos)
	recorde = score_max
	tela.fill([0, 0, 0])
	tela.blit(img003, [0, 0])
	font = pygame.font.Font('nasa.ttf', int(40 * escala))
	text = font.render(str(pontos), True, [255, 255, 255])
	text2 = font.render(str(recorde), True, [255, 255, 255])
	tela.blit(text, [int(160 * escala), int(350 * escala)])
	tela.blit(text2, [int(160 * escala), int(550 * escala)])
	pygame.display.update()
	pygame.time.wait(10000)

# Introdução do game
def introducao():
	global player_cor
	intro = True
	select = 2
	while intro:
		tela.fill([0, 0, 0])
		tela.blit(img002, [0, 0])

		if select == 1:
			tela.blit(img002b, [int(30 * escala), int(350 * escala)])
			player_cor = 0

		if select == 2:
			tela.blit(img002b, [int(185 * escala), int(350 * escala)])
			player_cor = 1

		if select == 3:
			tela.blit(img002b, [int(370 * escala), int(350 * escala)])
			player_cor = 2

		tela.blit(carro1, [int(40 * escala), int(375 * escala)])
		tela.blit(carro2, [int(195 * escala), int(375 * escala)])
		tela.blit(carro3, [int(380 * escala), int(375 * escala)])
		pygame.display.update()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_a:
					select -= 1

				if event.key == pygame.K_d:
					select += 1

				if event.key == pygame.K_RETURN:
					intro = False

		if select < 1:
			select = 1

		if select > 3:
			select = 3

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
obstaculo2_x, obstaculo2_y = int(220 * escala), int(-654 * escala)
x = 0
y = 0
pontos = 0
nivel = 0

# Exibe logo do game
tela.blit(img001, [0, 0])
pygame.display.update()
pygame.time.wait(3000)

introducao()

# Permitido entrada de comando com tecla pressionada
pygame.key.set_repeat(1, 1)

# Loop principal
running = True
while running:
	# Declarando o FPS
	clock = pygame.time.Clock()
	clock.tick(60)
	velocidade = int(10 * escala)
	velocidade = velocidade + nivel

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
				velocidade = int(velocidade * 2)

	# Criando retangulos de colisão
	player_area = pygame.Rect(player_x, player_y, int(80 * escala), int(150 * escala))
	obstaculo1_area = pygame.Rect(obstaculo1_x, obstaculo1_y, int(68 * escala), int(145 * escala))
	obstaculo2_area = pygame.Rect(obstaculo2_x, obstaculo2_y, int(68 * escala), int(145 * escala))

	# Detectando colisão entre carros
	if player_area.colliderect(obstaculo1_area):
		print('Game Over!')
		gameover(pontos)
		running = False

	if player_area.colliderect(obstaculo2_area):
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
		nivel = int(pontos / 10)

	# Desenha carros na tela	
	tela.blit(obstaculo1[obstaculo1_cor], obstaculo1_area)
	tela.blit(obstaculo2[obstaculo2_cor], obstaculo2_area)
	tela.blit(player[player_cor], player_area)

	# Movendo os obstaculos
	lista_posicao_obstaculo = (int(60 * escala), int(200 * escala), int(350 * escala))

	obstaculo1_y += velocidade / 2
	if obstaculo1_y >= int(800 * escala):
		obstaculo1_y = int(-154 * escala)
		sorteia_lista1 = random.randint(0, 2)
		if sorteia_lista1 == 0:
			obstaculo1_x = lista_posicao_obstaculo[0]
		if sorteia_lista1 == 1:
			obstaculo1_x = lista_posicao_obstaculo[1]
		if sorteia_lista1 == 2:
			obstaculo1_x = lista_posicao_obstaculo[2]

		obstaculo1_cor = random.randint(0, 2)

	obstaculo2_y += velocidade / 2
	if obstaculo2_y >= int(800 * escala):
		obstaculo2_y = int(-154 * escala)
		sorteia_lista2 = random.randint(0, 2)
		if sorteia_lista1 == sorteia_lista2:
			sorteia_lista2 = 2
			if sorteia_lista1 == sorteia_lista2:
				sorteia_lista2 = 1
		if sorteia_lista2 == 0:
			obstaculo2_x = lista_posicao_obstaculo[0]
		if sorteia_lista2 == 1:
			obstaculo2_x = lista_posicao_obstaculo[1]
		if sorteia_lista2 == 2:
			obstaculo2_x = lista_posicao_obstaculo[2]

		obstaculo2_cor = random.randint(0, 2)

	pygame.display.update()

# Encerra o pygame
pygame.quit()