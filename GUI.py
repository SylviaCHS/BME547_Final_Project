from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image


class GUI:
    def __init__(self, root):

        root.title('Image Processor GUI')

        top_label = ttk.Label(root, text="Image Processor")
        top_label.grid(column=0, row=0, columnspan=4)

        name_label = ttk.Label(root, text="User Name:")
        name_label.grid(column=0, row=1)

        self.user_name = StringVar()
        name_entry = ttk.Entry(root, textvariable=self.user_name)
        name_entry.grid(column=1, row=1)

        self.new_factor = StringVar()
        th_check = ttk.Checkbutton(root, text='New User',
                                   variable=self.new_factor,
                                   onvalue=True, offvalue=False)
        th_check.grid(column=2, row=1)

        # Get file names
        self.filename = StringVar()
        import_btn = ttk.Button(root, text='Import File(s)',
                                command=lambda: self.import_file())
        import_btn.grid(column=1, row=2)

        # Select processing method
        method_label = ttk.Label(root, text="Processing Method:")
        method_label.grid(column=2, row=2)

        # Dropdown Menu
        self.method = StringVar()
        choices = ['Histogram Equalization', 'Contrast Stretching',
                   'Log Compression', 'Reverse Video']
        self.method.set('Histogram Equalization')  # set the default option
        dropdown = ttk.OptionMenu(root, self.method, *choices)
        dropdown.grid(column=3, row=2)

        run_btn = ttk.Button(root, text='Run Analysis',
                             command=lambda: self.run_function())
        run_btn.grid(column=0, row=3, columnspan=4)

        # Seperate Analysis and Display
        ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=4,
                                                    columnspan=5, sticky='ew')
        # Display original image (Need calling function)
        image_obj = Image.open('IMG63.jpeg')
        self.image = ImageTk.PhotoImage(image_obj.resize((96, 128)))
        img_label = Label(root, image=self.image)  # assigns the image object to a label
        img_label.grid(column=0, row=5, columnspan=2)

        # Display processed image (Need calling function)
        image_obj = Image.open('IMG63.jpeg')
        self.image = ImageTk.PhotoImage(image_obj.resize((96, 128)))
        img_label = Label(root, image=self.image)  # assigns the image object to a label
        img_label.grid(column=2, row=5, columnspan=2)

        

    def import_file(self):
        from tkinter import filedialog
        self.filename = filedialog.askopenfilenames(
            initialdir="/", title="Select file",
            filetypes=(("JPEG files", "*.jpeg"),
                       ("PNG files", "*.png"),
                       ("TIFF files", "*.tiff"),
                       ("ZIP files", "*.zip"),
                       ("all files", "*.*")))

    def run_function(self):
        print('Running analysis...', self.filename)
        print(type(self.filename))


if __name__ == '__main__':
    root = Tk()  # Makes main window
    gui = GUI(root)
    root.mainloop()  # Shows window
