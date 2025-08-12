import pygame
from copy import deepcopy
from random import choice, randrange

W,H=10,20
TILE=45
GAME_RES=W*TILE,H*TILE
RES=750,940
FPS=60

pygame.init()
sc=pygame.display.set_mode(RES)
game_sc=pygame.Surface(GAME_RES)
clock=pygame.time.Clock()

grid=[pygame.Rect(x*TILE,y*TILE,TILE,TILE) for x in range(W) for y in range(H)]

fig_pos=[ [(-1,0),(-2,0),(0,0),(1,0)],
          [(0,-1),(-1,-1),(-1,0),(0,0)],
          [(-1,0),(-1,1),(0,0),(0,-1)],
          [(0,0),(-1,0),(0,1),(-1,-1)],
          [(0,0),(0,-1),(0,1),(-1,-1)],
          [(0,0),(0,-1),(0,1),(1,-1)],
          [(0,0),(0,-1),(0,1),(-1,0)]]

figures=[[pygame.Rect(x+W//2,y+1,1,1) for x,y in f] for f in fig_pos]

field=[[0 for _ in range(W)] for _ in range(H)]

anim_count,anim_speed,anim_limit=0,60,2000

# прості кольори замість фону
bg_color=(10,10,30)
game_bg_color=(20,20,50)

def get_color():
    return (randrange(30,256),randrange(30,256),randrange(30,256))

figure,next_figure=deepcopy(choice(figures)),deepcopy(choice(figures))
color,next_color=get_color(),get_color()

score,lines=0,0
scores={0:0,1:100,2:300,3:700,4:1500}

def check_borders():
    for i in range(4):
        if figure[i].x<0 or figure[i].x>W-1:
            return False
        if figure[i].y>H-1:
            return False
        if field[figure[i].y][figure[i].x]:
            return False
    return True

def get_record():
    try:
        with open('record','r') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record','w') as f:
            f.write('0')
        return '0'

def set_record(record,score):
    rec=max(int(record),score)
    with open('record','w') as f:
        f.write(str(rec))

font=pygame.font.SysFont('Arial',45)
main_font=pygame.font.SysFont('Arial',65)

title_tetris=main_font.render('TETRIS',True,(255,140,0))
title_score=font.render('score:',True,(0,255,0))
title_record=font.render('record:',True,(128,0,128))

while True:
    record=get_record()
    dx,rotate=0,False
    sc.fill(bg_color)
    game_sc.fill(game_bg_color)
    for i_rect in grid:
        pygame.draw.rect(game_sc,(40,40,40),i_rect,1)

    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            exit()
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_LEFT:
                dx=-1
            elif e.key==pygame.K_RIGHT:
                dx=1
            elif e.key==pygame.K_DOWN:
                anim_limit=100
            elif e.key==pygame.K_UP:
                rotate=True

    figure_old=deepcopy(figure)
    for i in range(4):
        figure[i].x+=dx
        if not check_borders():
            figure=deepcopy(figure_old)
            break

    anim_count+=anim_speed
    if anim_count>anim_limit:
        anim_count=0
        figure_old=deepcopy(figure)
        for i in range(4):
            figure[i].y+=1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x]=color
                figure,color=next_figure,next_color
                next_figure,next_color=deepcopy(choice(figures)),get_color()
                anim_limit=2000
                break

    center=figure[0]
    figure_old=deepcopy(figure)
    if rotate:
        for i in range(4):
            x=figure[i].y-center.y
            y=figure[i].x-center.x
            figure[i].x=center.x - x
            figure[i].y=center.y + y
            if not check_borders():
                figure=deepcopy(figure_old)
                break

    line,lines=H-1,0
    for row in range(H-1,-1,-1):
        count=0
        for i in range(W):
            if field[row][i]:
                count+=1
            field[line][i]=field[row][i]
        if count<W:
            line-=1
        else:
            anim_speed+=3
            lines+=1

    score+=scores[lines]

    for y,row in enumerate(field):
        for x,col in enumerate(row):
            if col:
                r=pygame.Rect(x*TILE,y*TILE,TILE-2,TILE-2)
                pygame.draw.rect(game_sc,col,r)

    for i in range(4):
        r=pygame.Rect(figure[i].x*TILE,figure[i].y*TILE,TILE-2,TILE-2)
        pygame.draw.rect(game_sc,color,r)

    for i in range(4):
        r=pygame.Rect(next_figure[i].x*TILE+380,next_figure[i].y*TILE+185,TILE-2,TILE-2)
        pygame.draw.rect(sc,next_color,r)

    sc.blit(game_sc,(20,20))
    sc.blit(title_tetris,(485,-10))
    sc.blit(title_score,(535,780))
    sc.blit(font.render(str(score),True,(255,255,255)),(550,840))
    sc.blit(title_record,(525,650))
    sc.blit(font.render(record,True,(255,215,0)),(550,710))

    for i in range(W):
        if field[0][i]:
            set_record(record,score)
            field=[[0 for _ in range(W)] for _ in range(H)]
            anim_count,anim_speed,anim_limit=0,60,2000
            score=0
            for i_rect in grid:
                pygame.draw.rect(game_sc,get_color(),i_rect)
                sc.blit(game_sc,(20,20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)
