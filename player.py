"""
This file contains the logic for rendering and controlling player
input.
"""
import os
import pygame
import math

class Player:
    def __init__(
            self, 
            screen,
            fps: int,
            animation_speed: int,
            selection: str, 
            path_to_spritesheets: str,
            sprite_size: tuple[int, int]
        ):
        # rendering variables
        spritesheet_path = path_to_spritesheets + f"/{selection}"
        self.sprite_size = sprite_size
        self.fps = fps
        self.screen = screen
        self.wall_padding = 0
        self.current_time = 0
        self.last_update_time = 0
        self.animation_speed = animation_speed
        self.spritesheets = self._load_spritesheets(spritesheet_path)
        
        # movement variables
        self.facing_left = False
        self.x, self.y = 100, 100
        self.speed = 4
        self.jump_height = 1


    def handle_input(self, keys):
        """Iterate over pressed keys and handle player input."""
        walking = False
        running = False

        # handle movement
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            self._handle_movement(keys)
            running = True 

        if walking:
            sprite = self._get_sprite(self.spritesheets["walk"])
        elif running:
            sprite = self._get_sprite(self.spritesheets["run"])
        else:
            sprite = self._get_sprite(self.spritesheets["idle"])
        
        self.draw(sprite)


    def draw(self, sprite):
        if self.facing_left:
            sprite = pygame.transform.flip(sprite, self.facing_left, False) 

        self.screen.blit(sprite, (self.x, self.y))


    def _handle_movement(self, keys):
        # handle the case where multiple keys are held down at once
        if keys[pygame.K_a] and keys[pygame.K_w]:
            self.facing_left = True
            self.x -= self.speed / math.sqrt(2)
            self.y -= self.speed / math.sqrt(2)
        elif keys[pygame.K_a] and keys[pygame.K_s]:
            self.facing_left = True
            self.x -= self.speed / math.sqrt(2)
            self.y += self.speed / math.sqrt(2)
        elif keys[pygame.K_d] and keys[pygame.K_w]:
            self.facing_left = False
            self.x += self.speed / math.sqrt(2)
            self.y -= self.speed / math.sqrt(2)
        elif keys[pygame.K_d] and keys[pygame.K_s]:
            self.facing_left = False
            self.x += self.speed / math.sqrt(2)
            self.y += self.speed / math.sqrt(2)

        elif keys[pygame.K_a]:   # Move left
            self.facing_left = True
            self.x -= self.speed
        elif keys[pygame.K_d]:  # Move right
            self.facing_left = False
            self.x += self.speed
        elif keys[pygame.K_w]:     # Move up
            self.y -= self.speed
        elif keys[pygame.K_s]:   # Move down
            self.y += self.speed

        # handle potential out of bounds for the player
        if self.x - self.speed < 0:
            self.x = 0
        elif self.x + self.speed > (self.screen.get_size()[0] - self.sprite_size[0] - self.wall_padding):
            self.x = self.screen.get_size()[0] - self.sprite_size[0] - self.wall_padding
        if self.y - self.speed < 0:
            self.y = 0
        elif self.y + self.speed > (self.screen.get_size()[1] - self.sprite_size[1] - self.wall_padding):
            self.y = self.screen.get_size()[1] - self.sprite_size[1] - self.wall_padding


    def _get_sprite(self, spritesheet: dict):
        """Gets the next needed sprite to render to the screen."""
        sprite = pygame.Surface(self.sprite_size, pygame.SRCALPHA)

        # calculate x for the sprite in the spritesheet
        x = spritesheet["current_frame"] * self.sprite_size[0]
        sprite.blit(spritesheet["sheet"], (0,0), (x, 0, *self.sprite_size))

        # update the frame number and return the sprite
        self.current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        if self.current_time - self.last_update_time > self.animation_speed:
            self.last_update_time = self.current_time  # Reset the last update time
            spritesheet["current_frame"] = (spritesheet["current_frame"] + 1) % spritesheet["max_frames"]
        
        return sprite


    def _load_spritesheets(self, path_to_spritesheets: str):
        """Load in all spritesheets from a directory."""
        spritesheets = {}

        # read in the spritesheets for the selected character
        for filename in os.listdir(path_to_spritesheets):
            name, extension = os.path.splitext(filename)
            if extension == ".png":
                file_path = os.path.join(path_to_spritesheets, filename)

                # load the image and store it in dictionary
                spritesheet = pygame.image.load(file_path).convert_alpha()
                spritesheets[name] = {
                    "sheet": spritesheet, 
                    "current_frame": 0,
                    "max_frames": spritesheet.get_width() // self.sprite_size[1]
                }

        return spritesheets
