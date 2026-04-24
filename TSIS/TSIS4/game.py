import pygame
from worm import Worm
from food import Food, Poison_food
from wall import Wall
from power_up import Powerup


pygame.init()

tile_width=20


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
  

def run_game(screen,clock,personal_best, snake_color,settings):
  running=True
  score=0
  foods_eaten = 0
  level=0
  font = pygame.font.Font(None, 30)
  speed=5

  worm=Worm(tile_width)
  worm.color = tuple(snake_color)
  wall = Wall(tile_width)
  food=Food(tile_width,worm,wall)
  poison=Poison_food(tile_width,worm,wall)
  powerup = Powerup(tile_width, worm, wall)

  active_effect = None
  effect_start = 0
  shield_active = False
  base_speed = 5

  while running:
    filtered_events=[]
    for event in pygame.event.get():
      if event.type==pygame.QUIT:
        return score,level, False
      else:
        filtered_events.append(event)

  
    create_background(screen,400,300)
    
    worm.process_input(filtered_events)
    worm.move()

    if wall.hit_wall(worm.points[0]):
      if shield_active:
        shield_active = False  # щит сработал, game over не наступает
      else:
        running = False

    pos = food.can_eat(worm.points[0])
    if pos is not None:
      worm.increase(pos)
      score+=food.weight
      foods_eaten+=1
      food=Food(tile_width,worm,wall)

      if foods_eaten % 3 == 0:
                  wall.next_level() 
                  level+=1
                  speed+=1
                  if level >= 3:              # ← добавь эти две строки
                    wall.add_obstacles(worm)

    head = worm.points[0]
    if head.X < 0 or head.X >= 400 or head.Y < 0 or head.Y >= 300:
      running = False

    if food.is_expired():
          food = Food(tile_width, worm, wall)

    if poison.can_eat(worm.points[0]):
      if len(worm.points)>3:
        worm.points=worm.points[:-2]
      else:
        return score, level,False
      poison=Poison_food(tile_width,worm,wall)
    
    if poison.is_expired():
      poison = Poison_food(tile_width, worm, wall)
    

    if powerup.can_collect(worm.points[0]):
      active_effect = powerup.kind
      effect_start = pygame.time.get_ticks()

      if active_effect == "speed":
            speed = base_speed + 3
      elif active_effect == "slow":
            speed = max(2, base_speed - 2)
      elif active_effect == "shield":
            shield_active = True
      
      powerup = Powerup(tile_width, worm, wall)

    if powerup.is_expired():
        powerup = Powerup(tile_width, worm, wall)

    if active_effect in ("speed", "slow"):
        if pygame.time.get_ticks() - effect_start > 5000:
            speed = base_speed
            active_effect = None

   


    

    worm.draw(screen)
    if settings["grid"]:
        for x in range(0, 400, tile_width):
            pygame.draw.line(screen, (0,0,0), (x, 0), (x, 300), 1)
        for y in range(0, 300, tile_width):
            pygame.draw.line(screen, (0,0,0), (0, y), (400, y), 1)
    food.draw(screen)
    wall.draw(screen)
    poison.draw(screen)
    powerup.draw(screen)

    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    best_text  = font.render(f"Best: {personal_best}", True, (0, 0, 0))


    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 35))
    screen.blit(best_text,  (10, 60))


    pygame.display.flip()
    clock.tick(speed)
  return score,level, False
