import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QDialog
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import uic
from PyQt5.QtCore import QUrl, QTimer
import requests
from datetime import datetime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtGui import QDesktopServices

class YoutubeOpener(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        btn = QPushButton('Открыть YouTube', self)
        btn.clicked.connect(self.open_youtube)
        btn.move(50, 50)

    def open_youtube(self):
        url = QUrl('https://www.youtube.com/')
        QDesktopServices.openUrl(url)

class InstagramOpener(QDialog):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        btn = QPushButton('Открыть Instagram', self)
        btn.clicked.connect(self.open_instagram)
        btn.move(50, 50)

    def open_instagram(self):
        url = QUrl('https://www.instagram.com/')
        QDesktopServices.openUrl(url)

class MapDialog(QDialog):
    def __init__(self):
        super(MapDialog, self).__init__()

        layout = QVBoxLayout(self)

        # Создаем виджет для отображения веб-страниц
        self.webview = QWebEngineView()
        layout.addWidget(self.webview)

        url = QUrl("https://www.google.com/maps")
        self.webview.setUrl(url)

class MyWindow(QWidget):
    def __init__(self):
        super(MyWindow, self).__init__()

        # Загрузка интерфейса из файла .ui
        self.ui = uic.loadUi('speaker.ui', self)
        self.ui.buttonmap.clicked.connect(self.show_map)
        url = 'http://127.0.0.1:8000/'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.text
            self.ui.label.setText(str(data[0:5]))
            self.ui.label_2.setText(str(data[6:10]).replace(',', '')+'°')

        now = datetime.now()
        today_date = now.strftime("%d")
        day_of_week = now.strftime("%A")
        self.ui.label_3.setText(str(today_date)+','+str(day_of_week))

        self.song_paths = ['musics/Ed Sheeran – Shape of You.mp3', 'musics/Alan Walker – Faded.mp3']
        self.current_song_index = 0

        self.ui.pushButton_3.clicked.connect(self.play_song)

        self.ui.stop.clicked.connect(self.stop_song)

        self.ui.next.clicked.connect(self.next_song)

        self.ui.previous.clicked.connect(self.previous_song)


        self.media_player = QMediaPlayer()
        self.current_position = 0

        self.ui.youtube.clicked.connect(self.show_youtube)
        self.ui.instagram.clicked.connect(self.show_instagram)


    def show_map(self):
        self.map_dialog = MapDialog()
        self.map_dialog.exec()

    def show_youtube(self):
        self.youtube_dialog = YoutubeOpener()
        self.youtube_dialog.exec()

    def show_instagram(self):
        self.instagram_dialog = InstagramOpener()
        self.instagram_dialog.exec()

    def play_song(self):



        if not self.media_player.isAudioAvailable():

            media = QMediaContent(QUrl.fromLocalFile(self.song_paths[self.current_song_index]))
            self.media_player.setMedia(media)
        else:

            self.media_player.setPosition(self.current_position)

        # Воспроизводим песню
        self.media_player.play()
        self.ui.song.setText(str(self.song_paths[self.current_song_index]).replace('musics/', ''))
    def stop_song(self):
        self.current_position = self.media_player.position()
        self.media_player.stop()

    def next_song(self):
        # Переходим к следующей песне
        self.current_song_index = (self.current_song_index + 1) % len(self.song_paths)
        song_path = self.song_paths[self.current_song_index]


        media = QMediaContent(QUrl.fromLocalFile(song_path))
        self.media_player.setMedia(media)
        self.media_player.play()


        self.ui.song.setText((self.song_paths[self.current_song_index].replace('musics/', '')))

    def previous_song(self):
        # Переходим к следующей песне
        self.current_song_index = (self.current_song_index - 1) % len(self.song_paths)
        song_path = self.song_paths[self.current_song_index]


        media = QMediaContent(QUrl.fromLocalFile(song_path))
        self.media_player.setMedia(media)
        self.media_player.play()


        self.ui.song.setText((self.song_paths[self.current_song_index].replace('musics/', '')))

def main():
    app = QApplication([])
    window = MyWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()