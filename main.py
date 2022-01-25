import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QUrl, QEvent
from PyQt5.QtGui import QIcon
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib.request
import time
from IPython.display import display
from webdriver_manager.chrome import ChromeDriverManager
import warnings
warnings.filterwarnings(action='ignore')
from PyQt5.QtWebEngineWidgets import QWebEngineSettings, QWebEngineView

__version__ = 'capston'
__author__ = '624호'


class YouTubePlayer(QWidget):
    def __init__(self, video_id, parent=None):
        super().__init__()
        self.parent = parent
        self.video_id = video_id

        defaultSettings = QWebEngineSettings.globalSettings()
        defaultSettings.setFontSize(QWebEngineSettings.MinimumFontSize, 25)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.input = QLineEdit()
        self.input.installEventFilter(self)
        self.input.setText(self.video_id)
        self.addWebView(self.input.text())

    def eventFilter(self, source, event):
         if event.type() == QEvent.KeyPress:
                 self.updateVideo()
         return super().eventFilter(source, event)

    def addWebView(self, video_id):
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl(f'https://www.youtube.com/embed/{self.video_id}?rel=0'))
        self.layout.addWidget(self.webview)


class YouTubeWindow(QWidget):
    def __init__(self, url):
        super().__init__()
        self.setWindowTitle('YouTube Video Player')
        self.setWindowIcon(QIcon('yt.png'))
        self.setMinimumSize(900, 500)
        self.players = []

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.videoGrid = QGridLayout()
        self.layout.addLayout(self.videoGrid)

        self.player = YouTubePlayer(url, parent=self)
        self.videoGrid.addWidget(self.player, 0, 0)

        self.layout.addWidget(QLabel(__version__ + ' by ' + __author__), alignment=Qt.AlignBottom | Qt.AlignRight)


def get_video():
    feature = input('검색어를 입력하시오 : ')

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.youtube.com')

    n = 3
    while n > 0:
        print('웹페이지를 불러오는 중입니다..' + '..' * n)
        time.sleep(1)
        n -= 1

    src = driver.find_element_by_name("search_query")
    src.send_keys(feature)
    src.send_keys(Keys.RETURN)

    n = 2
    while n > 0:
        print('검색 결과를 불러오는 중입니다..' + '..' * n)
        time.sleep(1)
        n -= 1

    print('데이터 수집 중입니다....')

    html = driver.page_source
    soup = BeautifulSoup(html)

    df_title = []
    df_link = []
    df_writer = []
    df_view = []
    df_date = []

    for i in range(len(soup.find_all('ytd-video-meta-block', 'style-scope ytd-video-renderer byline-separated'))):
        title = soup.find_all('a', {'id': 'video-title'})[i].text.replace('\n', '')
        link = 'https://www.youtube.com/' + soup.find_all('a', {'id': 'video-title'})[i]['href']
        writer = \
        soup.find_all('ytd-channel-name', 'long-byline style-scope ytd-video-renderer')[i].text.replace('\n', '').split(
            ' ')[0]
        view = \
        soup.find_all('ytd-video-meta-block', 'style-scope ytd-video-renderer byline-separated')[i].text.split('•')[
            1].split('\n')[3]
        date = \
        soup.find_all('ytd-video-meta-block', 'style-scope ytd-video-renderer byline-separated')[i].text.split('•')[
            1].split('\n')[4]

        df_title.append(title)
        df_link.append(link)
        df_writer.append(writer)
        df_view.append(view)
        df_date.append(date)

    df_just_video = pd.DataFrame(columns=['영상제목', '채널명', '영상url', '조회수', '영상등록날짜'])

    df_just_video['영상제목'] = df_title
    df_just_video['채널명'] = df_writer
    df_just_video['영상url'] = df_link
    df_just_video['조회수'] = df_view
    df_just_video['영상등록날짜'] = df_date

    df_just_video.to_csv('C:\\Users\\c\\df_just_video.csv', encoding='utf-8-sig', index=False)

    driver.close()

    result = input('데이터프레임 저장이 완료되었습니다! 데이터프레임을 조회하시겠습니까? (y/n)')

    if result == 'y':
        display(df_just_video)
        question = input('원하는 영상을 재생하시겠습니까? (y/n)')
        if question == 'y':
            button = int(input('재생하고자 하는 영상의 번호(출력된 표 가장 왼쪽의 번호)를 입력해주세요.'))
            url = df_just_video['영상url'][button]
            return url.replace("https://www.youtube.com//watch?v=","")

        else:
            exit()
    else:
        exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = YouTubeWindow(get_video())
    window.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('player Window Closed')