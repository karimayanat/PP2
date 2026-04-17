import pygame

class MusicPlayer:
    def __init__(self):
        self.tracks = ["music/BBB.mpeg", "music/FIRE.mpeg"]
        self.index = 0
        pygame.mixer.init()
    def play(self):
        try:
            pygame.mixer.music.load(self.tracks[self.index])
            pygame.mixer.music.play()
        except:
            print("Error loading track")
    def stop(self):
        pygame.mixer.music.stop()
    def next(self):
        self.index = (self.index + 1) % len(self.tracks)
        self.play()
    def prev(self):
        self.index = (self.index - 1) % len(self.tracks)
        self.play()
    def current_track(self):
        return self.tracks[self.index]