import pygame
from setting import *
from button import Button
from game_object import Bullet, draw_text, BossLvl3Bullet
import time
import random
import sys


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Battle")
icon = pygame.image.load("images/icon.png")
menu = pygame.image.load("images/menu.jpg")
game = pygame.image.load("images/game.jpg")
monster = pygame.image.load("images/monster.png")
boss = pygame.image.load("images/Boss1.png")
boss = pygame.transform.scale(boss, (boss_width, boss_height))
monster = pygame.transform.scale(monster, (monster_width, monster_height))
monster_lvl2 = pygame.image.load("images/monster_lvl2.png")
monster_lvl2 = pygame.transform.scale(monster_lvl2, (monster_lvl2_width, monster_lvl2_height))
monster_lvl3 = pygame.image.load("images/monster_lvl3.png")
monster_lvl3 = pygame.transform.scale(monster_lvl3, (monster_lvl3_width, monster_lvl3_height))
boss_lvl2 = pygame.image.load("images/boss_lvl2.png")
boss_lvl2 = pygame.transform.scale(boss_lvl2, (boss_lvl2_width, boss_lvl2_height))
boss_lvl3 = pygame.image.load("images/boss_lvl3.png")
boss_lvl3 = pygame.transform.scale(boss_lvl3, (boss_lvl3_width, boss_lvl3_height))
game = pygame.transform.scale(game, (screen_width, screen_height))
menu = pygame.transform.scale(menu, (screen_width, screen_height))
bullet_image = pygame.image.load("images/Meteorit.png")
bullet_image = pygame.transform.scale(bullet_image, (40, 40))
pygame.display.set_icon(icon)
rocket_image = pygame.image.load("images/rocket.png")
rocket_image = pygame.transform.scale(rocket_image, (rocket_width, rocket_height))
music_button_img = pygame.image.load("images/Music.png")
sound_button_img = pygame.image.load("images/Volume.png")

# Масштабування зображень кнопок
music_button_img = pygame.transform.scale(music_button_img, (70, 70))
sound_button_img = pygame.transform.scale(sound_button_img, (70, 70))

music_button_pos = (screen_width - 100, 20)
sound_button_pos = (screen_width - 100, 100)

music_button_rect = music_button_img.get_rect(topleft=music_button_pos)
sound_button_rect = sound_button_img.get_rect(topleft=sound_button_pos)


game_over_sound = pygame.mixer.Sound("audio/Game Over.mp3")
lvl_sound = pygame.mixer.Sound("audio/Level.mp3")
lost_life_sound = pygame.mixer.Sound("audio/lives.mp3")
sound = pygame.mixer.Sound("audio/Bullets.mp3")
sound.set_volume(0.5)
pygame.mixer.music.load("audio/music.mp3")
pygame.mixer.music.set_volume(0.5)  # Налаштуйте гучність від 0.0 (тишина) до 1.0 (максимум)
pygame.mixer.music.play(-1)

button = Button(screen_width // 2 - 100, screen_height // 3, 200, 50, "Розпочати гру", (130, 64, 163), 24)
menu_shown = True
button_shown = True
space_pressed = False
start_game = False
game_over = False
boss_spawned = False
boss_lvl2_spawned = False
boss_lvl3_spawned = False
level_started = False
final_started = False
boss_killed = False
boss_lvl2_killed = False
lives = 3
current_sound = None
font = pygame.font.SysFont(None, 50)
spawn_time = time.time() + monster_spawn_delay


music_on = True
sound_on = True

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()

def toggle_sound():
    global sound_on
    sound_on = not sound_on

    if sound_on:
        if game_over:
            game_over_sound.play()
        elif level_started:
            lvl_sound.play()
        elif lives:
            lost_life_sound.play()
    else:
        sound.stop()
        game_over_sound.stop()
        lvl_sound.stop()
        lost_life_sound.stop()

def draw_countdown(count):
    font = pygame.font.SysFont(None, 200)
    text = font.render(str(count), True, (255, 255, 255))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.update()

def countdown():
    for i in range(3, 0, -1):
        screen.blit(game, (0, 0))
        draw_countdown(i)
        time.sleep(1)

    screen.blit(game, (0, 0))
    draw_countdown("Почали!")
    time.sleep(1)

def start_new_level():
    global boss_spawned, boss_health, monster_count, game_over, start_game, menu_shown, button_shown, button, space_pressed, spawn_time, level_started, boss_killed
    monsters.clear()
    bullets.clear()
    monsters_lvl2.clear()
    monster_count = 0
    boss_spawned = False
    boss_health = 0
    game_over = False
    start_game = False
    menu_shown = False
    button_shown = False
    button.visible = False
    space_pressed = False
    spawn_time = time.time() + monster_spawn_delay
    rocket_x = 50
    rocket_y = screen_height // 2 - rocket_height // 2
    screen.blit(game, (0, 0))
    pygame.display.update()
    time.sleep(1)
    draw_text("Другий Рівень", font, (255, 255, 255), screen, screen_width // 2 - 100,
              screen_height // 2)
    pygame.display.update()
    time.sleep(2)
    if sound_on:
        lvl_sound.play()
    level_started = True
    if boss_killed:
        spawn_monsters_level2()

def start_final_game():
    global boss_lvl2_spawned, boss_lvl2_health, monster_lvl2_count, game_over, start_game, menu_shown, button_shown, button, space_pressed, spawn_time, final_started
    monsters.clear()
    bullets.clear()
    boss_lvl2_bullets.clear()
    monsters_lvl2.clear()
    monster_count = 0
    monster_lvl2_count = 0
    boss_lvl2_spawned = False
    boss_lvl2_health = 0
    game_over = False
    start_game = False
    menu_shown = False
    button_shown = False
    button.visible = False
    space_pressed = False
    boss_lvl2_killed = True
    spawn_time = time.time() + monster_spawn_delay
    rocket_x = 50
    rocket_y = screen_height // 2 - rocket_height // 2
    screen.blit(game, (0, 0))
    pygame.display.update()
    time.sleep(1)
    draw_text("Фінал!", font, (255, 255, 255), screen, screen_width // 2 - 100, screen_height // 2)
    pygame.display.update()
    time.sleep(2)
    final_started = True
    if sound_on:
        lvl_sound.play()
    if boss_lvl2_killed:
        spawn_monsters_level3()


def spawn_monsters_level2():
    global monsters_lvl2, spawn_time_lvl2, boss_lvl2_x, boss_lvl2_y, monster_lvl2_count
    if boss_killed:
        monsters_lvl2.clear()
        spawn_time_lvl2 = current_time + monster_lvl2_spawn_delay
        boss_lvl2_x = screen_width - boss_lvl2_width
        boss_lvl2_y = screen_height // 2 - boss_lvl2_height // 2
        monster_lvl2_count = 0

    def spawn_monster_lvl2():
        monster_lvl2_x = screen_width
        monster_lvl2_y = random.randint(0, screen_height - monster_lvl2_height)
        monsters_lvl2.append((monster_lvl2_x, monster_lvl2_y))

    def spawn_monster_group():
        num_monsters = random.randint(1, 3)
        for _ in range(num_monsters):
            spawn_monster_lvl2()
            global monster_lvl2_count
            monster_lvl2_count += 1

    def spawn_monsters_with_delay():
        while monster_lvl2_count < 40:
            spawn_monster_group()
            time.sleep(2)

    import threading
    threading.Thread(target=spawn_monsters_with_delay).start()


def update_monsters_lvl2():
    current_time = time.time()
    global boss_lvl2_shot_time
    for i, (monster_lvl2_x, monster_lvl2_y) in enumerate(monsters_lvl2):
        if i < len(last_shot_time_lvl2):
            if current_time - last_shot_time_lvl2[i] >= monster_lvl2_cooldown:
                new_bullet_lvl2 = Bullet(monster_lvl2_x, monster_lvl2_y + monster_lvl2_height // 2, -monster_lvl2_bullet_speed, "monster_lvl2")
                monster_lvl2_bullets.append(new_bullet_lvl2)
                last_shot_time_lvl2[i] = current_time
    if boss_lvl2_spawned and current_time - boss_lvl2_shot_time >= boss_lvl2_shot_interval:
        new_bullet_lvl2_middle = Bullet(boss_lvl2_x, boss_lvl2_y + boss_lvl2_height // 2, -boss_lvl2_bullet_speed, "boss_lvl2")
        boss_lvl2_bullets.append(new_bullet_lvl2_middle)
        new_bullet_lvl2_lower = Bullet(boss_lvl2_x, boss_lvl2_y + boss_lvl2_height // 4, -boss_lvl2_bullet_speed, "boss_lvl2")
        boss_lvl2_bullets.append(new_bullet_lvl2_lower)
        new_bullet_lvl2_upper = Bullet(boss_lvl2_x, boss_lvl2_y + 3 * boss_lvl2_height // 4, -boss_lvl2_bullet_speed, "boss_lvl2")
        boss_lvl2_bullets.append(new_bullet_lvl2_upper)
        boss_lvl2_shot_time = current_time

def update_boss_lvl2_position():
    global boss_lvl2_y, boss_lvl2_direction
    if boss_lvl2_y <= 0:
        boss_lvl2_direction = 1
    elif boss_lvl2_y + boss_lvl2_height >= screen_height:
        boss_lvl2_direction = -1
    boss_lvl2_y += boss_lvl2_speed * boss_lvl2_direction

def spawn_monsters_level3():
    global monsters_lvl3, spawn_time_lvl3, boss_lvl3_x, boss_lvl3_y, monster_lvl3_count
    if boss_lvl2_killed:
        monsters_lvl3.clear()
        spawn_time_lvl3 = current_time + monster_lvl3_spawn_delay
        boss_lvl2_x = screen_width - boss_lvl2_width
        boss_lvl2_y = screen_height // 2 - boss_lvl2_height // 2
        monster_lvl3_count = 0

    def spawn_monster_lvl3():
        monster_lvl3_x = screen_width
        monster_lvl3_y = random.randint(0, screen_height - monster_lvl3_height)
        monsters_lvl3.append((monster_lvl3_x, monster_lvl3_y))

    def spawn_monster_final():
        num_monsters = random.randint(1, 3)
        for _ in range(num_monsters):
            spawn_monster_lvl3()
            global monster_lvl3_count
            monster_lvl3_count += 1

    def spawn_monsters_final_delay():
        while monster_lvl3_count < 20:
            spawn_monster_final()
            time.sleep(2)

    import threading
    threading.Thread(target=spawn_monsters_final_delay).start()

def update_boss_lvl3_bullets():
    current_time = time.time()
    global boss_lvl3_shot_time

    if boss_lvl3_spawned and current_time - boss_lvl3_shot_time >= boss_lvl3_shot_interval:
        new_bullet_lvl3_middle = BossLvl3Bullet(boss_lvl3_x, boss_lvl3_y + boss_lvl3_height // 2,
                                                -boss_lvl3_bullet_speed,
                                                bullet_image)
        boss_lvl3_bullets.append(new_bullet_lvl3_middle)
        new_bullet_lvl3_lower = BossLvl3Bullet(boss_lvl3_x, boss_lvl3_y + boss_lvl3_height // 4,
                                               -boss_lvl3_bullet_speed,
                                               bullet_image)
        boss_lvl3_bullets.append(new_bullet_lvl3_lower)
        new_bullet_lvl3_upper = BossLvl3Bullet(boss_lvl3_x, boss_lvl3_y + 3 * boss_lvl3_height // 4,
                                               -boss_lvl3_bullet_speed,
                                               bullet_image)
        boss_lvl3_bullets.append(new_bullet_lvl3_upper)
        boss_lvl3_shot_time = current_time

def draw_boss_lvl3_bullets(screen):
    for bullet_lvl3 in boss_lvl3_bullets:
        bullet_lvl3.update()
        bullet_lvl3.draw(screen)
def update_monsters_lvl3():
    current_time = time.time()
    global boss_lvl3_shot_time
    for i, (monster_lvl3_x, monster_lvl3_y) in enumerate(monsters_lvl3):
        if i < len(last_shot_time_lvl3):
            if current_time - last_shot_time_lvl3[i] >= monster_lvl3_cooldown:
                new_bullet_lvl3 = Bullet(monster_lvl3_x, monster_lvl3_y + monster_lvl3_height // 2, -monster_lvl3_bullet_speed, "monster_lvl2")
                monster_lvl3_bullets.append(new_bullet_lvl3)
                last_shot_time_lvl3[i] = current_time


running = True
while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if music_button_rect.collidepoint(mouse_pos):
                    toggle_music()
                if sound_button_rect.collidepoint(mouse_pos):
                    toggle_sound()

        current_time = time.time()

        if menu_shown:
            screen.blit(menu, (0, 0))
            if button_shown:
                screen.blit(music_button_img, music_button_pos)
                screen.blit(sound_button_img, sound_button_pos)
                button.draw(screen)

        if start_game:
            countdown()
            level_started = False
            start_game = False
            screen.blit(game, (0, 0))
            pygame.display.update()

        if not menu_shown:
            screen.blit(game, (0, 0))
            screen.blit(rocket_image, (rocket_x, rocket_y))

        if not menu_shown:
            screen.blit(game, (0, 0))
            screen.blit(rocket_image, (rocket_x, rocket_y))
            draw_text("Життя: " + str(lives), font, (255, 255, 255), screen, 10, 10)

            for i in range(len(monsters)):
                monster_x, monster_y = monsters[i]
                monsters[i] = (monster_x - monster_speed, monster_y)

            if current_time >= spawn_time and monster_count < 20 and not boss_killed:
                num_monsters = random.randint(1, 3)
                for _ in range(num_monsters):
                    monster_x = 1190
                    monster_y = random.randint(0, screen_height - monster_height)
                    monsters.append((monster_x, monster_y))
                    monster_count += 1
                spawn_time = current_time + monster_spawn_delay

            for monster_x, monster_y in monsters:
                screen.blit(monster, (monster_x, monster_y))

            if monster_count >= 20 and not boss_spawned:
                boss_x = screen_width - boss_width
                boss_y = screen_height // 2 - boss_height // 2
                boss_spawned = True
                boss_health = 0

            if boss_spawned:
                screen.blit(boss, (boss_x, boss_y))


            if level_started:
                update_monsters_lvl2()
                for monster_lvl2_x, monster_lvl2_y in monsters_lvl2:
                    screen.blit(monster_lvl2, (monster_lvl2_x, monster_lvl2_y))

                for i in range(len(monsters_lvl2)):
                    monster_lvl2_x, monster_lvl2_y = monsters_lvl2[i]
                    monsters_lvl2[i] = (monster_lvl2_x - monster_lvl2_speed, monster_lvl2_y)

                if current_time >= spawn_time and monster_lvl2_count < 30 and not boss_killed:
                    for _ in range(random.randint(1, 3)):
                        monster_lvl2_x = screen_width
                        monster_lvl2_y = random.randint(0, screen_height - monster_lvl2_height)
                        monsters_lvl2.append((monster_lvl2_x, monster_lvl2_y))
                        monster_lvl2_count += 1
                    spawn_time_lvl2 = current_time + monster_lvl2_spawn_delay

                for bullet in bullets:
                    for i, (monster_lvl2_x, monster_lvl2_y) in enumerate(monsters_lvl2):
                        if (monster_lvl2_x < bullet.rect.x < monster_lvl2_x + monster_lvl2_width and
                                monster_lvl2_y < bullet.rect.y < monster_lvl2_y + monster_lvl2_height):
                            if bullet.source != "monster_lvl2" and bullet.source != "player":
                                del monsters_lvl2[i]
                                bullets.remove(bullet)
                                break

                for bullet in monster_lvl2_bullets:
                    bullet.update()
                    pygame.draw.circle(screen, (255, 0, 0), (bullet.rect.x, bullet.rect.y), 3)

                for bullet in boss_lvl2_bullets:
                    bullet.update()
                    pygame.draw.circle(screen, (181, 224, 9), (bullet.rect.x, bullet.rect.y), 10)

                for bullet in boss_lvl2_bullets:
                    if bullet.rect.colliderect(pygame.Rect(rocket_x, rocket_y, rocket_width, rocket_height)):
                        lives -= 1
                        lost_life_sound.play()
                        boss_lvl2_bullets.remove(bullet)
                        if lives == 0:
                            game_over = True
                        break

                monster_lvl2_bullets = [bullet for bullet in monster_lvl2_bullets if bullet.rect.x > 0]

                if monster_lvl2_count >= 40 and not boss_lvl2_spawned:
                    boss_lvl2_x = screen_width - boss_lvl2_width
                    boss_lvl2_y = screen_height // 2 - boss_lvl2_height // 2
                    boss_lvl2_spawned = True
                    boss_lvl2_health = 0
                if boss_lvl2_spawned:
                    update_boss_lvl2_position()
                    screen.blit(boss_lvl2, (boss_lvl2_x, boss_lvl2_y))

                for bullet in bullets[:]:
                    if boss_lvl2_spawned and boss_lvl2_x < bullet.rect.x < boss_lvl2_x + boss_lvl2_width and \
                            boss_lvl2_y < bullet.rect.y < boss_lvl2_y + boss_lvl2_height and bullet.source == "player":
                        bullets.remove(bullet)
                        boss_lvl2_health += 1
                        if boss_lvl2_health >= 150:
                            boss_lvl2_spawned = False
                            boss_lvl2_killed = True
                            draw_text("Молодець! Тепер цікавіше :)", font, (255, 255, 255), screen,
                                      screen_width // 2 - 200,
                                      screen_height // 2)
                            pygame.display.update()
                            pygame.time.wait(2000)
                            if boss_lvl2_killed:
                                start_final_game()

            if final_started:
                update_monsters_lvl3()
                for monster_lvl3_x, monster_lvl3_y in monsters_lvl3:
                    screen.blit(monster_lvl3, (monster_lvl3_x, monster_lvl3_y))

                for i in range(len(monsters_lvl3)):
                    monster_lvl3_x, monster_lvl3_y = monsters_lvl3[i]
                    monsters_lvl3[i] = (monster_lvl3_x - monster_lvl3_speed, monster_lvl3_y)

                if current_time >= spawn_time_lvl3 and monster_lvl3_count < 20 and not boss_lvl2_killed:
                    for _ in range(random.randint(1, 3)):
                        monster_lvl3_x = screen_width
                        monster_lvl3_y = random.randint(0, screen_height - monster_lvl3_height)
                        monsters_lvl3.append((monster_lvl3_x, monster_lvl3_y))
                        monster_lvl3_count += 1
                    spawn_time_lvl3 = current_time + monster_lvl3_spawn_delay

                if monster_lvl3_count >= 20 and not boss_lvl3_spawned:
                    all_monsters_off_screen = all(monster_lvl3_x < 0 for monster_lvl3_x, _ in monsters_lvl3)

                    if all_monsters_off_screen:
                        draw_text("БОСС", font, (255, 255, 255), screen, screen_width // 2 - 50,
                                  screen_height // 2 - 25)
                        pygame.display.update()
                        boss_spawn_timer = pygame.time.get_ticks()
                        while pygame.time.get_ticks() - boss_spawn_timer < 2000:
                            pass

                        boss_lvl3_x = screen_width - boss_lvl3_width
                        boss_lvl3_y = screen_height // 2 - boss_lvl3_height // 2
                        boss_lvl3_spawned = True
                        boss_lvl3_health = 0

                        boss_speed_x = random.randint(1, 1)
                        boss_speed_y = random.randint(1, 1)

                if boss_lvl3_spawned:
                    update_boss_lvl3_bullets()
                    draw_boss_lvl3_bullets(screen)

                    boss_lvl3_x += boss_speed_x
                    boss_lvl3_y += boss_speed_y

                    if boss_lvl3_x < 0 or boss_lvl3_x > screen_width - boss_lvl3_width:
                        boss_speed_x = -boss_speed_x
                    if boss_lvl3_y < 0 or boss_lvl3_y > screen_height - boss_lvl3_height:
                        boss_speed_y = -boss_speed_y

                    screen.blit(boss_lvl3, (boss_lvl3_x, boss_lvl3_y))

                for bullet in monster_lvl3_bullets:
                    bullet.update()
                    pygame.draw.circle(screen, (255, 0, 0), (bullet.rect.x, bullet.rect.y), 3)

                pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if button.is_clicked(event.pos):
                    menu_shown = not menu_shown
                    if not menu_shown:
                        screen.blit(game, (0, 0))
                        monsters = []
                        bullets = []
                        rocket_x = 50
                        rocket_y = screen_height // 2 - rocket_height // 2
                        game_over = False
                        monster_count = 0
                        boss_spawned = False
                        boss_health = 0
                    button_shown = False
                    button.visible = False
                    start_game = True
                    spawn_time = current_time + monster_spawn_delay
                    pygame.display.update()


        keys = pygame.key.get_pressed()
        if not menu_shown:
            if keys[pygame.K_LEFT] and rocket_x > 0:
                rocket_x -= 1.5
            if keys[pygame.K_RIGHT] and rocket_x < screen_width - rocket_width:
                rocket_x += 1.5
            if keys[pygame.K_UP] and rocket_y > 0:
                rocket_y -= 1.5
            if keys[pygame.K_DOWN] and rocket_y < screen_height - rocket_height:
                rocket_y += 1.5
            if keys[pygame.K_SPACE] and len(bullets) < 3:
                new_bullet = Bullet(rocket_x + rocket_width, rocket_y + rocket_height // 2, bullet_speed, "player")
                bullets.append(new_bullet)
                if sound_on:
                    sound.play()
                    pass




        for bullet in bullets:
            bullet.update()
            pygame.draw.circle(screen, (255, 255, 255), (bullet.rect.x, bullet.rect.y), 2)

        bullets = [bullet for bullet in bullets if bullet.rect.x < screen_width]

        pygame.display.update()

        for bullet in bullets:
            for i, (monster_x, monster_y) in enumerate(monsters):
                if monster_x < bullet.rect.x < monster_x + monster_width and \
                        monster_y < bullet.rect.y < monster_y + monster_height:
                    del monsters[i]
                    break

        for bullet in bullets:
            for i, (monster_lvl2_x, monster_lvl2_y) in enumerate(monsters_lvl2):
                if monster_lvl2_x < bullet.rect.x < monster_lvl2_x + monster_lvl2_width and \
                        monster_lvl2_y < bullet.rect.y < monster_lvl2_y + monster_lvl2_height:
                    del monsters_lvl2[i]
                    break

        for bullet in bullets:
            for i, (monster_x, monster_y) in enumerate(monsters_lvl3):
                if (monster_x < bullet.rect.x < monster_x + monster_width and
                        monster_y < bullet.rect.y < monster_y + monster_height):
                    del monsters_lvl3[i]
                    bullets.remove(bullet)
                    break

        for bullet in bullets[:]:
            if boss_spawned and boss_x < bullet.rect.x < boss_x + boss_width and \
                    boss_y < bullet.rect.y < boss_y + boss_height:
                bullets.remove(bullet)
                boss_health += 1
                if boss_health >= 50:
                    boss_spawned = False
                    boss_killed = True
                    draw_text("Це було легко, йдемо далі! :)", font, (255, 255, 255), screen, screen_width // 2 - 200,
                              screen_height // 2)
                    pygame.display.update()
                    pygame.time.wait(2000)
                    if boss_killed:
                        start_new_level()


        for bullet in bullets:
            if boss_lvl3_spawned and (boss_lvl3_x < bullet.rect.x < boss_lvl3_x + boss_lvl3_width and
                                      boss_lvl3_y < bullet.rect.y < boss_lvl3_y + boss_lvl3_height):
                bullets.remove(bullet)
                boss_health += 1
                if boss_health >= 50:
                    boss_lvl3_spawned = False
                    monsters.clear()
                    bullets.clear()
                    screen.fill((0, 0, 0))
                    draw_text("Молодець, ти пройшов гру!", font, (255, 255, 255), screen, screen_width // 2 - 200 - 100,
                              screen_height // 2)
                    draw_text("Цю гру створила студентка групи 202-ТК Варинська Євгенія", font, (255, 255, 255), screen,
                              screen_width // 2 - 400 - 100, screen_height // 2 + 50)
                    pygame.display.update()
                    pygame.time.wait(10000)
                    pygame.quit()
                    sys.exit()


        if not menu_shown and not game_over:

            for bullet_lvl3 in boss_lvl3_bullets:
                if (rocket_x < bullet_lvl3.rect.x < rocket_x + rocket_width and
                        rocket_y < bullet_lvl3.rect.y < rocket_y + rocket_height):
                    lives -= 1
                    if sound_on:
                        lost_life_sound.play()
                    boss_lvl3_bullets.remove(bullet_lvl3)
                    if lives == 0:
                        game_over = True
                        break

            for monster_x, monster_y in monsters:
                if (rocket_x < monster_x + monster_width and
                        rocket_x + rocket_width > monster_x and
                        rocket_y < monster_y + monster_height and
                        rocket_y + rocket_height > monster_y):
                    lives -= 1
                    if sound_on:
                        lost_life_sound.play()
                    monsters.remove((monster_x, monster_y))
                    if lives == 0:
                        game_over = True
                    break

                for monster_x, monster_y in monsters_lvl3:
                    if (rocket_x < monster_x + monster_width and
                            rocket_x + rocket_width > monster_x and
                            rocket_y < monster_y + monster_height and
                            rocket_y + rocket_height > monster_y):
                        lives -= 1
                        if sound_on:
                            lost_life_sound.play()
                        monsters_lvl3.remove((monster_x, monster_y))
                        if lives == 0:
                            game_over = True
                        break

                if boss_spawned:
                    if (rocket_x < boss_x + boss_width and
                            rocket_x + rocket_width > boss_x and
                            rocket_y < boss_y + boss_height and
                            rocket_y + rocket_height > boss_y):
                        game_over = True

            for monster_lvl2_x, monster_lvl2_y in monsters_lvl2:
                if (rocket_x < monster_lvl2_x + monster_lvl2_width and
                        rocket_x + rocket_width > monster_lvl2_x and
                        rocket_y < monster_lvl2_y + monster_lvl2_height and
                        rocket_y + rocket_height > monster_lvl2_y):
                    lives -= 1
                    if sound_on:
                        lost_life_sound.play()
                    monsters_lvl2.remove((monster_lvl2_x, monster_lvl2_y))
                    if lives == 0:
                        game_over = True
                    break

                if boss_lvl2_spawned:
                    if (rocket_x < boss_lvl2_x + boss_lvl2_width and
                            rocket_x + rocket_width > boss_lvl2_x and
                            rocket_y < boss_lvl2_y + boss_lvl2_height and
                            rocket_y + rocket_height > boss_lvl2_y):
                        game_over = True
                        break

            for bullet in monster_lvl2_bullets:
                if (rocket_x < bullet.rect.x < rocket_x + rocket_width and
                        rocket_y < bullet.rect.y < rocket_y + rocket_height):
                    lives -= 1
                    if sound_on:
                        lost_life_sound.play()
                    bullets_to_remove.append(bullet)
                    if lives == 0:
                        game_over = True
                    break

            for bullet in bullets_to_remove:
                if bullet in monster_lvl2_bullets:
                    monster_lvl2_bullets.remove(bullet)

            for bullet in monster_lvl3_bullets:
                if (rocket_x < bullet.rect.x < rocket_x + rocket_width and
                        rocket_y < bullet.rect.y < rocket_y + rocket_height):
                    lives -= 1
                    if sound_on:
                        lost_life_sound.play()
                    boss_lvl3_bullets_to_remove.append(bullet)
                    if lives == 0:
                        game_over = True
                    break

            for monster_x, monster_y in monsters_lvl3:
                if (rocket_x < monster_x + monster_width and
                        rocket_x + rocket_width > monster_x and
                        rocket_y < monster_y + monster_height and
                        rocket_y + rocket_height > monster_y):
                    lives -= 1
                    if sound_on:
                        lost_life_sound.play()
                    monsters_lvl3.remove((monster_x, monster_y))
                    if lives == 0:
                        game_over = True
                    break

            for bullet in bullets_to_remove3:
                if bullet in monster_lvl3_bullets:
                    monster_lvl3_bullets.remove(bullet)

        if game_over:
            game_over_text = font.render("Game Over", True, (255, 0, 0))
            screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 25))
            pygame.display.update()
            time.sleep(2)
            game_over = False
            menu_shown = True
            button_shown = True
            button.visible = True
            boss_killed = False
            monsters.clear()
            bullets.clear()
            boss_lvl3_spawned = False
            monster_lvl2_bullets.clear()
            boss_lvl2_bullets.clear()
            monsters_lvl2.clear()
            monsters_lvl3.clear()
            lives = 3
            if sound_on:
                game_over_sound.play()
            if boss_lvl2_spawned:
                boss_lvl2_spawned = False
            if boss_lvl3_spawned:
                boss_lvl3_spawned = False