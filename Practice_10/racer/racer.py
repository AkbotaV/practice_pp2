import pygame
import sys
import random
import time 

pygame.init()
pygame.mixer.init()

screen_width=400
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Racer")
running=True

speed=5
speed_coin=3
coins_collected=0
score=0
clock=pygame.time.Clock()

INC_SPEED=pygame.USEREVENT +1
SPAWN_COIN=pygame.USEREVENT+2
pygame.time.set_timer(SPAWN_COIN,1000)
pygame.time.set_timer(INC_SPEED,1000)

background=pygame.image.load("AnimatedStreet.png")
crash_sound = pygame.mixer.Sound("crash.wav")
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

font=pygame.font.Font(None,40)
font_small=pygame.font.Font(None,40)
game_over=font.render("GAME OVER",True,(0,0,0))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
      super().__init__()
      self.image=pygame.image.load("Enemy.png")
      self.rect=self.image.get_rect()
      self.rect.center=(random.randint(40,screen_width-40),0)

    def move(self):
      global score
      self.rect.move_ip(0,speed)
      if self.rect.top>600:
        score+=1
        self.rect.top=0
        self.rect.center=(random.randint(30,370),0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
      super().__init__()
      self.image=pygame.image.load("Player.png")
      self.rect=self.image.get_rect()
      self.rect.center=(160,520)

    def move(self):
      pressed_keys=pygame.key.get_pressed()
      if self.rect.left >0:
        if pressed_keys[pygame.K_LEFT]:
          self.rect.move_ip(-5,0)
      if self.rect.right <screen_width:
        if pressed_keys[pygame.K_RIGHT]:
          self.rect.move_ip(5,0)


class Coin(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.image=pygame.image.load("coin.png")
    
    self.image = pygame.transform.scale(self.image, (50,50))
    self.rect=self.image.get_rect()
    self.rect.center=(random.randint(30,370),0)
  
  def move(self):

      self.rect.move_ip(0,speed_coin)
      if self.rect.bottom > screen_height:
        self.kill()


P1=Player()
E1=Enemy()

enemies=pygame.sprite.Group()
enemies.add(E1)
coins=pygame.sprite.Group()
all_sprites=pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)



while running:
  for event in pygame.event.get():
    if event.type==SPAWN_COIN:
      if len(coins)<3 and random.random()<0.7:
        new_coin=Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)

    if event.type==INC_SPEED:
      speed+=0.5

    if  event.type==pygame.QUIT:
      running=False
      
  screen.blit(background,(0,0))
  scores = font_small.render(f"Score:{str(score)}", True, (0,0,0))
  screen.blit(scores, (10,10))

  for entity in all_sprites:
    screen.blit(entity.image,entity.rect)
    entity.move()

  if pygame.sprite.spritecollideany(P1,enemies):
    pygame.mixer.music.stop()
    crash_sound.play()
    time.sleep(0.5)
    screen.fill((255,0,0))
    screen.blit(game_over,(80,300))
    pygame.display.update()
    for entity in all_sprites:
      entity.kill()
    time.sleep(2)
    pygame.quit()
    sys.exit()
  
  hit_coins = pygame.sprite.spritecollide(P1, coins, True)

  for coin in hit_coins:
    coins_collected+=1
  
  coin_text=font.render(f"coins: {coins_collected}",True,(0,0,0))
  screen.blit(coin_text,(screen_width-150,10))
  
  pygame.display.update()
  clock.tick(60)


pygame.quit()
sys.exit()


