import pygame as pg
from fighter import *
from skelly import *
from pygame import mixer

mixer.init()
pg.init()

RESOLUTION = WIDTH, HEIGHT = 1200, 674
clock = pg.time.Clock()
FPS = 60
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Hoodie Boogie")

intro_count = 3
last_count_update = pg.time.get_ticks()

WARRIOR_SIZE = 150
WARRIOR_SCALE = 3.5
WARRIOR_OFFSET = [72, 46]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

pg.mixer.music.load("assets/audio/music.mp3")
pg.mixer.music.set_volume(.75)
pg.mixer.music.play(-1, 0, 5000)
sword_fx = pg.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(.5)
magic_sound = pg.mixer.Sound("assets/audio/magic.wav")
magic_sound.set_volume(1.25)

bg_image = pg.image.load("assets/images/background/Third-Strike-Subway.jpeg").convert_alpha()
skeleton_sprites = [
    pg.image.load("assets/images/Skeleton/Idle.png").convert_alpha(),
    pg.image.load("assets/images/Skeleton/Walk.png").convert_alpha(),
    pg.image.load("assets/images/Skeleton/Jump.png").convert_alpha(),
    pg.image.load("assets/images/Skeleton/Attack.png").convert_alpha(),
    pg.image.load("assets/images/Skeleton/Take Hit.png").convert_alpha(),
    pg.image.load("assets/images/Skeleton/Death.png").convert_alpha()
]
wizard_sprite = pg.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()
victory_image = pg.image.load("assets/images/icons/fatality.png").convert_alpha()
GREEN = (0, 205, 0)
YELLOW = (214, 203, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (242, 145, 48)
SKELETON_ANIMATION_STEPS = [4, 4, 3, 8, 4, 4]
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

count_font = pg.font.Font("assets/fonts/bloodscratch.ttf", 80)
score_font = pg.font.Font("assets/fonts/turok.ttf", 40)
round_over = False
round_over_cooldown = 3000
score = [0, 0]


def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_bg():
    scaled_bg = pg.transform.scale(bg_image, (WIDTH, HEIGHT))
    screen.blit(scaled_bg, (0, 0))


def draw_health(health, x, y):
    ratio = health / 100
    pg.draw.rect(screen, WHITE, (x - 2.5, y - 2.5, 505, 35))
    pg.draw.rect(screen, RED, (x, y, 500, 30))
    pg.draw.rect(screen, GREEN, (x, y, 500 * ratio, 30))


fighter_1 = SkFighter(1, 135, 410, False, WARRIOR_DATA, skeleton_sprites, SKELETON_ANIMATION_STEPS, sword_fx)
fighter_2 = Fighter(2, 985, 410, True, WIZARD_DATA, wizard_sprite, WIZARD_ANIMATION_STEPS, magic_sound)
run = True
while run:
    clock.tick(FPS)
    draw_bg()
    draw_health(fighter_1.health, 25, 50)
    draw_health(fighter_2.health, 675, 50)
    draw_text(f"P1: {score[0]}", score_font, ORANGE, 25, 80)
    draw_text(f"P2: {score[1]}", score_font, ORANGE, 675, 80)

    if intro_count <= 0:
        fighter_1.move(WIDTH, HEIGHT, target=fighter_2)
        fighter_2.move(WIDTH, HEIGHT, target=fighter_1)
    else:
        draw_text(str(intro_count), count_font, RED, WIDTH / 2 - 10, HEIGHT / 3)
        if (pg.time.get_ticks() - last_count_update) >= 1000:
            last_count_update = pg.time.get_ticks()
            intro_count -= 1

    fighter_1.draw(screen)
    fighter_2.draw(screen)
    fighter_1.update_animation()
    fighter_2.update_animation()

    if not round_over:
        if not fighter_1.alive:
            score[1] += 1
            round_over = True
            round_over_time = pg.time.get_ticks()
        if not fighter_2.alive:
            score[0] += 1
            round_over = True
            round_over_time = pg.time.get_ticks()
    else:
        screen.blit(victory_image, (125, 150))
        if pg.time.get_ticks() - round_over_time > round_over_cooldown:
            round_over = False
            intro_count = 3
            fighter_1 = SkFighter(1, 135, 410, False, WARRIOR_DATA, skeleton_sprites, SKELETON_ANIMATION_STEPS, sword_fx)
            fighter_2 = Fighter(2, 985, 410, True, WIZARD_DATA, wizard_sprite, WIZARD_ANIMATION_STEPS, magic_sound)

    for event in pg.event.get():
        if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
            run = False

    pg.display.update()

pg.quit()
