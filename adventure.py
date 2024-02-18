import pygame
from classes_adventure import Player, Platform, Bullet, Enemy, Label, LifeBar, Bau, Boss, Boss_bullet, Boss_Life_Bar, \
    Bomb, Potion, energy_bar

from pygame import *
from random import choice, random

pygame.init()
mixer.init()

size = (600, 600) # Tamanho do ecra
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Aventuras de nebur")

bg1 = pygame.image.load('background images/background 1.1.png') # imagem de fundo do jogo

clock = pygame.time.Clock()

menu_sound = mixer.Sound("nebur intro.ogg") # som do menu e do jogo
shoot_sound = mixer.Sound("dark-shoot.ogg") # som quando o nebur dispara uma bola de fogo

label = Label()# classe label que apresenta o score do jogo
labels = pygame.sprite.Group(label)

#imagens das plataformas
img_plat1 = pygame.image.load("plats images/block1.png").convert_alpha()
img_plat2 = pygame.image.load("plats images/block2.png").convert_alpha()
img_plat3 = pygame.image.load("plats images/block3.png").convert_alpha()
img_plat4 = pygame.image.load("plats images/block4.png").convert_alpha()

plat1 = Platform(120, 410, img_plat1)
plat2 = Platform(300, 310, img_plat2)
plat3 = Platform(280, 150, img_plat3)
plat4 = Platform(90, 240, img_plat4)
plat5 = Platform(50, 140, img_plat1)
plat6 = Platform(430, 215, img_plat3)
platGroup = pygame.sprite.Group(plat1, plat2, plat3, plat4, plat5, plat6)

#plataformas do nivel do boss
plat7 = Platform(120, 380, img_plat1)
plat8 = Platform(300, 310, img_plat1)
plat9 = Platform(130, 250, img_plat3)
Boss_platGroup = pygame.sprite.Group(plat7, plat8, plat9)

player = Player()
players = pygame.sprite.Group(player)

bullets = pygame.sprite.Group() # grupo das bolas de fogo do nebur
# ------ inimigos on Ground
enemy1 = Enemy(450, 415, 230, 510)
enemy2 = Enemy(310, 415, 230, 510)
enemy3 = Enemy(350, 415, 230, 510)
# -----inimigo plat 1
enemy4 = Enemy(130, 330, 110, 210)
# -----inimigp plat 2
enemy5 = Enemy(410, 220, 310, 450)
enemy6 = Enemy(380, 220, 320, 440)
# ----inimigo plat 4
# enemy7 = Enemy(120, 140, 60, 120)
enemy7 = Enemy(120, 140, 60, 180)
# ----inimigo plat 5
enemy8 = Enemy(100, 50, 60, 120)

enemies = pygame.sprite.Group(enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, enemy8)

boss1 = Boss(450, 415, 110, 510) # boss do primeiro nivel
boss_group = pygame.sprite.Group(boss1)
"""for i in range(3):
    enemies.add(Enemy(choice([400, 300]), 414))
"""

bau1 = Bau(475, 451) # bau do primerio nivel
baus = pygame.sprite.Group(bau1)

bau2 = Bau(350, 280) # baus do nivel boss
bossBau = pygame.sprite.Group(bau2)

life = LifeBar() # barra de nivel do nebur
lifeGroup = pygame.sprite.Group(life)

bossLife = Boss_Life_Bar() # barra de vida do boss
bosslifeGroup = pygame.sprite.Group(bossLife)

energyBar = energy_bar(50, 35) # brra que mostra a quantidade de bolas de fogo desponiveis
energyGroup = pygame.sprite.Group(energyBar)


#bombas do primeiro nivel
bomb1 = Bomb(300, 453)
bomb2 = Bomb(180, 212)
bomb3 = Bomb(450, 186)
bombGroup = pygame.sprite.Group(bomb1, bomb2, bomb3)

#bombas do segundo nivel
bomb4 = Bomb(500, 453)
bomb5 = Bomb(100, 453)
bomb6 = Bomb(260, 453)
bossBomb = pygame.sprite.Group(bomb4, bomb5, bomb6)

potion1 = Potion(300, 125) #poção do primeiro nivel
potionGroup = pygame.sprite.Group(potion1)

potion2 = Potion(160, 225) #poção do segundo nivel
Boss_potionGroup = pygame.sprite.Group(potion2)


#interface quando o jogador perde
run_dead = False
def lose():
    pause_img = pygame.image.load("interface/lose.png")
    screen.blit(pause_img, (0, 0))
    global dead

    while run_dead:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    dead = False

        pygame.display.update()
        clock.tick(15)




#interface para quando o jogo tiver pausado
pause = False
def paused():
    pause_img = pygame.image.load("interface/pause.png")
    screen.blit(pause_img, (0, 0))
    global pause

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p: # se p voltar a ser clicado o jogo é pausado
                    pause = False

        pygame.display.update()
        clock.tick(15)

# interface menu do jogo
KeepGoing = True
playing = False
def game_intro():
    img_list = [pygame.image.load("interface/menu1.png"), pygame.image.load("interface/menu2.png"), pygame.image.load("interface/menu3.png")]
    index = 0
    menu = img_list[index]
    screen.blit(menu, (0, 0))
    menu_sound.play()
    global KeepGoing
    global playing

    while KeepGoing:

        pygame.time.delay(40)
        menu = img_list[index]
        screen.blit(menu, (0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                KeepGoing = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    KeepGoing = False

                if e.key == pygame.K_RETURN:
                    index += 1

                    if index > 2:
                        KeepGoing = False
                        playing = True

        pygame.display.update()


# pygame.mouse.set_visible(False)
run = True
boss_level = False


def game():
    menu_sound.set_volume(0.2)
    global run
    global boss_level
    global pausar
    #timer = pygame.time.Clock()

    while run:
        global pause
        global run_dead
        # timer.tick(20)
        pygame.time.delay(40)
        shoot = pygame.key.get_pressed()[K_SPACE]

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    run = False
                if e.key == pygame.K_b:
                    run = False
                    boss_level = True

                if e.key == pygame.K_p:
                    pause = True
                    paused()

            if player.Kills == 8:
                run = False
                boss_level = True

            if player.dead: # se o player estiver morto chama a função dead
                run_dead = True
                lose()

            if shoot: # se o jogador clicar space o nebur atira
                shoot_sound.play()
                player.energy_shoot -= 5

                if player.energy_shoot > 0: # so vai disparar se a barra de energia for maior que zero

                    if player.right:
                        player.image = player.img_list[2][1]
                        bullet = Bullet(player, player.rect.right, player.rect.y)
                        bullets.add(bullet)
                    else:
                        player.image = player.img_list[2][0]
                        bullet = Bullet(player, player.rect.left - 22, player.rect.y)
                        bullets.add(bullet)

        screen.blit(bg1, (0, 0))
        players.update(label, platGroup, enemies, boss_group)
        platGroup.update()
        bullets.update(platGroup, enemies, player, BossBullets, boss1)
        enemies.update(platGroup)
        labels.update()
        lifeGroup.update(player)
        energyGroup.update(player)
        baus.update(player)
        bombGroup.update(player)
        potionGroup.update(player)
        players.draw(screen)
        platGroup.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)
        labels.draw(screen)
        lifeGroup.draw(screen)
        bombGroup.draw(screen)
        energyGroup.draw(screen)
        baus.draw(screen)
        potionGroup.draw(screen)
        # draw.rect(screen, Color('cyan'), player.contactZone, 1)
        # draw.rect(screen, Color('cyan'), plat1.contactZone, 1)
        # draw.rect(screen, Color('cyan'), enemy1.contactZone, 1)
        pygame.display.update()


BossBullets = pygame.sprite.Group()
going = True
# nivel de boss
def boss():
    boss_bg = pygame.image.load('background images/background 1.1.png')
    player.rect.y = player.pos_init
    player.health = 200 # neste nivel a vida do player é restaurada
    player.energy_shoot = 100 # a energia tambem é restaurada
    player.rect.x = 71
    player.rect.y = 424

    global going

    while going:

        global pause
        global run_dead

        pygame.time.delay(40)
        screen.blit(boss_bg, (0, 0))
        shoot = pygame.key.get_pressed()[K_SPACE]

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                going = False

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_q:
                    going = False

                if e.key == pygame.K_p:
                    pause = True
                    paused()
            if player.dead:
                run_dead = True
                lose()

            if shoot:
                shoot_sound.play()
                player.energy_shoot -= 5

                if player.energy_shoot > 0:
                    if player.right:
                        player.image = player.img_list[2][1]
                        bullet = Bullet(player, player.rect.right, player.rect.y)
                        bullets.add(bullet)
                    else:
                        player.image = player.img_list[2][0]
                        bullet = Bullet(player, player.rect.left - 22, player.rect.y)
                        bullets.add(bullet)

            if boss1.shoot_attack: # so lançar a bola de fogo se modo de shot atttack estiver ativado
                boss_Bullet = Boss_bullet(boss1, boss1.rect.left, boss1.rect.y)
                BossBullets.add(boss_Bullet)

        players.update(label, Boss_platGroup, enemies, boss_group)
        boss_group.update(platGroup, player, bullets)
        # platGroup.update()
        bullets.update(platGroup, enemies, player, BossBullets, boss)
        BossBullets.update(Boss_platGroup, player)
        lifeGroup.update(player)
        bosslifeGroup.update(boss1)
        Boss_platGroup.update()
        Boss_potionGroup.update(player)
        energyGroup.update(player)
        bossBau.update(player)
        bossBomb.update(player)
        players.draw(screen)
        # platGroup.draw(screen)
        bullets.draw(screen)
        BossBullets.draw(screen)
        boss_group.draw(screen)
        lifeGroup.draw(screen)
        bosslifeGroup.draw(screen)
        Boss_platGroup.draw(screen)
        Boss_potionGroup.draw(screen)
        energyGroup.draw(screen)
        bossBomb.draw(screen)
        bossBau.draw(screen)
        pygame.display.update()

# função principal
def main():
    if not playing:
        game_intro()
    if playing:
        game()

    if boss_level:
        for plat in platGroup:
            plat.kill()

        for e in enemies:
            e.kill()

        for b in bombGroup:
            b.kill()

        for p in potionGroup:
            p.kill()

        for bau in baus:
            bau.kill()

        boss()


if __name__ == "__main__":
    main()
