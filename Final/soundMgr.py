import pygame
from pygame.locals import *
import random as rand
class SoundMgr:
    
    path = "media/sounds/"
    musExt = ".mp3"
    sfxExt = ".ogg"
    debug = False
    
    def __init__(self, engine):
        self.engine = engine
        

    def init(self):
        pygame.init()
        pygame.mixer.init()
        self.musicVolume = 100.0
   
        self.musicList = ["liverpool", "bvb", "arsenal", "liverpool", "bvb"]
        self.sfxList = ["break", "bounce"]
        self.celebrationList = ["cel1", "cel2", "cel3", "cel4", "cel5", "cel6", "cel7"]
        self.celebrationNum = len(self.celebrationList) - 1
        
        if SoundMgr.debug:
            self.playMusic("Champions_League_theme")
            self.playSound("break")


    def playMusic(self, music, num = -1):
        pygame.mixer.music.load(SoundMgr.path + music + SoundMgr.musExt)
        pygame.mixer.music.play(num)
        pygame.mixer.music.set_volume(self.musicVolume / 100.0)

    def playSound(self, sfx):
        sound = pygame.mixer.Sound(SoundMgr.path + sfx + SoundMgr.sfxExt)
        sound.play()
    
    def playACelebration(self):
        songNum = rand.randint(0, self.celebrationNum)
        self.playMusic(self.celebrationList[songNum], 0)
        self.musicVolume = 100

    def soundBusy(self):
        return pygame.mixer.get_busy()

    def musicBusy(self):
        return pygame.mixer.music.get_busy()

    def stopMusic(self, music):
        pygame.mixer.music.stop()

    def upVolume(self):
        self.musicVolume += 1

    def downVolume(self):
        self.musicVolume -= 1

    def setVolume(self, vol):
        self.musicVolume = vol
        pygame.mixer.music.set_volume(self.musicVolume / 100.0)

