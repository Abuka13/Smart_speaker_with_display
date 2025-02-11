import sys
import os
import cv2
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton, QDialog, QLabel, QMessageBox)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QUrl, QTimer, QDateTime
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QDesktopServices
from PyQt5 import uic
import requests
from datetime import datetime
import pytz

class CameraDialog(QDialog):
    def __init__(self):
        super(CameraDialog, self).__init__()

        self.setWindowTitle("Камера")
        self.resize(640, 480)

        # Основной лэйаут
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Виджет для отображения видео
        self.video_label = QLabel("Запуск камеры...")
        self.video_label.setStyleSheet("background-color: black; color: white;")
        self.layout.addWidget(self.video_label)

        # Кнопка для фотографирования
        self.photo_button = QPushButton("Сделать фото")
        self.photo_button.clicked.connect(self.take_photo)
        self.layout.addWidget(self.photo_button)

        # Таймер для обновления кадров
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Запуск камеры
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            QMessageBox.critical(self, "Ошибка", "Не удалось открыть камеру.")
            self.close()

        self.timer.start(30)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Преобразуем кадр в формат для PyQt
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.video_label.setPixmap(pixmap)

    def take_photo(self):
        ret, frame = self.cap.read()
        if ret:
            # Создаем папку pictures, если ее нет
            pictures_dir = os.path.join(os.getcwd(), 'pictures')
            if not os.path.exists(pictures_dir):
                os.makedirs(pictures_dir)

            # Сохранение текущего кадра в файл
            filename = os.path.join(pictures_dir, "photo.jpg")
            cv2.imwrite(filename, frame)
            QMessageBox.information(self, "Фото", f"Фото сохранено как {filename}.")

    def closeEvent(self, event):
        # Освобождаем ресурсы камеры при закрытии окна
        self.timer.stop()
        if self.cap.isOpened():
            self.cap.release()
        event.accept()

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
        try:
            url = 'http://127.0.0.1:8000/'
            response = requests.get(url)
            if response.status_code == 200:
                temp_value = ''.join(char for char in response.text if char.isdigit() or char == '-')
                self.ui.label_2.setText(f"{temp_value}°C")
            else:
                self.ui.label_2.setText("N/A")
        except requests.RequestException:
            self.ui.label_2.setText("N/A")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        now = datetime.now()
        today_date = now.strftime("%d")
        day_of_week = now.strftime("%A")
        self.ui.label_3.setText(str(today_date)+','+str(day_of_week))

        self.song_paths = ['musics/Ed Sheeran – Shape of You.mp3', 'musics/Alan Walker – Faded.mp3', 'musics/Manu Chao - Me Gustas Tu (Official Audio).mp3', 'musics/Evergreen_EXTENDED_Original_Audio___Richy_Mitch_&_The_Coal_Miners.mp3']
        self.current_song_index = 0

        self.ui.pushButton_3.clicked.connect(self.play_song)

        self.ui.stop.clicked.connect(self.stop_song)

        self.ui.next.clicked.connect(self.next_song)

        self.ui.previous.clicked.connect(self.previous_song)

        self.media_player = QMediaPlayer()
        self.current_position = 0

        self.ui.youtube.clicked.connect(self.show_youtube)
        self.ui.instagram.clicked.connect(self.show_instagram)
        self.ui.camera.clicked.connect(self.open_camera)

    def update_time(self):
        astana_tz = pytz.timezone("Asia/Almaty")  # Часовой пояс Астаны (UTC+6)
        now_astana = datetime.now(astana_tz).strftime("%H:%M:%S")  # Формат времени
        self.ui.label.setText(now_astana)  # Убедитесь, что label есть в UI

    def show_map(self):
        self.map_dialog = MapDialog()
        self.map_dialog.exec()

    def show_youtube(self):
        self.youtube_dialog = YoutubeOpener()
        self.youtube_dialog.exec()

    def show_instagram(self):
        self.instagram_dialog = InstagramOpener()
        self.instagram_dialog.exec()

    def open_camera(self):
        self.camera_dialog = CameraDialog()
        self.camera_dialog.exec()

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
        # Переходим к предыдущей песне
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
