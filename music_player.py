# music_player.py

import pygame
import random

class MusicPlayer:
    def __init__(self, songs=None, volume=0.7):
        pygame.init()
        if songs is None:
            songs = [
                "music/2024世界12強棒球錦標賽 - 賽事主題曲【就一起】完整版.mp3", 
                "music/小男孩樂團 Men Envy Children【我想要擁有你 Make You Mine】Netflix影集《影后》插曲 Official Music Video.mp3", 
                "music/Mayday五月天 [ 如果我們不曾相遇What If We Had Never Met ] Official Music Video.mp3"
            ]
        
        self.songs = songs
        self.volume = volume
        pygame.mixer.music.set_volume(self.volume)
    
    def play_random_song(self):
        selected_song = random.choice(self.songs)
        print(f"正在播放: {selected_song}")
        pygame.mixer.music.load(selected_song)
        pygame.mixer.music.play()

    def play_background_music(self):
        self.play_random_song()
        running = True
        while running:
            if not pygame.mixer.music.get_busy():
                self.play_random_song()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def stop_music(self):
        pygame.mixer.music.stop()
        pygame.quit()

