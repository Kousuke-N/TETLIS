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
WALL, NONE, BLUE, RED, GREEN, YELLOW, ORANGE, SKY, PURPLE = (-1, 0, 1, 2, 3, 4, 5, 6, 7) 
WAIT, FALL, LAND = (0, 1, 2)
UPWARD, RIGHTWARD, DOWNWARD, LEFTWARD = (0, 1, 2, 3)

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

        self.board = Board()

        self.frame_cont = 0
        self.fall_rate = 10 # ブロックが落下するフレーム数
        self.block_state = WAIT
        self.fast_rate = False

    def update(self):
        if self.game_state == PLAY:
            self.frame_cont += 1
            if self.block_state == WAIT:
                self.block = Block()
                self.board.set_block(self.block)
                self.board.put_block(self.block)
                self.block_state = FALL
            elif self.block_state == FALL:
                if (self.frame_cont % self.fall_rate == 0) or (self.fast_rate == True and self.frame_cont % 3 == 0):
                    if self.board.down() == False:
                        self.frame_cont = 0
                        self.block_state = LAND
            elif self.block_state == LAND:
                if self.frame_cont > 5:
                    if self.board.down() != False:
                        self.block_state = FALL
                        return
                    self.board.merge_board()
                    self.board.check_remove()
                    if self.board.is_gameover() == True:
                        self.game_state = GAMEOVER
                    self.block_state = WAIT

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), SCR_RECT)
        if self.game_state == TITLE:
            screen.blit(self.title_image, (220, 80))
            screen.blit(self.play_menu_image, (240, 250))
            screen.blit(self.quit_menu_image, (240, 300))
            screen.blit(self.title_note_image, (220, 350))
            if self.cur_menu == PLAY_MENU:
                screen.blit(self.cursor_image, (220, 265))
            if self.cur_menu == QUIT_MENU:
                screen.blit(self.cursor_image, (220, 315))
        elif self.game_state == PLAY:
            self.board.draw(screen)
        elif self.game_state == GAMEOVER:
            screen.blit(self.game_over_image, (182, 80))

    def key_handler(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_UP:
                    if self.game_state == TITLE:
                        # メニューカーソルを1つアップ
                        self.cur_menu -=1
                        if self.cur_menu < 0:
                            self.cur_menu = 0
                    elif self.game_state == PLAY:
                        pass
                elif event.key == K_DOWN:
                    if self.game_state == TITLE:
                        # メニューカーソルを1つダウン
                        self.cur_menu +=1
                        if self.cur_menu > 1:
                            self.cur_menu = 1
                    elif self.game_state == PLAY:
                        self.fast_rate = True
                elif event.key == K_SPACE:
                    if self.game_state == TITLE:
                        # メニュー選択
                        if self.cur_menu == PLAY_MENU:
                            self.init_game()
                            self.game_state = PLAY
                        elif self.cur_menu == QUIT_MENU:
                            pygame.quit()
                            sys.exit()
            elif event.type == KEYUP:
                if self.game_state == PLAY:
                   self.fast_rate = False

        pressed_keys = pygame.key.get_pressed()
        # if self.frame_cont % 5 == 0:
        if pressed_keys[K_RIGHT]:
            if self.game_state == PLAY:
                if self.frame_cont % 5 == 0:
                    self.board.right()
        if pressed_keys[K_LEFT]:
            if self.game_state == PLAY:
                if self.frame_cont % 5 == 0:
                    self.board.left()


    def load_images(self):
        self.title_image = pygame.image.load("./img/title.png")
        self.play_menu_image = pygame.image.load("./img/play_menu.png")
        self.quit_menu_image = pygame.image.load("./img/quit_menu.png")
        self.cursor_image = pygame.image.load("./img/cursor.png")
        self.title_note_image = pygame.image.load("./img/title_note.png")
        self.game_over_image = pygame.image.load("./img/game_over.png")

    def load_sounds(self):
        pass

##########################################################################

class Board():
    def __init__(self):
        self.rect = pygame.Rect((20, 20), (240, 400))  
        self.board_data = [[-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],  # 表示されない
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],  # 表示されない
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],  # 表示されない
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],  # 表示されない
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1],
                           [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1, -1]]

        self.init_block_data()

    def init_block_data(self):
        self.block_data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), self.rect)
        for i in range(21):
            for j in range(12):
                # ブロックの描画
                if self.board_data[i+4][j] == WALL or self.block_data[i+4][j] == WALL:
                    pygame.draw.rect(screen, (128, 128, 128), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

                elif self.board_data[i+4][j] == NONE and self.block_data[i+4][j] == NONE:
                    pygame.draw.rect(screen, (0, 0, 0),
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

                elif self.board_data[i+4][j] == BLUE or self.block_data[i+4][j] == BLUE:
                    pygame.draw.rect(screen, (0, 0, 255), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

                elif self.board_data[i+4][j] == RED or self.block_data[i+4][j] == RED:
                    pygame.draw.rect(screen, (255, 0, 0), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

                elif self.board_data[i+4][j] == GREEN or self.block_data[i+4][j] == GREEN:
                    pygame.draw.rect(screen, (0, 255, 0), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

                elif self.board_data[i+4][j] == YELLOW or self.block_data[i+4][j] == YELLOW:
                    pygame.draw.rect(screen, (255, 255, 0), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

                elif self.board_data[i+4][j] == ORANGE or self.block_data[i+4][j] == ORANGE:
                    pygame.draw.rect(screen, (255, 165, 0), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))   

                elif self.board_data[i+4][j] == SKY or self.block_data[i+4][j] == SKY:
                    pygame.draw.rect(screen, (135, 206, 235), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

                elif self.board_data[i+4][j] == PURPLE or self.block_data[i+4][j] == PURPLE:
                    pygame.draw.rect(screen, (128, 0, 128), 
                        pygame.Rect((20+j*20, 40+i*20), (20, 20)))

    def set_block(self, block):
        self.block = block

    def put_block(self, block):
        shape = block.shape
        for i in range(4):
            for j in range(4):
                self.block_data[i][4+j] = shape[i][j]

    def down(self):
        for i in range(24):
            for j in range(12):
                if self.block_data[i][j] > 0:
                    if self.board_data[i+1][j] != 0:
                        return False

        self.block_data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]] + self.block_data
        return True

    def right(self):
        for i in range(25):
            for j in range(11):
                if self.block_data[i][j] > 0:
                    if self.board_data[i][j + 1] != 0:
                        return False

        for i in range(25):
            self.block_data[i] = [0] + self.block_data[i]
        return True

    def left(self):
        for i in range(25):
            for j in range(11):
                if self.block_data[i][j + 1] > 0:
                    if self.board_data[i][j] != 0:
                        return False

        for i in range(25):
            for j in range(12):
                if j < 11:
                    self.block_data[i][j] = self.block_data[i][j+1]
                if j == 11:
                    self.block_data[i][j] = 0
        return True

    def rotate_r(self):
        r_block_data = [[0 for i in range(12)] for j in range(25)]
        r_list = [[ 0, 1],
                  [-1, 0]]
        for i in range(21):
            for j in range(12):
                if self.block_data[i+4][j] > 0:
                    x = i+4
                    y = j

    def merge_board(self):
        for i in range(25):
            for j in range(12):
                if self.block_data[i][j] > 0:
                    self.board_data[i][j] = self.block_data[i][j]

        self.init_block_data()

    def check_remove(self):
        for i in range(24):
            for j in range(10):
                if self.board_data[i][1+j] == NONE:
                    break
                if j == 9:
                    self.remove_line(i)

    def remove_line(self, line):
        for j in range(10):
            self.board_data[line][j+1] = NONE

        for i in range(line):
            for j in range(10):
                self.board_data[line-i][1+j] = self.board_data[line-i-1][1+j]


    def is_gameover(self):
        if self.board_data[4][5] > 0 or self.board_data[4][6] > 0:
            return True

    def check_block(self):
        pass

##########################################################################

class Block():
    def __init__(self):
        self.type = random.randint(BLUE, PURPLE)
        self.block_ward = UPWARD

        if self.type == BLUE:
            self.block = [[[1,2], [2,2], [3,1], [3,2]], 
                         [[2,0], [1,0], [1,1], [1,2]], 
                         [[0,0], [0,1], [1,0], [1,2]], 
                         [[0,0], [0,1], [0,2], [1,2]]]
            self.shape = [[0, 0, 0, 0],
                          [0, 0, 1, 0],
                          [0, 0, 1, 0],
                          [0, 1, 1, 0]] 
        elif self.type == RED:
            self.block = [[[0,1], [1,1], [2,1], [3,1]], 
                         [[0,0], [1,0], [1,1], [1,2]], 
                         [[0,0], [0,1], [1,0], [1,2]], 
                         [[0,0], [0,1], [0,2], [1,2]]]
            self.shape = [[0, 0, 0, 0],
                          [0, 0, 2, 0],
                          [0, 2, 2, 0],
                          [0, 2, 0, 0]] 
        elif self.type == GREEN:
            self.block = [[[0,1], [1,1], [2,1], [3,1]], 
                         [[0,0], [1,0], [1,1], [1,2]], 
                         [[0,0], [0,1], [1,0], [1,2]], 
                         [[0,0], [0,1], [0,2], [1,2]]]
            self.shape = [[0, 0, 0, 0],
                          [0, 3, 0, 0],
                          [0, 3, 3, 0],
                          [0, 0, 3, 0]] 
        elif self.type == YELLOW:
            self.block = [[[0,1], [1,1], [2,1], [3,1]], 
                         [[0,0], [1,0], [1,1], [1,2]], 
                         [[0,0], [0,1], [1,0], [1,2]], 
                         [[0,0], [0,1], [0,2], [1,2]]]
            self.shape = [[0, 0, 0, 0],
                          [0, 4, 0, 0],
                          [0, 4, 0, 0],
                          [0, 4, 4, 0]]  
        elif self.type == ORANGE:
            self.block = [[[0,1], [1,1], [2,1], [3,1]], 
                         [[0,0], [1,0], [1,1], [1,2]], 
                         [[0,0], [0,1], [1,0], [1,2]], 
                         [[0,0], [0,1], [0,2], [1,2]]]
            self.shape = [[0, 0, 0, 0],
                          [0, 0, 0, 0],
                          [0, 5, 5, 0],
                          [0, 5, 5, 0]]  
        elif self.type == SKY:
            self.block = [[[0,1], [1,1], [2,1], [3,1]], 
                         [[0,0], [1,0], [1,1], [1,2]], 
                         [[0,0], [0,1], [1,0], [1,2]], 
                         [[0,0], [0,1], [0,2], [1,2]]]
            self.shape = [[0, 6, 0, 0],
                          [0, 6, 0, 0],
                          [0, 6, 0, 0],
                          [0, 6, 0, 0]] 
        elif self.type == PURPLE:
            self.block = [[[0,1], [1,1], [2,1], [3,1]], 
                         [[0,0], [1,0], [1,1], [1,2]], 
                         [[0,0], [0,1], [1,0], [1,2]], 
                         [[0,0], [0,1], [0,2], [1,2]]]
            self.shape = [[0, 0, 0, 0],
                          [0, 7, 0, 0],
                          [0, 7, 7, 0],
                          [0, 7, 0, 0]]                  

    def update(self):
        pass

    def draw(self, screen):
        pass
        
    def get_block(self):
        return self.block

##########################################################################

if __name__ == "__main__":
    Main()
