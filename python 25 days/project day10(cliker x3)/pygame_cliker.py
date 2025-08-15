import pygame
pygame.init()
display=pygame.display.set_mode((128,64))
text=pygame.font.Font(None,24)
count=0
max_count=100
min_count=0
ramk_width=118
ramk_height=56
run=True
clicked=False
while run:
    mouse_pos=pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if event.button==1 and pygame.Rect(
                (display.get_width()-ramk_width)//2,
                (display.get_height()-ramk_height)//2,ramk_width,ramk_height).collidepoint(mouse_pos):
                clicked=True
                if count<max_count:
                    count+=1
        if event.type==pygame.MOUSEBUTTONUP:
            if event.button==1:
                clicked=False
    display.fill((100,100,100))
    ramk_rect = pygame.Rect(
        (display.get_width()-ramk_width)//2,
        (display.get_height()-ramk_height)//2,ramk_width,ramk_height)
    if clicked:
        anim_rect=ramk_rect.inflate(-10,-6)
    else:
        anim_rect=ramk_rect
    pygame.draw.rect(display,(255,0,0),anim_rect)
    button = text.render(str(count),True,(0,0,0))
    rect = button.get_rect(center=ramk_rect.center)
    display.blit(button,rect)
    pygame.display.update()
pygame.quit()