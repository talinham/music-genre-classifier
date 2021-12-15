from tkinter import *
from tkinter import filedialog

root = Tk()

root.geometry("500x300")
my_text= Text(root, height = 1, width = 20)

myLabel1 = Label(root, text = "Music Genre Classifier")
myLabel1.config(font =("Helvetica", 15))
myLabel1.place(x=150, y=0)

myLabel2 = Label(root, text = "Select a song: ")
myLabel2.config(font =("Helvetica", 12))
myLabel2.place(x=50, y=100)
my_text.place(x=160 , y=100)

runButton = Button(root, text = "       Run      ")
runButton.place(x=320, y=200)

def select_files():
    filetypes = (('wav files', '*.wav'),('All files', '*.*'))

    filenames = filedialog.askopenfilename(
        title='Open files',
        initialdir='/',
        filetypes=filetypes)

    my_text.insert(INSERT, filenames)
   

# open button
browseButton = Button( root, text=' Browse ',command=select_files)
browseButton.place(x=335, y =100)



root.mainloop()

