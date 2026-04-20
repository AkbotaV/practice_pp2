import pygame
from ball import draw_ball

pygame.init()
screen=pygame.display.set_mode((800,500))
done=False
x=400
y=250

while not done:
  for event in pygame.event.get():
      if event.type==pygame.QUIT:
        done=True

      if event.type==pygame.KEYDOWN:
        if event.key==pygame.K_UP and y-20>=25:
          y-=20
        elif event.key==pygame.K_DOWN and y+20<=500-25:
          y+=20
        elif event.key==pygame.K_LEFT and x-20>=25:
          x-=20
        elif event.key==pygame.K_RIGHT and x+20<=800-25:
          x+=20
  screen.fill((255,255,255))
  draw_ball(screen,x,y)
  pygame.display.flip()
  