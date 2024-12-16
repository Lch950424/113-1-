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
![播放音樂]([https://fengchia-my.sharepoint.com/:i:/g/personal/d1353491_o365_fcu_edu_tw/EeVvYsow2dpKtsGpOBv3AmABWeio8eU-A2JFblfoOXyQ3Q?e=1hQ1es](https://fengchia-my.sharepoint.com/:f:/g/personal/d1353491_o365_fcu_edu_tw/Eu-L6yCkh8ZNs_eoAU6j-0kBq7sojxx-6RDkB4fBw04bxg?e=wXBx7d))
## #設定音樂、音效音量
```python
# 設定音樂音量
pygame.mixer.music.set_volume(0.7)  # 將音樂音量設為 70%

# 設定音效音量
shoot_sound.set_volume(0.3)        # 將射擊音效音量設為 30%
hit_sound.set_volume(0.4)          # 將擊中音效音量設為 40%
damage_sound.set_volume(0.6)       # 將受傷音效音量設為 60%
```
