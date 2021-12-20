import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt, QTimer
import os
import random, time
from audioread.exceptions import NoBackendError
import pygame
import audioread
from mutagen.mp3 import MP3
from styleSheets import *

pygame.init() # Initialize pygame

#global vaiables
songList = []
currentVolume = 0;
currentSongIndex = None
muted = False
playing = True
timerCount = 0
pauseTimer = 0
songLength = 0

class Player(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sweet Beat Music Player")
        self.setWindowIcon(QIcon("images/appIcon.svg"))
        self.setStyleSheet("background-color: black;")
        self.setGeometry(600, 150, 500, 750)
        self.center()
        self.UI()
        
        self.show()
        
    #set window in center of screen    
    def center(self):
        #frame geo is geometry of the image view corresponding to the main window
        frameGm = self.frameGeometry()
        #get size of screen
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        #get center point of screen
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        #set framegm to center
        frameGm.moveCenter(centerPoint)
        #move player window to center
        self.move(frameGm.topLeft())
        
    def UI(self):
        self.widgets()
        self.layouts()
        
    ###########################################Widgets################################################
    def widgets(self): 
        self.progressBar = QProgressBar()
        self.progressBar.setTextVisible(False)
        self.progressBar.setStyleSheet(progressBarStyle())
        #force repaint every time there is a change due to chunck lag on stylesheet
        self.progressBar.valueChanged.connect(self.progressBar.repaint)
        
        #progress bar labels
        self.songTimeLabel = QLabel("0:00")
        self.songTimeLabel.setStyleSheet("background-color: #ff6320;")
        self.songLengthLabel = QLabel("/ 0:00")
        self.songLengthLabel.setStyleSheet("background-color: #ff6320;")
        
        #buttons
        self.addBtn = QToolButton()
        self.addBtn = self.buttonSettings(self.addBtn, "images/add.png", 50, "Add a song")
        self.addBtn.clicked.connect(self.addSong)
        
        self.shuffleBtn  = QToolButton()
        self.shuffleBtn = self.buttonSettings(self.shuffleBtn, "images/shuffle.png", 50, "Shuffle")
        self.shuffleBtn.clicked.connect(self.shufflePlaylist)
        
        self.previousBtn = QToolButton()
        self.previousBtn = self.buttonSettings(self.previousBtn, "images/previous.png", 50, "Previous Song")
        self.previousBtn.clicked.connect(self.playPrevious)
        
        self.playBtn = QToolButton()
        self.playBtn = self.buttonSettings(self.playBtn, "images/play.png", 70, "Play")
        self.playBtn.clicked.connect(self.playSong)
        
        self.nextBtn = QToolButton()
        self.nextBtn = self.buttonSettings(self.nextBtn, "images/next.png", 50, "Next Song")
        self.nextBtn.clicked.connect(self.playNext)
        
        self.muteBtn = QToolButton()
        self.muteBtn = self.buttonSettings(self.muteBtn, "images/unmuted.png", 25, "Mute")
        self.muteBtn.clicked.connect(self.muteSong)
        
        #volume slider
        self.volumeBar = QSlider()
        self.volumeBar.setOrientation(Qt.Horizontal)
        self.volumeBar.setToolTip("Volume")
        self.volumeBar.setStyleSheet("background-color: #ff6320;")
        self.volumeBar.setValue(80)
        self.volumeBar.setMinimum(0)
        self.volumeBar.setMaximum(100)
        #set initial value of mixer. between 0 and 1
        pygame.mixer.music.set_volume(0.7)
        #when value changes, trigger function
        self.volumeBar.valueChanged.connect(self.setVolume)
        
        #####playlist#####
        self.playlist = QListWidget()
        self.playlist.doubleClicked.connect(self.playSong)
        
        ####Timer####
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.updateProgressBar)
        
        
    ##########################################layouts###############################################
    def layouts(self):
        self.main = QVBoxLayout()
        self.topMain = QVBoxLayout()
        self.topGroupBox = QGroupBox("Sweet Beat", self)
        self.topGroupBox.setStyleSheet(groupBoxStyle())
        self.top = QHBoxLayout()
        self.middle = QHBoxLayout()
        self.bottom = QVBoxLayout()
        
        #Adding widgets/layouts
        
        #top layout widgets
        self.top.addWidget(self.progressBar)
        self.top.addWidget(self.songTimeLabel)
        self.top.addWidget(self.songLengthLabel)
        
        #topMid layout widgets
        self.middle.addStretch()
        self.middle.addWidget(self.addBtn)
        self.middle.addWidget(self.shuffleBtn)
        self.middle.addWidget(self.previousBtn)
        self.middle.addWidget(self.playBtn)
        self.middle.addWidget(self.nextBtn)
        self.middle.addWidget(self.volumeBar)
        self.middle.addWidget(self.muteBtn)
        self.middle.addStretch()
        
        #bottom layout widgets
        self.bottom.addWidget(self.playlist)
        
        #set the order/position of layouts
        self.topMain.addLayout(self.top)
        self.topMain.addLayout(self.middle)
        self.topGroupBox.setLayout(self.topMain)
        #numbers in arguments are setting aspect ratios
        self.main.addWidget(self.topGroupBox, 35)
        self.main.addLayout(self.bottom, 65)
        self.setLayout(self.main)
        
    #######################################Button Functions##############################################
    
    #Stlye function for QToolButtons
    def buttonSettings(self, btn, icon, iconSize, tooltip):
        btn.setIcon(QIcon(str(icon)))
        btn.setIconSize(QSize(iconSize, iconSize))
        btn.setToolTip(tooltip)
        btn.setStyleSheet(toolBtnStyle())
        
        return btn
    
    def addSong(self):
        playlist = QFileDialog.getOpenFileName(None, "Add Song", "", "Sound Files (*.mp3 *.ogg *.wav)")
        filename = os.path.basename(playlist[0])
        self.playlist.addItem(filename)
        songList.append(playlist[0])
        
    def shufflePlaylist(self):
        random.shuffle(songList)
        self.playlist.clear()
        for song in songList:
            filename = os.path.basename(song)
            self.playlist.addItem(filename)
    
    #handles loading+playing track, alsoreads song length and sets values for P-bar and counter
    #definition is used in playSong, playPrevious, playNext functions        
    def loadPlayReadTrack(self, index):
        global currentSongIndex
        global playing
        global songLength
        global songList
        
        try:
            pygame.mixer.music.load(str(songList[index]))
            pygame.mixer.music.play()
            self.timer.start()
            currentSongIndex = index
                
            try: 
                with audioread.audio_open(str(songList[index])) as f:
                    totalsec = f.duration
                    totalsec = round(totalsec)
                    songLength = totalsec
                    
                    #update progress bar label
                    min,sec = divmod(songLength, 60)
                    self.songLengthLabel.setText("/ "+str(min)+":"+str(sec))
                    
                    self.progressBar.setValue(0)
                    self.progressBar.setMaximum(totalsec)
            except(NoBackendError):
                #if sounds file is mp3, try with mutagen
                try:
                    totalsec = MP3(str(songList[index]))
                    songLength = totalsec.info.length
                    songLength = round(songLength)
                    
                    #update progress bar label
                    min,sec = divmod(songLength, 60)
                    self.songLengthLabel.setText("/ "+str(min)+":"+str(sec))
                    
                    self.progressBar.setValue(0)
                    self.progressBar.setMaximum(songLength)
                    
                except:
                    print("Cannot match audio file format")
            
            self.playBtn.setIcon(QIcon("images/pause.png"))
            self.playBtn.setToolTip("Pause")
            playing = True
                
        except:
            #pygame only allows 16bit mp3, ogg, wav files
            print("Error, unable to play format")
            mbox = QMessageBox.information(self, "Format Error", "Unable to play format. Only 16bit .mp3, .ogg, .wav available")
            
    def playSong(self):
        global playing
        global songLength
        global songList
        global timerCount
        global pauseTimer
        global currentSongIndex
        
        focusedSongIndex = self.playlist.currentRow()
        
        #if clicking same song or pause btn on same song
        if (currentSongIndex == focusedSongIndex):
            if (playing == True):
                pygame.mixer.music.pause()
                self.playBtn.setIcon(QIcon("images/play.png"))
                self.playBtn.setToolTip("Play")
                self.timer.stop()
                playing = False
            else:
                pygame.mixer.music.unpause()
                self.playBtn.setIcon(QIcon("images/pause.png"))
                self.playBtn.setToolTip("Pause")
                self.timer.start()
                playing = True
        else:
            #if new song started, reset the timers for progress bar
            timerCount = 0
            pauseTimer = 0
            
            #send song index to play function
            self.loadPlayReadTrack(focusedSongIndex)
            
    def playPrevious(self):
        global timerCount
        global currentSongIndex
        global pauseTimer
        global songList
        
        previousSongIndex = currentSongIndex - 1
        
        #reset the timers for progress bar
        timerCount = 0
        pauseTimer = 0
        
        if (previousSongIndex < 0): #if at start of playlist, play last track
            #change focus element to last track of songlist track and set global currentSongIndex to same
            self.playlist.setCurrentRow(len(songList) - 1)
            currentSongIndex = len(songList) - 1
            
            #send song index to play function
            self.loadPlayReadTrack(len(songList) - 1)
        
        else: #else play previous
            #change focus element to previous track and set global currentSongIndex to previous track
            self.playlist.setCurrentRow(currentSongIndex - 1)
            currentSongIndex -= 1
            
            #send song index to play function
            self.loadPlayReadTrack(previousSongIndex)
            
    def playNext(self):
        global songList
        global timerCount
        global currentSongIndex
        global pauseTimer
        
        nextSongIndex = currentSongIndex + 1
        #reset the timers for progress bar
        timerCount = 0
        pauseTimer = 0
        
        if (nextSongIndex >= len(songList)): #if at end of playlist, play first track    
            #change focus element to first track and set global currentSongIndex to same
            self.playlist.setCurrentRow(0)
            currentSongIndex = 0
            
            #send song index to play function
            self.loadPlayReadTrack(0)
            
        else: #else play next track
            #reset the timers for progress bar
            timerCount = 0
            pauseTimer = 0
            
            #change focus element to next track and set global currentSongIndex to same
            self.playlist.setCurrentRow(currentSongIndex + 1)
            currentSongIndex += 1
            
            #send song index to play function
            self.loadPlayReadTrack(nextSongIndex)

    def setVolume(self):
        volume = self.volumeBar.value()
        volumeToMixer = volume / 100
        pygame.mixer.music.set_volume(volumeToMixer)
        
    def muteSong(self):
        global muted
        global currentVolume
        
        if (muted == False):
            currentVolume = self.volumeBar.value()
            self.volumeBar.setValue(0)
            pygame.mixer.music.set_volume(0)
            muted = True
            self.muteBtn.setIcon(QIcon("images/mute.png"))
            self.muteBtn.setToolTip("Unmute")
        else:
            self.volumeBar.setValue(currentVolume)
            pygame.mixer.music.set_volume(currentVolume / 100)
            muted = False
            self.muteBtn.setIcon(QIcon("images/unmuted.png"))
            self.muteBtn.setToolTip("Mute")
            
    def updateProgressBar(self):
        global timerCount
        global songLength
        global pauseTimer
        
        #ensures progress bar starts on correct time if song paused
        if pauseTimer != 0:
            timerCount = pauseTimer
            self.songTimeLabel.setText(time.strftime("%M:%S", time.gmtime(timerCount)))
            pauseTimer = 0
        
        timerCount += 1
        pauseTimer = timerCount
        self.progressBar.setValue(timerCount)
        self.songTimeLabel.setText(time.strftime("%M:%S", time.gmtime(timerCount)))
        if (timerCount == songLength):
            self.timer.stop()

def main():
    App = QApplication(sys.argv)
    player = Player()
    sys.exit(App.exec_())
    
if __name__ == "__main__":
    main()