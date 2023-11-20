import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCarousel:
    def __init__(self, root):
        self.root = root
        self.image_label = tk.Label(root)
        self.image_label.pack(fill="both", expand=True)
        self.images = []
        self.current_image_index = 0

        self.load_images_button = tk.Button(root, text="上传图片", command=self.load_images)
        self.load_images_button.pack(side="bottom")

    def load_images(self):
        filepaths = filedialog.askopenfilenames(title="选择图片", filetypes=[("图片文件", "*.png;*.jpg;*.jpeg;*.bmp")])
        self.images = [Image.open(filepath) for filepath in filepaths]
        if self.images:
            self.show_image()

    def show_image(self):
        if not self.images:
            return
        image = self.images[self.current_image_index]
        #image = image.resize((360, 550), Image.ANTIALIAS) 
        image = image.resize((360, 550), Image.Resampling.LANCZOS) 

        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo
        self.current_image_index = (self.current_image_index + 1) % len(self.images)
        self.root.after(3000, self.show_image)  # 3秒后显示下一张图片

root = tk.Tk()
root.title("图片轮播")
root.geometry("360x600")

carousel = ImageCarousel(root)

root.mainloop()
