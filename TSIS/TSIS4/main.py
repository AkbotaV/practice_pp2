import pygame
from db import create_table, get_or_create_player, get_best_score,leaderboard,save_session
from game import run_game
import json

def load_settings():
    try:
        with open("settings.json", "r") as f:
            return json.load(f)
    except:
        return {
            "snake_color": [64, 70, 194],
            "grid": False,
            "sound": False
        }

def save_settings(settings):
    with open("settings.json", "w") as f:
        json.dump(settings, f, indent=4)



pygame.init()
settings = load_settings()
create_table()

state="menu"
username=""
player_id=None
running=True
personal_best=0
last_score = 0
last_level = 0


screen=pygame.display.set_mode((400,300))
pygame.display.set_caption("snake")
 
font=pygame.font.Font(None,50)
small_font=pygame.font.Font(None,30)
clock=pygame.time.Clock()

def draw_button(screen,rect,text):
  pygame.draw.rect(screen,(180,180,180),rect)
  pygame.draw.rect(screen,(0,0,0),rect,2)
  txt=small_font.render(text,True,(0,0,0))
  txt_rect=txt.get_rect(center=rect.center)
  screen.blit(txt, txt_rect)

play_button        = pygame.Rect(120, 150, 160, 35)
settings_button    = pygame.Rect(120, 190, 160, 35)
leaderboard_button = pygame.Rect(120, 230, 160, 35)
quit_button        = pygame.Rect(120, 270, 160, 35)
back_button        = pygame.Rect(120, 250, 160, 35)
grid_button        = pygame.Rect(100, 80,  200, 35)
sound_button       = pygame.Rect(100, 130, 200, 35)

while running:
  screen.fill((240,240,240))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
            running = False
    
    if  state=="menu":

      if  event.type==pygame.KEYDOWN:
        if event.key==pygame.K_BACKSPACE:
         username=username[:-1]
        elif event.key==pygame.K_RETURN:
         if username.strip()!="":
            player_id=get_or_create_player(username)
            personal_best=get_best_score(player_id)
            state="game"
        else:
              if len(username) < 15:
                 username += event.unicode

      if event.type==pygame.MOUSEBUTTONDOWN:
        if play_button.collidepoint(event.pos):
          if username.strip()!="":
            player_id=get_or_create_player(username)
            personal_best=get_best_score(player_id)
            state="game"

        elif quit_button.collidepoint(event.pos):
          running=False
        
        elif leaderboard_button.collidepoint(event.pos):
          state = "leaderboard"
        
        elif settings_button.collidepoint(event.pos):
          state = "settings"

    elif state == "game":

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                state = "menu"

    
    elif state == "leaderboard":
      if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
        state = "menu"

      if event.type == pygame.MOUSEBUTTONDOWN:
        if back_button.collidepoint(event.pos):
            state = "menu"
      
    elif state == "gameover":
        if event.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(event.pos):
                state = "game"
            elif quit_button.collidepoint(event.pos):
                state = "menu"

    elif state == "settings":
      if event.type == pygame.MOUSEBUTTONDOWN:
        if back_button.collidepoint(event.pos):
            save_settings(settings)
            state = "menu"
        elif grid_button.collidepoint(event.pos):
            settings["grid"] = not settings["grid"]
        elif sound_button.collidepoint(event.pos):
            settings["sound"] = not settings["sound"]
        elif pygame.Rect(150, 180, 100, 30).collidepoint(event.pos):  # ← добавь
            colors = [
                [64, 70, 194],    # синий (дефолт)
                [0, 200, 80],     # зелёный
                [220, 50, 50],    # красный
                [255, 200, 40],   # золотой
                [160, 60, 220],   # фиолетовый
            ]
            current = settings["snake_color"]
            if current in colors:
                i = colors.index(current)
                settings["snake_color"] = colors[(i + 1) % len(colors)]
            else:
                settings["snake_color"] = colors[0]
        


  if state == "menu":
        #Title
        title = font.render("Snake Game", True, (0, 0, 0))
        title_rect = title.get_rect(center=(400 // 2, 40))
        screen.blit(title, title_rect)

        # Username label
        label = small_font.render("Enter username:", True, (0, 0, 0))
        label_rect = label.get_rect(center=(400 // 2, 90))
        screen.blit(label, label_rect)

        # Input box
        input_box = pygame.Rect(100, 110, 200, 35)
        pygame.draw.rect(screen, (255, 255, 255), input_box)
        pygame.draw.rect(screen, (0, 0, 0), input_box, 2)

        name_surface = small_font.render(username, True, (0, 0, 0))
        screen.blit(name_surface, (input_box.x + 8, input_box.y + 6))

        # Buttons
        draw_button(screen, play_button, "Play")
        draw_button(screen, settings_button, "Settings")
        draw_button(screen, quit_button, "Quit")
        draw_button(screen, leaderboard_button, "Leaderboard")


  elif state == "game":
      score, level, quit_game = run_game(screen, clock, personal_best, settings["snake_color"],settings)
      if quit_game:
          running = False
      else:
          save_session(player_id, score, level)
          personal_best = get_best_score(player_id)
          last_score = score
          last_level = level
          state = "gameover"

  elif state == "gameover":
      screen.fill((240, 240, 240))
      title = font.render("Game Over!", True, (200, 0, 0))
      screen.blit(title, title.get_rect(center=(200, 50)))

      s = small_font.render(f"Score: {last_score}", True, (0, 0, 0))
      l = small_font.render(f"Level: {last_level}", True, (0, 0, 0))
      b = small_font.render(f"Best:  {personal_best}", True, (0, 0, 0))
      screen.blit(s, (140, 120))
      screen.blit(l, (140, 150))
      screen.blit(b, (140, 180))

      draw_button(screen, play_button, "Retry")
      draw_button(screen, quit_button, "Menu")



  elif state == "leaderboard":
    lead_text=font.render("Leaderboard", True, (0,0,0))
    lead_rect=lead_text.get_rect(center=(400//2,20))
    screen.blit(lead_text,lead_rect)

    top_scores = leaderboard()

    y = 50
    rank = 1
    for row in top_scores:
        display_name = row[0]
        score_value = row[1]
        level_value = row[2]

        line = small_font.render(f"{rank}. {display_name}  S:{score_value}  L:{level_value}", True, (0, 0, 0))
        screen.blit(line, (20, y))
        y += 25
        rank += 1

    draw_button(screen, back_button, "Back")


  elif state == "settings":
    screen.fill((240, 240, 240))
    title = font.render("Settings", True, (0, 0, 0))
    screen.blit(title, title.get_rect(center=(200, 30)))

    grid_text  = "Grid: ON"  if settings["grid"]  else "Grid: OFF"
    sound_text = "Sound: ON" if settings["sound"] else "Sound: OFF"

    draw_button(screen, grid_button,  grid_text)
    draw_button(screen, sound_button, sound_text)
    draw_button(screen, back_button,  "Save & Back")

    color = tuple(settings["snake_color"])
    pygame.draw.rect(screen, color, pygame.Rect(150, 180, 100, 30))
    label = small_font.render("Snake color", True, (0, 0, 0))
    screen.blit(label, (145, 215))

  pygame.display.flip()
  clock.tick(60)

pygame.quit()


