from random import randint

from pygame import *

init()

WIDTH = 1000
HEIGHT = 800
window = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()

class Sprite:
    def __init__(self, x, y, width, height, img_path=None):
        self.img = img_path
        if self.img:
            self.img = transform.scale(image.load(img_path), (width, height))
            self.rect = self.img.get_rect()
            self.rect.x = x
            self.rect.y = y
        else:
            self.rect = Rect(x, y, width, height)

    # метод відображення спрайтів
    def reset(self):
        if self.img:
            window.blit(self.img, (self.rect.x, self.rect.y))
        else:
            draw.rect(window, (255, 0, 0), self.rect)

class Enemy(Sprite):
    def __init__(self, x, y, width, height, image_path=None):
        super().__init__(x, y, width, height, image_path)
        self.enemy_speed=2

    def movement(self, ):
        self.rect.y += self.enemy_speed

class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__(x, y, 10, 20) # Размеры пули 10x20
        self.speed = 12 # Скорость пули

    def update(self):
        self.rect.y -= self.speed  # Пуля летит вверх
        if self.rect.bottom < 0:  # Удаляем пулю, если она ушла за экран
            return True
        return False


def update_player():
    keys = key.get_pressed()
    if keys[K_d]:
        player.rect.x += player_speed
    if keys[K_a]:
        player.rect.x -= player_speed

def update_player_with_mouse():
    mouse_x = mouse.get_pos()[0]
    player.rect.centerx = mouse_x
    #обмеження
    if player.rect.left < 0:
        player.rect.left = 0
    if player.rect.right > WIDTH:
        player.rect.right = WIDTH

enemies = list()
for i in range(6):
    enemies.append(Enemy(randint(0, 900), randint(-600, -100), 150, 150, 'img/enemies/enemy.png'))
bullets = list()
player_speed = 7
player = Sprite(0, 650, 170, 150, 'img/player/player.png')
while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:  # Выстрел на SPACE
                bullet = Bullet(player.rect.centerx - 5, player.rect.top)
                bullets.append(bullet)
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:  # ЛКМ (Left Mouse Button)
                bullet = Bullet(player.rect.centerx - 5, player.rect.top)
                bullets.append(bullet)

    window.fill((0, 0, 0))
    player.reset()

    for enemy in enemies:
        enemy.reset()
        enemy.movement()

        if enemy.rect.y >= 815:
            del  enemy
            enemy = Enemy(randint(0, 900), -100, 100, 100)

    for bullet in bullets[:]:
        if bullet.update():
            bullets.remove(bullet)
        else:
            bullet.reset()

    display.update()
    clock.tick(60)

    update_player()
    update_player_with_mouse()
