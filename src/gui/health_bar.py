import random

import pygame

from src.fblitter import FBLITTER
from src.settings import SCALE_FACTOR
from src.support import import_image

PLAYER_HP = "player_hp"
PLAYER_IS_SICK = "player_is_sick"
PLAYER_HP_STATE = "player_hp_state"


class HealthProgressBar:
    def __init__(self, hp):
        self.pos = (80, 26)

        # storing all three cat images
        self.cat_imgs = []
        self.outgroup_cat_imgs = []
        for i in range(3):
            img = import_image(f"images/ui/health_bar/health_cat_{i + 1}.png")
            outgrp_img = import_image(
                f"images/ui/health_bar/outgroup_health{i + 1}.png"
            )
            img = pygame.transform.scale_by(img, 0.7)
            outgrp_img = pygame.transform.scale_by(outgrp_img, 0.7)
            rect = img.get_rect(midright=(self.pos[0] + 10, self.pos[1] + 20))
            self.cat_imgs.append((img, rect))
            self.outgroup_cat_imgs.append((outgrp_img, rect))
        self.curr_cat = 0  # current cat index.

        # health bar frame
        self.health_bar = pygame.transform.scale(
            import_image("images/ui/health_bar/health_bar.png", True),
            (70 * SCALE_FACTOR * 0.8, 14 * SCALE_FACTOR * 0.8),
        )
        self.health_bar_rect = self.health_bar.get_rect(topleft=self.pos)

        # health (inside the health bar).
        self.color = (255, 255, 255)
        self.hp_rect = pygame.Rect(
            self.pos[0],
            self.pos[1],
            self.health_bar.get_width(),
            self.health_bar.get_height(),
        )
        self.hp_rect.inflate_ip(0, -16)

        # health points
        self.hp = hp  # health points
        self.max_hp = hp
        # self.per_width_hp will be substract / added as per intensity.

        # shake
        self.SHAKE_INTENSITY = 0

        # colors for health bar.
        self.colors = {
            "Red": pygame.Color(210, 0, 55),
            "Yellow": pygame.Color(253, 253, 144),
            "Green": pygame.Color(201, 255, 117),
        }

    def render(self, screen, outgroup=False):
        health_percent = self.hp / self.max_hp
        # shake
        if health_percent <= 0.3:
            offset = (
                random.uniform(-1, 1) * self.SHAKE_INTENSITY,
                random.uniform(-1, 1) * self.SHAKE_INTENSITY,
            )
        else:
            offset = (0, 0)

        # cat img changing.
        if health_percent > 0.5:
            self.curr_cat = 0
        elif 0.5 >= health_percent > 0.25:
            self.curr_cat = 1
        else:
            self.curr_cat = 2

        # drawing
        # health
        self.hp_rect.width = health_percent * self.health_bar_rect.width
        FBLITTER.draw_rect(
            self.color,
            self.hp_rect.move(offset),
            border_top_right_radius=12,
            border_bottom_right_radius=12,
        )
        # pygame.draw.rect(
        #     screen,
        #     self.color,
        #     self.hp_rect.move(offset[0], offset[1]),
        #     border_top_right_radius=12,
        #     border_bottom_right_radius=12,
        # )
        # frame
        FBLITTER.schedule_blit(self.health_bar, self.health_bar_rect.move(offset))
        # screen.blit(
        #     self.health_bar,
        #     (self.health_bar_rect.x + offset[0], self.health_bar_rect.y + offset[1]),
        # )
        # emote
        cat_img, cat_rect = (
            self.cat_imgs[self.curr_cat]
            if not outgroup
            else self.outgroup_cat_imgs[self.curr_cat]
        )
        FBLITTER.schedule_blit(cat_img, cat_rect.move(offset))
        # screen.blit(cat_img, (cat_rect.x + offset[0], cat_rect.y + offset[1]))

    def apply_damage(self, intensity):
        self.hp = pygame.math.clamp(self.hp - intensity, 0, self.max_hp)

    def apply_health(self, intensity):
        self.hp = pygame.math.clamp(self.hp + intensity, 0, self.max_hp)

    def change_color(self):
        t = self.hp / self.max_hp
        if t >= 0.5:
            factor = 1 - (t - 0.5) * 2
            self.color = self.colors["Green"].lerp(self.colors["Yellow"], factor**1.5)
        else:
            factor = t * 2
            self.color = self.colors["Red"].lerp(self.colors["Yellow"], factor)

    def draw(self, screen, outgroup=False):
        self.change_color()
        self.render(screen, outgroup)
