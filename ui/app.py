import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog as fd
"""
Each frame is what we would consider a window. I'm using one 'main' window (MainWindow()) to contain the different frames
Add changes in the class definitons. (Don't edit MainWindow unless u have to!)

"""



class MainWindow(tk.Tk):
    
    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs) 
        self.wm_title("Video Encrypter/Decrypter v1")

        root = tk.Frame(self, height=400, width=600,bg='blue')
        root.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (ImportFrame, EncryptFrame, DecryptFrame):
            frame = F(root, self)
            self.frames[F] = frame

            
        #Start off with the HomePage()
        self.show_frame(ImportFrame)

    def show_frame(self, frame_to_show):
        """
        Method that shows a frame by raising it to the top
        """
        frame = self.frames[frame_to_show]
        # raises the current frame to the top
        frame.tkraise()
        return None

class ImportFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='red')
        self.pack(side="top", fill="both", expand=True)

        label = tk.Label(self, text="TITLE",font=('Helvetica',36,'bold'))
        label.pack(side=tk.TOP,pady=20,padx=10,fill="x")

        self.secret_filepath = tk.StringVar("Secret Image Filepath")
        self.mask_filepath = tk.StringVar("Mask Image Filepath")

        self.secret_filepath_enty = tk.Entry(self,width=50,textvariable=self.secret_filepath)
        self.secret_filepath_enty.pack(side=tk.LEFT,anchor='nw',padx=10,pady=10)

        self.mask_filepath_enty = tk.Entry(self,width=50,textvariable=self.secret_filepath)
        self.mask_filepath_enty.pack(side=tk.LEFT,anchor='nw',padx=10,pady=10)

        openFileButton = tk.Button(self,text="OPEN",command=lambda: self.open_file(self.secret_filepath,self.secretImage))
        openFileButton.pack(side=tk.LEFT,anchor='nw',padx=5,pady=10)

        

        self.secretImage = tk.Label(self,bg="green")
        self.secretImage.pack(side = "bottom", fill = "both", expand = "yes")

        self.maskImage = tk.Label(self)
        self.maskImage.pack(side = "bottom", fill = "both", expand = "yes")

        

         # We use the switch_window_button in order to call the show_frame() method as a lambda function
        switch_window_button = tk.Button(
            self,
            text="Go to the Side Page",
            command=lambda: controller.show_frame(EncryptFrame),
        )
    def open_file(self,filepath_to_update,img_to_update):
        allowed_filetypes = [("Images","*.png"),("Videos","*.mp4")]
        imgfile = fd.askopenfile()
        filepath_to_update.set(imgfile.name)
        path = filepath_to_update.get()
        self.img = ImageTk.PhotoImage(image=Image.open(path))
        img_to_update.config(image=self.img)
        
        
    

    
    
       

class EncryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="This is the Side Page")
        label.pack(padx=10, pady=10)

        switch_window_button = tk.Button(
            self,
            text="Go to the Completion Screen",
            command=lambda: controller.show_frame(DecryptFrame),
        )
        switch_window_button.pack(side="bottom", fill=tk.X)


class DecryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Screen, we did it!")
        label.pack(padx=10, pady=10)
        switch_window_button = ttk.Button(
            self, text="Return to menu", command=lambda: controller.show_frame(ImportFrame)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)

if __name__ == "__main__":
    testObj = MainWindow()
    testObj.geometry("800x450")
    testObj.mainloop()
