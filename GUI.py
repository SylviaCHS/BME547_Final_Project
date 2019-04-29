from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
import os
import client
from tkinter import filedialog
import zipfile
import io


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
        # self.filepath = StringVar()
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
        run_btn.grid(column=1, row=3, columnspan=2)

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
        raw_label = ttk.Label(root, text="Original Image")
        raw_label.grid(column=1, row=5, columnspan=1)
        image = ImageTk.PhotoImage(Image.new('RGB', (96, 128)))
        self.raw_img_label = Label(root, image=image)
        self.raw_img_label.grid(column=1, row=6, columnspan=1)

        # Display original histogram
        rhist_label = ttk.Label(root, text="Original Histogram")
        rhist_label.grid(column=2, row=5, columnspan=1)
        self.raw_hist_label = Label(root, image=image)
        self.raw_hist_label.grid(column=2, row=6, columnspan=1)

        # Display processed image (Need calling function)
        pro_label = ttk.Label(root, text="Processed Image")
        pro_label.grid(column=3, row=5, columnspan=1)
        self.pro_img_label = Label(root, image=image)
        self.pro_img_label.grid(column=3, row=6, columnspan=1)

        # Display histogram
        phist_label = ttk.Label(root, text="Processed Histogram")
        phist_label.grid(column=4, row=5, columnspan=1)
        self.pro_hist_label = Label(root, image=image)
        self.pro_hist_label.grid(column=4, row=6, columnspan=1)

        # Display image metrics
        self.raw_metrics = {'Error': 'Please load a image first'}
        self.pro_metrics = {'Error': 'Please load a image first'}
        im_metrics_btn = ttk.Button(root,
                                    text="Display Original Image Metrics",
                                    command=lambda: self.display_metrics2())
        im_metrics_btn.grid(column=1, row=7)

        # Display image metrics
        im_metrics_btn2 = ttk.Button(root,
                                     text="Display Processed Image Metrics",
                                     command=lambda: self.display_metrics3())
        im_metrics_btn2.grid(column=3, row=7)

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

        # pop-up window to display metrics
        metrics_btn = ttk.Button(root, text="Display Metrics",
                                 command=lambda: self.display_metrics())
        metrics_btn.grid(column=4, row=9)

        self.msg = StringVar()
        msg_label = Message(root, textvariable=self.msg,
                            relief=RAISED, width=400)
        msg_label.grid(column=3, row=3, columnspan=2)

        self.msg2 = StringVar()
        msg_label2 = Message(root, textvariable=self.msg2,
                             relief=RAISED, width=400)
        msg_label2.grid(column=0, row=9, columnspan=4)

    def display_metrics(self):
        """
        Callback function for metrics_btn
        A window will pop-up to display the user metadata of previous user
        actions / metrics including:
         - How many times has a user run each process
         - latency for running different processing
        """
        metrics = client.user_metrics(self.user_name.get())
        messagebox.showinfo("Metrics", metrics)

    def display_metrics2(self):
        """
           Callback function for im_metrics_btn1
           A window will pop-up to display the original image metadata
           including:
            Timestamp when uploaded
            Time to process the image(s)
            Image size (e.g., X x Y pixels)
        """
        messagebox.showinfo("Original Image Metrics", self.raw_metrics)

    def display_metrics3(self):
        """
           Callback function for im_metrics_btn2
           A window will pop-up to display the processed image metadata
           including:
            Timestamp when uploaded
            Time to process the image(s)
            Image size (e.g., X x Y pixels)
        """
        messagebox.showinfo("Processed Image Metrics", self.pro_metrics)

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
        try:
            self.filepath
        except AttributeError:
            self.msg.set('Error: Please select file(s) to import')
        else:
            ID = self.user_name.get()
            new = self.new_factor.get()
            # Upload new image
            if new == '1':
                try:
                    self.msg.set(client.post_new_user(ID))
                    check_user(self.msg.get())
                except ValueError:
                    pass
                else:
                    self.msg.set(run_analysis(self.filepath, ID,
                                              self.method.get()))

            else:
                self.msg.set(run_analysis(self.filepath, ID,
                                          self.method.get()))

    def load_function(self):
        """
        Control the load button
        Load a list of processed images in the database. User could choose one
        or more images to download. If only one image is chosen the resulted
        plot will be displayed in the GUI. If multiple file is chosen, the
        files will be zip to a zip archive and save to a designated path.
        """
        self.image_names = client.get_image_list(self.user_name.get())
        # clear listbox
        self.name_list.delete(0, END)

        for i in self.image_names:
            self.name_list.insert(END, i)

    def download_function(self):
        """
        Callback function that controls the download button

        When clicked, it would:
            - Ask user for the directory they want to save the file
            - If a single image is chosen, the original and processed image as
              as well as the before and after histogram will be displayed in
              GUI. An image will be also saved to the designated folder
            - If multiple images are chosen, NO images will be displayed. A
              zip archive of these images will be save to the designated
              folder.
            - User could choose the file type they want, default is JPEG.
        """
        # Ask user for directory and user ID
        savepath = filedialog.askdirectory()
        ID = self.user_name.get()

        self.msg2.set('Saving files to the designated folder')

        # Get selected filenames
        index = self.name_list.curselection()
        select_files = [self.image_names[i] for i in index]

        single = check_multi_single(select_files)

        if single is True:

            filename = select_files[0]
            try:
                pro_img_obj, raw_img_obj, raw_img_name, \
                    pro_hist_obj, raw_hist_obj = get_image_pair(filename, ID)
            except ValueError:
                self.msg2.set(get_image_pair(filename, ID))
            else:
                # Get Image metrics
                self.raw_metrics = client.image_metrics(ID, raw_img_name)
                self.pro_metrics = client.image_metrics(ID, filename)

                s = self.raw_metrics['size']
                size = image_size(s)

                # display the raw and process image in GUI
                raw_img = ImageTk.PhotoImage(raw_img_obj.resize(size))
                self.raw_img_label.configure(image=raw_img)
                self.raw_img_label.image = raw_img

                pro_img = ImageTk.PhotoImage(pro_img_obj.resize(size))
                self.pro_img_label.configure(image=pro_img)
                self.pro_img_label.image = pro_img

                # display raw and process histogram in GUI
                raw_hist = ImageTk.PhotoImage(raw_hist_obj.resize([385, 450]))
                self.raw_hist_label.configure(image=raw_hist)
                self.raw_hist_label.image = raw_hist

                pro_hist = ImageTk.PhotoImage(pro_hist_obj.resize([385, 450]))
                self.pro_hist_label.configure(image=pro_hist)
                self.pro_hist_label.image = pro_hist

                # Save file to a designated folder
                full_name = savepath + '/' + filename + '.' + self.saveas.get()
                pro_img_obj.save(full_name)

        else:
            download_multiple(select_files, savepath, ID, self.saveas.get())


def image_size(size):
    """
    Determine the image size of the images to be displayed in GUI
    The original width to height ratio will be preserved.

    Max width/height is set to be 300, and the other dimension will be
    adjusted accordingly.

    Args:
        size (list): Original image size

    Returns:
        new_size (list): New image size suitable for GUI
    """
    l_max = max(size)
    if l_max > 300:
        num = l_max/300
    else:
        num = 1
    w = round(size[0] / num)
    h = round(size[1] / num)
    new_size = [w, h]
    return new_size


def get_image_pair(filename, ID):
    """
    Communicate with server and database to get original and processed images,
    pre and post-processing histogram.

    Args:
        filename (str): filename of processed image
        ID (str): user name

    Returns:
        pro_img (image object): post-processed image
        raw_img (image object): original image
        raw_img_name (str): original image name
        pro_hist (image object): histogram of original image
        raw_hist (image object): histogram of processed image
    """
    r = client.get_image_file(ID, filename)

    try:
        check_r_type(r)
    except TypeError:
        return r
    else:
        pro_img_arr, method = client.get_image(r)
        pro_img = Image.fromarray(pro_img_arr)
        raw_img_name = filename.replace('_' + method, "")

        r_raw = client.get_image_file(ID, raw_img_name)

        try:
            check_r_type(r)
        except TypeError:
            return r
        else:
            raw_img_arr, _ = client.get_image(r_raw)
            raw_img = Image.fromarray(raw_img_arr)

            pro_hist = Image.fromarray(client.get_histogram(ID, filename))

            raw_hist = Image.fromarray(client.get_histogram(ID, raw_img_name))
            return pro_img, raw_img, raw_img_name, pro_hist, raw_hist



def check_r_type(r):
    if type(r) is str:
        raise TypeError('Get Error message.')

def get_file_name(filepath):  # need pytest
    """
    Extract filename and extension from filepath

    Args:
        filepath (str):  full filepath of the image including filename and ext

    Returns:
        filename (str): filename without path and extension
        extension (str): image type, ex. '.png'

    """
    filename, extension = os.path.splitext(filepath.split('/')[-1])
    return filename, extension


def check_multi_single(filenames):
    """
    Check if multiple or single file is chosen.

    Args:
        filenames (list): A list of all the filepaths or string of
                                filepath

    Returns:
        single (bool): Return whether it is a single file (True)
                       or multiple files (False)
    """
    num = len(filenames)
    if num == 1:
        single = bool(1)
    else:
        single = bool(0)
    return single


def run_analysis(filepath, ID, method):
    """
    Call other function to run analysis and upload the results to the database
    It can both accept one single .zip file or one/multiple image file(s)
    Args:
        filepath (tuple): A tuple of filepath(s)
        ID (str): user name
        method (str): Required processing method

    Returns:
        msg (str): Message informing the user if the program is running
                    properly or there is an error or warning.

    """
    filename, extension = get_file_name(filepath[0])
    if extension == '.zip':
        msg = run_zip_analysis(filepath, ID, method)
    else:
        msg = run_images_analysis(filepath, ID, method)
    return msg


def run_zip_analysis(filepath, ID, method):
    """
    Run image analysis for zip archive

    Args:
        filepath (str): full filepath with filename of the zip archive
        ID (str): user name
        method (str): processing method

    Returns:
        msg (str):  Message informing the user if the program is running
                    properly or there is an error or warning.
    """
    with zipfile.ZipFile(filepath[0]) as zf:
        for entry in zf.namelist():
            if not entry.startswith("__"):  # Get rid hidden files in zip
                with zf.open(entry) as file:
                    data = file.read()
                    fh = io.BytesIO(data)
                    Image.open(fh)

                filename, extension = get_file_name(file.name)

                # Save raw image to database
                msg = client.upload_file(ID, filename,
                                         extension, fh.getvalue())
                err, msg = check_msg(msg)
                if err is False:  # if no error in uploading image
                    # Request to process image
                    client.process_image(ID, filename, method)
    return msg


def check_msg(msg):
    """
    Check if message contains Error or Warning for run_analysis functions.

    Args:
        msg (str): Message from server/client code

    Returns:
        err (bool): True for there is an error
        msg (str): Message informing the user if the program is running
                    properly or there is an error or warning.

    """
    err = bool(0)
    if 'Error' in msg:
        err = bool(1)
    elif "Warning" in msg:
        msg = 'Success! Warning: Image already exists. ' \
              'Processing ran on existing image'
    else:
        msg = 'Image saved successfully'
    return err, msg


def check_user(msg):
    """
    Check if message contains Error for get new_user_id function.
    Raise a ValueError if message contains "Error"
    Args:
        msg (str): Message from server code
    """
    if "Error" in msg:
        raise ValueError('User already exists.')


def run_images_analysis(filepath, ID, method):
    """
    Upload image(s) and run the required analysis for multiple or single image
    file(s)

    Args:
        filepath (str): filepath of the image including filename
        ID (str): user name
        method (str): user specified image processing method

    Returns:
        msg (str): Message informing the user if the program is running
                    properly or there is an error or warning.

    """
    for path in filepath:
        try:
            Image.open(path)
        except IOError:
            msg = 'Please import images files, or just a single zip archive'
        else:
            filename, extension = get_file_name(path)

            # Save raw image to database
            msg = client.upload_file(ID, filename, extension, path)

            err, msg = check_msg(msg)

            if err is False:  # if no error in uploading image
                # Request to process image
                client.process_image(ID, filename, method)
        return msg


def download_multiple(select_files, savepath, id, ext):
    """
    Download multiple processed images in a zip archive.

    Args:
        select_files (list): list of names of selected images
        savepath (str): path of folder user chose
        id (str): user name
        ext (str): User specified image type

    """
    with zipfile.ZipFile(savepath + '/processed_images.zip', mode='w') as zf:

        for file in select_files:
            pro_img_arr, _, _, _, _ = get_image_pair(file, id)
            pro_img = Image.fromarray(pro_img_arr)
            output = io.BytesIO()
            pro_img.save(output, format=ext)
            filename = file + '.' + ext
            zf.writestr(filename, output.getvalue())


if __name__ == '__main__':
    root = Tk()  # Makes main window
    gui = GUI(root)
    root.mainloop()  # Shows window
