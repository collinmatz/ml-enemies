"""This file contains logic to control the main game loop."""

import pygame

from player import Player


class Game:
    def __init__(self, window_size: tuple[int, int]):
        # initialize PyGame
        pygame.init()
        pygame.display.set_caption("ML Enemies")

        # game constants
        self.animation_speed = 100
        self.fps = 60

        # game objects
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()

        # one of dude, owlet, or pink
        player_selection = "dude"
        self.spritesheets_sizes = {
            "assets/characters": (32, 32),
            "assets/characters-bow": (42, 42)
        }
        self.selected_sheet = "assets/characters-bow"

        self.player = Player(
            self.screen, 
            self.fps, 
            self.animation_speed, 
            player_selection, 
            self.selected_sheet, 
            self.spritesheets_sizes[self.selected_sheet]
        )

    def run(self):
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill((0,0,0))
                
            # handle player input
            keys = pygame.key.get_pressed()
            self.player.handle_input(keys)

            pygame.display.flip()

            self.clock.tick(self.fps)

        pygame.quit()