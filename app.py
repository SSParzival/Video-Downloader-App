import sys
import os
import re
import subprocess
from typing import List
from pathlib import Path
from pytubefix import YouTube, Playlist
import requests
import bs4
from tqdm import tqdm
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QTextEdit,
    QRadioButton,
    QButtonGroup,
    QProgressBar,
    QWidget,
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QThread, pyqtSignal


OUTPUT_DIR = r"C:\Users\mativ\Documents"
FILE_TYPE = "mp4"  # Default file type


class VideoDownloader(QThread):
    finished = pyqtSignal()
    progress = pyqtSignal(int)
    log_message = pyqtSignal(str)
    progress_update = pyqtSignal(float)

    def __init__(self, urls: List[str], output_dir: str, file_type: str):
        super().__init__()
        self.urls = urls
        self.output_dir = output_dir
        self.file_type = file_type
        self.total_videos = 0  # Total number of videos across all playlists
        self.downloaded_videos = 0  # Counter for downloaded videos

    def run(self):
        self.log_message.emit("Starting downloads...")
        failed_downloads = []

        self.total_videos = sum(
            self.get_playlist_video_count(url) if "playlist?list=" in url else 1
            for url in self.urls
        )
        self.log_message.emit(f"Total videos to download: {self.total_videos}")

        self.downloaded_videos = 0  # Counter for downloaded videos

        for url in self.urls:
            try:
                url = url.strip()
                if "youtube.com" in url or "youtu.be" in url:
                    if "playlist?list=" in url:
                        self.download_playlist(url)
                    else:
                        self.download_video(url)
                elif "twitter.com" in url or "x.com" in url:
                    self.download_twitter_video(url)
                else:
                    self.log_message.emit(f"Unsupported URL: {url}")
                    failed_downloads.append(url)
            except Exception as e:
                self.log_message.emit(f"Failed to download {url}: {str(e)}")
                failed_downloads.append(url)

        if failed_downloads:
            self.log_message.emit("\n" + "=" * 40)
            self.log_message.emit("     ❌ Some downloads failed ❌")
            self.log_message.emit("Failed URLs:")
            for failed_url in failed_downloads:
                self.log_message.emit(f"- {failed_url}")
            self.log_message.emit("=" * 40 + "\n")
        else:
            self.log_message.emit("\n" + "=" * 40)
            self.log_message.emit("       🎉 All downloads completed! 🎉")
            self.log_message.emit("=" * 40 + "\n")

        self.finished.emit()

    def download_video(self, url):
        try:
            yt = YouTube(url)
            if self.file_type == "mp3":
                audio_stream = yt.streams.filter(only_audio=True, abr="160kbps").last()
                if audio_stream is not None:
                    self.download_with_retry(
                        audio_stream, output_path=self.output_dir, rename_to_ext="mp3"
                    )
                    self.downloaded_videos += 1  # Increment downloaded videos
                    self.progress.emit(
                        int(self.downloaded_videos / self.total_videos * 100)
                    )  # Update progress

                else:
                    self.log_message.emit(f"No audio stream found for {yt.title}.")
            elif self.file_type == "mp4":
                video_stream = (
                    yt.streams.filter(progressive=False, file_extension="mp4")
                    .order_by("resolution")
                    .desc()
                    .first()
                )
                audio_stream = yt.streams.filter(
                    only_audio=True, file_extension="mp4"
                ).first()

                if video_stream is not None and audio_stream is not None:
                    if not os.path.exists(self.output_dir):
                        os.makedirs(self.output_dir)

                    video_file = self.download_with_retry(
                        video_stream,
                        output_path=self.output_dir,
                        filename="temp_video.mp4",
                    )
                    audio_file = self.download_with_retry(
                        audio_stream,
                        output_path=self.output_dir,
                        filename="temp_audio.mp4",
                    )
                    yt.title = re.sub(r"[<>:\"/\\|?*']", "", yt.title)
                    if video_file and audio_file:
                        output_file = Path(self.output_dir) / f"{yt.title}.mp4"

                        # Use subprocess to run ffmpeg with -progress flag
                        command = [
                            "ffmpeg",
                            "-i",
                            video_file,
                            "-i",
                            audio_file,
                            "-c:v",
                            "copy",
                            "-c:a",
                            "aac",
                            "-strict",
                            "experimental",
                            "-y",
                            str(output_file),
                            "-nostats",
                            "-loglevel",
                            "info",
                        ]
                        process = subprocess.Popen(
                            command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            universal_newlines=True,
                        )

                        # Read ffmpeg output and filter progress updates
                        for line in process.stderr:  # type: ignore
                            if "progress=" in line:
                                self.log_message.emit(line.strip())
                                # Extract progress from line and update progress bar
                                progress_match = re.search(
                                    r"progress=\s*([\d.]+)", line
                                )
                                if progress_match:
                                    progress = float(progress_match.group(1))
                                    self.progress.emit(
                                        int(progress)
                                    )  # Update progress bar

                        # Wait for ffmpeg process to finish
                        process.communicate()
                        # Clean up temp files
                        os.remove(video_file)
                        os.remove(audio_file)

                        if output_file.exists():
                            self.log_message.emit(
                                f"{yt.title} has been successfully downloaded."
                            )
                            self.downloaded_videos += 1  # Increment downloaded videos
                            self.progress.emit(
                                int(self.downloaded_videos / self.total_videos * 100)
                            )  # Update progress
                        else:
                            self.log_message.emit(
                                f"ERROR: {yt.title} could not be downloaded."
                            )
                    else:
                        self.log_message.emit(
                            f"Temporary files missing for {yt.title}."
                        )
                else:
                    self.log_message.emit(f"No suitable streams found for {yt.title}.")
            else:
                self.log_message.emit("Unsupported file type.")
        except Exception as e:
            self.log_message.emit(f"Error processing {url}: {e}")

    def download_playlist(self, playlist_url):
        try:
            playlist = Playlist(playlist_url)
            for video_url in playlist.video_urls:
                self.download_video(video_url)
        except Exception as e:
            self.log_message.emit(f"Error downloading playlist {playlist_url}: {e}")

    def download_with_retry(
        self,
        stream,
        output_path,
        filename=None,
        rename_to_ext=None,
        max_retries=3,
        delay=5,
    ):
        attempt = 0
        while attempt < max_retries:
            try:
                out_file = stream.download(output_path=output_path, filename=filename)
                if rename_to_ext:
                    base, ext = os.path.splitext(out_file)
                    new_file = Path(f"{base}.{rename_to_ext}")
                    os.rename(out_file, new_file)
                    return str(new_file)
                return out_file
            except Exception as e:
                self.log_message.emit(
                    f"Error downloading {stream.default_filename}: {e}"
                )
                attempt += 1
                if attempt < max_retries:
                    self.log_message.emit(f"Retrying... ({attempt}/{max_retries})")
                    self.sleep(delay)
                else:
                    self.log_message.emit("Max retries reached. Download failed.")
                    return None

    def download_twitter_video(self, url):
        try:
            # Fetch video info from twitsave
            api_url = f"https://twitsave.com/info?url={url}"
            response = requests.get(api_url)
            response.raise_for_status()  # Ensure we got a valid response
            data = bs4.BeautifulSoup(response.text, "html.parser")

            # Find the download button and available quality options
            download_button = data.find_all("div", class_="origin-top-right")[0]
            quality_buttons = download_button.find_all("a")

            if not quality_buttons:
                print(f"No download links found for {url}.")
                return

            # Get the highest quality video URL
            highest_quality_url = quality_buttons[0].get("href")

            # Determine the video file name
            file_name_element = data.find_all("div", class_="leading-tight")[
                0
            ].find_all("p", class_="m-2")

            if not file_name_element:
                print(f"Could not determine video file name for {url}.")
                return

            file_name = file_name_element[0].text.strip()
            file_name = re.sub(r"[^\w\s\-]", "", file_name) + ".mp4"

            download_path = os.path.join(self.output_dir, file_name)

            # Download the video
            with open(download_path, "wb") as file:
                response = requests.get(highest_quality_url, stream=True)
                response.raise_for_status()  # Ensure we got a valid response
                total_size = int(response.headers.get("content-length", 0))
                block_size = 1024
                progress_bar = tqdm(
                    total=total_size, unit="B", unit_scale=True, desc=file_name
                )

                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)

                progress_bar.close()
                print(f"Video downloaded successfully: {file_name}")

                # Increment downloaded videos and update progress
                self.downloaded_videos += 1
                progress_percentage = int(
                    self.downloaded_videos / self.total_videos * 100
                )
                self.progress.emit(progress_percentage)

        except requests.RequestException as e:
            print(f"Failed to fetch video info from {url}: {e}")
        except Exception as e:
            print(f"An error occurred while downloading video from {url}: {e}")


    def get_playlist_video_count(self, playlist_url):
        try:
            playlist = Playlist(playlist_url)
            return len(playlist.video_urls)
        except Exception as e:
            self.log_message.emit(
                f"Error getting playlist video count for {playlist_url}: {e}"
            )
            return 0


class YoutubeDownloader(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Video Downloader")
        self.setGeometry(100, 100, 600, 400)

        icon_path = "images.ico"  # Replace with your icon file path
        self.setWindowIcon(QIcon(icon_path))

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout(widget)
        label = QLabel("Video Downloader", widget)
        layout.addWidget(label)

        # URL Label and QTextEdit for URLs
        self.url_label = QLabel("YouTube or Twitter URLs (one per line):", self)
        self.url_input = QTextEdit(self)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        # Destination Label and LineEdit
        self.dest_label = QLabel("Destination Folder:", self)
        self.dest_input = QLineEdit(self)
        self.dest_input.setReadOnly(False)
        layout.addWidget(self.dest_label)
        layout.addWidget(self.dest_input)

        # Browse Button
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.browse_button)

        # Format Selection
        self.format_label = QLabel("Select Format:", self)
        layout.addWidget(self.format_label)

        self.mp3_radio = QRadioButton("MP3", self)
        self.mp4_radio = QRadioButton("MP4", self)
        self.mp4_radio.setChecked(True)  # Set MP4 as default

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.mp3_radio)
        self.button_group.addButton(self.mp4_radio)

        layout.addWidget(self.mp3_radio)
        layout.addWidget(self.mp4_radio)

        # Download Button
        self.download_button = QPushButton("Download", self)
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        # Progress Bar
        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        # Output Log
        self.output_log = QTextEdit(self)
        self.output_log.setReadOnly(True)
        layout.addWidget(self.output_log)

    def browse_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(
            self, "Select Destination Folder", options=options
        )
        if folder:
            self.dest_input.setText(folder)

    def log_message(self, message):
        self.output_log.append(message)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def start_download(self):
        urls_text = self.url_input.toPlainText()
        urls = urls_text.splitlines()  # Split by lines to get individual URLs
        dest_folder = self.dest_input.text()
        file_type = "mp3" if self.mp3_radio.isChecked() else "mp4"

        # Clear output log before starting new download
        self.output_log.clear()

        if not urls or not dest_folder:
            QMessageBox.warning(
                self,
                "Input Error",
                "Please enter valid YouTube URLs and select a destination folder.",
            )
            return

        self.progress_bar.setValue(0)
        self.thread = QThread()  # Create a QThread
        self.worker = VideoDownloader(
            urls, dest_folder, file_type
        )  # Create a worker object
        self.worker.moveToThread(self.thread)  # Move worker to the thread
        self.thread.started.connect(
            self.worker.run
        )  # Connect thread started signal to worker run method
        self.worker.progress.connect(
            self.update_progress
        )  # Connect worker progress signal to update_progress method
        self.worker.log_message.connect(
            self.log_message
        )  # Connect worker log_message signal to log_message method
        self.worker.finished.connect(
            self.thread.quit
        )  # Connect worker finished signal to thread quit method
        self.worker.finished.connect(
            self.worker.deleteLater
        )  # Ensure worker object gets deleted
        self.thread.finished.connect(
            self.thread.deleteLater
        )  # Ensure thread object gets deleted
        self.thread.start()  # Start the thread


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set application icon
    app_icon_path = "images.ico"
    app.setWindowIcon(QIcon(app_icon_path))

    window = YoutubeDownloader()
    window.show()

    sys.exit(app.exec_())
