#imports
import pygame
import random
pygame.init()
#settings varible
setting={
    "row":16,
    "col":16,
    "mines":16,
    "width":512,
    "height":512
}
#settings display
display=pygame.display.set_mode((setting["width"],setting["height"]),pygame.RESIZABLE)
pygame.display.set_caption("сапер")
times=pygame.time.Clock()
text=pygame.font.SysFont(None,32)
#variable color
white = (255, 255, 255)
red=(255,0,0)
black=(0,0,0)
grey=(100,100,100)
blue=(0,0,255)
green=(0,255,0)
#varible
mine_activy=None
size_block = setting['width']//setting['col']
#classes
class Area:
    __slots__=("x","y","bomb","open_block","flag","near","seen")
    def __init__(self,x,y,bomb=False):
        self.x=x
        self.y=y
        self.bomb=bomb
        self.seen=False
        self.flag=False
        self.near=0

    def draw(self,surface):
        global mine_activy
        rect=pygame.Rect(self.x *size_block,self.y*size_block,size_block,size_block)
        if mine_activy is not None and (self.x,self.y)==mine_activy:
            pygame.draw.rect(surface,green,rect)
            pygame.draw.circle(surface,red,rect.center,size_block//4)
        elif self.seen:
            pygame.draw.rect(surface,white,rect)
            if self.bomb:
                pygame.draw.circle(surface,red,rect.center,size_block//4)
            elif self.near>0:
                text_mine=text.render(str(self.near),True,black)
                surface.blit(text_mine,(rect.x+size_block//3,rect.y+size_block//4))
        else:
            pygame.draw.rect(surface,grey,rect)
            if self.flag:
                pygame.draw.circle(surface,blue,rect.center,size_block//4)

        pygame.draw.rect(surface,black,rect,1)
def update_mines():
    total_area=setting["row"]*setting["col"]
    setting["mines"]=max(1,total_area//8)
def load_area():
    load=[[Area(x,y) for y in range(setting["row"])] for x in range(setting["col"])]
    mines_placed=0
    while mines_placed<setting["mines"]:
        x=random.randint(0,setting["col"]-1)
        y=random.randint(0,setting['row']-1)
        if not load[x][y].bomb:
            load[x][y].bomb=True
            mines_placed+=1

    for x in range(setting["col"]):
        for y in range(setting["row"]):
            if load[x][y].bomb:
                continue
            count=0
            for nx in range(max(0,x-1),min(setting["col"],x+2)):
                for ny in range(max(0,y-1),min(setting["row"],y+2)):
                    if load[nx][ny].bomb:
                        count+=1
            load[x][y].near=count
    return load
def open_block(load,x,y):
    stack=[(x,y)]
    while stack:
        cx,cy=stack.pop()
        if cx<0 or cy<0 or cx>=setting["col"] or cy>=setting["row"]:
            continue
        cell=load[cx][cy]
        if cell.seen or cell.bomb:
            continue
        cell.seen=True
        if cell.near==0:
            for dx in [-1,0,1]:
                for dy in [-1,0,1]:
                    if dx==0 and dy==0:
                        continue
                    nx,ny=cx+dx,cy+dy
                    stack.append((nx,ny))
def win(load):
    for col in load:
        for area in col:
            if not area.bomb and not area.seen:
                return False
    return True
def message(surface,message):
    font_large=pygame.font.SysFont(None,64)
    text_surf=font_large.render(message,True,(255,0,0))
    rect=text_surf.get_rect(center=(setting["width"]//2,setting["height"]//2))
    surface.blit(text_surf,rect)
def summary(game_over,game_win,minutes,seconds):
    width=400
    height=400
    summary_display=pygame.display.set_mode((width,height))
    pygame.display.set_caption("рахунок")
    font_large=pygame.font.SysFont(None,48)
    font_small=pygame.font.SysFont(None,24)
    run=True
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            if event.type==pygame.KEYDOWN:
                run=False
        summary_display.fill(grey)
        if game_over:
            text_result=font_large.render("game over", True,(255,50,50))
        elif game_win:
            text_result=font_large.render("you win", True,(50,255,50))
        else:
            text_result=font_large.render("game end",True,white)
        summary_display.blit(text_result,(width//2-text_result.get_width()//2,30))
        stats=[
            f"time play:{minutes}m {seconds}s",
            f"mines:{setting['mines']}",
            f"map size:{setting['row']} x {setting['col']}",
            "press any key to exit"
        ]
        for i,line in enumerate(stats):
            txt_surf=font_small.render(line,True,(200,200,200))
            summary_display.blit(txt_surf,(20,100+i*40))
        pygame.display.flip()
        pygame.time.Clock().tick(30)
    pygame.quit()
def place_mines(load, dontwork):
    mines_placed=0
    while mines_placed<setting["mines"]:
        x=random.randint(0,setting["col"]-1)
        y=random.randint(0,setting["row"]-1)
        if (x,y) in dontwork:
            continue
        if not load[x][y].bomb:
            load[x][y].bomb=True
            mines_placed+=1
    for x in range(setting["col"]):
        for y in range(setting["row"]):
            if load[x][y].bomb:
                continue
            count=0
            for nx in range(max(0,x-1),min(setting["col"],x+2)):
                for ny in range(max(0,y-1),min(setting["row"],y+2)):
                    if load[nx][ny].bomb:
                        count+=1
            load[x][y].near=count
def play():
    global size_block
    global display
    global setting
    global mine_activy
    run=True
    game_over=False
    game_win=False
    click_done=False
    start_time=pygame.time.get_ticks()
    size_block=setting["width"] // setting["col"]
    load=[[Area(x, y) for y in range(setting["row"])] for x in range(setting['col'])]
    while run:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False
            elif event.type==pygame.VIDEORESIZE:
                setting["width"], setting["height"] = event.w, event.h
                setting["col"] = max(1, setting["width"] // size_block)
                setting["row"] = max(1, setting["height"] // size_block)
                display = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                load = [[Area(x, y) for y in range(setting["row"])] for x in range(setting["col"])]
                update_mines()
                click_done=False
                game_over=False
                game_win=False
                mine_activy=None
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if not game_over and not game_win:
                    mx,my=pygame.mouse.get_pos()
                    x,y=mx//size_block,my//size_block
                    if x<setting["col"] and y<setting["row"]:
                        area=load[x][y]
                        if event.button==1:
                            if not area.flag:
                                if not click_done:
                                    dontwork=[]
                                    for dx in [-1, 0, 1]:
                                        for dy in [-1, 0, 1]:
                                            nx,ny=x+dx,y+dy
                                            if 0<=nx<setting["col"] and 0<=ny<setting["row"]:
                                                dontwork.append((nx,ny))
                                    place_mines(load,dontwork)
                                    click_done=True
                                if area.bomb:
                                    game_over=True
                                    mine_activy=(x,y)
                                    for row in load:
                                        for c in row:
                                            c.seen=True
                                else:
                                    open_block(load,x,y)
                                    if win(load):
                                        game_win=True
                        elif event.button==3:
                            if not area.seen:
                                area.flag=not area.flag
        display.fill(white)
        for col in load:
            for area in col:
                area.draw(display)
        if game_over:
            message(display,"game over")
        elif game_win:
            message(display,"you win")
        pygame.display.flip()
        times.tick(30)
    elapsed_ms= pygame.time.get_ticks() - start_time
    elapsed_sec=elapsed_ms//1000
    minutes =elapsed_sec// 60
    seconds =elapsed_sec %60
    summary(game_over,game_win,minutes,seconds)
    pygame.quit()
if __name__=="__main__":
    play()
