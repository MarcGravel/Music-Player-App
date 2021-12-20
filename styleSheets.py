def toolBtnStyle():
    return """
        QToolButton {
            border: none;
            background: transparent;
        }
        QToolButton QWidget {
            color: black;
        }
    """

def groupBoxStyle():
    return """
        QGroupBox {
            background: QLinearGradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));
            background: QLinearGradient( x1:0 y1:0, x2:1 y2:0, stop:0 #ff6320, stop:1 #cc3d00);
            font: 15pt Bold;
            color: white;
            border: 2px solid grey;
            border-radius: 15px;
        }
    """
    
def progressBarStyle():
    return """
        QProgressBar {
            border: 1px solid #000;
            background: white;
            height: 16px;
            border-radius: 3px;
        }
        QProgressBar::chunk {
            border-radius: 2px;
            background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1,
            stop: 0 #05b8cc,
            stop: 0.4999 #eee,
            stop: 0.5 #ddd,
            stop: 1 #05b8cc );
        }
    """
    
def playlistStyle():
    return """
        QListWidget {
            background: QLinearGradient(spread:pad, x1:0 y1:0, x2:1 y2:0, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));
            background: QLinearGradient( x1:0 y1:0, x2:1 y2:0, stop:0 #ffbfa3, stop:1 #ffd4c2);
            color: black;
            border-radius: 15px;
            border: 3px solid grey;
            padding: 12px 12px;
            font: 12pt Helvetica;
        }
    """
