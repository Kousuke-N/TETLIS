#!/usr/bin/env python
#coding: utf-8
import pygame
from pygame.locals import *
import os
import math
import random
import sys

SCR_RECT = Rect(0, 0, 640, 480)
PLAY_MENU, QUIT_MENU = (0, 1)       # メニュー項目
TITLE, PLAY, GAMEOVER = (0, 1, 2)   # ゲーム状態

##########################################################################

class Main():
    def __init__(self):
        pygame.init() 
        screen = pygame.display.set_mode(SCR_RECT.size)
        pygame.display.set_caption("TETRIS")
        # 素材のロード
        self.load_images()
        self.load_sounds()
        # ゲームの初期化
        self.init_game()
        clock = pygame.time.Clock()
        #ゲームループ開始
        while True:
            clock.tick(60)
            screen.fill((0, 0, 0))
            self.update()
            self.draw(screen)
            pygame.display.update()     # 画面の更新
            self.key_handler()

    def init_game(self):
        """ゲームの初期化"""
        self.game_state = TITLE
        self.cur_menu = PLAY_MENU


    def update(self):
        pass

    def draw(self, screen):
        pass

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def load_images(self):
        pass

    def load_sounds(self):
        pass

##########################################################################

if __name__ == "__main__":
    Main()
