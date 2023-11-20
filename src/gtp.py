import tkinter as tk
from tkinter import filedialog, ttk
import threading
import time
from gtts import gTTS
import os
from pygame import mixer
from PIL import Image, ImageTk


class ChatGPTApp:
    def __init__(self, root,inputTextBox):
        self.root = root
        self.root.title("ChatGPT多媒体应用")

        '''
        setx设置永久用户环境变量

        setx env_name env_value
        setx加上/m参数表示设置的是系统的环境变量
        setx env_name env_value /m

        
        #openai.api_key = os.getenv("OPENAI_API_KEY")

        #openai.api_key = 'xxx'

        #self.client = OpenAI(api_key="sk-Ckxxx",)

        '''
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),)
	 

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
                model="gpt-3.5-turbo",
                messages=[
                    #{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input},
                    #{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
                    #{"role": "user", "content": "Where was it played?"}
                ]
                )
            '''
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
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[voice_id].id)
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def play_audio(file):
    mixer.init()
    mixer.music.load(file)
    mixer.music.play()

def type_writer_effect(widget, text, delay=100, style='Typewriter'):
    widget.delete('1.0', tk.END)
    if style == 'Typewriter':
        for char in text:
            widget.insert(tk.END, char)
            widget.update()
            time.sleep(delay / 1000.0)
    elif style == 'FadeIn':
        # 实现淡入效果的代码
        pass
    # 可以添加更多的动画风格

def play_text_and_animate(text, voice_id, rate, style):
    def thread_function():
        play_text_with_pyttsx3(text, voice_id, rate)
        type_writer_effect(animate, text, delay=int(300 - animate_speed.get()), style=style)

    threading.Thread(target=thread_function, daemon=True).start()

def upload_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        image = image.resize((360, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(window, image=photo)
        label.image = photo
        label.place(x=0, y=0, relwidth=1, relheight=1)

def play_from_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
            play_text_and_animate(text, voice_selector.current(), int(voice_speed.get()), animationStyle.get())

window = tk.Tk()
window.title("通过CHAT GPT对话生成应用程序")
window.geometry("360x500")

inputText = tk.Text(window, height=3, font=("Arial", 9))
inputText.grid(row=0, column=0, columnspan=2, sticky='ew')

playFromText = tk.Button(window, text="从编辑框播放", command=lambda: play_text_and_animate(inputText.get("1.0", "end-1c"), voice_selector.current(), int(voice_speed.get()), animationStyle.get()))
playFromText.grid(row=1, column=0, sticky='ew')

playFromFile = tk.Button(window, text="从文件播放", command=play_from_file)
playFromFile.grid(row=1, column=1, sticky='ew')

background = tk.Button(window, text="切换背景", command=upload_image)
background.grid(row=2, column=0, sticky='ew')

animationStyle = ttk.Combobox(window, values=['Typewriter', 'FadeIn'])
animationStyle.current(0)
animationStyle.grid(row=2, column=1, sticky='ew')

voice_speed = tk.Scale(window, from_=50, to=200, orient='horizontal')
voice_speed.grid(row=3, column=0, columnspan=2, sticky='ew')

animate_speed = tk.Scale(window, from_=0, to=300, orient='horizontal')
animate_speed.grid(row=4, column=0, columnspan=2, sticky='ew')

animate = tk.Text(window, height=5, font=("Arial", 16))
animate.grid(row=5, column=0, columnspan=2, sticky='ew')

voice_selector = ttk.Combobox(window, values=["Male", "Female"])
voice_selector.current(0)
voice_selector.grid(row=6, column=0, columnspan=2, sticky='ew')

window.mainloop()
