"""
android 対応　発表用
楕円が描画できないため、別の図形を使う
"""
import sys
from math import floor
from random import randint
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, K_SPACE, MOUSEBUTTONUP

WIDTH = 25  #default 20
HEIGHT = 14 #default 15
SIZE = 50
NUM_OF_BOMBS = 50 #80 or 200 or300
EMPTY = 0 #何もない（まだ開いていない）
BOMB = 1 #爆弾あり（まだ開いていない）
OPENED = 2 #すでに開いた
OPEN_COUNT = 0
#再帰メソッドで使われる
CHECKED = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
#特殊な状態の座標の保持
S_CHECKED = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

pygame.init()
SURFACE = pygame.display.set_mode([WIDTH*SIZE, HEIGHT*SIZE])
FPSCLOCK = pygame.time.Clock()

def num_of_bomb(field, x_pos, y_pos):
    """ 周囲にある爆弾の数を返す """
    count = 0
    for yoffset in range(-1, 2):
        for xoffset in range(-1, 2):
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and \
                field[ypos][xpos] == BOMB:
                count += 1
    return count

def open_tile(field, x_pos, y_pos):
    """ タイルをオープン """
    global OPEN_COUNT
    if CHECKED[y_pos][x_pos]:  # 既にチェック済みのタイル
        return

    CHECKED[y_pos][x_pos] = True

    for yoffset in range(-1, 2):
        for xoffset in range(-1, 2):
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and \
                field[ypos][xpos] == EMPTY:
                field[ypos][xpos] = OPENED
                OPEN_COUNT += 1
                count = num_of_bomb(field, xpos, ypos)
                if count == 0 and \
                    not (xpos == x_pos and ypos == y_pos):
                    open_tile(field, xpos, ypos)

def serch_bomb(field):
    gap = True
    test = 0
    while gap:
        #1,2の数を数える
        befor_1 = 0
        befor_2 = 0
        for i in range(HEIGHT):
            befor_1 += S_CHECKED[i].count(1)
        for i in range(HEIGHT):
            befor_2 += S_CHECKED[i].count(2)

        #全体に対して絶対爆弾を見つける
        for y_pos in range(HEIGHT):
            for x_pos in range(WIDTH):
                #数字が見えている場合
                if num_of_bomb(field,x_pos,y_pos) > 0 and \
                    field[y_pos][x_pos] == OPENED:
                    #aは爆弾があると予測されない未開封
                    #bは爆弾があると予測される未開封
                    #cは爆弾がないことが確定した未開封 →開封とみなしたい
                    a = 0
                    b = 0
                    c = 0
                    d = num_of_bomb(field,x_pos,y_pos)
                    #9*9マス　a,bを数える
                    for yoffset in range(-1, 2):
                        for xoffset in range(-1, 2):
                            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
                            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT:
                                if field[ypos][xpos] != OPENED:
                                    if S_CHECKED[ypos][xpos] == 1 :
                                        b += 1
                                    elif S_CHECKED[ypos][xpos] == 2:
                                        c += 1
                                    else:
                                        a += 1
                    #爆弾が確定する条件
                    if a == d-b-c:
                        for yoffset in range(-1, 2):
                            for xoffset in range(-1, 2):
                                xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
                                if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT:
                                    if field[ypos][xpos] != OPENED and \
                                        S_CHECKED[ypos][xpos] != 1 and \
                                        S_CHECKED[ypos][xpos] != 2 :
                                        S_CHECKED[ypos][xpos] = 1

        #全体に対して絶対安全予測を立てる
        for y_pos in range(HEIGHT):
            for x_pos in range(WIDTH):
                #数字が見えている場合
                if num_of_bomb(field,x_pos,y_pos) > 0 and \
                    field[y_pos][x_pos] == OPENED:
                    #aは爆弾があると予測されない未開封
                    #bは爆弾があると予測される未開封
                    #cは爆弾がないことが確定した未開封 →開封とみなしたい
                    a = 0
                    b = 0
                    c = 0
                    d = num_of_bomb(field,x_pos,y_pos)
                    #9*9マス　a,bを数える
                    for yoffset in range(-1, 2):
                        for xoffset in range(-1, 2):
                            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
                            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT:
                                if field[ypos][xpos] != OPENED:
                                    if S_CHECKED[ypos][xpos] == 1 :
                                        b += 1
                                    elif S_CHECKED[ypos][xpos] == 2:
                                        c += 1
                                    else:
                                        a += 1
                    #安全が確定する条件
                    if d-b <= 0:
                        for yoffset in range(-1, 2):
                            for xoffset in range(-1, 2):
                                xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
                                if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT:
                                    if field[ypos][xpos] != OPENED and \
                                        S_CHECKED[ypos][xpos] != 1 and \
                                        S_CHECKED[ypos][xpos] != 2 :
                                        S_CHECKED[ypos][xpos] = 2
        after_1 = 0
        after_2 = 0
        for i in range(HEIGHT):
            after_1 += S_CHECKED[i].count(1)
        for i in range(HEIGHT):
            after_2 += S_CHECKED[i].count(2)
        gap = (after_1-befor_1 != 0) or (after_2-befor_2 != 0)
        test += 1



def main():
    """ メインルーチン """
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_clear = largefont.render("!!CLEARED!!",
                                     True, (0, 255, 225))
    message_over = largefont.render("GAME OVER!!",
                                    True, (0, 255, 225))
    message_rect = message_clear.get_rect()
    message_rect.center = (WIDTH*SIZE/2, HEIGHT*SIZE/2)
    game_over = False

    field = [[EMPTY for xpos in range(WIDTH)]
             for ypos in range(HEIGHT)]

    # 爆弾を設置
    count = 0
    while count < NUM_OF_BOMBS:
        xpos, ypos = randint(0, WIDTH-1), randint(0, HEIGHT-1)
        if field[ypos][xpos] == EMPTY:
            field[ypos][xpos] = BOMB
            count += 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #左クリック
            if event.type == MOUSEBUTTONDOWN and \
                event.button == 1:
                xpos, ypos = floor(event.pos[0] / SIZE),\
                             floor(event.pos[1] / SIZE)
                if field[ypos][xpos] == BOMB:
                    game_over = True
                else:
                    open_tile(field, xpos, ypos)
                    serch_bomb(field)

        # 描画
        SURFACE.fill((0, 0, 0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                tile = field[ypos][xpos]
                rect = (xpos*SIZE, ypos*SIZE, SIZE, SIZE)
                rect2 = ((xpos-1)*SIZE,(ypos-1)*SIZE,3*SIZE,3*SIZE)
                pos =(xpos*SIZE + int(SIZE/2) , ypos*SIZE + int(SIZE/2))

                if tile == EMPTY or tile == BOMB:
                    pygame.draw.rect(SURFACE,
                                     (192, 192, 192), rect)
                    if game_over and tile == BOMB:
                        pygame.draw.circle(SURFACE,
                                            (225, 225, 0), pos,int(SIZE/2))
                elif tile == OPENED:
                    count = num_of_bomb(field, xpos, ypos)
                    if count > 0:
                        num_image = smallfont.render(
                            "{}".format(count), True, (255, 255, 0))
                        SURFACE.blit(num_image,
                                     (xpos*SIZE+10, ypos*SIZE+10))
                if S_CHECKED[ypos][xpos] == 1:
                    pygame.draw.line(SURFACE,(0,0,225),
                    (xpos*SIZE,ypos*SIZE),(xpos*SIZE+SIZE,ypos*SIZE+SIZE),10)
                    pygame.draw.line(SURFACE,(0,0,225),
                    (xpos*SIZE+SIZE,ypos*SIZE),(xpos*SIZE,ypos*SIZE+SIZE),10)
                if S_CHECKED[ypos][xpos] == 2 and tile != OPENED:
                    pygame.draw.circle(SURFACE,
                                        (225, 0, 0), pos,int(SIZE/2),10)

        # 線の描画
        for index in range(0, WIDTH*SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96),
                             (index, 0), (index, HEIGHT*SIZE))
        for index in range(0, HEIGHT*SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96),
                             (0, index), (WIDTH*SIZE, index))

        # メッセージの描画
        if OPEN_COUNT == WIDTH*HEIGHT - NUM_OF_BOMBS:
            SURFACE.blit(message_clear, message_rect.topleft)
        elif game_over:
            SURFACE.blit(message_over, message_rect.topleft)

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
