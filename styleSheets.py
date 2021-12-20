def toolBtnStyle():
    return """
        QToolButton {
            border: none;
            background-color: #ff6320;
        }
    """

def groupBoxStyle():
    return """
        QGroupBox {
            background-color: #ff6320;
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
