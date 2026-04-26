import pygame
from persistence import load_leaderboard, save_settings

pygame.font.init()

font = pygame.font.Font(None, 40)
small_font = pygame.font.Font(None, 28)

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (180,180,180)


def draw_text(screen, text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_button(screen, text, rect):
    pygame.draw.rect(screen, GRAY, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    txt = small_font.render(text, True, BLACK)
    screen.blit(txt, txt.get_rect(center=rect.center))


def button_clicked(rect, event):
    return event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(event.pos)

def main_menu(screen):
    play_btn = pygame.Rect(120, 200, 160, 40)
    leaderboard_btn = pygame.Rect(120, 260, 160, 40)
    settings_btn = pygame.Rect(120, 320, 160, 40)
    quit_btn = pygame.Rect(120, 380, 160, 40)

    while True:
        screen.fill(WHITE)
        draw_text(screen, "RACER GAME", 110, 100)

        draw_button(screen, "Play", play_btn)
        draw_button(screen, "Leaderboard", leaderboard_btn)
        draw_button(screen, "Settings", settings_btn)
        draw_button(screen, "Quit", quit_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if button_clicked(play_btn, event):
                return "play"

            if button_clicked(leaderboard_btn, event):
                return "leaderboard"

            if button_clicked(settings_btn, event):
                return "settings"

            if button_clicked(quit_btn, event):
                pygame.quit()
                exit()

        pygame.display.update()



def username_input(screen):
    name = ""

    while True:
        screen.fill(WHITE)
        draw_text(screen, "Enter name:", 120, 200)
        draw_text(screen, name, 120, 260)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 10:
                        name += event.unicode

        pygame.display.update()


def leaderboard_screen(screen):
    data = load_leaderboard()
    back_btn = pygame.Rect(120, 500, 160, 40)

    while True:
        screen.fill(WHITE)
        draw_text(screen, "LEADERBOARD", 90, 50)

        y = 120
        for i, entry in enumerate(data):
            text = f"{i+1}. {entry['name']} - {entry['score']} ({entry.get('distance',0)}m)"
            draw_text(screen, text, 80, y)
            y += 40

        draw_button(screen, "Back", back_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if button_clicked(back_btn, event):
                return

        pygame.display.update()
  

def settings_screen(screen, settings):
    back_btn = pygame.Rect(120, 450, 160, 40)
    sound_btn = pygame.Rect(100, 200, 200, 40)
    diff_btn = pygame.Rect(100, 260, 200, 40)   
    color_btn = pygame.Rect(100, 320, 200, 40)

    DIFFICULTIES = ["easy", "normal", "hard"]
    COLORS = ["red", "blue", "green"]

    while True:
        screen.fill(WHITE)
        draw_text(screen, "SETTINGS", 120, 100)

        draw_button(screen, f"Sound: {settings['sound']}", sound_btn)
        draw_button(screen, f"Difficulty: {settings['difficulty']}", diff_btn)   
        draw_button(screen, f"Color: {settings['car_color']}", color_btn) 
        draw_button(screen, "Back", back_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if button_clicked(sound_btn, event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if button_clicked(diff_btn, event):                               
                i = DIFFICULTIES.index(settings["difficulty"])
                settings["difficulty"] = DIFFICULTIES[(i + 1) % 3]
                save_settings(settings)

            if button_clicked(color_btn, event):                               
                i = COLORS.index(settings["car_color"])
                settings["car_color"] = COLORS[(i + 1) % 4]
                save_settings(settings)

            if button_clicked(back_btn, event):
                return

        pygame.display.update()