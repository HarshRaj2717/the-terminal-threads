import tkinter as tk
from PIL import ImageTk, Image
import cv2
from tkinter import ttk
from tkinter import filedialog as fd
from image_handler.image_handler import ImageHandler
from vid_handler.frame_extraction import VideoMerger



"""
Each frame is what we would consider a window. I'm using one 'main' window (MainWindow()) to contain the different frames
Add changes in the class definitons. (Don't edit MainWindow unless u have to!)

"""

cached_files = {}
cached_filepaths = {}
imageorvideo = ""


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Video Encrypter/Decrypter v1")

        root = tk.Frame(self, height=450, width=800, bg='blue')
        root.pack(side="top", fill="both", expand=True)

        self.frames = {}
        for F in (ImportFrame, EncryptFrame,DecryptFrame):
            frame = F(root, self)
            self.frames[F] = frame
            frame.pack_forget()

        # Start off with the HomePage()
        self.show_frame(ImportFrame)

    def show_frame(self, frame_to_show, frame_to_hide=None):
        if frame_to_hide == None:
            frame_to_hide = frame_to_show
        """
        Method that shows a frame by raising it to the top
        """
        frame_to_show = self.frames[frame_to_show]
        frame_to_hide = self.frames[frame_to_hide]
        frame_to_hide.pack_forget()
        # raises the current frame to the top
        frame_to_show.pack(fill='both', expand=True)
        frame_to_show.tkraise()

        return None


class ImportFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='red')
        self.pack(side="top", fill="both", expand=True)

        title = tk.Label(self, text="TITLE", font=('Helvetica', 16, 'bold'))
        title.pack(side=tk.TOP, anchor='n', pady=10, padx=10, fill="x")

        self.secret_filepath = tk.StringVar(self)
        self.mask_filepath = tk.StringVar(self)
        self.open_file_img = ImageTk.PhotoImage(image=Image.open("ui/assets/open_folder.png").resize((14,14)))

        mask_frame = tk.Frame(self, bg='yellow')
        mask_frame.pack(side=tk.LEFT, fill='both', expand=True)

        secret_frame = tk.Frame(self, bg='purple')
        secret_frame.pack(side=tk.LEFT, fill='both', expand=True)

        secret_filepath_entry = tk.Entry(secret_frame, width=30,textvariable=self.secret_filepath)
        secret_filepath_entry.grid(column=1,row=0,padx=0,pady=5,sticky='E')

        secret_filepath_lbl = tk.Label(secret_frame,text="Secret Image Filepath: ")
        secret_filepath_lbl.grid(column=0,row=0,padx=5,pady=5)

        secret_file_btn = tk.Button(secret_frame, image=self.open_file_img, command=lambda: self.open_file(
        self.secret_filepath, self.secretImage, "secret_image"))
        secret_file_btn.grid(column=2,row=0,padx=5)

        self.secretImage = tk.Label(secret_frame,width=45,height=12)
        self.secretImage.grid(column=0,row=6,columnspan=4,rowspan=2,padx=40,pady=20)

        mask_filepath_entry = tk.Entry(mask_frame, width=30, textvariable=self.mask_filepath)
        mask_filepath_entry.grid(column=1,row=0,padx=0,pady=5,sticky='E')

        mask_filepath_lbl = tk.Label(mask_frame,text="Mask Image Filepath: ")
        mask_filepath_lbl.grid(column=0,row=0,padx=5,pady=5)

        mask_file_btn = tk.Button(mask_frame, image=self.open_file_img, command=lambda: self.open_file(
        self.mask_filepath,self.maskImage,'mask_image'))
        mask_file_btn.grid(column=2,row=0,padx=5)

        self.maskImage = tk.Label(mask_frame, bg='blue',width=45,height=12)
        self.maskImage.grid(column=0,row=6,columnspan=4,rowspan=2,padx=40,pady=20)
        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        self.encrypt_window_button = tk.Button(
            self,
            text="Import Images/Videos First!",
            command=lambda: self.switch_to_encrypt_frame(controller),
            state=tk.DISABLED
        )

        
        self.encrypt_window_button.pack(before=mask_frame, side="bottom", anchor='s', fill='y', pady=10)

    def switch_to_encrypt_frame(self, controller):
        controller.show_frame(EncryptFrame, ImportFrame)

    def open_file(self, file_path_str,img_widget,label_for_cache):
        allowed_filetypes = [("Images & Videos", "*.png *.mp4 *.avi *.jpg")]
        imgfile = fd.askopenfile(filetypes=allowed_filetypes)
        file_path_str.set(imgfile.name)
        self.load_file(label_for_cache,file_path_str,img_widget)

    def load_file(self,label,filepathStr,img_to_update):
        path = filepathStr.get()
        if path[-4:] == ".png":
            cached_files[label] = ImageTk.PhotoImage(image=Image.open(path).resize((320,180)))
            cached_filepaths[label] = path
            img_to_update.config(image=cached_files[label],width=320,height=180)
            if self.mask_filepath.get() != "" and self.secret_filepath.get() != "":
                self.encrypt_window_button.config(state=tk.NORMAL,text="Ready To Encrypt!")
        elif filepathStr.get()[-4:] == ".mp4":

            # frame_extracter = frame_extraction.VideoExtractor.extract_frames()
            cached_filepaths[label] = path
            if self.mask_filepath.get() != "" and self.secret_filepath.get() != "":
                self.encrypt_window_button.config(state=tk.NORMAL,text="Ready To Encrypt!")
            videoObj = cv2.VideoCapture(path)
            while(videoObj.isOpened()):
                ret, frame = videoObj.read()
                cv2.imshow('video', frame)
                if cv2.waitKey(1) & 0xFF == 27:
                    # 27 == key code for escape key
                    break
            videoObj.release()
            cv2.destroyAllWindows()
        else:
            raise FileExistsError("EDED")




class EncryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg='red')
        self.pack(side="top", fill="both", expand=True)

        label = tk.Label(self, text="ENCRYPT FRAME", font=('Helvetica', 16, 'bold'))
        label.pack(side=tk.TOP, anchor='n', pady=20, padx=10, fill="x")

        steg_frame = tk.Frame(self, bg='grey')
        steg_frame.pack(side=tk.RIGHT, fill='both', expand=True)

        img_frame = tk.Frame(self, bg='yellow')
        img_frame.pack(side=tk.LEFT, fill='both', expand=True)

        encrypt_button = tk.Button(steg_frame, text="ENCRYPT", command=lambda: self.load_and_encrypt())
        encrypt_button.pack(side=tk.TOP, anchor='n', padx=5, pady=10)

        self.secretImage = tk.Label(img_frame, bg="green")
        self.secretImage.pack(side=tk.TOP, anchor='w', fill='both',padx=10,pady=10)

        self.maskImage = tk.Label(img_frame, bg='blue')
        self.maskImage.pack(side=tk.TOP, anchor='e', fill="both",padx=10,pady=10)

        self.stegImage = tk.Label(steg_frame, bg='blue')
        self.stegImage.pack(fill='both',expand=True)

        self.imgs = {}

    def load_and_encrypt(self):
        if imageorvideo == 'image':
            self.maskImage.config(image=cached_files["mask"],width=100)
            self.secretImage.config(image=cached_files["secret"],width=100)
            imagehandling = ImageHandler(1)
            imagehandling.encode_image(cached_filepaths["secret"], cached_filepaths["mask"])
            path = "samples\output.png"
            cached_files["output"] = ImageTk.PhotoImage(image=Image.open(path).resize((240,135)))
            cached_filepaths["output"] = path
            self.stegImage.config(image=cached_files["output"], height=200, width=200)
        elif imageorvideo == 'video':
            videomerger = VideoMerger(cached_filepaths["mask"], cached_filepaths['secret_'], 1)
        else:
            raise NameError("BIG BIG ERRO")




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