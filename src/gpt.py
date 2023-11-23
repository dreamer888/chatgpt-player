import sys
import os
from os import path

import tkinter as tk
from tkinter import filedialog, ttk
import pyttsx3
import threading
from PIL import Image, ImageTk
import cv2

import vlc
import platform

from openai import OpenAI

from pathlib import Path
import pygame
from threading import Thread
import time 

#pip3 install opencv-python
#pip3  pyinstaller
#pyinstaller  gtp.py  生成exe文件   #打包成 exe文件

'''
Author ：75039960@qq.com,  18665802636
'''



class ChatGPTApp:
    def __init__(self, root,inputTextBox):
        self.root = root
        self.root.title("ChatGPT多媒体应用")

        '''
        setx设置永久用户环境变量
        setx OPENAI_API_KEY "sk-xxx"
        setx加上/m参数表示设置的是系统的环境变量
        setx env_name env_value /m
 
        #openai.api_key = os.getenv("OPENAI_API_KEY")
        #openai.api_key = 'xxx'
        #self.client = OpenAI(api_key="sk-Ckxxx",)
        '''  
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),)
        print(self.client.models.list())
        #self.client = OpenAI(api_key="sk-",)
	 
        # 创建用户输入框
        self.user_input_box =inputTextBox
        
    def send_message(self):
      
        show_InputText(True)
        self.user_input = self.user_input_box.get("1.0", "end-1c").replace("\n"," ")

        def  thread_function():
            def  thread_function_animate():
                update_subtitle(animate_canvas,chatgpt_response)
            chatgpt_response = self.get_chatgpt_response(self.user_input)
                 
            threading.Thread(target=thread_function_animate, daemon=True).start()
            #update_subtitle(animate_canvas,chatgpt_response)
            self.text2Speech(chatgpt_response)

        if self.user_input:   
            threading.Thread(target=thread_function, daemon=True).start()      
           
    def get_chatgpt_response(self, user_input):
        try:

            response = self.client.chat.completions.create(
                #model="gpt-3.5-turbo",
                model="gpt-4-turbo",
                messages=[
                    #{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                    #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                    #{"role": "user", "content": "Where was it played?"}
                ]
                )
            '''
            #下面的调用模式已经被放弃
            response = OpenAI.Completion.create(
              engine="text-davinci-003",
              prompt=self.user_input,
              max_tokens=1500
            )
            '''

            print("resp1="+response.choices[0].message.content)   
            #return response.choices[0].text.strip()
            return response.choices[0].message.content.strip()
        except Exception as e:
            return "出现错误: " + str(e)


    def text2Speech(self,textInput):
            response = self.client.audio.speech.create(   
            model = "tts-1", 
            voice = "alloy",  
            input=textInput
            )
    
            outfile =  "temp.mp3"

            if path.exists(outfile):
                os.remove(outfile)

            response.stream_to_file(outfile)   
            self.start_play_mp3(outfile)

    def start_play_mp3(self,file_path):
        """ 开始播放动画文字 """
        thread = Thread(target=self.play_mp3,args=(file_path, 1))
        thread.start()

    def play_mp3(self,file_path,nouse):
        # 初始化pygame
        pygame.mixer.init()

        # 加载音频文件   
        pygame.mixer.music.load(file_path)
        # 播放音频
        pygame.mixer.music.play()

        # 等待播放完成
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(5)
        pygame.mixer.music.unload()


#修改下面的代码，让视频可以自动适应容器self.canvas 的大小， 并且填满360x360的屏幕， 其它功能不需要修改
class VlcVideoPlayer:

    def __init__(self, root):
        self.root = root

        self.vlc_instance = vlc.Instance()
        self.player = self.vlc_instance.media_player_new()

        self.canvas = tk.Canvas(self.root, width=360, height=(360*4/5))

        self.canvas.grid(row=6, column=0, columnspan=2, sticky="ew")
        


        self.root.bind("<Configure>", self.on_resize)  ###

        #self.canvas.pack()

        self.playvideo  = self.canvas

        self.playvideo.grid(row=6, column=0,sticky="ew")

 

        # 默认隐藏视频播放组件
        #self.playvideo.grid_remove()
        #self.root.update()

        if platform.system() == "Windows":
            self.player.set_hwnd(self.canvas.winfo_id())
        else:
            self.player.set_xwindow(self.canvas.winfo_id())

    def on_resize(self, event):
        # 获取 Canvas 的当前大小
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # 更新 VLC 播放器的视窗大小
        if platform.system() == 'Windows':
            self.player.set_hwnd(self.canvas.winfo_id())
        else:
            self.player.set_xwindow(self.canvas.winfo_id())

        # 重新调整视频播放器的视窗大小
        self.player.video_set_scale(0)  # 自动缩放
        self.player.video_set_aspect_ratio(f"{width}:{height}")

    def open_video(self):
        video_path = filedialog.askopenfilename(title="Select a Video File", 
                                                filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
        if video_path:
            media = self.vlc_instance.media_new(video_path)
            self.player.set_media(media)
            self.player.play()

        self.playvideo.grid()
        picture_player.image_label.grid_remove()
        show_InputText(False)

    def stop_video(self):
        
        if self.player:
            self.player.stop()      
 


class VideoPlayer:
    def __init__(self, root):
        self.root = root
     
        #self.pack()
        self.create_widgets()

    def create_widgets(self):
    
        # 视频播放组件
        #self.playvideo = tk.Label(self.root)
        #self.playvideo.grid(row=6, column=0, columnspan=2, sticky="ew")
        #self.videoFilePath =None
        self.video_source = ""
        self.upload_video_button = tk.Button(self.root, text="视频", command=self.upload_and_play)
        self.upload_video_button.grid(row=1, column=1, sticky="ew")


        self.canvas = tk.Canvas(self.root, width=screen_width, height=300)

        self.canvas.grid(row=6, column=0, columnspan=2, sticky="ew")

        #self.canvas.pack()

        self.playvideo  = self.canvas

        self.playvideo.grid(row=6, column=0,sticky="ew")

        # 默认隐藏视频播放组件
        self.playvideo.grid_remove()

        self.delay = 15   # ms
        self.playing = False
        self.vid = None

    def upload_and_play(self):
        # 停止当前播放的视频
        self.stop_video()

        self.playvideo.grid()
        picture_player.image_label.grid_remove()

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
                frame = cv2.resize(frame, (self.canvas.winfo_width(),self.canvas.winfo_height()))
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.playvideo.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.root.after(self.delay, self.update_video)
        else:
            if self.vid:
                self.vid.release()

    def stop_video(self):
        self.playing = False
        if self.vid:
            self.vid.release()
            self.vid = None
        #thread.join() 相当于 thread.join(None)，表示无限期等待。


class PicturePlayer:
    def __init__(self, root):
        self.root = root
        self.image_label = tk.Label(root)
        #self.image_label.grid(row=6, column=0, columnspan=2, sticky="nsew")
        self.image_label.grid(row=6, column=0, columnspan=2, sticky="ew")

        self.images = []
        self.current_image = 0

    def add_images(self):

        #类成员里面是可以直接调用全局变量的
        videoPlayer.stop_video()
        videoPlayer.playvideo.grid_remove()
        #self.root.videoPlayer.grid_remove()

        show_InputText(False)

        self.image_label.grid()

        filepaths = filedialog.askopenfilenames(title="选择图片", filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")])
        self.images.extend(filepaths)
        if not self.images:
            return
        self.show_image()

    def show_image(self):
        if not self.images:
            return
        image_path = self.images[self.current_image]
        img = Image.open(image_path)
        #img = img.resize((360, 200), Image.Resampling.LANCZOS)  # 调整图片大小以适应标签
        img = img.resize((screen_width, 300), Image.Resampling.LANCZOS)  # 调整图片大小以适应标签 #root.winfo_width()


        img = ImageTk.PhotoImage(img)
         
        self.image_label.config(image=img)
        self.image_label.image = img  # 避免图片被垃圾回收
        self.current_image = (self.current_image + 1) % len(self.images)
        self.root.after(5000, self.show_image)  # 每3秒更换一次图片

def play_text_with_pyttsx3(text, voice_id, rate):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def type_writer_effect(widget, text, delay=100):
    widget.config(state='normal')
    widget.delete('1.0', tk.END)
    for char in text:
        widget.insert(tk.END, char)
        widget.update()
        widget.after(delay)
    widget.config(state='disabled')



def update_subtitle(animate_canvas,full_text):

    def scroll_text(x):
        animate_canvas.move("subtitle", -2, 0)
        x -= 2
        if x + animate_canvas.bbox(text_id)[2] > -100:  # 增加额外的滚动距离
            animate_canvas.after(25, scroll_text, x)
        else:
            animate_canvas.delete(text_id)  # 删除文本，确保没有残留
                
    x = animate_canvas.winfo_width()
    text_id = animate_canvas.create_text(x, 20, text=full_text, tags="subtitle", font=("Helvetica", 16), fill="white", anchor="w")
    scroll_text(x)


def play_text_and_animate(text, voice_id, rate, delay):
    def thread_function():
        play_text_with_pyttsx3(text, voice_id, rate)

    show_InputText(True)
    threading.Thread(target=thread_function, daemon=True).start()
    #type_writer_effect(animate, text, delay)
    update_subtitle(animate_canvas,text)
    #threading.Thread(target=update_subtitle, args={animate_canvas,text},daemon=True).start()



def play_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            full_text = "    ".join(line.strip() for line in file)
      
        def thread_function():
            play_text_with_pyttsx3(full_text, voice_selector.current(), int(voice_speed.get()))
        def scroll_text(x):
            animate_canvas.move("subtitle", -2, 0)
            x -= 2
            if x + animate_canvas.bbox(text_id)[2] > -100:  # 增加额外的滚动距离
                animate_canvas.after(25, scroll_text, x)
            else:
                animate_canvas.delete(text_id)  # 删除文本，确保没有残留

        x = animate_canvas.winfo_width()
        text_id = animate_canvas.create_text(x, 20, text=full_text, tags="subtitle", font=("Helvetica", 16), fill="white", anchor="w")
        scroll_text(x)

        #play_text_and_animate(text, voice_id, rate, delay)
        #args={full_text, voice_selector.current(), int(voice_speed.get())}
        #threading.Thread(target=play_text_with_pyttsx3, args=args,daemon=True).start() 
        threading.Thread(target=thread_function, daemon=True).start() 
        #args2={animate_canvas, full_text}
        #threading.Thread(target=update_subtitle, args=args2,daemon=True).start()
  
    def play_file_subtitle():
        with open(self.filename, "r", encoding="utf-8") as file:
            full_text = "    ".join(line.strip() for line in file)

        x = self.animate_canvas.winfo_width()
        text_id = self.animate_canvas.create_text(x, 20, text=full_text, tags="subtitle", font=("Helvetica", 16), fill="white", anchor="w")

        def scroll_text(x):
            self.animate_canvas.move("subtitle", -2, 0)
            x -= 2
            if x + self.animate_canvas.bbox(text_id)[2] > -100:  # 增加额外的滚动距离
                self.animate_canvas.after(25, scroll_text, x)
            else:
                self.animate_canvas.delete(text_id)  # 删除文本，确保没有残留

        scroll_text(x)


def change_background():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        image = Image.open(file_path)
        image = image.resize((360, 600), Image.Resampling.LANCZOS)
        bg_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=bg_image, anchor='nw')
        canvas.image = bg_image


def show_InputText(flag=True):
    if  flag :
        inputText.grid()
        picture_player.image_label.grid_remove()
        videoPlayer.playvideo.grid_remove()
    else: 
        inputText.grid_remove()


########################main################################################


screen_width=400
screen_height=640
geometry = "400x640"
root = tk.Tk()
root.title("CHAT-GPT对话生成应用程序")
root.geometry(geometry)

canvas = tk.Canvas(root, width=screen_width, height=screen_height)
canvas.grid(row=0, column=0, rowspan=11, columnspan=2, sticky="nsew")



background = tk.Button(root, text="切换风格", command=change_background)
background.grid(row=1, column=0, columnspan=1,sticky="ew")


# 创建图片播放器实例
picture_player = PicturePlayer(root)


# 上传视频按钮
#upload_video_button = tk.Button(root, text="视频", command=upload_video)
#upload_video_button.grid(row=1, column=1, sticky="ew")
 
# 创建video播放器实例
#videoPlayer = VideoPlayer(root)

videoPlayer = VlcVideoPlayer(root)


#上传视频按钮
upload_video_button = tk.Button(root, text="视频", command=videoPlayer.open_video)
upload_video_button.grid(row=1, column=1, sticky="ew")



# 添加按钮来选择图片
add_pictures_button = tk.Button(root, text="图片轮播", command=picture_player.add_images)
add_pictures_button.grid(row=2, column=0,columnspan=1,sticky="ew")

# 添加按钮来选择图片


voice_selector = ttk.Combobox(root, values=["Voice 1", "Voice 2", "Voice 3"])
voice_selector.grid(row=3, column=0, sticky="ew")
voice_selector.current(0)  # 设置默认选项为列表中的第一个

animationStyle = ttk.Combobox(root, values=["Style 1", "Style 2", "Style 3"])
animationStyle.grid(row=3, column=1, sticky="ew")
animationStyle.current(0)  # 设置默认选项为列表中的第一个


playFromText = tk.Button(root, text="从编辑框播放", command=lambda: play_text_and_animate(inputText.get("1.0", "end").replace("\n"," "), voice_selector.current(), int(voice_speed.get()), int(200 - animate_speed.get())))
playFromText.grid(row=4, column=0, sticky="ew")

playFromFile = tk.Button(root, text="从文件播放", command=play_from_file)
playFromFile.grid(row=4, column=1, sticky="ew")


voice_speed = tk.Scale(root, from_=50, to=200, orient="horizontal", label="语音速度")
voice_speed.grid(row=5, column=0, columnspan=1, sticky="ew")
voice_speed.set(148)  # 设置默认 速度为148

animate_speed = tk.Scale(root, from_=50, to=150, orient="horizontal", label="动画速度")
animate_speed.grid(row=5, column=1, columnspan=1, sticky="ew")
animate_speed.set(58)  # 设置默认动画速度为58

#animate = tk.Text(root, height=5, state='disabled', wrap='word',bg='black',fg='white',font=('楷体',12,'bold'))

inputText = tk.Text(root, height=6, width=1 ,font=("Arial", 9)) #text="输入文字，然后点击从编辑框播放，就可以转化为语音了~~~")
inputText.grid(row=6, column=0, columnspan=2, sticky="ew")
inputText.grid_remove()


chatGptApp= ChatGPTApp(root,inputText)

chat_button = tk.Button(root, text="GPT对话",command=chatGptApp.send_message)
chat_button.grid(row=2, column=1,columnspan=1,sticky="ew")


animate_canvas = tk.Canvas(root, bg="black", height=50,width =100)
animate_canvas.grid(row=7, column=0, columnspan=2, sticky="ew")



root.mainloop()
