import pygame
from worm import Worm
from food import Food
from wall import Wall

pygame.init()

tile_width=20
score=0
level=0
font = pygame.font.Font(None, 30)
speed=5

def create_background(screen,width,height):
  colors=[(171, 191, 71),(196, 212, 119)]
  y=0
  while y<height:
    x=0
    while x<width:
      row=y//tile_width
      col=x//tile_width
      pygame.draw.rect(screen,colors[(row+col)%2],pygame.Rect(x,y,tile_width,tile_width))
      x+=tile_width
    y+=tile_width
  

running=True
screen=pygame.display.set_mode((400,300))
clock=pygame.time.Clock()

worm=Worm(tile_width)
wall = Wall(tile_width)
food1=Food(tile_width,worm,wall)
food2=Food(tile_width,worm,wall)

while running:
  filtered_events=[]
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False
    else:
      filtered_events.append(event)

 
  create_background(screen,400,300)
  
  worm.process_input(filtered_events)
  worm.move()

  if wall.hit_wall(worm.points[0]):
    running=False

  pos=food.can_eat(worm.points[0])
  if(pos!=None):
    worm.increase(pos)
    score+=1
    food=Food(tile_width,worm,wall)
    if score % 3 == 0:
                wall.next_level() 
                level+=1
                speed+=1


  head = worm.points[0]
  if head.X < 0 or head.X >= 400 or head.Y < 0 or head.Y >= 300:
    running = False

  

  worm.draw(screen)
  food.draw(screen)
  wall.draw(screen)

  score_text = font.render(f"Score: {score}", True, (0, 0, 0))
  level_text = font.render(f"Level: {level}", True, (0, 0, 0))

  screen.blit(score_text, (10, 10))
  screen.blit(level_text, (10, 35))


  pygame.display.flip()
  clock.tick(speed)

pygame.quit()