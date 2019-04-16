from tkinter import *
from tkinter import ttk
from tkinter import filedialog


def design_window():
    def ok_function():

        pass

    root = Tk()  # Makes main window
    root.title('Image Processor GUI')

    top_label = ttk.Label(root, text="Image Processor")
    top_label.grid(column=0, row=0)

    name_label = ttk.Label(root, text="User Name:")
    name_label.grid(column=0, row=1)

    user_name = StringVar()
    name_entry = ttk.Entry(root, textvariable=user_name)
    name_entry.grid(column=1, row=1)

    new_factor = StringVar()
    th_check = ttk.Checkbutton(root, text='New User', variable=new_factor, onvalue=True, offvalue=False)
    th_check.grid(column=1, row=2)

    root.mainloop()  # Shows window


if __name__ == '__main__':
    design_window()
