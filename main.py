
# =================================== IMPORT THE RELEVANT MODULES ======================================================
import requests, io
from tkinter import *
import ttkbootstrap as tkb
from PIL import Image, ImageTk, UnidentifiedImageError, ImageFont, ImageDraw, ImageGrab
from tkinter import filedialog, messagebox, font

# ============================================= CONSTANTS ==============================================================
MAIN_WIN_WIDTH = 800
MAIN_WIN_HEIGHT = 800
CAN_WIDTH = 500
CAN_HEIGHT = 500
MENU_WIDTH = 200
MENU_HEIGHT = 500
MIN_SIZE = (800, 800)

# =================================== CREATE A TKINTER MAIN WINDOW USING CLASSES =======================================


class MainWindow(tkb.Window):
    def __init__(self, themename, title, size, minsize):
        super().__init__()
        self.themename = themename
        self.title(title)
        self.size = size
        self.minsize = minsize

        # ============================== CREATE TWO FRAMES WITHIN THE MAIN WINDOW ======================================
        self.top_menu = tkb.Frame(self)
        self.top_menu.grid(row=0, column=0, columnspan=2)

        self.canvas_frame = tkb.Frame(self)
        self.canvas_frame.grid(row=1, column=0, padx=20, pady=20)

        self.menu_frame = tkb.Frame(self, width=MENU_WIDTH, height=MENU_HEIGHT)
        self.menu_frame.grid(row=1, column=1, padx=20, pady=20)

        # ========================= SUPERIMPOSE A CANVAS ON THE FIRST FRAME OF THE MAIN WINDOW =========================
        self.canvas = Canvas(self.canvas_frame, width=CAN_WIDTH, height=CAN_HEIGHT, bg="#87CEEB", relief="groove")
        self.canvas.pack()

        # ================== SUPERIMPOSE INSTRUCTIONAL BUTTONS ON THE SECOND FRAME OF THE MAIN WINDOW ==================

        self.close_app = tkb.Button(self.menu_frame, text="CLOSE_APP", command=self.close_app)
        self.close_app.grid(row=0, column=0, padx=20, pady=20)

        self.select_img = tkb.Button(self.menu_frame, text="CHOOSE IMAGE", command=self.select_img)
        self.select_img.grid(row=1, column=0, padx=20, pady=20)

        self.add_watermark = tkb.Button(self.menu_frame, text="ADD_WATERMARK", command=self.add_watermark)
        self.add_watermark.grid(row=2, column=0, padx=20, pady=20)

    # ========================================= CLOSE THE APP ==========================================================

    def close_app(self):
        self.destroy()

    # =============================================== CHOOSE AN IMAGE BUTTON ===========================================
    def select_img(self):
        # ====== THE IMAGE BUTTON SHOULD OPEN TOP LEVEL WINDOW WITH OPTIONS TO CHOOSE IMAGES ===========================
        self.image_options_window = ImageOptionsWindow()
        self.image_options_window.image_win_widgets()

    # =================================== ADD A WATERMARK TO THE IMAGE CHOSEN ==========================================
    def add_watermark(self):
        close_app = Button(main_window.top_menu, text="CLOSE_APP")
        close_app.pack(side=LEFT, padx=100)

        add_text = Button(main_window.top_menu, text="ADD_TEXT", command=self.add_text)
        add_text.pack(side=LEFT, padx=5)

        add_logo = Button(main_window.top_menu, text="ADD_LOGO", command=self.add_logo)
        add_logo.pack(side=LEFT, padx=5)

        save_remove = Button(main_window.top_menu, text="SAVE & REMOVE FILES",
                             command=self.save_remove)
        save_remove.pack(side=LEFT, padx=100)
        self.add_watermark.config(state=DISABLED)

    def add_text(self):
        # ====================================== ADD TEXT TO THE IMAGE =================================================
        img_size = self.image_options_window.converted_img.width(), self.image_options_window.converted_img.height()

        font_type = font.Font(family="Times New Romans", weight="bold", size=50)
        watermark_text = input("Please enter your water mark text: ")

        value = font_type.metrics()
        text_height = value["ascent"] + value["descent"]
        text_width = font_type.measure(watermark_text)
        print(text_width, text_height)

        scale = min(img_size[0]/text_width, img_size[1]/text_height)
        print(scale)

        watermark_text_size = font_type["size"]

        if text_width > img_size[0] or text_height > img_size[1]:
            while text_width > img_size[0] or text_height > img_size[1]:
                watermark_text_size = int(watermark_text_size * scale)
                font_type = font.Font(family="Times New Romans", size=watermark_text_size)
                value = font_type.metrics()
                text_height = value["ascent"] + value["descent"]
                text_width = font_type.measure(watermark_text)
            print(text_width, text_height)
        text_x = CAN_WIDTH - text_width/2
        text_y = CAN_HEIGHT - text_height
        print(text_x, text_y)

        main_window.canvas.create_text(text_x, text_y,
                                       font=watermark_text_size,
                                       fill="white",
                                       text=watermark_text,
                                       anchor="center")
        main_window.canvas.pack()

    def add_logo(self):

        # =================== CHOOSE WATERMARK IMAGE TO SUPERIMPOSE ON THE IMAGE UPLOADED TO CANVAS ====================
        try:
            watermark_img_path = filedialog.askopenfilename(parent=self,
                                                            initialdir="/",
                                                            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"),
                                                                  ("All Files", "*.*")])

            watermark_img = Image.open(watermark_img_path)

            watermark_img_width, watermark_img_height = watermark_img.size
            print(f"The watermark image, width: {watermark_img_width} height: {watermark_img_height}")
            scale = min(CAN_WIDTH/(4*watermark_img_width), CAN_HEIGHT/(4*watermark_img_height))
            print(f'The scale: {scale}')

            if watermark_img_width >= CAN_WIDTH/4 or watermark_img_height >= CAN_HEIGHT/4:
                while watermark_img_width > CAN_WIDTH/4 or watermark_img_height > CAN_HEIGHT/4:
                    watermark_img_width = int(watermark_img_width * scale)
                    watermark_img_height = int(watermark_img_height * scale)
                    print(f"the resized img width: {watermark_img_width}, the resized img height: {watermark_img_height}")

                watermark_img = watermark_img.resize((watermark_img_width, watermark_img_height))
                self.formatted_watermark_img = ImageTk.PhotoImage(watermark_img)
                messagebox.showinfo(title="Warning",
                                    message="The uploaded image is larger than the canvas, it will be resized")

        except UnidentifiedImageError:
            messagebox.showwarning(title="Image Error",
                                   message="The file selected is not an image, please make sure it is an image file")

        main_window.canvas.create_image(CAN_WIDTH/2, CAN_HEIGHT/2, anchor=NW, image=self.formatted_watermark_img)
        main_window.canvas.pack()

    def save_remove(self):
        # Get the coordinates of the top left corner of the canvas
        canvas_x = main_window.canvas.winfo_rootx()
        canvas_y = main_window.canvas.winfo_rooty()
        print(f"canvas_x: {canvas_x}, canvas_y:{canvas_y}")

        # Get the coordinates of the bottom right corner of the canvas
        canvas_width = main_window.canvas.winfo_width()
        canvas_height = main_window.canvas.winfo_height()
        canvas_x2 = canvas_x + canvas_width
        canvas_y2 = canvas_y + canvas_height

        bbox = (canvas_x, canvas_y, canvas_x2, canvas_y2)
        print(bbox)

        image = ImageGrab.grab(bbox)
        image_name = input("Please enter the name for the watermarked image: ")
        image_ext = input("Please choose the file extension you prefer: ")
        image.save(f"{image_name}.{image_ext}")
        main_window.canvas.delete("all")

        main_window.top_menu.destroy()
        main_window.select_img.config(state=NORMAL)
        self.add_watermark.config(state=NORMAL)


class ImageOptionsWindow(tkb.Toplevel):

    def __int__(self, parent, canvas, image_choice):
        super().__init__(parent)

        self.converted_img = None

        self.formatted_watermark_img = None

        self.image_win_widgets()

        self.get_image()

    def image_win_widgets(self):

        img_frame_main = tkb.Frame(self)
        img_frame_main.pack(expand=True, fill="both")

        from_comp_frame = tkb.Frame(img_frame_main)
        from_comp_frame.pack(expand=True, fill="both")

        other_opt_frame = tkb.Frame(img_frame_main)
        other_opt_frame.pack(expand=True, fill="both")

        from_computer = tkb.Button(from_comp_frame, text="FROM COMPUTER", command=self.from_computer)
        from_computer.pack(pady=20)

        from_web = tkb.Button(other_opt_frame, text="FROM WEB", command=self.from_web)
        from_web.grid(row=0, column=0, padx=20, pady=20)

        main_window.select_img.config(state=DISABLED)

    def get_image(self):

        try:
            img_file_path = filedialog.askopenfilename(parent=self,
                                                       initialdir="/",
                                                       filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"),
                                                              ("All Files", "*.*")])

            selected_img = Image.open(img_file_path)

            # ----------------- ESTABLISH THE IMAGE SIZE AND RESIZE TO FIT CANVAS IF NECESSARY -------------------------
            img_width, img_height = selected_img.size
            # print(f"the image width: {img_width}, the image height: {img_height}")

            scale = min(CAN_WIDTH/img_width, CAN_HEIGHT/img_height)

            if img_width > CAN_WIDTH or img_height > CAN_HEIGHT:
                while img_width > CAN_WIDTH or img_height > CAN_HEIGHT:
                    img_width = int(img_width * scale)
                    img_height = int(img_height * scale)
                    # print(f"the resized img width: {img_width}, the resized img height: {img_height}")

                selected_img = selected_img.resize((img_width, img_height))
                messagebox.showinfo(title="Warning",
                                    message="The uploaded image is larger than the canvas, it will be resized")

                self.converted_img = ImageTk.PhotoImage(selected_img)
                main_window.canvas.create_image(CAN_WIDTH / 2, CAN_HEIGHT / 2, anchor=CENTER, image=self.converted_img)
                main_window.canvas.pack()

        except UnidentifiedImageError:
            message = messagebox.showwarning(title="Image Error",
                                             message="Image could not be read, ensure that it is an image file")

        return self.converted_img.width(), self.converted_img.height()

    def from_web(self):

        try:
            # Load the image from the internet
            img_url = input("Please copy and paste the image URL: ")
            response = requests.get(img_url)
            web_img = Image.open(io.BytesIO(response.content))

            img_width, img_height = web_img.size

            scale = min(CAN_WIDTH / img_width, CAN_HEIGHT / img_height)

            if img_width > CAN_WIDTH or img_height > CAN_HEIGHT:
                while img_width > CAN_WIDTH or img_height > CAN_HEIGHT:
                    img_width = int(img_width * scale)
                    img_height = int(img_height * scale)
                    # print(f"the resized img width: {img_width}, the resized img height: {img_height}")

                web_img = web_img.resize((img_width, img_height))
                messagebox.showinfo(title="Warning",
                                    message="The uploaded image is larger than the canvas, it will be resized")

                self.web_img_convert = ImageTk.PhotoImage(web_img)
                main_window.canvas.create_image(CAN_WIDTH / 2, CAN_HEIGHT / 2, anchor=CENTER, image=self.web_img_convert)
                main_window.canvas.pack()

        except UnidentifiedImageError:

            message = messagebox.showwarning(title="Image Error",
                                             message="Image could not be read, ensure that it is an image file")

        return self.web_img_convert.width(), self.web_img_convert.height()

    def from_computer(self):
        self.get_image()
        main_window.image_options_window.destroy()


# =========================================== INSTANTIATE YOUR APP =====================================================
main_window = MainWindow(themename="pulse",
                         title="Watermark App",
                         size=(MAIN_WIN_WIDTH, MAIN_WIN_HEIGHT),
                         minsize=MIN_SIZE,
                         )

main_window.mainloop()
