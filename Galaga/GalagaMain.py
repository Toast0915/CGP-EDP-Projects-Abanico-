import pygame
import random
import tkinter as tk
import sys

WIDTH = 1000
HEIGHT = 750

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 80, 80)
BLUE = (80, 180, 255)
GREEN = (0, 255, 120)
YELLOW = (255, 255, 0)
PURPLE = (180, 80, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 170, 0)

def main_game(ship_type):

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Nebula Strike")

    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24)
    big_font = pygame.font.SysFont("Arial", 60)

    player = pygame.Rect(WIDTH // 2, HEIGHT - 90, 60, 60)

    bullets = []
    enemy_bullets = []

    explosions = []
    damage_numbers = []

    powerups = []

    player_speed = 5

    formation_speed = 0.8
    formation_direction = 1

    enemy_fire_rate = 0.00025

    last_shot = 0

    rapid_mode = False
    rapid_timer = 0

    spread_mode = False
    spread_timer = 0

    laser_mode = False
    laser_timer = 0

    shoot_delay = 320

    level = 1
    score = 0
    lives = 5

    paused = False
    game_over = False

    boss_active = False

    boss_health = 700
    boss_max_health = 700

    boss_x = WIDTH // 2
    boss_y = 120

    boss_direction = 1

    boss_attack_timer = 0
    boss_attack_type = 1

    boss_hit_counter = 0

    stars = []

    for i in range(150):

        stars.append([
            random.randint(0, WIDTH),
            random.randint(0, HEIGHT),
            random.randint(1, 3),
            random.randint(1, 4)
        ])

    enemies = []

    def create_wave():

        enemies.clear()

        rows = 3
        cols = 5

        patterns = [
            (-250, 100),
            (WIDTH + 250, 100),
            (WIDTH // 2, -250)
        ]

        count = 0

        for row in range(rows):

            for col in range(cols):

                spawn = patterns[count % 3]

                enemy = {
                    "rect": pygame.Rect(
                        spawn[0],
                        spawn[1],
                        50,
                        50
                    ),

                    "target_x": 250 + col * 100,
                    "target_y": 100 + row * 80
                }

                enemies.append(enemy)

                count += 1

    create_wave()

    while True:

        clock.tick(60)

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:

                    paused = not paused

                if event.key == pygame.K_r and game_over:

                    main_game(ship_type)

        if paused:

            pause_text = big_font.render(
                "PAUSED",
                True,
                WHITE
            )

            screen.blit(
                pause_text,
                (WIDTH // 2 - 140, HEIGHT // 2)
            )

            pygame.display.update()

            continue

        screen.fill(BLACK)

        for star in stars:

            pygame.draw.circle(
                screen,
                WHITE,
                (star[0], star[1]),
                star[2]
            )

            star[1] += star[3]

            if star[1] > HEIGHT:

                star[0] = random.randint(0, WIDTH)
                star[1] = 0

        if rapid_mode and current_time > rapid_timer:

            rapid_mode = False
            shoot_delay = 320

        if spread_mode and current_time > spread_timer:

            spread_mode = False

        if laser_mode and current_time > laser_timer:

            laser_mode = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.x > 0:

            player.x -= player_speed

        if keys[pygame.K_RIGHT] and player.x < WIDTH - player.width:

            player.x += player_speed

        if keys[pygame.K_SPACE]:

            if current_time - last_shot > shoot_delay:

                if ship_type == 1:

                    bullets.append({
                        "rect": pygame.Rect(
                            player.centerx - 3,
                            player.y,
                            6,
                            18
                        ),
                        "dx": 0,
                        "damage": 2,
                        "color": CYAN
                    })

                elif ship_type == 2:

                    bullets.append({
                        "rect": pygame.Rect(
                            player.centerx - 10,
                            player.y,
                            6,
                            18
                        ),
                        "dx": -1,
                        "damage": 1,
                        "color": GREEN
                    })

                    bullets.append({
                        "rect": pygame.Rect(
                            player.centerx + 6,
                            player.y,
                            6,
                            18
                        ),
                        "dx": 1,
                        "damage": 1,
                        "color": GREEN
                    })

                elif ship_type == 3:

                    bullets.append({
                        "rect": pygame.Rect(
                            player.centerx - 5,
                            player.y,
                            10,
                            28
                        ),
                        "dx": 0,
                        "damage": 4,
                        "color": PURPLE
                    })

                if spread_mode:

                    bullets.append({
                        "rect": pygame.Rect(
                            player.centerx,
                            player.y,
                            6,
                            18
                        ),
                        "dx": -3,
                        "damage": 1,
                        "color": YELLOW
                    })

                    bullets.append({
                        "rect": pygame.Rect(
                            player.centerx,
                            player.y,
                            6,
                            18
                        ),
                        "dx": 3,
                        "damage": 1,
                        "color": YELLOW
                    })

                last_shot = current_time

        ship_color = BLUE

        if ship_type == 2:

            ship_color = GREEN

        elif ship_type == 3:

            ship_color = PURPLE

        pygame.draw.polygon(
            screen,
            ship_color,
            [
                (player.centerx, player.y - 25),
                (player.x + 8, player.y + 45),
                (player.x + 52, player.y + 45)
            ]
        )

        pygame.draw.rect(
            screen,
            CYAN,
            (
                player.x + 18,
                player.y + 8,
                24,
                18
            )
        )

        pygame.draw.polygon(
            screen,
            ORANGE,
            [
                (player.x + 20, player.y + 45),
                (player.x + 30, player.y + 65),
                (player.x + 40, player.y + 45)
            ]
        )

        for bullet_data in bullets[:]:

            bullet = bullet_data["rect"]

            bullet.y -= 10
            bullet.x += bullet_data["dx"]

            pygame.draw.rect(
                screen,
                bullet_data["color"],
                bullet
            )

            if bullet.y < 0:

                bullets.remove(bullet_data)

        if not boss_active:

            all_arrived = True

            for enemy_data in enemies:

                enemy = enemy_data["rect"]

                tx = enemy_data["target_x"]
                ty = enemy_data["target_y"]

                enemy.x += (tx - enemy.x) * 0.03
                enemy.y += (ty - enemy.y) * 0.03

                if abs(enemy.x - tx) > 3:

                    all_arrived = False

            if all_arrived:

                for enemy_data in enemies:

                    enemy_data["target_x"] += (
                        formation_direction *
                        formation_speed
                    )

                left_edge = min(
                    enemy["target_x"]
                    for enemy in enemies
                )

                right_edge = max(
                    enemy["target_x"]
                    for enemy in enemies
                )

                if right_edge >= WIDTH - 120:

                    formation_direction = -1

                if left_edge <= 120:

                    formation_direction = 1

        for enemy_data in enemies:

            enemy = enemy_data["rect"]

            if random.random() < enemy_fire_rate:

                enemy_bullets.append(
                    pygame.Rect(
                        enemy.centerx,
                        enemy.bottom,
                        5,
                        14
                    )
                )

        for enemy_data in enemies[:]:

            enemy = enemy_data["rect"]

            pygame.draw.polygon(
                screen,
                RED,
                [
                    (enemy.centerx, enemy.y),
                    (enemy.x, enemy.y + 40),
                    (enemy.x + 50, enemy.y + 40)
                ]
            )

            pygame.draw.circle(
                screen,
                PURPLE,
                (enemy.centerx, enemy.centery),
                10
            )

            if laser_mode:

                laser_rect = pygame.Rect(
                    player.centerx - 5,
                    0,
                    10,
                    player.y
                )

                if enemy.colliderect(laser_rect):

                    explosions.append({
                        "x": enemy.centerx,
                        "y": enemy.centery,
                        "radius": 5,
                        "max_radius": 30,
                        "color": CYAN
                    })

                    enemies.remove(enemy_data)

                    score += 10

                    continue

            for bullet_data in bullets[:]:

                bullet = bullet_data["rect"]

                if enemy.colliderect(bullet):

                    bullets.remove(bullet_data)

                    damage_numbers.append({
                        "x": enemy.centerx,
                        "y": enemy.y,
                        "text": str(
                            bullet_data["damage"]
                        ),
                        "timer": 40
                    })

                    explosions.append({
                        "x": enemy.centerx,
                        "y": enemy.centery,
                        "radius": 5,
                        "max_radius": 35,
                        "color": random.choice([
                            RED,
                            ORANGE,
                            YELLOW
                        ])
                    })

                    enemies.remove(enemy_data)

                    score += 10

                    if random.randint(1, 100) <= 12:

                        powerups.append({
                            "rect": pygame.Rect(
                                enemy.x,
                                enemy.y,
                                24,
                                24
                            ),

                            "type": random.choice([
                                "rapid",
                                "spread",
                                "life",
                                "laser"
                            ])
                        })

                    break

        if laser_mode:

            pygame.draw.rect(
                screen,
                CYAN,
                (
                    player.centerx - 5,
                    0,
                    10,
                    player.y
                )
            )

        for bullet in enemy_bullets[:]:

            bullet.y += 3 + (level * 0.12)

            pygame.draw.rect(
                screen,
                ORANGE,
                bullet
            )

            if bullet.y > HEIGHT:

                enemy_bullets.remove(bullet)

            elif bullet.colliderect(player):

                enemy_bullets.remove(bullet)

                explosions.append({
                    "x": player.centerx,
                    "y": player.centery,
                    "radius": 10,
                    "max_radius": 40,
                    "color": ORANGE
                })

                lives -= 1

                if lives <= 0:

                    game_over = True

        if boss_active:

            boss_x += boss_direction * 2

            if boss_x >= WIDTH - 180:

                boss_direction = -1

            if boss_x <= 180:

                boss_direction = 1

            pygame.draw.polygon(
                screen,
                PURPLE,
                [
                    (boss_x, boss_y - 70),
                    (boss_x - 180, boss_y + 20),
                    (boss_x - 120, boss_y + 90),
                    (boss_x + 120, boss_y + 90),
                    (boss_x + 180, boss_y + 20)
                ]
            )

            pygame.draw.circle(
                screen,
                CYAN,
                (boss_x, boss_y + 10),
                50
            )

            pygame.draw.circle(
                screen,
                RED,
                (boss_x, boss_y + 10),
                20
            )

            pygame.draw.rect(
                screen,
                RED,
                (
                    180,
                    20,
                    int(
                        (
                            boss_health /
                            boss_max_health
                        ) * 640
                    ),
                    25
                )
            )

            if current_time - boss_attack_timer > 2500:

                boss_attack_type = random.randint(1, 3)

                boss_attack_timer = current_time

            if boss_attack_type == 1:

                if random.randint(1, 100) <= 5:

                    for i in [-50, 0, 50]:

                        enemy_bullets.append(
                            pygame.Rect(
                                boss_x + i,
                                boss_y + 60,
                                10,
                                22
                            )
                        )

            elif boss_attack_type == 2:

                if random.randint(1, 100) <= 5:

                    for i in range(-5, 6):

                        enemy_bullets.append(
                            pygame.Rect(
                                boss_x + i * 20,
                                boss_y + 60,
                                8,
                                20
                            )
                        )

            elif boss_attack_type == 3:

                if random.randint(1, 100) <= 10:

                    enemy_bullets.append(
                        pygame.Rect(
                            random.randint(
                                boss_x - 150,
                                boss_x + 150
                            ),
                            boss_y + 60,
                            7,
                            18
                        )
                    )

            boss_hitbox = pygame.Rect(
                boss_x - 180,
                boss_y - 70,
                360,
                170
            )

            if laser_mode:

                laser_rect = pygame.Rect(
                    player.centerx - 5,
                    0,
                    10,
                    player.y
                )

                if boss_hitbox.colliderect(laser_rect):

                    boss_health -= 0.4

            for bullet_data in bullets[:]:

                bullet = bullet_data["rect"]

                if boss_hitbox.colliderect(bullet):

                    bullets.remove(bullet_data)

                    boss_health -= bullet_data["damage"]

                    damage_numbers.append({
                        "x": bullet.x,
                        "y": bullet.y,
                        "text": str(
                            bullet_data["damage"]
                        ),
                        "timer": 40
                    })

                    boss_hit_counter += 1

                    explosions.append({
                        "x": bullet.x,
                        "y": bullet.y,
                        "radius": 5,
                        "max_radius": 20,
                        "color": CYAN
                    })

                    if boss_hit_counter >= 30:

                        boss_hit_counter = 0

                        powerups.append({
                            "rect": pygame.Rect(
                                boss_x,
                                boss_y + 50,
                                24,
                                24
                            ),

                            "type": random.choice([
                                "rapid",
                                "spread",
                                "life",
                                "laser"
                            ])
                        })

                    if boss_health <= 0:

                        for i in range(35):

                            explosions.append({
                                "x": random.randint(
                                    boss_x - 180,
                                    boss_x + 180
                                ),
                                "y": random.randint(
                                    boss_y - 70,
                                    boss_y + 90
                                ),
                                "radius": random.randint(10, 20),
                                "max_radius": random.randint(40, 80),
                                "color": random.choice([
                                    RED,
                                    ORANGE,
                                    YELLOW,
                                    PURPLE
                                ])
                            })

                        ending_cutscene(
                            screen,
                            clock
                        )

                        return

        for powerup in powerups[:]:

            powerup["rect"].y += 2

            color = CYAN

            if powerup["type"] == "rapid":

                color = YELLOW

            elif powerup["type"] == "spread":

                color = GREEN

            elif powerup["type"] == "life":

                color = BLUE

            elif powerup["type"] == "laser":

                color = PURPLE

            pygame.draw.circle(
                screen,
                color,
                (
                    powerup["rect"].centerx,
                    powerup["rect"].centery
                ),
                12
            )

            if player.colliderect(
                powerup["rect"]
            ):

                if powerup["type"] == "rapid":

                    rapid_mode = True
                    rapid_timer = current_time + 8000
                    shoot_delay = 170

                elif powerup["type"] == "spread":

                    spread_mode = True
                    spread_timer = current_time + 8000

                elif powerup["type"] == "life":

                    lives += 1

                elif powerup["type"] == "laser":

                    laser_mode = True
                    laser_timer = current_time + 6000

                powerups.remove(powerup)

        for explosion in explosions[:]:

            pygame.draw.circle(
                screen,
                explosion["color"],
                (
                    int(explosion["x"]),
                    int(explosion["y"])
                ),
                int(explosion["radius"])
            )

            explosion["radius"] += 2

            if (
                explosion["radius"] >=
                explosion["max_radius"]
            ):

                explosions.remove(explosion)

        for dmg in damage_numbers[:]:

            dmg_text = font.render(
                dmg["text"],
                True,
                YELLOW
            )

            screen.blit(
                dmg_text,
                (dmg["x"], dmg["y"])
            )

            dmg["y"] -= 1

            dmg["timer"] -= 1

            if dmg["timer"] <= 0:

                damage_numbers.remove(dmg)

        if len(enemies) == 0 and not boss_active:

            if level % 5 == 0:

                boss_active = True

            else:

                level += 1

                formation_speed += 0.05
                enemy_fire_rate += 0.00003

                create_wave()

        score_text = font.render(
            f"Score: {score}",
            True,
            WHITE
        )

        lives_text = font.render(
            f"Lives: {lives}",
            True,
            GREEN
        )

        level_text = font.render(
            f"Level: {level}",
            True,
            CYAN
        )

        screen.blit(score_text, (20, 40))
        screen.blit(lives_text, (20, 80))
        screen.blit(level_text, (20, 120))

        if game_over:

            over_text = big_font.render(
                "GAME OVER",
                True,
                RED
            )

            restart_text = font.render(
                "Press R To Restart",
                True,
                WHITE
            )

            screen.blit(
                over_text,
                (WIDTH // 2 - 220,
                 HEIGHT // 2 - 40)
            )

            screen.blit(
                restart_text,
                (WIDTH // 2 - 100,
                 HEIGHT // 2 + 40)
            )

        pygame.display.update()

def ending_cutscene(screen, clock):

    font = pygame.font.SysFont("Arial", 28)

    big_font = pygame.font.SysFont(
        "Arial",
        60
    )

    button = pygame.Rect(
        370,
        520,
        260,
        70
    )

    ship_x = 150

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if button.collidepoint(
                    event.pos
                ):

                    pygame.quit()

                    show_menu()

                    return

        screen.fill(BLACK)

        for i in range(120):

            pygame.draw.circle(
                screen,
                WHITE,
                (
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT)
                ),
                1
            )

        title = big_font.render(
            "MISSION COMPLETE",
            True,
            CYAN
        )

        msg = font.render(
            "The Nebula Fleet Has Been Defeated",
            True,
            WHITE
        )

        msg2 = font.render(
            "Peace Has Returned To The Galaxy",
            True,
            WHITE
        )

        screen.blit(title, (220, 180))
        screen.blit(msg, (250, 300))
        screen.blit(msg2, (260, 340))

        ship_x += 2

        pygame.draw.polygon(
            screen,
            CYAN,
            [
                (ship_x + 30, 520),
                (ship_x, 580),
                (ship_x + 60, 580)
            ]
        )

        pygame.draw.rect(
            screen,
            BLUE,
            button
        )

        button_text = font.render(
            "BACK TO MENU",
            True,
            WHITE
        )

        screen.blit(
            button_text,
            (400, 540)
        )

        pygame.display.update()

        clock.tick(60)

def start_ship1():

    root.destroy()

    main_game(1)

def start_ship2():

    root.destroy()

    main_game(2)

def start_ship3():

    root.destroy()

    main_game(3)

def show_menu():

    global root

    root = tk.Tk()

    root.title("Nebula Strike")

    root.geometry("600x520")

    root.configure(bg="black")

    title = tk.Label(
        root,
        text="NEBULA STRIKE",
        font=("Arial", 32, "bold"),
        fg="cyan",
        bg="black"
    )

    title.pack(pady=30)

    info = tk.Label(
        root,
        text="""
SELECT YOUR SHIP

BLUE SHIP
Balanced Fighter

GREEN SHIP
Fast Dual Fighter

PURPLE SHIP
Heavy Laser Fighter

CONTROLS:
LEFT / RIGHT = MOVE
SPACE = SHOOT
P = PAUSE
R = RESTART
""",
        font=("Arial", 14),
        fg="white",
        bg="black"
    )

    info.pack(pady=20)

    btn1 = tk.Button(
        root,
        text="BLUE SHIP",
        font=("Arial", 16),
        width=20,
        bg="blue",
        fg="white",
        command=start_ship1
    )

    btn1.pack(pady=10)

    btn2 = tk.Button(
        root,
        text="GREEN SHIP",
        font=("Arial", 16),
        width=20,
        bg="green",
        fg="white",
        command=start_ship2
    )

    btn2.pack(pady=10)

    btn3 = tk.Button(
        root,
        text="PURPLE SHIP",
        font=("Arial", 16),
        width=20,
        bg="purple",
        fg="white",
        command=start_ship3
    )

    btn3.pack(pady=10)

    root.mainloop()

show_menu()