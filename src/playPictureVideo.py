import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

class VideoPlayer:
    def __init__(self, root, root_title):
        self.root = root
        self.root.title(root_title)

        self.video_source = ""

        self.canvas = tk.Canvas(root, width=600, height=400)
        self.canvas.pack()

        self.btn_upload_play = tk.Button(root, text="上传视频", width=15, command=self.upload_and_play)
        self.btn_upload_play.pack(anchor=tk.CENTER, expand=True)

        self.btn_stop = tk.Button(root, text="停止", width=15, command=self.stop_video)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True)

        self.delay = 15   # ms
        self.playing = False
        self.vid = None

        self.root.mainloop()

    def upload_and_play(self):
        # 停止当前播放的视频
        self.stop_video()

        # 上传新视频
        self.video_source = filedialog.askopenfilename(title="选择视频文件", filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
        if self.video_source:
            self.playing = True
            self.vid = cv2.VideoCapture(self.video_source)
            self.update_video()

    def update_video(self):
        if self.playing:
            ret, frame = self.vid.read()
            if ret:
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.root.after(self.delay, self.update_video)
        else:
            if self.vid:
                self.vid.release()

    def stop_video(self):
        self.playing = False
        if self.vid:
            self.vid.release()
            self.vid = None

# Create a root window and pass it to the VideoPlayer object
root = tk.Tk()
VideoPlayer(root, "Python Video Player")
