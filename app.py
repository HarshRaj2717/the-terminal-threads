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
bitcount = 4
key = 0


class MainWindow(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("Video Encrypter/Decrypter v1")

        root = tk.Frame(self, height=450, width=800)
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
        tk.Frame.__init__(self, parent)
        self.pack(side="top", fill="both", expand=True)

        title = tk.Label(self, text="TITLE", font=('Helvetica', 16, 'bold'))
        title.pack(side=tk.TOP, anchor='n', pady=10, padx=10, fill="x")

        self.secret_filepath = tk.StringVar(self)
        self.mask_filepath = tk.StringVar(self)
        self.bitcount = tk.IntVar(self)
        self.key = tk.IntVar(self)
        self.open_file_img = ImageTk.PhotoImage(image=Image.open("ui/assets/open_folder.png").resize((14,14)))
        
    
        mask_frame = tk.Frame(self,)
        mask_frame.pack(side=tk.LEFT, fill='both', expand=True)

        secret_frame = tk.Frame(self)
        secret_frame.pack(side=tk.LEFT, fill='both', expand=True)

        details_frame = tk.Frame(self,)
        details_frame.pack(side=tk.BOTTOM, fill='both',anchor='s',ipady=40,before=mask_frame)


        secret_filepath_entry = tk.Entry(secret_frame, width=30,textvariable=self.secret_filepath)
        secret_filepath_entry.grid(column=1,row=0,padx=0,pady=5,sticky='E')

        secret_filepath_lbl = tk.Label(secret_frame,text="Secret Image Filepath: ")
        secret_filepath_lbl.grid(column=0,row=0,padx=5,pady=5)

        secret_file_btn = tk.Button(secret_frame, image=self.open_file_img, command=lambda: self.open_file(
        self.secret_filepath, self.secretImage, "secret"))
        secret_file_btn.grid(column=2,row=0,padx=5)

        self.secretImage = tk.Label(secret_frame,width=45,height=12)
        self.secretImage.grid(column=0,row=6,columnspan=4,rowspan=2,padx=40,pady=20)

        mask_filepath_entry = tk.Entry(mask_frame, width=30, textvariable=self.mask_filepath)
        mask_filepath_entry.grid(column=1,row=0,padx=0,pady=5,sticky='E')

        mask_filepath_lbl = tk.Label(mask_frame,text="Mask Image Filepath: ")
        mask_filepath_lbl.grid(column=0,row=0,padx=5,pady=5)

        mask_file_btn = tk.Button(mask_frame, image=self.open_file_img, command=lambda: self.open_file(
        self.mask_filepath,self.maskImage,'mask'))
        mask_file_btn.grid(column=2,row=0,padx=5)

        self.maskImage = tk.Label(mask_frame,width=45,height=12)
        self.maskImage.grid(column=0,row=6,columnspan=4,rowspan=2,padx=40,pady=20)
        # We use the switch_window_button in order to call the show_frame() method as a lambda function
        self.encrypt_window_button = tk.Button(
            details_frame,
            text="Import Images/Videos First!",
            command=lambda: self.switch_to_frame_and_run(controller,EncryptFrame),
            state=tk.DISABLED
        )
        self.decrypt_window_button = tk.Button(
            details_frame,
            text="Import Mask Image First!",
            command=lambda: self.switch_to_frame_and_run(controller,DecryptFrame),
            state=tk.DISABLED
        )

        self.decrypt_window_button.pack(side="left",fill='both',expand=True,padx=40)

        key_lbl = tk.Label(details_frame,text="Key (8 numbers): ")
        key_lbl.pack(side='left',padx=2)

        reg=details_frame.register(self.key_size_limit)
        key_entry = tk.Entry(details_frame,textvariable=self.key,validate='key',validatecommand=(reg, '%P'),width=10)

        key_entry.pack(side='left')

        bit_lbl = tk.Label(details_frame,text="Bitcount: ").pack(side="left",padx=2)
        B2 = tk.Radiobutton(details_frame, text="2", variable=self.bitcount, value=2)
        B4 = tk.Radiobutton(details_frame, text="4", variable=self.bitcount, value=4)
        B2.pack(side="left")
        B4.pack(side="left")
        B4.select()

        self.encrypt_window_button.pack(side="left",fill='both',expand=True,padx=40)


        # B6 = tk.Radiobutton(details_frame, text="6", variable=self.bitcount, value=6,command=lambda: self.update_key_and_bitcount()).pack(side='left')


    def key_size_limit(self,input:str):
        if len(input) <= 8 and input.isnumeric():
           return True
        else:
            return False
        ...
    def switch_to_frame_and_run(self, controller,frame):
        global bitcount
        global key
        key = int(self.key.get())
        bitcount = self.bitcount.get()
        controller.show_frame(frame, ImportFrame)

    def open_file(self, file_path_str,img_widget,label_for_cache):
        allowed_filetypes = [("Images & Videos", "*.png *.mp4 *.avi *.jpg")]
        imgfile = fd.askopenfile(filetypes=allowed_filetypes)
        file_path_str.set(imgfile.name)
        self.load_file(label_for_cache,file_path_str,img_widget)

    def load_file(self,label,filepathStr,img_to_update):
        global imageorvideo
        path = filepathStr.get()
        if self.mask_filepath.get() != "":
            self.decrypt_window_button.config(state=tk.NORMAL,text="Ready To Decrypt!")
            if self.mask_filepath.get() != "" and self.secret_filepath.get() != "":
                    self.encrypt_window_button.config(state=tk.NORMAL,text="Ready To Encrypt!")
        if path[-4:] == ".png":
            imageorvideo = 'image'
            cached_files[label] = ImageTk.PhotoImage(image=Image.open(path).resize((320,180)))
            cached_filepaths[label] = path
            img_to_update.config(image=cached_files[label],width=320,height=180)
           
        elif filepathStr.get()[-4:] == ".mp4"  or filepathStr.get()[-4:] == ".avi":
            imageorvideo = 'video'
            # frame_extracter = frame_extraction.VideoExtractor.extract_frames()
            cached_filepaths[label] = path
            videoObj = cv2.VideoCapture(path)
            frame_extraction_successful, first_frame = videoObj.read()
            if not frame_extraction_successful:
                print('Failed to read current frame')
                raise Exception('Issue while reading first frame of video')
            first_frame = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
            videoObj.release()
        else:
            raise FileExistsError("EDED")


class EncryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent,)
        self.pack(side="top", fill="both", expand=True)

        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP,fill='both',ipady=10)

        steg_frame = tk.Frame(self)
        steg_frame.pack(side=tk.RIGHT, fill='both', expand=True)

        img_frame = tk.Frame(self)
        img_frame.pack(side=tk.LEFT, fill='both', expand=True)

        title = tk.Label(top_frame, text="ENCRYPT FRAME", font=('Helvetica', 16, 'bold'))
        title.pack(side=tk.TOP, anchor='n', pady=5, padx=10, fill="x")

        self.secretImage = tk.Label(img_frame)
        self.secretImage.pack(side=tk.BOTTOM, anchor='w', fill='both',padx=10,pady=10)

        self.maskImage = tk.Label(img_frame)
        self.maskImage.pack(side=tk.BOTTOM, anchor='e', fill="both",padx=10,pady=10)

        self.stegImage = tk.Label(steg_frame)
        self.stegImage.pack(fill='both',expand=True)

        back_button = tk.Button(top_frame,text="Back to Home",command= lambda: controller.show_frame(ImportFrame,EncryptFrame)).pack(side="right")

        encrypt_button = tk.Button(steg_frame, text="ENCRYPT", command=lambda: self.load_and_encrypt())
        encrypt_button.pack(side=tk.TOP, anchor='n', padx=5, pady=10)

        self.imgs = {}

    def load_and_encrypt(self):
        if imageorvideo == 'image':
            self.maskImage.config(image=cached_files["mask"],width=100)
            self.secretImage.config(image=cached_files["secret"],width=100)
            imagehandling = ImageHandler(key)
            imagehandling.encode_image(cached_filepaths["secret"], cached_filepaths["mask"],bit_count=bitcount)
            path = "samples/output.png"
            cached_files["output"] = ImageTk.PhotoImage(image=Image.open(path).resize((480,270)))
            cached_filepaths["output"] = path
            self.stegImage.config(image=cached_files["output"],)
        elif imageorvideo == 'video':
            videomerger = VideoMerger(cached_filepaths["mask"], cached_filepaths['secret'], 1)
            videomerger.encode_video()


class DecryptFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.pack(side="top", fill="both", expand=True)

        top_frame = tk.Frame(self)
        top_frame.pack(side=tk.TOP,fill='both',ipady=10)

        decrypted_frame = tk.Frame(self)
        decrypted_frame.pack(side=tk.LEFT, fill='both', expand=True)

        steg_frame = tk.Frame(self)
        steg_frame.pack(side=tk.RIGHT, fill='both', expand=True)

        title = tk.Label(top_frame, text="DECRYPT FRAME", font=('Helvetica', 16, 'bold'))
        title.pack(side=tk.TOP, anchor='n', pady=20, padx=10, fill="x")

        back_button = tk.Button(top_frame,text="Back to Home",command= lambda: controller.show_frame(ImportFrame,DecryptFrame)).pack(side="right")


        self.stegImage = tk.Label(steg_frame)
        self.stegImage.pack(side=tk.BOTTOM, anchor='w', fill='both',padx=10,pady=10)

        self.decryptedImage = tk.Label(decrypted_frame)
        self.decryptedImage.pack(side=tk.BOTTOM, anchor='e', fill="both",padx=10,pady=10)

        encrypt_button = tk.Button(steg_frame, text="DECRYPT", command=lambda: self.load_and_decrypt())
        encrypt_button.pack(side=tk.TOP, anchor='n', padx=5, pady=10)


        self.imgs = {}
    def load_and_decrypt(self):
        if imageorvideo == 'image':
            self.decryptedImage.config(image=cached_files["mask"],width=100)
            imagehandling = ImageHandler(key)
            imagehandling.decode_image(cached_filepaths["mask"])
            path = "samples/decrypted.png"
            cached_files["decrypted"] = ImageTk.PhotoImage(image=Image.open(path).resize((480,270)))
            cached_filepaths["decrypted"] = path
            self.stegImage.config(image=cached_files["decrypted"],)
        elif imageorvideo == 'video':
            videomerger = VideoMerger(cached_filepaths["mask"], cached_filepaths['secret'], 1)
            videomerger.decode_video()
        


if __name__ == "__main__":
    testObj = MainWindow()
    testObj.geometry("800x450")
    testObj.mainloop()