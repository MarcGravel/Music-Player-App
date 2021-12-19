import sys
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize, Qt
import os
import random

songlist = []

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
        
    #############################Widgets##################################
    def widgets(self): 
        self.progressBar = QProgressBar()
        
        #buttons
        self.addBtn = QToolButton()
        self.addBtn.setIcon(QIcon("images/add.png"))
        self.addBtn = self.buttonStyle(self.addBtn, "Add a song")
        self.addBtn.clicked.connect(self.addSong)
        
        self.shuffleBtn  = QToolButton()
        self.shuffleBtn.setIcon(QIcon("images/shuffle.png"))
        self.shuffleBtn = self.buttonStyle(self.shuffleBtn, "Shuffle")
        self.shuffleBtn.clicked.connect(self.shufflePlaylist)
        
        self.previousBtn = QToolButton()
        self.previousBtn.setIcon(QIcon("images/previous.png"))
        self.previousBtn = self.buttonStyle(self.previousBtn, "Previous Song")
        
        self.playBtn = QToolButton()
        self.playBtn.setIcon(QIcon("images/play.png"))
        self.playBtn = self.buttonStyle(self.playBtn, "Play")
        self.playBtn.setIconSize(QSize(70, 70))
        
        self.nextBtn = QToolButton()
        self.nextBtn.setIcon(QIcon("images/next.png"))
        self.nextBtn = self.buttonStyle(self.nextBtn, "Next Song")
        
        self.muteBtn = QToolButton()
        self.muteBtn.setIcon(QIcon("images/mute.png"))
        self.muteBtn = self.buttonStyle(self.muteBtn, "Mute")
        self.muteBtn.setIconSize(QSize(25, 25))
        
        #volume slider
        self.volumeBar = QSlider()
        self.volumeBar.setOrientation(Qt.Horizontal)
        self.volumeBar.setToolTip("Volume")
        
        #####playlist#####
        self.playlist = QListWidget()
        
        
        self.setStyleSheet("""QToolTip {
                                background-color: black;
                                color: white;
                                border: black solid 1px;
                                }""") 
    
    #Stlye function for btns
    def buttonStyle(self, btn, tooltip):
        btn.setIconSize(QSize(50, 50))
        btn.setStyleSheet("border: none;")
        btn.setToolTip(tooltip)
        
        return btn
        
        
    #############################layouts###################################
    def layouts(self):
        self.main = QVBoxLayout()
        self.topMain = QVBoxLayout()
        self.topGroupBox = QGroupBox("Music Player", self)
        self.topGroupBox.setStyleSheet("Background-color: #ff6320")
        self.top = QHBoxLayout()
        self.middle = QHBoxLayout()
        self.bottom = QVBoxLayout()
        
        #Adding widgets/layouts
        
        #top layout widgets
        self.top.addWidget(self.progressBar)
        
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
        
    #############Button Functions###################
    def addSong(self):
        playlist = QFileDialog.getOpenFileName(None, "Add Song", "", "Sound Files (*.mp3 *.ogg *.wav)")
        filename = os.path.basename(playlist[0])
        self.playlist.addItem(filename)
        songlist.append(filename)
        
    def shufflePlaylist(self):
        random.shuffle(songlist)
        self.playlist.clear()
        for song in songlist:
            self.playlist.addItem(song)
    
def main():
    App = QApplication(sys.argv)
    player = Player()
    sys.exit(App.exec_())
    
if __name__ == "__main__":
    main()