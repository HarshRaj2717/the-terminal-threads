import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
from tkinter import filedialog as fd
from encrypt import encrypt
from decrypt import decrypt


"""
Each frame is what we would consider a window. I'm using one 'main' window (MainWindow()) to contain the different frames
Add changes in the class definitons. (Don't edit MainWindow unless u have to!)

"""

cached_images = {}


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
            frame.pack_forget()
            
        #Start off with the HomePage()
        self.show_frame(ImportFrame)

    def show_frame(self, frame_to_show,frame_to_hide = None):
        if frame_to_hide == None:
            frame_to_hide = frame_to_show
        """
        Method that shows a frame by raising it to the top
        """
        frame_to_show = self.frames[frame_to_show]
        frame_to_hide = self.frames[frame_to_hide]
        frame_to_hide.pack_forget()
        # raises the current frame to the top
        frame_to_show.pack(fill='both',expand=True)
        frame_to_show.tkraise()
        
        return None

class ImportFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='red')
        self.pack(side="top", fill="both", expand=True)

        label = tk.Label(self, text="TITLE",font=('Helvetica',36,'bold'))
        label.pack(side=tk.TOP,anchor='n',pady=20,padx=10,fill="x")

        self.secret_filepath = tk.StringVar(self,"Secret Image Filepath")
        self.mask_filepath = tk.StringVar(self,"Mask Image Filepath")
        
        mask_frame = tk.Frame(self,bg='yellow')
        mask_frame.pack(side=tk.LEFT,fill='both',expand=True)

        secret_frame = tk.Frame(self,bg='purple')
        secret_frame.pack(side=tk.LEFT,fill='both',expand=True)

        secret_filepath_entry = tk.Entry(secret_frame,width=50,textvariable=self.secret_filepath)
        secret_filepath_entry.pack(side=tk.TOP,anchor='n',padx=10,pady=10)

        secret_file_button = tk.Button(secret_frame,text="OPEN",command=lambda: self.open_file(self.secret_filepath,self.secretImage,"secret_image"))
        secret_file_button.pack(side=tk.TOP,anchor='n',padx=5,pady=10)

        mask_filepath_entry = tk.Entry(mask_frame,width=50,textvariable=self.mask_filepath)
        mask_filepath_entry.pack(side=tk.TOP,anchor='n',padx=10,pady=10)

        mask_file_button = tk.Button(mask_frame,text="OPEN",command=lambda: self.open_file(self.mask_filepath,self.maskImage,"mask_image"))
        mask_file_button.pack(side=tk.TOP,anchor='n',padx=5,pady=10)

        self.secretImage = tk.Label(secret_frame,bg="green")
        self.secretImage.pack(side=tk.TOP,anchor='w',fill='both')

        self.maskImage = tk.Label(mask_frame,bg='blue')
        self.maskImage.pack(side=tk.TOP,anchor='e',fill="both")


         # We use the switch_window_button in order to call the show_frame() method as a lambda function
        switch_window_button = tk.Button(
            self,
            text="Go to Encrypt Frame",
            command=lambda: self.switch_to_encrypt_frame(controller),
        )
        switch_window_button.pack(before=mask_frame,side="bottom",anchor='s',fill='y',pady=10)

    def switch_to_encrypt_frame(self,controller):
        controller.show_frame(EncryptFrame,ImportFrame)
        

    def open_file(self,filepath_to_update,img_to_update,label):
        allowed_filetypes = [("Images","*.png"),("Videos","*.mp4")]
        imgfile = fd.askopenfile()
        filepath_to_update.set(imgfile.name)
        path = filepath_to_update.get()
        cached_images[label]= ImageTk.PhotoImage(image=Image.open(path))
        img_to_update.config(image=cached_images[label],height=200,width=200)
        

class EncryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,bg='red')
        self.pack(side="top", fill="both", expand=True)

        label = tk.Label(self, text="ENCRYPT FRAME",font=('Helvetica',36,'bold'))
        label.pack(side=tk.TOP,anchor='n',pady=20,padx=10,fill="x")
        

        steg_frame = tk.Frame(self,bg='grey')
        steg_frame.pack(side=tk.RIGHT,fill='both',expand=True)

        img_frame = tk.Frame(self,bg='yellow')
        img_frame.pack(side=tk.LEFT,fill='both',expand=True)

        mask_file_button = tk.Button(img_frame,text="OPEN",command=lambda: self.load_and_encrypt())
        mask_file_button.pack(side=tk.TOP,anchor='n',padx=5,pady=10)

        self.secretImage = tk.Label(img_frame,bg="green")
        self.secretImage.pack(side=tk.TOP,anchor='w',fill='both')

        self.maskImage = tk.Label(img_frame,bg='blue')
        self.maskImage.pack(side=tk.TOP,anchor='e',fill="both")

        self.imgs = {}

    def load_and_encrypt(self):
        self.maskImage.config(image=cached_images["mask_image"])
        self.secretImage.config(image=cached_images["secret_image"])
        encrypt.encrypt_frame()



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
