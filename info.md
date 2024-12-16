## #import
在python一開始先宣告函式庫
此程式需使用pygame
```python
import pygame
```
## #初始化pygame
```python
pygame.init()
```
## #載入音效
在遊戲中加入音效
```python
#變數名稱 = pygame.mixer.Sound("檔案名稱")
shoot_sound = pygame.mixer.Sound("shoot.wav")
hit_sound = pygame.mixer.Sound("hit.wav")
damage_sound = pygame.mixer.Sound("damage.wav")
```
## #加入背景音樂
在遊戲中播放背景音樂
```python
#設定MP3文件的資料夾
mp3_folder = "music"
#獲取MP3文件列表
mp3_files = [file for file in os.listdir(mp3_folder) if file.endswitch(".mp3")]

if mp3_files:
    random_mp3 = random.choice(mp3_files)
    random_mp3_path = os.path.join(mp3_folder, random_mp3)
    pygame.mixer.music.load(random_mp3_path)
    pygame.mixer.music.play(-1) #無限循環播放
    print(f"正在播放: {random_mp3}")
else:
    print("資料夾中沒有 MP3 文件!")
```
> 正在播放: Mayday五月天 [ 如果我們不曾相遇What If We Had Never Met ] Official Music Video.mp3
## #設定音樂、音效音量
```python
# 設定音樂音量
pygame.mixer.music.set_volume(0.7)  # 將音樂音量設為 70%

# 設定音效音量
shoot_sound.set_volume(0.3)        # 將射擊音效音量設為 30%
hit_sound.set_volume(0.4)          # 將擊中音效音量設為 40%
damage_sound.set_volume(0.6)       # 將受傷音效音量設為 60%
```
## #遊戲參數設定
```python
# 設定視窗
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # 視窗大小1280*720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")  # 視窗名稱 Game
game_over = False  # 初始化遊戲狀態

# 設定顏色變數
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HEALTH_COLOR = (255, 0, 0)
LIGHT_YELLOW = (255, 239, 179)

# 設定血量
MAX_HEALTH = 100  # 玩家最大血量
current_health = MAX_HEALTH  # 當前血量
invincible = True  # 玩家受傷後無敵狀態
invincible_time = 2  # 無敵時間2秒

# 設定玩家的參數
PLAYER_SIZE = 70  # 玩家圖片大小
player_x, player_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2  # 玩家起始位置(螢幕中心)
player_speed = 4  # 玩家移動速度
player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)  # 玩家大小

# 設定子彈的參數
BULLET_SIZE = 20  # 子彈圖片大小
bullets = []  # 用來存儲所有子彈的列表

# 設定敵人的參數
ENEMY_SIZE = 50  # 敵人圖片大小
enemies = []  # 用來存儲所有敵人的列表

# 設定敵人和子彈生成
NUM_INITIAL_ENEMIES = 3  # 開始時生成3個敵人
ENEMY_SPAWN_INTERVAL = 3000  # 每3秒(3000毫秒)生成一個新敵人
MIN_ENEMY_SPAWN_INTERVAL = 1500  # 最短生成間隔1.5秒
ENEMY_INCREMENT_INTERVAL = 5000  # 每5秒增加敵人生成數量
base_enemy_count = 1  # 每次生成的敵人數量基數

last_increment_time = pygame.time.get_ticks()  # 用於追蹤上次增量的時間
last_enemy_spawn_time = pygame.time.get_ticks()  # 追蹤上次生成敵人的時間
SHOOT_DELAY = 400  # 每0.4秒才能射擊一次
last_shoot_time = pygame.time.get_ticks()  # 追蹤上次射擊的時間

# 設定分數
score = 0  # 初始分數
start_time = pygame.time.get_ticks()  # 紀錄遊戲開始時間
```
## #載入程式所需圖片
```python
#玩家
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))
#玩家(無敵時)
player_invincible_image = pygame.image.load("invincible.png")
player_invincible_image = pygame.transform.scale(player_invincible_image, (PLAYER_SIZE, PLAYER_SIZE))
#近距離敵人
enemy_image = pygame.image.load("enemy.png")
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))
#遠距離敵人
enemy2_image = pygame.image.load("enemy2.png")
enemy2_image = pygame.transform.scale(enemy2_image, (ENEMY_SIZE, ENEMY_SIZE))
#玩家子彈
bullet_image = pygame.image.load("bullet.png")
bullet_image = pygame.transform.scale(bullet_image, (BULLET_SIZE, BULLET_SIZE))
#敵人子彈
bullet2_image = pygame.image.load("bullet2.png")
bullet2_image = pygame.transform.scale(bullet2_image, (BULLET_SIZE, BULLET_SIZE))
```
## #子彈程式
```python
# 發射子彈(滑鼠左鍵)（朝滑鼠游標方向）
def shoot_bullet():
    global last_shoot_time
    
    current_time = pygame.time.get_ticks()  # 獲取當前時間
    if current_time - last_shoot_time >= SHOOT_DELAY:  # 檢查射擊間隔(0.4秒)
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
        shoot_sound.play()
        last_shoot_time = current_time  # 更新上次射擊的時間

# 子彈移動
def move_bullets():
    global bullets
    for bullet in bullets[:]:
        if bullet.get('type') == 'enemy2':  # enemy2 子彈
            speed_multiplier = 0.8  # enemy2 子彈速度快
        else:
            speed_multiplier = 1

        bullet['rect'].x += bullet['dx'] * 10 * speed_multiplier
        bullet['rect'].y += bullet['dy'] * 10 * speed_multiplier

        # 子彈超出畫面時移除
        if bullet in bullets and (
            bullet['rect'].x < 0 or 
            bullet['rect'].x > SCREEN_WIDTH or 
            bullet['rect'].y < 0 or 
            bullet['rect'].y > SCREEN_HEIGHT
        ):
            bullets.remove(bullet)
```
## #敵人主程式
```python
# 創建敵人
def create_enemy():
    global enemies

    # 每次最多生成 3 個敵人
    max_new_enemies = min(3, base_enemy_count)  # 取基數與 3 的較小值

    for _ in range(max_new_enemies):  # 循環最多生成 3 個敵人
        edge = random.choice(["top", "bottom", "left", "right"])
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

        # 隨機選擇生成普通敵人還是射擊敵人
        is_shooter = random.random() < 0.3  # 30%的機率會是射擊敵人
        image = enemy_image if not is_shooter else enemy2_image
        enemies.append(Enemy(enemy_x, enemy_y, image, is_shooter))



# 檢查子彈與敵人的碰撞
def check_bullet_collisions():
    global enemies, bullets, score
    for bullet in bullets[:]:
        if bullet.get('type') == 'enemy2':  # 忽略敵人子彈
            continue

        for enemy in enemies[:]:
            if bullet['rect'].colliderect(enemy.rect):
                hit_sound.play()
                bullets.remove(bullet)
                
                if enemy.is_shooter:
                    score += 2  # 對射擊型敵人給 2 分
                else:
                    score += 1  # 普通敵人加 1 分

                enemies.remove(enemy)
                break

# 敵人移動方向
def move_enemies():
    global enemies, player_rect
    for enemy in enemies[:]:
        # 計算玩家與敵人的中心點
        enemy_center = (enemy.rect.x + ENEMY_SIZE // 2, enemy.rect.y + ENEMY_SIZE // 2)
        player_center = (player_x + PLAYER_SIZE // 2, player_y + PLAYER_SIZE // 2)
        
        # 計算朝向玩家的方向
        direction = (player_center[0] - enemy_center[0], player_center[1] - enemy_center[1])
        length = math.sqrt(direction[0] ** 2 + direction[1] ** 2)
        
        # 避免除以零錯誤
        if length != 0:
            direction = (direction[0] / length, direction[1] / length)
        
        # 設定敵人移動速度，射擊型敵人更慢
        move_speed = 2 if not enemy.is_shooter else 0.5  # 設定射擊型敵人更慢

        # 移動敵人
        enemy.rect.x += direction[0] * move_speed
        enemy.rect.y += direction[1] * move_speed

        # 如果敵人是射擊型敵人，讓它發射子彈
        if enemy.is_shooter:
            enemy.shoot()
```
