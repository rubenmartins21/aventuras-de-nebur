import pygame
from pygame import *
from random import choice, random

clocktick = pygame.USEREVENT + 1
pygame.time.set_timer(clocktick, 1200)
mixer.init()

#class do nebur
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.img_list = [
            [pygame.image.load("nebur images/walk sprite 1.png").convert_alpha(),
             pygame.image.load("nebur images/walk sprite 2.png").convert_alpha(),
             pygame.image.load("nebur images/walk sprite 3.png").convert_alpha()],

            [pygame.image.load("nebur images/walk sprite left 1.png").convert_alpha(),
             pygame.image.load("nebur images/walk sprite left 2.png").convert_alpha(),
             pygame.image.load("nebur images/walk sprite left 3.png").convert_alpha()],

            [pygame.image.load("nebur images/Sprite attack left.png").convert_alpha(),
             pygame.image.load("nebur images/Sprite attack right.png").convert_alpha()],

            [pygame.image.load("nebur images/sprite sword attack 1.png").convert_alpha(),
             pygame.image.load("nebur images/sprite sword attack 2.png").convert_alpha()],

            [pygame.image.load("nebur images/sprite sword attack left 1.png").convert_alpha(),
             pygame.image.load("nebur images/sprite sword attack left 2.png").convert_alpha()]]

        self.index = 0
        self.image = self.img_list[0][self.index]

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 0
        # self.jump_speed = 0
        self.onGround = True
        # self.onPlat = False
        self.pos_init = 424#posição no chão
        self.rect.x = 71
        self.rect.y = self.pos_init
        self.tam = 5
        self.contactZone = Rect(self.rect.x + 5, self.rect.bottom - self.tam, self.rect.w - 10, self.tam + 2)
        self.Kills = 0 #numero de inimigos mortos ... incrementa o score do jogo
        self.right = True #direção que o player esta
        self.health = 200 # vida do nebur
        self.dead = False # se o nebur esta morto ou não
        self.jump_speed = -30
        self.y_vel = 0
        self.flag_jump = {'subindo': False, 'descendo': False}
        self.mode_Attack = False
        self.energy_shoot = 100
        self.sword_sound = mixer.Sound("knifeSlice.ogg")



    def update(self, label, platGroup, enemies, bossGroup):

        pressed = pygame.key.get_pressed()
        up = pressed[K_UP]
        # down = pressed[K_DOWN]
        left = pressed[K_LEFT]
        right = pressed[K_RIGHT]
        attack = pressed[K_a]

        if up:
            if self.onGround:
                self.y_vel = self.jump_speed

        if left:
            self.right = False
            if self.rect.x > 40: #limite esquerdo do jogo
                self.image = self.img_list[1][self.index]
                self.speed = 10

                rangex = self.rect.x - self.speed
                while self.rect.x != rangex:
                    self.rect.x -= 1
                    self.atualizarContactZone()
                    if self.collidePlat(platGroup):
                        print('collide left')
                        self.rect.x += 2
                        self.atualizarContactZone()
                        break

                self.index += 1
                if self.index > 2:
                    self.index = 0
            else:
                print('collide left')

        if right:
            self.right = True
            if self.rect.x < 528: #limite direita do jogo
                self.image = self.img_list[0][self.index]
                self.speed = 10

                rangex = self.rect.x + self.speed
                while self.rect.x != rangex:
                    self.rect.x += 1
                    self.atualizarContactZone()
                    if self.collidePlat(platGroup):
                        print('collide right')
                        self.rect.x -= 2
                        self.atualizarContactZone()
                        break

                self.index += 1
                if self.index > 2:
                    self.index = 0
            else:
                print('collide right')

        if attack: # se o player entrar em modo de ataque

            self.sword_sound.play()

            self.mode_Attack = True

            if self.right:

                if self.index > 1:
                    self.index = 0
                self.image = self.img_list[3][self.index]
                self.index += 1


            elif not self.right:

                if self.index > 1:
                    self.index = 0
                if self.index == 1:
                    self.rect.left -= 29
                if self.index == 0:
                    self.rect.left += 29

                self.image = self.img_list[4][self.index]
                self.index += 1

        if not attack:
            self.mode_Attack = False

        self.collideEnemies(enemies)
        self.control_flag_jump(platGroup)
        self.jump(platGroup)
        self.control_flag_jump(platGroup)
        self.gravity_force(5)
        self.atualizarContactZone()
        #self.collideBau(baus)
        self.sword_attack(enemies, bossGroup)

        label.text = "Score: %d" % self.Kills

    def atualizarContactZone(self): #atualizar o rect embaixo dos pes do player
        self.contactZone = Rect(self.rect.x + 5, self.rect.bottom - self.tam, self.rect.w - 10, self.tam + 2)

    def collidePlat(self, platGroup): #se colidir com uma plataforma ao andar para direita ou para esquerda
        for plat in platGroup:
            if pygame.sprite.collide_rect(self, plat):
                return True

    def collide_zone_contact_plat(self, platGroup): # se esitver sobre uma plataforma
        for plat in platGroup:
            if self.contactZone.colliderect(plat.contactZone):
                return True

    def collideEnemies(self, enemies):
        if pygame.sprite.spritecollideany(self, enemies):
            self.health -= 3
            print('damage', self.health)

        if self.health <= 0:
            self.kill()
            self.dead = True

    def control_flag_jump(self, platGroup): # controla o salto do player
        if self.y_vel > 0:
            self.flag_jump['subindo'], self.flag_jump['descendo'] = False, True
            self.onGround = False
        elif self.y_vel < 0:
            self.flag_jump['subindo'], self.flag_jump['descendo'] = True, False
            self.onGround = False
        elif self.y_vel == 0 and self.rect.y != self.pos_init and not self.collide_zone_contact_plat(platGroup):
            self.flag_jump['subindo'], self.flag_jump['descendo'] = False, True
            self.onGround = False
        elif self.y_vel == 0 and self.rect.y != self.pos_init and self.collide_zone_contact_plat(platGroup):
            self.flag_jump['subindo'], self.flag_jump['descendo'] = False, False
            self.onGround = True
        elif self.rect.y == self.pos_init:
            self.flag_jump['subindo'], self.flag_jump['descendo'] = False, False
            self.onGround = True

    def jump(self, platGroup): # funçao que faz o player saltar
        if self.flag_jump['subindo']:
            y_range = self.rect.y + self.y_vel
            while self.rect.y != y_range:
                self.rect.y -= 1
                self.atualizarContactZone()
                if self.collidePlat(platGroup):
                    print('collide up')
                    self.y_vel = 0
                    break
        elif self.flag_jump['descendo']:
            y_range = self.rect.y + self.y_vel
            while self.rect.y != y_range:
                self.rect.y += 1
                self.atualizarContactZone()
                if self.collide_zone_contact_plat(platGroup) or self.rect.y == self.pos_init:
                    print('collide down')
                    self.y_vel = 0
                    break

    def gravity_force(self, gravity): # gravidae que coloca o player no chão
        if not self.onGround:
            self.y_vel += gravity


    def sword_attack(self, enemies, bossGroup): # ataques com a espada

        if self.mode_Attack:
            for e in enemies:
                if pygame.sprite.collide_rect(self, e):
                    e.sword_damage += 1

                if e.sword_damage > 4:
                    e.kill()
                    e.enemydead_sound.play()
                    self.Kills += 1

            for b in bossGroup:

                if pygame.sprite.collide_rect(self, b):
                    b.health -= 15

                    if b.health < 0:
                        b.kill()

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.image.load("block1.png").convert_alpha()
        self.image = img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.posx = x
        self.posy = y
        self.tam = 5
        self.contactZone = Rect(x, y, self.rect.w, self.tam) # rect que fica em cima do plat
        # self.contactZone2 = Rect(x, y + 25, self.rect.w, self.tam + 3)

    def update(self):
        self.rect.x = self.posx
        self.rect.y = self.posy


class Bullet(pygame.sprite.Sprite):
    def __init__(self, player, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = [pygame.image.load("nebur images/energy_effect.png").convert_alpha(),
                         pygame.image.load("nebur images/energy_effect left.png").convert_alpha()]
        self.image = self.img_list[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 15
        self.rect.x = x
        self.rect.y = y + 22
        self.direction = player.right

    def update(self, platforms, Enemies, player, BossBuletts, boss):
        if self.direction:
            self.image = self.img_list[0]
            self.rect.x += self.speed
        else:
            self.image = self.img_list[1]
            self.rect.x -= self.speed

        for plat in platforms:
            if self.rect.right > 528 or self.rect.left < 40 or pygame.sprite.collide_rect(self, plat):
                self.kill() # se a bola de fogo ultrapassar os limites ou colidir com um plat desaparece

        for e in Enemies:
            if pygame.sprite.collide_rect(self, e):
                e.shoots += 1 # a cada bola de fogo acertado incrementa-se o numero de balas recebidas pelo inimigo
                self.kill()
                # self.dead = True

            if e.shoots > 2: # se o numero de shoots for maior que tres o inimigo morre
                e.kill()
                e.enemydead_sound.play()
                player.Kills += 1
                # player.dead = True

        for b in BossBuletts: # se houver uma colisao entre as dus bolas de fogo as duas desaoacem
            if pygame.sprite.collide_rect(self, b):
                self.kill()
                b.kill()


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        pygame.sprite.Sprite.__init__(self)

        self.img_list = [
            [pygame.image.load("possum images/enemie 1.png").convert_alpha(),
             pygame.image.load("possum images/enemie 2.png").convert_alpha(),
             pygame.image.load("possum images/enemie 3.png").convert_alpha(),
             pygame.image.load("possum images/enemie 4.png").convert_alpha()],

            [pygame.image.load("possum images/enemie left 1.png").convert_alpha(),
             pygame.image.load("possum images/enemie left 2.png").convert_alpha(),
             pygame.image.load("possum images/enemie left 3.png").convert_alpha(),
             pygame.image.load("possum images/enemie left 4.png").convert_alpha()]]

        self.index = 0
        self.image = self.img_list[0][self.index]

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = y  # 415
        self.rect.x = x  # choice([400, 300])
        self.left_limit = a
        self.right_limit = b
        self.posInit = 415
        self.right = choice([True, False])
        self.speedx = 4
        self.shoots = 0
        self.sword_damage = 0
        self.tam = 5
        self.onGround = False
        self.contactZone = Rect(self.rect.x + 5, self.rect.bottom - self.tam, self.rect.w - 10, self.tam + 2)
        self.enemydead_sound = mixer.Sound("enemy_dead.ogg")


    def update(self, platGroup):

        self.move()
        self.direction()
        self.isOnground(platGroup)
        self.gravity_force(5)
        self.atualizarContactZone()

    def isOnground(self, platGroup): # verificar se o sprite esta no chão
        if self.rect.y == self.posInit or self.collide_zone_contact_plat(platGroup):
            self.onGround = True

        elif not self.rect.y == self.posInit and not self.collide_zone_contact_plat(platGroup):
            self.onGround = False

    def gravity_force(self, gravity):
        if not self.onGround:
            self.rect.y += gravity

    def collide_zone_contact_plat(self, platGroup):
        for plat in platGroup:
            if self.contactZone.colliderect(plat.contactZone):
                return True

    def atualizarContactZone(self):
        self.contactZone = Rect(self.rect.x + 5, self.rect.bottom - self.tam, self.rect.w - 10, self.tam + 2)

    def move(self):

        if self.right:

            if self.rect.x < 512:
                self.rect.x += self.speedx

            self.image = self.img_list[0][self.index]
            self.index += 1
            if self.index > 3:
                self.index = 0

        elif not self.right:

            if self.rect.x > 40:
                self.rect.x -= self.speedx

            self.image = self.img_list[1][self.index]
            self.index += 1
            if self.index > 3:
                self.index = 0

    def direction(self):
        if self.rect.x == self.right_limit:
            self.right = False

        elif self.rect.x == self.left_limit:
            self.right = True


class Label(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("None", 30)
        self.text = "Score : "
        self.center = (450, 50)
        self.color = (153, 149, 97)

    def update(self):
        self.image = self.font.render(self.text, 1, self.color)
        self.rect = self.image.get_rect()
        self.rect.center = self.center


class LifeBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("life bar images/lifebar_frame.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.posx = 50
        self.posy = 5
        self.w = 70
        self.length = self.w
        self.rectLife = Rect(7, 7, self.w, 10)
        self.lifeBar = None

    def update(self, player):
        self.lifeBar = pygame.draw.rect(self.image, (255, 255, 255), self.rectLife)
        self.rect.x = self.posx
        self.rect.y = self.posy
        self.w = player.health / 100 * self.length
        self.rectLife = Rect(7, 7, self.w, 10)
        if player.health > 0:
            self.lifeBar = pygame.draw.rect(self.image, (67, 174, 178), self.rectLife)


class Bau(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("bonus/bau.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.bau_sound = mixer.Sound("MS_Realization.ogg")

    def update(self, player):
        self.collideBau(player)


    def collideBau(self, player):
        #for b in baus:
        if pygame.sprite.collide_rect(self, player):
            self.bau_sound.play()
            player.energy_shoot = 100
            self.kill()



class Boss(pygame.sprite.Sprite):
    def __init__(self, x, y, a, b):
        pygame.sprite.Sprite.__init__(self)

        self.img_list = [
            [pygame.image.load("possum images/boss1.png").convert_alpha(),
             pygame.image.load("possum images/boss2.png").convert_alpha(),
             pygame.image.load("possum images/boss3.png").convert_alpha(),
             pygame.image.load("possum images/boss4.png").convert_alpha()],

            [pygame.image.load("possum images/boss1left.png").convert_alpha(),
             pygame.image.load("possum images/boss2left.png").convert_alpha(),
             pygame.image.load("possum images/boss3left.png").convert_alpha(),
             pygame.image.load("possum images/boss4left.png").convert_alpha()],

            [pygame.image.load("possum images/boss shoot attack 1.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack 2.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack 3.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack 4.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack 5.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack 6.png").convert_alpha()],

            [pygame.image.load("possum images/boss shoot attack left 1.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack left 2.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack left 3.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack left 4.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack left 5.png").convert_alpha(),
             pygame.image.load("possum images/boss shoot attack left 6.png").convert_alpha()],

            [pygame.image.load("possum images/boss attack 1.png").convert_alpha(),
             pygame.image.load("possum images/boss attack 2.png").convert_alpha(),
             pygame.image.load("possum images/boss attack 3.png").convert_alpha()],

            [pygame.image.load("possum images/boss attack left 1.png").convert_alpha(),
             pygame.image.load("possum images/boss attack left 2.png").convert_alpha(),
             pygame.image.load("possum images/boss attack left 3.png").convert_alpha()]]

        self.index = 0
        self.image = self.img_list[0][self.index]

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = y  # 415
        self.rect.x = x  # choice([400, 300])
        self.left_limit = a
        self.right_limit = b
        self.posInit = 415
        self.right = choice([True, False])
        self.speedx = 0
        self.shoots = 0
        self.tam = 5
        self.shoot_attack = False
        self.mode_attack = False
        self.health = 210
        self.onGround = False
        self.contactZone = Rect(self.rect.x + 5, self.rect.bottom - self.tam, self.rect.w - 10, self.tam + 2)
        self.enemydead_sound = mixer.Sound("enemy_dead.ogg")

    def update(self, platGroup, player, bullets):
        self.move()
        self.direction(player)
        self.shootattack(player)
        #self.modeattack(player)
        self.boss_damage(bullets)
        # self.stop()
        self.isOnground(platGroup)
        self.gravity_force(5)
        self.atualizarContactZone()

    def isOnground(self, platGroup):
        if self.rect.y == self.posInit or self.collide_zone_contact_plat(platGroup):
            self.onGround = True

        elif not self.rect.y == self.posInit and not self.collide_zone_contact_plat(platGroup):
            self.onGround = False

    def gravity_force(self, gravity):
        if not self.onGround:
            self.rect.y += gravity

    def collide_zone_contact_plat(self, platGroup):
        for plat in platGroup:
            if self.contactZone.colliderect(plat.contactZone):
                return True

    def atualizarContactZone(self):
        self.contactZone = Rect(self.rect.x + 5, self.rect.bottom - self.tam, self.rect.w - 10, self.tam + 2)

    def move(self):

        if not self.stop():
            if self.right:

                if self.rect.x < 512:
                    self.speedx = 4
                    self.rect.x += self.speedx

                    if self.index > 3:
                        self.index = 0

                    self.image = self.img_list[0][self.index]
                    self.index += 1

            elif not self.right:

                if self.rect.x > 40:
                    self.speedx = 4
                    self.rect.x -= self.speedx

                    if self.index > 3:
                        self.index = 0

                    self.image = self.img_list[1][self.index]
                    self.index += 1

    def direction(self, player):
        if self.rect.x > player.rect.x:
            self.right = False

        elif self.rect.x < player.rect.x:
            self.right = True

    def shootattack(self, player):
        if self.right:
            if player.rect.x - self.rect.x < 100:  # or self.rect.x - player.rect.x > 100:
                self.shoot_attack = True
                # self.attack_timer()
                # print("attack index ", self.index)
                self.image = self.img_list[2][self.index]

                self.index += 1
                if self.index > 5:
                    self.index = 5
            else:
                self.shoot_attack = False

        elif not self.right:
            if self.rect.x - player.rect.x < 100:  # or self.rect.x - player.rect.x > 100:
                self.shoot_attack = True
                #self.attack_timer()
                print("attack index ", self.index)
                self.image = self.img_list[3][self.index]

                self.index += 1
                if self.index > 5:
                    self.index = 5

            else:
                self.shoot_attack = False

    """def attack_timer(self):
        self.shoot_attack = False
        for e in pygame.event.get():
            if e == clocktick:
                self.shoot_attack = True
                break

    def modeattack(self, player):
        if self.right:
            if player.rect.x - self.rect.x < 100:

                # if pygame.sprite.collide_rect(self, player):
                self.mode_attack = True

                if self.index > 2:
                    self.index = 0

                self.image = self.img_list[4][self.index]

                self.index += 1

            if pygame.sprite.collide_rect(self, player):
                player.health -= 5


            else:
                self.mode_attack = False

        elif not self.right:
            if self.rect.x - player.rect.x < 100:
                self.mode_attack = True

                if self.index > 2:
                    self.index = 0

                self.image = self.img_list[5][self.index]

                self.index += 1

            else:
                self.mode_attack = False"""

    def stop(self):

        #if self.mode_attack or self.shoot_attack:
        if self.shoot_attack:
            # self.speedx = 0
            return True

    def boss_damage(self, bullets):
        for b in bullets:
            if pygame.sprite.collide_rect(self, b):
                self.health -= 5
                b.kill()

        if self.health < 0:
            self.kill()
            self.enemydead_sound.play()


class Boss_bullet(pygame.sprite.Sprite):
    def __init__(self, boss, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.img_list = [pygame.image.load("possum images/boss shoot 4.png").convert_alpha(),
                         pygame.image.load("possum images/boss shoot left 4.png").convert_alpha()]
        self.image = self.img_list[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 8
        self.rect.x = x
        self.rect.y = y + 22
        self.direction = boss.right

    def update(self, platforms, player):

        if self.direction:
            self.image = self.img_list[0]
            self.rect.x += self.speed
        else:
            self.image = self.img_list[1]
            self.rect.x -= self.speed

        for plat in platforms:
            if self.rect.right > 528 or self.rect.left < 40 or pygame.sprite.collide_rect(self, plat):
                self.kill()

        # for p in player:
        if pygame.sprite.collide_rect(self, player):
            player.health -= 8
            self.kill()

        if player.health < 0:
            player.kill()
            player.dead = True


class Boss_Life_Bar(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("life bar images/lifebar_frame.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.posx = 400
        self.posy = 5
        self.w = 67
        self.length = self.w
        self.rectLife = Rect(7, 7, self.w, 10)
        self.lifeBar = None

    def update(self, boss):
        self.lifeBar = pygame.draw.rect(self.image, (255, 255, 255), self.rectLife)
        self.rect.x = self.posx
        self.rect.y = self.posy
        self.w = boss.health / 100 * self.length
        self.rectLife = Rect(7, 7, self.w, 10)
        if boss.health > 0:
            self.lifeBar = pygame.draw.rect(self.image, (68, 39, 231), self.rectLife)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bonus/bomb.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.bomb_sound = mixer.Sound("Bomba.ogg")

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            self.bomb_sound.play()
            player.health -= 20

            if player.health < 0:
                player.kill()
                player.dead = True


class Potion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bonus/potion.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.potion_sound = mixer.Sound("MS_Realization.ogg")

    def update(self, player):
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            self.potion_sound.play()
            player.health = 200

class energy_bar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("life bar images/lifebar_frame.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.posx = x
        self.posy = y
        self.w = 140
        self.length = self.w
        self.rectLife = Rect(7, 7, self.w, 10)
        self.lifeBar = None

    def update(self, player):
        self.lifeBar = pygame.draw.rect(self.image, (255, 255, 255), self.rectLife)
        self.rect.x = self.posx
        self.rect.y = self.posy
        self.w = player.energy_shoot / 100 * self.length
        self.rectLife = Rect(7, 7, self.w, 10)
        if player.energy_shoot > 0:
            self.lifeBar = pygame.draw.rect(self.image, (238, 63, 32), self.rectLife)