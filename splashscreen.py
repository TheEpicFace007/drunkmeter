import random
import sys
import tkinter

from PIL import Image, ImageTk

import autoupdate

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
        
        # Set the progress text
        self._gui_progress_text = tkinter.StringVar()
        self._gui_progress_text.set("Loading...")
        self._gui_progress_label = tkinter.Label(self, textvariable=self._gui_progress_text, bg="#f7cd00", fg="black")
        self._gui_progress_label.pack(fill="x", expand="yes", side="bottom")
        
        # Put the window on the center of the screen
        self.update_idletasks()
        self.geometry(f"+{int(self.winfo_screenwidth()/2 - self.winfo_width()/2)}+{int(self.winfo_screenheight()/2 - self.winfo_height()/2)}")

        # Set sizing constraints
        self.geometry(f"{splash_img.width}x{splash_img.height+30}")
        self.resizable(False, False)
        
        # Bind events
        self.bind("<<UpdateProgress>>", self.update_progress)
        
        self._root = root
    
    def hide_root(self, hide=True):
        """Toggle the root window, this is useful for hiding the root window while the splashscreen is active"""
        if hide:
            self._root.withdraw()
        else:
            self._root.deiconify()
            self._root.update()
    
    def update_progress(self, status):
        print(status)
        self.gui_progress_text.set(status)
        self.update_idletasks()
    
    @property
    def gui_progress_text(self):
        return self._gui_progress_text.get()
    @gui_progress_text.setter
    def gui_progress_text(self, value):
        self._gui_progress_text.set(value)
    @gui_progress_text.deleter
    def gui_progress_text(self):
        del self._gui_progress_text

if __name__ == '__main__':
    tk = tkinter.Tk()
    splash_img = Image.open("./splashscreen.png")
    splashscreen = SplashScreen(splash_img, tk)
    splashscreen.after(100, lambda: autoupdate.updateAllFiles(splashscreen))
    tk.mainloop()