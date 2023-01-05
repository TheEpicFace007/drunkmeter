import random
import sys
import tkinter

from PIL import Image, ImageTk

class SplashScreen(tkinter.Toplevel):
    def __init__(self, splash_img, root, *args, **kwargs):
        super(SplashScreen, self).__init__(root, *args, **kwargs)
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
        
        # Put the window on the center of the screen
        self.update_idletasks()
        self.geometry(f"+{int(self.winfo_screenwidth()/2 - self.winfo_width()/2)}+{int(self.winfo_screenheight()/2 - self.winfo_height()/2)}")

        # Set sizing constraints
        self.geometry(f"{splash_img.width}x{splash_img.height}")
        self.resizable(False, False)
        
        
    
    def toggle_root(self, hide=True):
        if hide:
            self.root.withdraw()
        else:
            self.root.deiconify()
            self.root.update()
            
        

        
if __name__ == '__main__':
    splash_img = Image.open("./splashscreen.png")
    splashscreen = SplashScreen(splash_img, tkinter.Tk())
    splashscreen.mainloop()