import os
import random
import sys
import threading
import tkinter
import tkinter.ttk as ttk

import tkmacosx
import ttkthemes
from mttkinter import mtTkinter
from PIL import Image, ImageTk


def get_5_most_common_color(image):
    """Get the 5 most common color in a PIL image"""
    # https://stackoverflow.com/a/431112/1149779
    width, height = image.size
    pixels = image.getcolors(width * height)
    most_common_colors = sorted(pixels, key=lambda t: t[0], reverse=True)
    return [pixel[1] for pixel in most_common_colors][:5]
    
def colortuple_to_hex(color):
    # Convert a color tuple to hex
    # https://stackoverflow.com/a/214657/1149779
    return '#%02x%02x%02x' % color

def is_color_dark(color):
    # Check if a color is dark
    # https://stackoverflow.com/a/3943023/1149779
    if type(color) == str and color.startswith("#"):
        # unpack RGB from hex color
        color = tuple(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    return sum(color) < 382

class SplashScreen(ttkthemes.ThemedTk, mtTkinter.Toplevel):
    def __init__(self, splash_img, most_common_color_idx=0, theme=None, *args, **kwargs):
        super(SplashScreen, self).__init__(theme=theme, *args, **kwargs)
        splash_img.thumbnail((600, 400))
        self.wm_attributes("-topmost", True)

        if sys.platform == "darwin":
            self.wm_attributes("-transparent", True)
            self.wm_attributes("-notify", True)
            self.wm_attributes("-fullscreen", False)
        elif sys.platform in ["win32", "cygwin"]:
            self.wm_attributes("-toolwindow", True)
            
        
        # Set the image
        self._gui_image_container = tkinter.Label(self)
        self._gui_image_container.image = ImageTk.PhotoImage(splash_img)
        self._gui_image_container.configure(image=self._gui_image_container.image)
        self._gui_image_container.pack(side='top', fill="both", expand="yes")
        self.geometry(f"{splash_img.width}x{splash_img.height+30}")

        # loading info label
        self._loading_label = tkinter.Label(self, text="")
        self._loading_label.config(font=("Helvetica", 20, "bold"), 
                                   fg=is_color_dark(get_5_most_common_color(splash_img)[most_common_color_idx]) and 'white' or 'black',
                                   bg=colortuple_to_hex(get_5_most_common_color(splash_img)[most_common_color_idx]), 
                                      borderwidth=0
                                   )
        self._loading_label.pack(fill="x", expand="yes")
        # loading bar 
        self.loading_bar = ttk.Progressbar(self, orient='horizontal', length=600, mode="indeterminate")
        self.loading_bar.pack(side='bottom', fill="x", expand="yes")
        self.loading_bar.start()
        # Set sizing constraints
        self.geometry(f"{splash_img.width}x{splash_img.height+(sys.platform in ['win32', 'cygwin'] and 50 or 40)}")
        self.resizable(False, False)
        # Put the window on the center of the screen
        self.eval('tk::PlaceWindow . center')
        
    @property
    def loading_status(self):
        return self._loading_label['text']
    
    @loading_status.setter
    def loading_status(self, value):
        self._loading_label['text'] = value
    
    def destroy(self):
        self.loading_bar.stop()
        return super(SplashScreen, self).destroy()

    def __delattr__(self, __name: str) -> None:
        return super().__delattr__(__name)
    
if __name__ == '__main__':
    splash_img = Image.open("./splashscreen.png")
    print(get_5_most_common_color(splash_img))
    
    splashscreen = SplashScreen(splash_img, most_common_color_idx=random.randint(0, 4))

    def after_few_seconds():
        import time
        for i in range(10):
            time.sleep(1)
            print(f"Loading... {i}")
            splashscreen.loading_status = f"Loading... {i}"
    threading.Thread(target=after_few_seconds).start()
    splashscreen.mainloop()
  