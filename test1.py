import pygame
import random
import math

# 初始化 Pygame
pygame.init()

# 設定顯示窗口大小
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Roguelike Game")

# 設定顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
HEALTH_COLOR = (255, 0, 0)  # 血量顏色
INVINCIBLE_COLOR = (255, 255, 0)  # 無敵顏色（黃色）

# 設定玩家的參數
PLAYER_SIZE = 20
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
player_speed = 5
player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)

# 設定血量
MAX_HEALTH = 100
current_health = MAX_HEALTH
invincible = False  # 無敵狀態
invincible_time = 0  # 無敵時間（毫秒）

# 設定子彈的參數
BULLET_SIZE = 10
bullets = []

# 設定敵人的參數
ENEMY_SIZE = 20
enemies = []

# 設定敵人數量
NUM_INITIAL_ENEMIES = 3  # 一開始生成 3 個敵人

# 設定生成新敵人的時間間隔（毫秒）
ENEMY_SPAWN_INTERVAL = 3000  # 每3秒生成一個敵人
last_enemy_spawn_time = pygame.time.get_ticks()  # 追蹤上次生成敵人的時間

# 設定子彈射擊的時間延遲（毫秒）
SHOOT_DELAY = 500  # 每500毫秒才能射擊一次
last_shoot_time = pygame.time.get_ticks()  # 追蹤上次射擊的時間

# 創建敵人，讓敵人只生成在邊緣
def create_enemy():
    """
    創建一個新的敵人並將其放到螢幕的邊緣上隨機的位置。
    """
    edge = random.choice(["top", "bottom", "left", "right"])  # 隨機選擇邊緣
    if edge == "top":
        # 在上邊界生成敵人
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = 0
    elif edge == "bottom":
        # 在下邊界生成敵人
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = SCREEN_HEIGHT - ENEMY_SIZE
    elif edge == "left":
        # 在左邊界生成敵人
        enemy_x = 0
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
    elif edge == "right":
        # 在右邊界生成敵人
        enemy_x = SCREEN_WIDTH - ENEMY_SIZE
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)

    enemies.append(pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))

# 發射子彈（朝滑鼠方向）
def shoot_bullet():
    """
    發射子彈，子彈會朝著滑鼠的方向移動。
    """
    global last_shoot_time
    current_time = pygame.time.get_ticks()
    if current_time - last_shoot_time >= SHOOT_DELAY:  # 檢查射擊延遲
        mouse_x, mouse_y = pygame.mouse.get_pos()  # 獲取滑鼠位置
        dx = mouse_x - (player_x + PLAYER_SIZE // 2)
        dy = mouse_y - (player_y + PLAYER_SIZE // 2)
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx /= distance
        dy /= distance

        bullet = {
            'rect': pygame.Rect(player_x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                                player_y + PLAYER_SIZE // 2 - BULLET_SIZE // 2, BULLET_SIZE, BULLET_SIZE),
            'dx': dx,  # 存儲子彈的移動方向
            'dy': dy   # 存儲子彈的移動方向
        }
        bullets.append(bullet)
        last_shoot_time = current_time  # 更新上次射擊的時間

# 移動子彈
def move_bullets():
    """
    移動所有子彈，使它們朝著設定的方向移動。
    """
    global bullets
    for bullet in bullets[:]:
        bullet['rect'].x += bullet['dx'] * 10  # 讓子彈根據方向移動
        bullet['rect'].y += bullet['dy'] * 10

        # 如果子彈超出屏幕，移除它
        if bullet['rect'].x < 0 or bullet['rect'].x > SCREEN_WIDTH or bullet['rect'].y < 0 or bullet['rect'].y > SCREEN_HEIGHT:
            bullets.remove(bullet)

# 檢查子彈與敵人的碰撞
def check_bullet_collisions():
    global enemies, bullets
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet['rect'].colliderect(enemy):  # 如果子彈與敵人碰撞
                enemies.remove(enemy)  # 移除敵人
                bullets.remove(bullet)  # 移除子彈
                break

# 計算敵人移動方向（朝玩家移動）
def move_enemies():
    global enemies, player_rect
    for enemy in enemies:
        enemy_center = (enemy.x + ENEMY_SIZE // 2, enemy.y + ENEMY_SIZE // 2)
        player_center = (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2)
        direction = (player_center[0] - enemy_center[0], player_center[1] - enemy_center[1])
        length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        if length != 0:
            direction = (direction[0] / length, direction[1] / length)
        enemy.x += direction[0] * 2
        enemy.y += direction[1] * 2

# 處理玩家碰撞與扣血
def check_player_collisions():
    global current_health, invincible, invincible_time
    if invincible:
        current_time = pygame.time.get_ticks()
        if current_time - invincible_time > 1000:  # 1秒後無敵狀態結束
            invincible = False

    if not invincible:
        for enemy in enemies:
            if player_rect.colliderect(enemy):  # 如果玩家與敵人碰撞
                current_health -= 10  # 扣除 10 點血量
                invincible = True  # 進入無敵狀態
                invincible_time = pygame.time.get_ticks()  # 記錄無敵時間

# 顯示遊戲畫面
def draw_game():
    screen.fill(BLACK)

    # 如果血量歸零，顯示 Game Over 並停止遊戲
    if current_health <= 0:
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        return True  # 結束遊戲

    # 改變玩家顏色為無敵顏色
    player_color = GREEN if not invincible else INVINCIBLE_COLOR

    # 畫玩家
    pygame.draw.rect(screen, player_color, player_rect)

    # 畫敵人
    for enemy in enemies:
        pygame.draw.rect(screen, RED, enemy)

    # 畫子彈
    for bullet in bullets:
        pygame.draw.rect(screen, BLUE, bullet['rect'])

    # 顯示血量
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = 10
    health_bar_y = 10
    pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, HEALTH_COLOR, (health_bar_x, health_bar_y, (current_health / MAX_HEALTH) * health_bar_width, health_bar_height))

    pygame.display.flip()
    return False  # 遊戲繼續進行

# 主遊戲循環
def game_loop():
    global player_x, player_y, player_rect, bullets, last_enemy_spawn_time
    # 一開始生成 3 個敵人
    for _ in range(NUM_INITIAL_ENEMIES):
        create_enemy()

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左鍵射擊
                shoot_bullet()

        # 處理玩家移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
        if keys[pygame.K_UP]:
            player_y -= player_speed
        if keys[pygame.K_DOWN]:
            player_y += player_speed

        # 更新玩家的矩形位置
        player_rect.x = player_x
        player_rect.y = player_y

        # 確保玩家不會移出螢幕
        player_rect.clamp_ip(screen.get_rect())

        # 計算當前時間，並與上次生成敵人的時間比較
        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL:
            create_enemy()  # 創建一個新敵人
            last_enemy_spawn_time = current_time  # 更新上次生成敵人的時間

        # 移動子彈
        move_bullets()

        # 檢查子彈與敵人的碰撞
        check_bullet_collisions()

        # 移動敵人
        move_enemies()

        # 檢查玩家與敵人的碰撞
        check_player_collisions()

        # 更新畫面並檢查是否 Game Over
        if draw_game():
            break  # 如果 Game Over，退出遊戲循環

        # 設定遊戲幀數
        clock.tick(30)

    pygame.quit()

# 開始遊戲
if __name__ == "__main__":
    game_loop()
