import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtGui import QIcon
# pip install PyQtWebEngine
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

__version__ = 'v1.1'
__author__ = 'Jie'


class YouTubePlayer(QWidget):
    def __init__(self, video_id, parent=None):
        super().__init__()
        self.parent = parent
        self.video_id = video_id

        defaultSettings = QWebEngineSettings.globalSettings()
        defaultSettings.setFontSize(QWebEngineSettings.MinimumFontSize, 25)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        topLayout = QHBoxLayout()
        self.layout.addLayout(topLayout)

        label = QLabel('Enter Video Id: ')
        self.input = QLineEdit()
        self.input.installEventFilter(self)
        self.input.setText(self.video_id)

        topLayout.addWidget(label, 1)
        topLayout.addWidget(self.input, 9)

        self.addWebView(self.input.text())

        buttonLayout = QHBoxLayout()
        self.layout.addLayout(buttonLayout)

        buttonUpdate = QPushButton('Update', clicked=self.updateVideo)
        buttonRemove = QPushButton('Delete', clicked=self.removePlayer)
        buttonLayout.addWidget(buttonUpdate)
        buttonLayout.addWidget(buttonRemove)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.updateVideo()
        return super().eventFilter(source, event)

    def addWebView(self, video_id):
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))
        self.layout.addWidget(self.webview)

    def updateVideo(self):
        video_Id = self.input.text()
        self.webview.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))

    def removePlayer(self):
        widget = self.sender().parent()
        widget.setParent(None)
        widget.deleteLater()

    def organizeLayout(self):
        playerCount = self.parent.videoGrid.count()
        players = []

        for i in reversed(range(playerCount)):
            player = self.parent.videoGrid.itemAt(i).widget()
            players.append(player)

        for indx, player in enumerate(players[::-1]):
            self.parent.videoGrid.addWidget(player, indx % 3, indx // 3)


class YouTubeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('YouTube Video Player')
        self.setWindowIcon(QIcon('yt.png'))
        self.setMinimumSize(900, 600)
        self.players = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        buttonAddPlayer = QPushButton('Add Player', clicked=self.addPlayer)
        self.layout.addWidget(buttonAddPlayer)

        self.videoGrid = QGridLayout()
        self.layout.addLayout(self.videoGrid)

        self.player = YouTubePlayer('r789UEtxlTI', parent=self)
        self.videoGrid.addWidget(self.player, 0, 0)

        self.layout.addWidget(QLabel(__version__ + 'by' + __author__), alignment=Qt.AlignBottom | Qt.AlignRight)

        self.setStyleSheet("""
            QPushButton{
                font-size: 28px;
                height: 40px;
                width: 40px;
                background-color: #E41937;
                color: white;
            }

            * {
                background-color: white;
                font-size: 30px;

            QLineEdit {
                background-color: white;
            }

        """)

    def addPlayer(self):
        playerCount = self.videoGrid.count()
        row = playerCount % 3
        col = playerCount // 3

        self.player = YouTubePlayer('', parent=self)
        self.videoGrid.addWidget(self.player, row, col)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = YouTubeWindow()
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('player Window Closed')