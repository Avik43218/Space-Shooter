import pygame
from os.path import join
from random import randint as rand
from random import uniform

from config import GameConfigSettings as C


#Classes
class Player(pygame.sprite.Sprite):

    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(C.WINDOW_WIDTH / 2, C.WINDOW_HEIGHT / 2))
        self.direction = pygame.math.Vector2()
        self.speed = 200

        self.can_shoot = True
        self.shoot_time = 0
        self.cooldown = 400

    def laser_timer(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.shoot_time >= self.cooldown:
            self.can_shoot = True

    def update(self, delta_time):

        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self.direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])

        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        self.rect.center += self.direction * self.speed * delta_time

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(sprite_group, laser_surf, self.rect.midtop)
            self.can_shoot = False
            self.shoot_time = pygame.time.get_ticks()

        self.laser_timer()


class Star(pygame.sprite.Sprite):

    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=(rand(1, C.WINDOW_WIDTH), rand(1, C.WINDOW_HEIGHT)))


class Laser(pygame.sprite.Sprite):

    def __init__(self, groups, surf, pos):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom=pos)

    def update(self, delta_time):
        self.rect.centery -= 400 * delta_time
        if self.rect.bottom < 0:
            self.kill()


class Meteor(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(center=pos)
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1) 
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.speed = rand(400, 500)

    def update(self, delta_time):
        self.rect.center += self.direction * self.speed * delta_time
        if game_start_time - self.start_time >= self.lifetime:
            self.kill()


# General setup
pygame.init()
clock = pygame.time.Clock()
display_surf = pygame.display.set_mode((C.WINDOW_WIDTH, C.WINDOW_HEIGHT))
game_start_time = pygame.time.get_ticks()


# Surfaces
player_surf = pygame.image.load(join('assets', '128px', 'player.png')).convert_alpha()
star_surf = pygame.image.load(join('assets', '128px', 'star.png')).convert_alpha()
laser_surf = pygame.image.load(join('assets', '128px', 'Laser.png')).convert_alpha()
meteor_surf = pygame.image.load(join('assets', '128px', 'Asteroid_03.png')).convert_alpha()


# Draw sprites
sprite_group = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()

for _ in range(30):
    Star(sprite_group, star_surf)

meteor = Meteor(meteor_surf, (rand(0, C.WINDOW_WIDTH), 0), sprite_group)
player = Player(sprite_group, player_surf)

meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 200)

running = True
while running:

    delta_time = clock.tick() / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == meteor_event:
            x, y = rand(0, C.WINDOW_WIDTH), 0
            Meteor(meteor_surf, (x, y), (sprite_group, meteor_sprites))

    sprite_group.update(delta_time)
    pygame.sprite.spritecollide(player, meteor_sprites, True)

    display_surf.fill(C.BACKGROUND_COLOR)

    sprite_group.draw(display_surf)

    pygame.display.update()

pygame.quit()
