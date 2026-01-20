# import sys
import os
from tkinter import font

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

from typing import Tuple

Coordinate = Tuple[int, int]
Color = Tuple[int, int, int]
pygame.init()

class GridDisplay:

    def __init__(self,
                #  maze: list,
                #  robot: list,
                #  player: list,
                #  MODE: str,
                #  size: Coordinate = (30,30),
                 nb_pixels_by_box: int=4,
                 grid_color: Color=(220, 220, 220),
                 bg_color: Color=(200, 200, 200),
                 text_color: Color=(0, 0, 0),
                 period_duration: int=100):
        
        self.maze = None
        self.robot = None
        self.player = None

        self.MODE = "auto"              # "auto", "player", "battle"
        self.difficulty = "small"       # "small", "medium", "large"
        self.maze_size = None

        self.screen_size = (60, 60)
        self.nb_pixels_by_box = nb_pixels_by_box
        self.colors = {"gr": grid_color, "bg": bg_color, "tx": text_color}
        self.screen_type = "home"   # "home", "mode", "difficulty", "game"
        self.game_start = False

        self.period_duration = period_duration
        self.period = 0

        self._initialize_display()

    def _initialize_display(self) -> None:              # check
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 12)
        
        # initialize the screen
        self.screen = pygame.display.set_mode(
            (self.screen_size[0] * self.nb_pixels_by_box,
             self.screen_size[1] * self.nb_pixels_by_box + 20)
        )

        # Home screen
        self.draw_mode_screen(events=[])

    def _is_quit_event(self, event):                    # see why it doesnt work
        mods = pygame.key.get_mods()
        if event.type == pygame.QUIT:
            return True
        elif (event.type == pygame.KEYDOWN 
              and (event.key == pygame.K_q or event.key == pygame.K_c)
              and mods & pygame.KMOD_CTRL):
            return True
        return False
        
    def next_period(self,events) -> bool:                      # check
        print(self.screen_type, " at start of next_period")
        cont = True
        pygame.display.flip()

        for event in events:
            if self._is_quit_event(event):
                cont = False

        if cont:
            pygame.time.wait(self.period_duration)
            self.period += 1
            self._draw_maze()
            # print(self.screen_type, " at middle of next_period")
            # if self.screen_type == "home":
            #     print(self.screen_type)
            #     self.draw_home_screen(events)
            # elif self.screen_type == "difficulty":
            #     self.draw_difficulty_screen(events)
            # elif self.screen_type == "mode":  
            #     print("mode screen")  
            #     self.draw_mode_screen(events)
            # elif self.screen_type == "game":
            #     self._draw_maze()
        return cont
                   
    def _draw_maze(self) -> None:                       # check

        self.screen.fill(self.colors["bg"])
        pygame.draw.rect(
                    self.screen,
                    (0, 0, 0),
                    (((self.screen_size[0] - self.maze_size[0])//2 - 1) * self.nb_pixels_by_box,
                      ((self.screen_size[1] - self.maze_size[1])//2 - 1) * self.nb_pixels_by_box,
                      (self.maze_size[0] + 2) * self.nb_pixels_by_box,
                      (self.maze_size[1] + 2) * self.nb_pixels_by_box)
                )
        
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                
                x = ((self.screen_size[0] - self.maze_size[0])//2 + j) * self.nb_pixels_by_box
                y = ((self.screen_size[1] - self.maze_size[1])//2 + i) * self.nb_pixels_by_box

                cell = self.maze[i][j]

                if cell == 0:
                    color = (0, 0, 0)  # wall = black
                elif self.MODE == "player" and i == self.robot[1] and j == self.robot[0]:
                    color = (255, 255, 255) # we dont show the robot in player mode
                elif i == self.robot[1] and j == self.robot[0]:
                    color = (0, 0, 255)  # robot = blue
                elif self.MODE == "auto" and i == self.player[1] and j == self.player[0]:
                    color = (255, 255, 255) # we dont show the player in robot mode
                elif i == self.player[1] and j == self.player[0]:
                    color = (128, 0, 128)  # player = purple
                elif i == self.maze_size[1]//2 and j == self.maze_size[0]//2:
                    color = (0, 255, 0)  # goal = green
                elif cell == 1:
                    color = (255, 255, 255)  # path = white
                elif cell == 2:
                    color = (255, 0, 0)  # item = red
                elif cell == 3:
                    color = (255, 165, 0)  # bomb = orange
                elif cell == 4:
                    color = (255, 255, 0)  # explosion = yellow
                elif cell == 5:
                    color = (200, 200, 200)  # cleared explosion = light gray
                else:
                    color = (100, 100, 100)

                pygame.draw.rect(
                    self.screen,
                    color,
                    (x, y, self.nb_pixels_by_box, self.nb_pixels_by_box)
                )

        # # Affiche la période
        # label = self.font.render(f"period: {self.period}", 1, self.colors["tx"])
        # self.screen.blit(label, (5, self.size[1] * self.nb_pixels_by_box + 2))

    def draw_home_screen(self, events) -> None:
        self.screen.fill(self.colors["bg"])
        color = (100, 100, 100)

        # Mode button
        button_rect_mode = pygame.Rect(
                        20 * self.nb_pixels_by_box,
                        10 * self.nb_pixels_by_box,
                        200,50
                        )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_mode
        )
        text_surface = self.font.render("MODE", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_mode.center)
        self.screen.blit(text_surface, text_rect)
        
        
        # Difficulty button
        button_rect_difficulty = pygame.Rect(
                20 * self.nb_pixels_by_box,
                20 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_difficulty
        )

        text_surface = self.font.render("Difficulty", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_difficulty.center)
        self.screen.blit(text_surface, text_rect)

        # score button
        button_rect = pygame.Rect(
                20 * self.nb_pixels_by_box,
                30 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect
        )

        text_surface = self.font.render("Score", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)

        # play button
        button_rect_play = pygame.Rect(
                20 * self.nb_pixels_by_box,
                40 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_play
        )
        text_surface = self.font.render("Play", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_play.center)
        self.screen.blit(text_surface, text_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
                pos = event.pos
                if button_rect_mode.collidepoint(pos):
                    self.screen_type = "mode"
                    print(self.screen_type, " at end of draw_home_screen")
                    
                elif button_rect_difficulty.collidepoint(pos):
                    self.screen_type = "difficulty"
                    
                elif button_rect_play.collidepoint(pos):
                    self.game_start = True
                    self.screen_type = "game"
        print(self.screen_type, " at end of draw_home_screen")

    def draw_difficulty_screen(self, events) -> None:
        self.screen.fill(self.colors["bg"])
        color = (100, 100, 100)

        # Easy button
        button_rect_easy = pygame.Rect(
                        20 * self.nb_pixels_by_box,
                        10 * self.nb_pixels_by_box,
                        200,50
                        )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_easy
        )
        text_surface = self.font.render("EASY", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_easy.center)
        self.screen.blit(text_surface, text_rect)


        # Medium button
        button_rect_medium = pygame.Rect(
                20 * self.nb_pixels_by_box,
                20 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_medium
        )

        text_surface = self.font.render("MEDIUM", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_medium.center)
        self.screen.blit(text_surface, text_rect)

        # Hard button
        button_rect_hard = pygame.Rect(
                20 * self.nb_pixels_by_box,
                30 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_hard
        )

        text_surface = self.font.render("HARD", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_hard.center)
        self.screen.blit(text_surface, text_rect)

        # back button
        button_rect_home = pygame.Rect(
                20 * self.nb_pixels_by_box,
                40 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_home
        )
        text_surface = self.font.render("BACK", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_home.center)
        self.screen.blit(text_surface, text_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if button_rect_easy.collidepoint(pos):
                    self.difficulty = "easy"
                    self.screen_type = "home"
                    return
                elif button_rect_medium.collidepoint(pos):
                    self.difficulty = "medium"
                    self.screen_type = "home"
                    return
                elif button_rect_hard.collidepoint(pos):
                    self.difficulty = "hard"
                    self.screen_type = "home"
                    return
                elif button_rect_home.collidepoint(pos):
                    self.screen_type = "home"
                    return

    def draw_mode_screen(self, events) -> None:
        self.screen.fill(self.colors["bg"])
        color = (100, 100, 100)

        # auto button
        button_rect_auto = pygame.Rect(
                        20 * self.nb_pixels_by_box,
                        10 * self.nb_pixels_by_box,
                        200,50
                        )
        
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_auto
        )
        text_surface = self.font.render("AUTO", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_auto.center)
        self.screen.blit(text_surface, text_rect)

        # labyrinth button
        button_rect_labyrinth = pygame.Rect(
                20 * self.nb_pixels_by_box,
                20 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_labyrinth
        )

        text_surface = self.font.render("LABYRINTH", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_labyrinth.center)
        self.screen.blit(text_surface, text_rect)

        # battle button
        button_rect_battle = pygame.Rect(
                20 * self.nb_pixels_by_box,
                30 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_battle
        )

        text_surface = self.font.render("BATTLE", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_battle.center)
        self.screen.blit(text_surface, text_rect)

        # back button
        button_rect_home = pygame.Rect(
                20 * self.nb_pixels_by_box,
                40 * self.nb_pixels_by_box,
                200,50
                )
        pygame.draw.rect(
            self.screen,
            color,
            button_rect_home
        )
        
        text_surface = self.font.render("BACK", True, (0,0,0))
        text_rect = text_surface.get_rect(center=button_rect_home.center)
        self.screen.blit(text_surface, text_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if button_rect_auto.collidepoint(pos):
                    self.MODE = "auto"
                    self.screen_type = "home"
                    return
                elif button_rect_labyrinth.collidepoint(pos):
                    self.MODE = "player"
                    self.screen_type = "home"
                    return
                elif button_rect_battle.collidepoint(pos):
                    self.MODE = "battle"
                    self.screen_type = "home"
                    return
                elif button_rect_home.collidepoint(pos):
                    self.screen_type = "home"
                    return

    def update_robot_position(self, new_position: Coordinate) -> None:
        self.robot = new_position
    
    def update_player_position(self, new_position: Coordinate) -> None:
        self.player = new_position

if __name__ == "__main__":

    maze = [
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 1, 0],
    ]

    gd = GridDisplay(
        maze=maze,
        size=(5, 5),
        nb_pixels_by_box=40,
        period_duration=20,
    )

    running = True
    while running:
        running = gd.next_period()
