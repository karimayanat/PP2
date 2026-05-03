import pygame
import sys
import racer
import ui
import persistence
from pygame.locals import *

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("assets/sounds/background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
crash_sound = pygame.mixer.Sound("assets/sounds/crash.wav")

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Advanced Racer Game")

FPS = 60
clock = pygame.time.Clock()
font_ui = pygame.font.SysFont("Verdana", 20)
background = pygame.image.load("assets/images/AnimatedStreet.png")

def game_loop(username, settings):
    base_speed = 4 if settings.get('difficulty') == "Easy" else 6
    racer.SPEED = base_speed
    score = 0
    coins = 0
    distance = 0
    finish_line = 10000
    
    active_power = None
    power_timer = 0
    shield_active = False
    
    is_slowed = False
    oil_timer = 0
    OIL_SLOW_DURATION = 3000
    
    player = racer.Player(settings.get('car_color', 'red'))
    enemy = racer.Enemy()
    coin = racer.Coin()
    hazard = racer.Hazard("oil")
    powerup = racer.PowerUp()
    
    racer.active_objects.empty()
    for obj in [enemy, coin, hazard, powerup]:
        racer.register(obj)

    running = True
    while running:
        dt = clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        if is_slowed:
            effective_speed = racer.SPEED * 0.4
            if current_time - oil_timer > OIL_SLOW_DURATION:
                is_slowed = False
        else:
            effective_speed = racer.SPEED
        distance += int(effective_speed / 2)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        player.move()
        for obj in racer.active_objects:
            obj.move(effective_speed)

        if distance > 0 and distance % 1500 == 0:
            racer.SPEED += 0.2

        if pygame.sprite.collide_rect(player, enemy):
            if shield_active:
                shield_active = False
                active_power = None
                enemy.reset()
            else:
                crash_sound.play()
                pygame.time.delay(1000)
                persistence.save_score(username, score, coins, distance)
                return ui.draw_game_over(SCREEN, score, coins, distance)

        if pygame.sprite.collide_rect(player, hazard):
            is_slowed = True
            oil_timer = current_time
            distance = max(0, distance - 100)
            hazard.reset()

        if pygame.sprite.collide_rect(player, coin):
            coins += coin.value
            score += coin.value * 10
            if coins % 10 == 0:
                racer.SPEED += 1
            coin.reset()

        if pygame.sprite.collide_rect(player, powerup):
            p_type = powerup.p_type
            active_power = p_type
            power_timer = current_time
            
            if p_type == "nitro":
                racer.SPEED += 5
            elif p_type == "shield":
                shield_active = True
            elif p_type == "repair":
                score += 500
                enemy.reset()
                active_power = "REPAIRED!"
            
            powerup.reset()

        if active_power == "nitro" and current_time - power_timer > 4000:
            racer.SPEED = max(base_speed, racer.SPEED - 5)
            active_power = None

        SCREEN.blit(background, (0, 0))
        
        SCREEN.blit(player.image, player.rect)
        racer.active_objects.draw(SCREEN)

        score_txt = font_ui.render(f"Score: {score}", True, (0, 0, 0))
        dist_txt = font_ui.render(f"Dist: {distance}/{finish_line}m", True, (0, 0, 0))
        coin_txt = font_ui.render(f"Coins: {coins}", True, (0, 0, 0))
        
        SCREEN.blit(score_txt, (10, 10))
        SCREEN.blit(dist_txt, (10, 35))
        SCREEN.blit(coin_txt, (10, 60))

        if active_power:
            p_color = (255, 0, 0) if is_slowed else (0, 120, 0)
            p_label = "SLOWED BY OIL" if is_slowed else f"POWER: {active_power.upper()}"
            ui.draw_text(SCREEN, p_label, 20, 250, 25, p_color)

        if distance >= finish_line:
            persistence.save_score(username, score, coins, distance)
            return ui.draw_game_over(SCREEN, score, coins, distance)

        pygame.display.update()

def main():
    current_settings = persistence.load_settings()
    while True:
        action = ui.draw_menu(SCREEN)
        
        if action == "play":
            username = ui.get_username(SCREEN)
            while True:
                result = game_loop(username, current_settings)
                if result == "menu":
                    break
        
        elif action == "leaderboard":
            ui.draw_leaderboard(SCREEN)
            
        elif action == "settings":
            current_settings = ui.draw_settings(SCREEN)

if __name__ == "__main__":
    main()