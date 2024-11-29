import pygame
import random
import math

# 初始化 Pygame
pygame.init()

# 設定視窗
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # 視窗大小
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")  # 視窗名稱

# 設定顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEALTH_COLOR = (255, 0, 0)
LIGHT_YELLOW = (255, 239, 179)

# 設定血量
MAX_HEALTH = 100  # 玩家最大血量
current_health = MAX_HEALTH  # 當前血量
invincible = False  # 玩家受傷後無敵狀態
invincible_time = 0  # 無敵時間

# 設定玩家的參數
PLAYER_SIZE = 50  # 玩家圖片大小
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # 玩家起始位置(螢幕中心)
player_speed = 5  # 玩家移動速度
player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)  # 玩家矩形(碰撞檢測)

# 設定子彈的參數
BULLET_SIZE = 20  # 子彈圖片大小
bullets = []  # 用來存儲所有子彈的列表

# 設定敵人的參數
ENEMY_SIZE = 50  # 敵人圖片大小
enemies = []  # 用來存儲所有敵人的列表

# 設定敵人和子彈生成
NUM_INITIAL_ENEMIES = 3  # 開始時生成3個敵人
ENEMY_SPAWN_INTERVAL = 2000  # 每2秒生成一個新敵人
last_enemy_spawn_time = pygame.time.get_ticks()  # 追蹤上次生成敵人的時間

SHOOT_DELAY = 500  # 每0.5秒才能射擊一次
last_shoot_time = pygame.time.get_ticks()  # 追蹤上次射擊的時間

# 載入圖片
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

player_invincible_image = pygame.image.load("invincible.png")
player_invincible_image = pygame.transform.scale(player_invincible_image, (PLAYER_SIZE, PLAYER_SIZE))

enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))

bullet_image = pygame.image.load("bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (BULLET_SIZE, BULLET_SIZE))


# 發射子彈（朝滑鼠游標方向）
def shoot_bullet():
    global last_shoot_time
    current_time = pygame.time.get_ticks()  # 獲取當前時間
    if current_time - last_shoot_time >= SHOOT_DELAY:  # 檢查射擊間隔(0.5秒)
        mouse_x, mouse_y = pygame.mouse.get_pos()  # 獲取滑鼠位置
        dx = mouse_x - (player_x + PLAYER_SIZE // 2)  # 計算子彈相對玩家的位置
        dy = mouse_y - (player_y + PLAYER_SIZE // 2)
        distance = math.sqrt(dx ** 2 + dy ** 2)  # 計算距離
        dx /= distance  # 歸一化方向向量
        dy /= distance

        bullet = {
            'rect': pygame.Rect(player_x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                                player_y + PLAYER_SIZE // 2 - BULLET_SIZE // 2, BULLET_SIZE, BULLET_SIZE),
            'dx': dx,  # 存儲子彈的移動方向
            'dy': dy   # 存儲子彈的移動方向
        }
        bullets.append(bullet)  # 將更新的子彈加入子彈列表
        last_shoot_time = current_time  # 更新上次射擊的時間

# 子彈移動
def move_bullets():
    global bullets
    for bullet in bullets[:]:  # 所有子彈
        bullet['rect'].x += bullet['dx'] * 10  # 根據方向移動子彈
        bullet['rect'].y += bullet['dy'] * 10

        # 子彈超出畫面時移除
        if bullet['rect'].x < 0 or bullet['rect'].x > SCREEN_WIDTH or bullet['rect'].y < 0 or bullet['rect'].y > SCREEN_HEIGHT:
            bullets.remove(bullet)

# 創建敵人
def create_enemy():
    edge = random.choice(["top", "bottom", "left", "right"])  # 隨機選擇敵人生成的邊緣位置(上下左右)
    if edge == "top":
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = 0
    elif edge == "bottom":
        enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
        enemy_y = SCREEN_HEIGHT - ENEMY_SIZE
    elif edge == "left":
        enemy_x = 0
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)
    elif edge == "right":
        enemy_x = SCREEN_WIDTH - ENEMY_SIZE
        enemy_y = random.randint(0, SCREEN_HEIGHT - ENEMY_SIZE)

    enemies.append(pygame.Rect(enemy_x, enemy_y, ENEMY_SIZE, ENEMY_SIZE))  # 生成敵人並加入敵人列表

# 檢查子彈與敵人的碰撞
def check_bullet_collisions():
    global enemies, bullets
    for bullet in bullets[:]:  # 所有子彈
        for enemy in enemies[:]:  # 對所有敵人
            if bullet['rect'].colliderect(enemy):  # 如果子彈與敵人碰撞
                enemies.remove(enemy)  # 移除敵人
                bullets.remove(bullet)  # 移除子彈
                break

# 敵人移動方向
def move_enemies():
    global enemies, player_rect
    for enemy in enemies:  # 所有敵人
        enemy_center = (enemy.x + ENEMY_SIZE // 2, enemy.y + ENEMY_SIZE // 2)  # 計算敵人中心點
        player_center = (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2)  # 計算玩家中心點
        direction = (player_center[0] - enemy_center[0], player_center[1] - enemy_center[1])  # 計算方向向量
        length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)  # 計算向量長度
        if length != 0:  # 如果長度不為 0
            direction = (direction[0] / length, direction[1] / length)  # 歸一化方向向量
        enemy.x += direction[0] * 2  # 按照歸一化方向移動敵人
        enemy.y += direction[1] * 2

# 處理玩家碰撞與扣血
def check_player_collisions():
    global current_health, invincible, invincible_time
    if invincible:
        current_time = pygame.time.get_ticks()
        if current_time - invincible_time > 1000:  # 扣血無敵狀態持續 1 秒
            invincible = False

    if not invincible:  # 如果不是無敵狀態
        for enemy in enemies:  # 所有敵人
            if player_rect.colliderect(enemy):  # 如果玩家與敵人碰撞
                current_health -= 10  # 扣10點血
                invincible = True  # 進入無敵狀態
                invincible_time = pygame.time.get_ticks()  # 記錄無敵時間
                break  # 每次碰撞只扣一次血量

# 顯示遊戲畫面
def draw_game():
    screen.fill(LIGHT_YELLOW)  # 設定背景顏色

    # 如果血量歸零，顯示 Game Over 並停止遊戲
    if current_health <= 0:
        font = pygame.font.SysFont(None, 50)
        game_over_text = font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)  # 等待 2 秒後退出遊戲
        return True  # 返回 True 表示遊戲結束

    # 畫玩家
    if invincible:
        screen.blit(player_invincible_image, player_rect.topleft)  # 無敵時顯示無敵圖片
    else:
        screen.blit(player_image, player_rect.topleft)  # 正常情況顯示玩家圖片

    # 畫敵人
    for enemy in enemies:
        screen.blit(enemy_image, enemy.topleft)

    # 顯示血量
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = 10
    health_bar_y = 10
    pygame.draw.rect(screen, WHITE, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, HEALTH_COLOR, (health_bar_x, health_bar_y, (current_health / MAX_HEALTH) * health_bar_width, health_bar_height))

    font = pygame.font.SysFont(None, 30)
    health_text = font.render(f"HP: {current_health}", True, BLACK)
    screen.blit(health_text, (health_bar_x + health_bar_width + 10, health_bar_y))

    # 繪製子彈
    for bullet in bullets:
        screen.blit(bullet_image, bullet['rect'].topleft)  # 使用 bullet_image 來繪製子彈

    pygame.display.flip()
    return False  # 返回 False 表示遊戲繼續進行

# 主遊戲循環
def game_loop():
    global player_x, player_y, player_rect, bullets, last_enemy_spawn_time
    # 生成敵人
    for _ in range(NUM_INITIAL_ENEMIES):
        create_enemy()

    clock = pygame.time.Clock()
    # 遊戲運行
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # 關閉遊戲

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            shoot_bullet()  # 當按下滑鼠左鍵時射擊

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # 玩家左移
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:  # 玩家右移
            player_x += player_speed
        if keys[pygame.K_UP]:  # 玩家上移
            player_y -= player_speed
        if keys[pygame.K_DOWN]:  # 玩家下移
            player_y += player_speed

        player_rect.x = player_x
        player_rect.y = player_y
        player_rect.clamp_ip(screen.get_rect())  # 防止玩家超出邊界

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time >= ENEMY_SPAWN_INTERVAL:
            create_enemy()  # 每隔指定時間創建一個敵人
            last_enemy_spawn_time = current_time

        move_bullets()  # 移動子彈
        check_bullet_collisions()  # 檢查子彈與敵人碰撞
        move_enemies()  # 移動敵人
        check_player_collisions()  # 檢查玩家碰撞

        if draw_game():  # 畫遊戲畫面並檢查是否結束
            break

        clock.tick(60)  # 設定遊戲每秒幀數為60

    pygame.quit()  # 結束 Pygame

if __name__ == "__main__":
    game_loop()  # 執行遊戲循環
