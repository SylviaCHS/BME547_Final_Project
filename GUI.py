from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import os
import client


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

        # Get file path
        self.filepath = StringVar()
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

        # Separate Analysis and Display
        ttk.Separator(root, orient=HORIZONTAL).grid(column=0, row=4,
                                                    columnspan=5, sticky='ew')

        # Load image locally
        load_btn = ttk.Button(root, text='Load File(s)',
                              command=lambda: self.load_function())
        load_btn.grid(column=0, row=5)

        # List box to display list of file names
        self.image_names = []
        self.name_list = Listbox(root, height=1, selectmode=MULTIPLE)

        self.name_list.grid(column=0, row=6, sticky=(N, W, E, S))

        # Scroll bar
        scroll = Scrollbar(root, orient=VERTICAL, command=self.name_list.yview)
        scroll.grid(column=0, row=6, sticky=(N, E, S))
        self.name_list['yscrollcommand'] = scroll.set
        scroll = Scrollbar(root, orient=HORIZONTAL,
                           command=self.name_list.xview)
        scroll.grid(column=0, row=6, sticky=(W, E, S))
        self.name_list['xscrollcommand'] = scroll.set

        # Display original image
        image = ImageTk.PhotoImage(Image.new('RGB', (96, 128)))
        self.raw_img_label = Label(root, image=image)
        self.raw_img_label.grid(column=1, row=6, columnspan=1)

        # Display histogram
        pro_hist_label = Label(root, image=image)
        pro_hist_label.grid(column=4, row=6, columnspan=1)

        # Display processed image (Need calling function)
        pro_img_label = Label(root, image=image)
        pro_img_label.grid(column=3, row=6, columnspan=1)

        # Display histogram
        pro_hist_label = Label(root, image=image)
        pro_hist_label.grid(column=4, row=6, columnspan=1)

        # Display timestamp when uploaded
        timestamp_label = ttk.Label(root, text="Timestamp when uploaded:")
        timestamp_label.grid(column=0, row=7)

        # Display time to process the image(s)
        duration_label = ttk.Label(root, text="Time to process the image(s):")
        duration_label.grid(column=2, row=7)

        # Select processing method
        size_label = ttk.Label(root, text="Image size:")
        size_label.grid(column=0, row=8)

        # Download the image
        save_label = ttk.Label(root, text="Save image(s) as:")
        save_label.grid(column=2, row=8)
        # Dropdown Menu
        self.saveas = StringVar()
        img_format = ['JPEG', 'PNG', 'TIFF']
        self.saveas.set('Histogram Equalization')  # set the default option
        dropdown2 = ttk.OptionMenu(root, self.saveas, *img_format)
        dropdown2.grid(column=3, row=8)
        # Download image or zip archive
        download_btn = ttk.Button(root, text='Download File(s)',
                                  command=lambda: self.download_function())
        download_btn.grid(column=4, row=8)

    def import_file(self):
        """
        Open a pop-up window to let user choose file(s)
        The full filepath will be stored in the class

        """
        from tkinter import filedialog
        self.filepath = filedialog.askopenfilenames(
            initialdir="/", title="Select file",
            filetypes=(("PNG files", "*.png"),
                       ("JPEG files", "*.jpeg"),
                       ("TIFF files", "*.tiff"),
                       ("ZIP files", "*.zip"),
                       ("all files", "*.*")))

    def run_function(self):
        """
        Control the 'run analysis' button to do the following commands:
            - Check if user is new. If yes, creat new user in mongoDB
            - Upload file(s) as images to mongoDB
            - Process the images using the specified
              method and store in mongoDB

        """
        ID = self.user_name.get()
        new = self.new_factor.get()

        # Upload new image
        if new == '1':
            client.post_new_user(ID)
        self.filename, self.extension = get_file_name(self.filepath)
        client.upload_file(ID, self.filename, self.extension, self.filepath[0])

        # Request to process image
        client.process_image(ID, self.filename, self.method.get())

    def load_function(self):
        """
        Control the load button
        Load a list of processed images in the database. User could choose one
        or more images to download. If only one image is chosen the resulted
        plot will be displayed in the GUI. If multiple file is chosen, the
        files will be zip to a zip archive and save to a designated path.

        Returns:

        """
        self.image_names = client.get_image_list(self.user_name.get())
        print(self.image_names)
        for i in self.image_names:
            self.name_list.insert(END, i)

    def download_function(self):
        """
        Control the download button

        Returns:

        """
        index = self.name_list.curselection()
        select_files = [self.image_names[i] for i in index]
        print(select_files, type(select_files))
        filename = select_files[0]  # Temporary
        img_arr = client.get_image(self.user_name.get(), filename)
        img = ImageTk.PhotoImage(Image.fromarray(img_arr).resize([100, 100]))
        self.raw_img_label.configure(image=img)
        self.raw_img_label.image = img


def get_file_name(filepath):
    """
    Extract filename and extension from filepath

    Args:
        filepath (StrVar):  filepath of the image

    Returns:
        filename (str): filename without path and extension
        extension (str): image type

    """
    filename, extension = os.path.splitext(filepath[0].split('/')[-1])
    return filename, extension


if __name__ == '__main__':
    root = Tk()  # Makes main window
    gui = GUI(root)
    root.mainloop()  # Shows window
