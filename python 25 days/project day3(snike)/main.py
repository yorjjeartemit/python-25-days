import pygame
import random
pygame.init()
size_display=(480, 480)
display=pygame.display.set_mode(size_display, pygame.RESIZABLE)
pygame.display.set_caption("snake")
clock=pygame.time.Clock()
fps=8
run=True
size1=20
serpent=[(5,5),(4,5),(3,5)]
dx,dy=1,0
def apple(snake,width,height,size2):
    apple_cost=max(min((width+height)//16,10),3)
    x1=width//size2
    y1=height//size2
    apples=[]
    while len(apples)<apple_cost:
        pos=(random.randint(0,x1-1),random.randint(0,y1-1))
        if pos not in snake and pos not in apples:
            apples.append(pos)
    return apples
apples=apple(serpent,display.get_width(),display.get_height(),size1)
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        elif event.type==pygame.VIDEORESIZE:
            apples=apple(serpent,display.get_width(),display.get_height(),size1)
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP and dy==0:
                dx,dy=0,-1
            elif event.key==pygame.K_DOWN and dy==0:
                dx,dy=0,1
            elif event.key==pygame.K_LEFT and dx==0:
                dx,dy=-1,0
            elif event.key==pygame.K_RIGHT and dx==0:
                dx,dy=1,0
    display.fill((100,100,100))
    x_square=display.get_width()//size1
    y_square=display.get_height()//size1
    head_x,head_y=serpent[0]
    new_head=((head_x+dx)%x_square,(head_y+dy)%y_square)
    if new_head in serpent[1:]:
        print("програш змійка вдарилась у себе")
        run=False
    serpent.insert(0,new_head)
    if len(apples)==0:
        print("перемога усі яблука зїдено")
        run=False
    if new_head in apples:
        apples.remove(new_head)
    else:
        serpent.pop()
    for segment in serpent:
        pygame.draw.rect(display,(0,255,0),(segment[0]*size1,segment[1]*size1,size1,size1))
    for i in apples:
        pygame.draw.rect(display,(255,0,0),(i[0]*size1,i[1]*size1,size1,size1))
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
