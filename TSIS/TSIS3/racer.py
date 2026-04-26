import pygame
import sys
import random
import time 
from ui import main_menu, leaderboard_screen, settings_screen, username_input
from persistence import load_settings, save_score
import os

BASE_DIR = os.path.dirname(__file__)
ASSETS = os.path.join(BASE_DIR, "assets")

pygame.init()
pygame.mixer.init()

screen_width=400
screen_height=600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Racer")
settings = load_settings()

SPAWN_COIN=pygame.USEREVENT+2
pygame.time.set_timer(SPAWN_COIN,1000)

background = pygame.image.load(os.path.join(ASSETS, "AnimatedStreet.png"))
crash_sound = pygame.mixer.Sound(os.path.join(ASSETS, "crash.wav"))
pygame.mixer.music.load(os.path.join(ASSETS, "background.wav"))

font=pygame.font.Font(None,40)
font_small=pygame.font.Font(None,40)
game_over=font.render("GAME OVER",True,(0,0,0))

clock = pygame.time.Clock()
N = 50

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
      super().__init__()
      self.image = pygame.image.load(os.path.join(ASSETS, "Enemy.png"))
      self.rect=self.image.get_rect()
      self.rect.center=(random.randint(40,screen_width-40),0)
      self.speed = speed

    def move(self):
      self.rect.move_ip(0,self.speed)
      if self.rect.top>600:
        self.rect.top=0
        self.rect.center=(random.randint(30,370),0)

class Player(pygame.sprite.Sprite):
    def __init__(self,color):
      super().__init__()
      self.image = pygame.image.load(os.path.join(ASSETS, f"player_{color}.png"))
      self.image = pygame.transform.scale(self.image, (50, 80))
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
    self.image = pygame.image.load(os.path.join(ASSETS, "coin.png"))
    coin_w=(random.randint(1,3))
    if coin_w==1:
      size_coin=25
      self.weight=10
    if coin_w==2:
      size_coin=40
      self.weight=20
    if coin_w==3:
      size_coin=55
      self.weight=30
    
    self.image = pygame.transform.scale(self.image, (size_coin, size_coin))
    self.rect=self.image.get_rect()
    self.rect.center=(random.randint(30,370),0)
  
  def move(self):

      self.rect.move_ip(0,speed_coin)
      if self.rect.bottom > screen_height:
        self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()

        self.type = random.choice(["oil", "barrier", "pothole"])


        if self.type == "oil":
            self.image = pygame.Surface((50, 30))
            self.image.fill((0, 0, 0))
        elif self.type == "barrier":
            self.image = pygame.Surface((70, 25))
            self.image.fill((255, 140, 0))
        else:
            self.image = pygame.Surface((45, 35))
            self.image.fill((100, 60, 40))

        self.rect = self.image.get_rect()
        self.speed = speed

        while True:
            self.rect.center = (random.randint(40, screen_width - 40), random.randint(-400, -50))
            if abs(self.rect.centerx - player.rect.centerx) > 70:
                break
    def move(self):
          self.rect.move_ip(0, self.speed)
          if self.rect.top > screen_height:
              self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.type = random.choice(["nitro", "shield", "repair"])

        if self.type == "nitro":
            self.image = pygame.image.load(os.path.join(ASSETS, "nitro.png"))
        elif self.type == "shield":
            self.image = pygame.image.load(os.path.join(ASSETS, "shield.png"))
        else:
            self.image = pygame.image.load(os.path.join(ASSETS, "repair.png"))

        self.image = pygame.transform.scale(self.image, (40, 40))
        self.spawn_time = pygame.time.get_ticks()

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, screen_width - 40), -50)

    def move(self):
        self.rect.move_ip(0, speed)
        if self.rect.top > screen_height:
            self.kill()
        if pygame.time.get_ticks() - self.spawn_time > 8000:
            self.kill()

def game_loop(username):
    global running, speed, speed_level, speed_coin, coins_collected, score

    diff = settings.get("difficulty", "normal")
    if diff == "easy":
        base_speed = 2
    elif diff == "hard":
        base_speed = 5
    else:
        base_speed = 3

    speed = base_speed

    speed_level=0
    speed_coin=3
    coins_collected=0
    score=0
    running=True
    distance = 0
    finish_distance = 3000

    active_power = None
    power_timer = 0
    shield = False

    SPAWN_ENEMY = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_ENEMY, 3500)
    SPAWN_OBSTACLE = pygame.USEREVENT + 4
    pygame.time.set_timer(SPAWN_OBSTACLE, 4500)
    SPAWN_POWER = pygame.USEREVENT + 5
    pygame.time.set_timer(SPAWN_POWER, 6000)

    P1 = Player(settings["car_color"])
    E1=Enemy()

    enemies=pygame.sprite.Group()
    enemies.add(E1)
    coins=pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites=pygame.sprite.Group()
    all_sprites.add(P1)
    all_sprites.add(E1)

    if settings["sound"]:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

    while running:
        for event in pygame.event.get():
          if event.type==SPAWN_COIN:
            if len(coins)<3 and random.random()<0.7:
              new_coin=Coin()
              coins.add(new_coin)
              all_sprites.add(new_coin)

          if  event.type==pygame.QUIT:
              running=False
          if event.type == SPAWN_ENEMY:
              if len(enemies) < 2:
                  new_enemy = Enemy()
                  new_enemy.speed = speed   
                  enemies.add(new_enemy)
                  all_sprites.add(new_enemy)
          if event.type == SPAWN_OBSTACLE:
              if len(obstacles) < 2:
                  obstacle = Obstacle(P1)
                  obstacles.add(obstacle)
                  all_sprites.add(obstacle)
          if event.type == SPAWN_POWER:
            if len(powerups) < 1:
              p = PowerUp()
              powerups.add(p)
              all_sprites.add(p)
        screen.blit(background,(0,0))
        distance += speed * 0.05
        score = coins_collected + int(distance // 10) + (speed_level * 10)
        remaining = max(0, finish_distance - distance)
        scores = font_small.render(f"Score:{str(score)}", True, (0,0,0))
        screen.blit(scores, (10,10))
        distance_text = font_small.render(f"Distance: {int(distance)}m", True, (0,0,0))
        screen.blit(distance_text, (10, 40))

        remaining_text = font_small.render(f"Left: {int(remaining)}m", True, (0,0,0))
        if active_power == "nitro":
            left = (4000 - (pygame.time.get_ticks() - power_timer)) // 1000
            power_text = font_small.render(f"Nitro: {left}s", True, (0,0,0))
        elif shield:
            power_text = font_small.render("Shield: ON", True, (0,0,0))
        else:
            power_text = font_small.render("Power: None", True, (0,0,0))

        screen.blit(power_text, (10, 100))
        screen.blit(remaining_text, (10, 70))

        for entity in all_sprites:
          screen.blit(entity.image,entity.rect)
          entity.move()
        for e in enemies:
          e.speed = speed
        for o in obstacles:     
          o.speed = speed  

        if pygame.sprite.spritecollideany(P1, enemies):
          if shield:
              shield = False
              active_power = None
              for e in pygame.sprite.spritecollide(P1, enemies, True):
                  all_sprites.remove(e)
          else:
              pygame.mixer.music.stop()
              if settings["sound"]:
                  crash_sound.play()

              save_score(username, score, distance)
              pygame.mixer.music.stop()

              screen.fill((30, 30, 30))
              screen.blit(font.render("GAME OVER", True, (220,50,50)), (100, 80))
              screen.blit(font_small.render(f"Player: {username}", True, (255,255,255)), (100, 180))
              screen.blit(font_small.render(f"Score: {score}", True, (255,255,255)), (100, 230))
              screen.blit(font_small.render(f"Distance: {int(distance)}m", True, (255,255,255)), (100, 280))
              screen.blit(font_small.render(f"Coins: {coins_collected}", True, (255,255,255)), (100, 330))

              retry_rect = pygame.Rect(50, 430, 130, 46)
              menu_rect  = pygame.Rect(220, 430, 130, 46)

              waiting = True
              while waiting:
                  mouse = pygame.mouse.get_pos()
                  for rect, label in [(retry_rect, "RETRY"), (menu_rect, "MENU")]:
                      pygame.draw.rect(screen, (80,80,80), rect, border_radius=8)
                      lbl = font_small.render(label, True, (255,255,255))
                      screen.blit(lbl, lbl.get_rect(center=rect.center))
                  pygame.display.update()
                  for event in pygame.event.get():
                      if event.type == pygame.QUIT:
                          pygame.quit(); sys.exit()
                      if event.type == pygame.MOUSEBUTTONDOWN:
                          if retry_rect.collidepoint(event.pos):
                               return game_loop(username)
                          if menu_rect.collidepoint(event.pos):
                              waiting = False
              return
          

        hit_obstacle = pygame.sprite.spritecollideany(P1, obstacles)

        if hit_obstacle:
            if hit_obstacle.type == "oil":
                speed = max(3, speed - 1)
                hit_obstacle.kill()
            else:
                pygame.mixer.music.stop()
                if settings["sound"]:
                    crash_sound.play()

                save_score(username, score, distance)
                pygame.mixer.music.stop()

                screen.fill((30, 30, 30))
                screen.blit(font.render("GAME OVER", True, (220,50,50)), (100, 80))
                screen.blit(font_small.render(f"Player: {username}", True, (255,255,255)), (100, 180))
                screen.blit(font_small.render(f"Score: {score}", True, (255,255,255)), (100, 230))
                screen.blit(font_small.render(f"Distance: {int(distance)}m", True, (255,255,255)), (100, 280))
                screen.blit(font_small.render(f"Coins: {coins_collected}", True, (255,255,255)), (100, 330))

                retry_rect = pygame.Rect(50, 430, 130, 46)
                menu_rect  = pygame.Rect(220, 430, 130, 46)

                waiting = True
                while waiting:
                    mouse = pygame.mouse.get_pos()
                    for rect, label in [(retry_rect, "RETRY"), (menu_rect, "MENU")]:
                        pygame.draw.rect(screen, (80,80,80), rect, border_radius=8)
                        lbl = font_small.render(label, True, (255,255,255))
                        screen.blit(lbl, lbl.get_rect(center=rect.center))
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit(); sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if retry_rect.collidepoint(event.pos):
                                 return game_loop(username)
                            if menu_rect.collidepoint(event.pos):
                                waiting = False
                return

        hit_power = pygame.sprite.spritecollide(P1, powerups, True)

        for p in hit_power:
            if active_power is None and not shield:
                if p.type == "nitro":
                    active_power = "nitro"
                    power_timer = pygame.time.get_ticks()
                elif p.type == "shield":
                    shield = True
                elif p.type == "repair":
                    if len(obstacles) > 0:
                      random.choice(obstacles.sprites()).kill()
                    active_power = None
        if active_power == "nitro":
          if pygame.time.get_ticks() - power_timer < 4000:
              speed = base_speed + 3
          else:
              active_power = None
              speed = base_speed + speed_level * 2


        hit_coins = pygame.sprite.spritecollide(P1, coins, True)

        for coin in hit_coins:
          coins_collected+=coin.weight
        
        new_level=coins_collected//N
        if new_level>speed_level:
          speed+=2
          speed_level=new_level

        if distance > 1000:
            pygame.time.set_timer(SPAWN_ENEMY, 2500)

        if distance > 2000:
            pygame.time.set_timer(SPAWN_ENEMY, 2000)
          

        coin_text=font.render(f"coins: {coins_collected}",True,(0,0,0))
        screen.blit(coin_text,(screen_width-150,10))

        if distance >= finish_distance:
          save_score(username, score + 500, distance)

          screen.fill((0,255,0))
          win_text = font.render("YOU WIN!", True, (0,0,0))
          screen.blit(win_text, (120, 250))

          pygame.display.update()
          time.sleep(2)
          return

        pygame.display.update()
        clock.tick(60)

    
while True:
    action = main_menu(screen)

    if action == "play":
        username = username_input(screen)
        game_loop(username)

    elif action == "leaderboard":
        leaderboard_screen(screen)

    elif action == "settings":
        settings_screen(screen, settings)


pygame.quit()
sys.exit()


