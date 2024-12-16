## #import
在python一開始先宣告函式庫
此程式需使用pygame
```python
#import pygame
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