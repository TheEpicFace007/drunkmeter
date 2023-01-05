import random
import sys
import tkinter

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

class SplashScreen(tkinter.Toplevel):
    def __init__(self, splash_img, root, theme=None, *args, **kwargs):
        super(SplashScreen, self).__init__(root, *args, **kwargs)
        root.withdraw()
        splash_img.thumbnail((600, 400))

        self.wm_attributes("-topmost", True)
        if sys.platform == "darwin":
            self.wm_attributes("-transparent", True)
            self.wm_attributes("-notify", True)
            self.wm_attributes("-fullscreen", False)
        elif sys.platform in ["win32", "cygwin"]:
            self.wm_attributes("-toolwindow", True)
        
        # Set the image
        self.splash_img = splash_img
        self.splash_img = ImageTk.PhotoImage(self.splash_img)
        self._gui_image_container = tkinter.Label(self, image=self.splash_img)
        self._gui_image_container.config(image=self.splash_img)
        
        self._gui_image_container.pack(fill="both", expand="yes")
        self.geometry(f"{splash_img.width}x{splash_img.height}")

        # Set sizing constraints
        self.geometry(f"{splash_img.width}x{splash_img.height}")
        self.resizable(False, False)
        # Put the window on the center of the screen
        self.update_idletasks()
        self.geometry(f"+{int(self.winfo_screenwidth()/2 - self.winfo_width()/2)}+{int(self.winfo_screenheight()/2 - self.winfo_height()/2)}")
        # Set the icon as icon.png
        root.iconphoto(True, tkinter.PhotoImage(file="./icon.png"))
        
if __name__ == '__main__':
    splash_img = Image.open("./splashscreen.png")
    splashscreen = SplashScreen(splash_img, None, most_common_color_idx=random.randint(0, 4))
    splashscreen.mainloop()