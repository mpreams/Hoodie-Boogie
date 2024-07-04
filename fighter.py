import pygame as pg


class Fighter:
    def __init__(self, player, x, y, flipped, data, sprite_sheet, animation_steps, sound):
        self.player = player
        self.size = data[0]
        self.scale = data[1]
        self.img_offset = data[2]
        self.animation_list = self.load_sprites(sprite_sheet, animation_steps)
        self.flipped = flipped
        self.action = 0  # 0:idle 1:run 2:jump 3:attack1 4:attack2 5:hit 6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pg.time.get_ticks()
        self.rect = pg.Rect((x, y, 80, 180))
        self.y_speed = 0
        self.attack_fx = sound
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True

    def load_sprites(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            tmp_img_list = []
            for x in range(animation):
                tmp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                tmp_img_list.append(pg.transform.scale(tmp_img, (self.size * self.scale, self.size * self.scale)))
            animation_list.append(tmp_img_list)
        return animation_list

    def move(self, width, height, target):
        SPEED = 10
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0

        key = pg.key.get_pressed()

        if not self.attacking and self.alive:
            # controls for player 2
            if self.player == 2:
                if key[pg.K_LEFT]:
                    dx = -SPEED
                    self.running = True
                if key[pg.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                if key[pg.K_UP] and not self.jump:
                    self.jump = True
                    self.y_speed = -30

                if key[pg.K_RSHIFT] or key[pg.K_SLASH]:
                    self.attack(target)
                    if key[pg.K_RSHIFT]:
                        self.attack_type = 1
                    if key[pg.K_SLASH]:
                        self.attack_type = 2

        # applies gravity by increasing speed at which y goes toward bottom
        self.y_speed += GRAVITY
        dy += self.y_speed

        # stop movement at edge of screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > width:
            dx = width - self.rect.right
        # stop falling when on floor
        if self.rect.bottom + dy > height - 75:
            self.jump = False
            self.y_speed = 0
            dy = height - 75 - self.rect.bottom

        if target.rect.centerx > self.rect.centerx:
            self.flipped = False
        else:
            self.flipped = True

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        # moves fighter
        self.rect.x += dx
        self.rect.y += dy

    def update_animation(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)  # death
        elif self.hit:
            self.update_action(5)  # hit
        elif self.attacking:
            if self.attack_type == 2:
                self.update_action(4)  # attack 2
            if self.attack_type == 1:
                self.update_action(3)  # attack 1
        elif self.jump:
            self.update_action(2)  # jump
        elif self.running:
            self.update_action(1)  # run
        else:
            self.update_action(0)  # idle
        cooldown = 49
        self.image = self.animation_list[self.action][self.frame_index]
        if pg.time.get_ticks() - self.update_time > cooldown:
            self.frame_index += 1
            self.update_time = pg.time.get_ticks()
        # if animation complete, reset
        if self.frame_index >= len(self.animation_list[self.action]):
            if not self.alive:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0
                # if attacking, reset and cooldown
                if self.action == 3 or self.action == 4:
                    self.attacking = False
                    self.attack_cooldown = 35
                # if hit, reset
                if self.action == 5:
                    self.hit = False
                    self.attacking = False
                    self.attack_cooldown = 0

    def attack(self, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            self.attack_fx.play()
            attacking_rect = pg.Rect(self.rect.centerx - (2.5 * self.rect.width * self.flipped), self.rect.y, 2.5 * self.rect.width, self.rect.height)
            if attacking_rect.colliderect(target.rect):
                target.health -= 5
                target.hit = True

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pg.time.get_ticks()

    def draw(self, surface):
        img = pg.transform.flip(self.image, self.flipped, False)
        surface.blit(img, (self.rect.x - (self.img_offset[0] * self.scale),
                                  self.rect.y - (self.img_offset[1] * self.scale)))
