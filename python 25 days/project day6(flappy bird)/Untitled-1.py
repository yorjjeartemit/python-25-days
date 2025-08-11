import pygame
import sys
import random
pygame.init()
pygame.display.set_caption("flappy bird")
size_display1=560
size_display2=480
display=pygame.display.set_mode((size_display1,size_display2))
fps=60
clock=pygame.time.Clock()
gravitoys=0.5
jump=-8
pipe_speed=3
pipe_gap=150
run=True
tick=pygame.time.get_ticks()
class Birds:
  def __init__(self):
    self.x=50
    self.y=size_display2//2
    self.radius=20
    self.y2=0
  def update(self):
    self.y2+=gravitoys
    self.y+=self.y2
    if self.y<self.radius:
      self.y=self.radius
      self.y2=0
    elif self.y>size_display2-self.radius:
      self.y=size_display2-self.radius
      self.y2=0
  def draw(self,surface):
    pygame.draw.circle(surface,(255,255,0),(int(self.x),int(self.y)),self.radius)
class Pipe:
    def __init__(self,x):
        self.x=x
        self.width=80
        self.height_top=random.randint(50,size_display2-pipe_gap-50)
        self.height_bottom=size_display2-self.height_top-pipe_gap
    def update(self):
        self.x-=pipe_speed
    def draw(self,surface):
        pygame.draw.rect(surface,(0,255,0),(self.x,0,self.width,self.height_top))
        pygame.draw.rect(surface,(0,255,0),(self.x,size_display2-self.height_bottom,self.width,self.height_bottom))
    def off_screen(self):
        return self.x+self.width<0
bird=Birds()
pipes=[Pipe(600),Pipe(900),Pipe(1200)]
def check(bird,pipes):
  if bird.y-bird.radius<=0 or bird.y+bird.radius>=size_display2:
    return True
  for pipe in pipes:
    if bird.x + bird.radius>pipe.x and bird.x-bird.radius<pipe.x+pipe.width:
      if bird.y-bird.radius<pipe.height_top or bird.y+bird.radius>size_display2-pipe.height_bottom:
        return True
  return False
while run:
  sec=(pygame.time.get_ticks()-tick)/1000
  if sec<2:
    bird.y2=0
  clock.tick(fps)
  bird.update()
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      run=False
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_SPACE:
        bird.y2=jump
        
  display.fill((135,206,232))
  for pipe in pipes:
    pipe.update()
    pipe.draw(display)
  if pipes and pipes[0].off_screen():
    pipes.pop(0)
    pipes.append(Pipe(size_display1+300))
  bird.draw(display)
  pygame.display.update()
  if check(bird,pipes):
    run=False
pygame.quit()
sys.exit()