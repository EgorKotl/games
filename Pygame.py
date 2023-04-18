# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random
from colors import *
f = open('record', 'r+')
WIDTH = 1200
HEIGHT = 650
FPS = 100
n = 5000
collect = 0
moneycount = 100
moneycoords = set()
energy = 1000
pos = pygame.Vector2((WIDTH / 2, HEIGHT / 2))
camera_pos = pygame.Vector2((WIDTH / 2, HEIGHT / 2))


class battery(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        x = random.randint(-n, WIDTH + n)
        y = random.randint(-n, HEIGHT + n)
        self.rect.center = (x, y)
        if pygame.sprite.spritecollide(self, mobs, True): pass


class shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((70, 70))
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2((WIDTH / 2, HEIGHT / 2))
        self.rect.center = (100, 100)

    def update(self, dt):
        global energy
        pressed = pygame.key.get_pressed()
        self.boost = pygame.Vector2((0, 0))
        if pressed[pygame.K_w]: self.boost -= (0, 1)
        if pressed[pygame.K_a]: self.boost -= (1, 0)
        if pressed[pygame.K_s]: self.boost -= (0, -1)
        if pressed[pygame.K_d]: self.boost -= (-1, 0)
        self.pos += self.boost * (dt / 5)
        self.rect.center = self.pos
        if not pressed[pygame.K_SPACE]:
            self.rect = self.image.get_rect()
            self.image = pygame.Surface((70, 70))
            # self.image.fill(BLUE)


        elif energy:
            self.image.fill(LIGHT_BLUE)
            energy -= 1
            if energy == 0:
                self.image.fill(BLACK)
                return
            if pygame.sprite.spritecollide(self, mobs, True): pass


class money(pygame.sprite.Sprite):
    def __init__(self):
        global moneycoords
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 20))
        self.rect = pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        x = random.randint(-n, WIDTH + n)
        y = random.randint(-n, HEIGHT + n)
        self.rect.center = (x, y)
        if pygame.sprite.spritecollide(self, mobs, True): pass

        #print(x, y)





class player(pygame.sprite.Sprite):
    def __init__(self):
        global user_text
        pygame.sprite.Sprite.__init__(self)
        self.pos = pygame.Vector2((WIDTH / 2, HEIGHT / 2))
        self.image = pygame.Surface((50, 50))
        try:
            self.image.fill(eval(user_text))
        except:
            self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        if pygame.sprite.spritecollide(self, mobs, True): pass

    def update(self, dt):
        global pos
        pressed = pygame.key.get_pressed()
        self.boost = pygame.Vector2((0, 0))
        if pressed[pygame.K_w]: self.boost -= (0, 1)
        if pressed[pygame.K_a]: self.boost -= (1, 0)
        if pressed[pygame.K_s]: self.boost -= (0, -1)
        if pressed[pygame.K_d]: self.boost -= (-1, 0)
        self.pos += self.boost * (dt / 5)
        self.rect.center = self.pos
        pos = self.pos
        global energy
        if pygame.sprite.spritecollide(self, batterys, True):
            energy = min(2000, energy + 50)
        global collect
        if pygame.sprite.spritecollide(player1, moneys, True):
            collect += 1


class mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speedx = 0
        self.speedy = 0
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        x = random.randint(-n, WIDTH + n)
        y = random.randint(-n, HEIGHT + n)
        self.rect.center = (x, y)


# Создаем игру и окно
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
base_font = pygame.font.Font(None, 32)

pygame.mixer.init()
colr=pygame.display.set_mode([WIDTH,HEIGHT ])
pygame.display.set_caption("Choose colour")
user_text=''

input_rect = pygame.Rect(WIDTH/2-100, HEIGHT/2, 200, 32)
color = pygame.Color('chartreuse4')
run=1

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            run=0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                text_s = base_font.render('LOADING...', True, (255, 255, 255))
                colr.blit(text_s, (WIDTH/2-100, HEIGHT/2+40))
                run = 0
                break

            elif event.key == pygame.K_BACKSPACE:

                user_text = user_text[:-1]

            else:
                user_text += event.unicode

    pygame.draw.rect(colr, color, input_rect)
    text_surface = base_font.render(user_text, True, (255, 255, 255))
    colr.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    input_rect.w = max(100, text_surface.get_width() + 10)
    pygame.display.flip()
    clock.tick(60)
background = pygame.Surface((2000, 2000))
background.fill((30, 30, 30))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
moneys = pygame.sprite.Group()
sh = shield()
all_sprites.add(sh)
for i in range(9000):
    m = mob()
    all_sprites.add(m)
    mobs.add(m)
player1 = player()
all_sprites.add(player1)
batterys = pygame.sprite.Group()
for i in range(moneycount):
    m = money()
    all_sprites.add(m)
    moneys.add(m)
for i in range(500):
    m = battery()
    all_sprites.add(m)
    batterys.add(m)
camera = pygame.Vector2((0, 0))
dt = 0
# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    screen.blit(background, camera)
    screen.fill(BLACK)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
    # Обновление

    all_sprites.update(dt)
    hits = pygame.sprite.spritecollide(player1, mobs, False)
    if hits:
        running = False
    camera_move = pygame.Vector2()
    pressed = pygame.key.get_pressed()
    if (camera_pos - pos)[0] > 300 or (pos - camera_pos)[0] > 300 or (camera_pos - pos)[1] > 100 or (pos - camera_pos)[
        1] > 100:
        if pressed[pygame.K_w]: camera_move += (0, 1)
        if pressed[pygame.K_a]: camera_move += (1, 0)
        if pressed[pygame.K_s]: camera_move += (0, -1)
        if pressed[pygame.K_d]: camera_move += (-1, 0)
        camera += camera_move * (dt / 5)
        camera_pos -= camera_move * (dt / 5)
        if camera_move.length() > 0: camera_move.normalize_ip()

    for s in all_sprites:
        screen.blit(s.image, s.rect.move(camera))
    # Рендеринг

    # all_sprites.draw(screen)
    # После отрисовки всего, переворачиваем экран
    my_font = pygame.font.SysFont('Calibri', 25)

    text_surface = my_font.render(f'Собрано монет: {collect} из {moneycount}', True, WHITE)
    screen.blit(text_surface, [0, 0])

    text_surface = my_font.render(f'Позиция: {int(pos[0])} {int(pos[1])}', True, WHITE)
    screen.blit(text_surface, [0, 20])

    text_surface = my_font.render(f'Энергия: {int(energy / 1000 * 100)}%', True, WHITE)
    screen.blit(text_surface, [0, 40])

    pygame.display.flip()
    dt = clock.tick(60)

print(f'Cобрано: {collect}, {int(collect / moneycount * 100)}%')
f.seek(0, 0)
q = f.readlines()
f.write(str(collect) + '\n')
f.close()
pygame.quit()
# saaaaawssыыыыыыыыыыыыыa            sa
