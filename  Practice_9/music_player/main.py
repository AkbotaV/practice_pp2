import pygame
import os

pygame.init()
pygame.mixer.init()

screen =pygame.display.set_mode((700, 400))
pygame.display.set_caption("Music Player")
running=True

music_folder = os.path.join(os.path.dirname(__file__), "music")
tracks = sorted([os.path.join(music_folder, f) for f in os.listdir(music_folder) if f.endswith(('.mp3'))])

current_index=0
big_font =pygame.font.SysFont("arial", 30)
small_font = pygame.font.SysFont("arial", 24)

full_length = 0

def play():
  global full_length
  pygame.mixer.music.load(tracks[current_index])
  pygame.mixer.music.play()
  sound = pygame.mixer.Sound(tracks[current_index])
  full_length = int(sound.get_length())

def stop():
  pygame.mixer.music.stop()

def next_track():
  global current_index
  current_index=(current_index+1)%len(tracks)
  play()

def previous_track():
  global current_index
  current_index=(current_index-1)%len(tracks)
  play()

def format_time(seconds):
  minutes=seconds//60
  secs=seconds%60
  return f"{minutes:02}:{secs:02}"

while running:
  for event in pygame.event.get():
    if event.type==pygame.QUIT:
      running=False
    if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_p:
        play()
      if event.key==pygame.K_s:
        stop()
      if event.key==pygame.K_n:
        next_track()   
      if event.key==pygame.K_b:
        previous_track()
        
      if event.key == pygame.K_q:
                running = False
                

  screen.fill((0,0,0))

  track_name=os.path.basename(tracks[current_index])
  text=big_font.render(track_name,True,(255,182,193))


  position = pygame.mixer.music.get_pos() // 1000

  position_text = small_font.render(f'{format_time(position)}/{format_time(full_length)}', True, (255, 255, 255))
  screen.blit(text,(50,150))
  screen.blit(position_text, (50, 200))
  pygame.display.flip()