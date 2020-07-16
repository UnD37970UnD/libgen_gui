from libgen_api import LibgenSearch
from tkinter import *
from tkinter import filedialog
import tkinter.font as tkFont
import wget
import os
from bs4 import BeautifulSoup
import requests
import re
LG = LibgenSearch()
filters = {}
x = '550'
y = '600'

windows_user = os.getlogin()
default_download_directory = "C:/Users/" + windows_user +"/Downloads/"

root = Tk()
root.geometry('{}x{}'.format(x, y))
root.resizable(False, False)
root.title("Books Downloader")
root.iconbitmap("icon.ico")

sw = 0
var_type = IntVar()
var_type.set(3)
Extension_type = "all"

progress = StringVar()
progress.set('no downloads actives')

TitleFontStyle = tkFont.Font(family="Lucida Grande", size=20)
TextFontStyle  = tkFont.Font(family="Lucida Grande", size=10)

def select_download_directory():
    global download_directory
    download_directory = filedialog.askdirectory(initialdir=default_download_directory,title="Select where to save the book")
    Download_dir_entry.delete (0,len(Download_dir_entry.get()))
    Download_dir_entry.insert(0,download_directory)

download_directory=default_download_directory

def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    progress.set(progress_message)
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()
    StatusBar.configure(text = progress_message)
    root.update()

def select_extension(value):
    global Extension_type
    if value == 2:
        Extension_type = "epub"
    elif value == 1:
        Extension_type = "pdf"
    else:
        Extension_type = "all"


def SearchClick():
    global Searchresults
    global lenght
    Options.delete(0,'end')
    if BookTitle_entry.get() == "":
        Searchresults=LG.search_author(BookAuthor_entry.get())
    else:
        if BookAuthor_entry.get() != "" or Extension_type != "all":
            if BookAuthor_entry.get() != "":
                filters["Author"] = BookAuthor_entry.get()
            filters["Extension"] = Extension_type
            Searchresults=LG.search_title_filtered(BookTitle_entry.get(), filters)
        else:
            Searchresults=LG.search_title(BookTitle_entry.get())
    lenght = len(Searchresults)
    for i in Searchresults:
        Options.insert(lenght, str(i.get("Title")) + " - " + str(i.get("Extension")) + " - " + str(i.get('Size')))
        Options.update


def download():
    cs = int(str(Options.curselection())[1:-2])
    url = Searchresults[cs].get('Mirror_1')
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    download_link = str(soup.find('a'))
    download_link = download_link[9:len(download_link) - 9]
    filename = wget.detect_filename(download_link)
    print(filename)
    rename = str(re.sub('[<>.:/\'",?*]', '', str(Searchresults[0].get("Title"))) + "." + str(Searchresults[0].get("Extension")))
    wget.download(download_link, download_directory, bar=bar_progress)
    os.rename(download_directory + str(filename), str(download_directory + rename))

StatusBar = Label(root)

Spacer0 = Label(root)
AppTitle = Label(root,text="Book downloader",font=TitleFontStyle,anchor="center")
Spacer1 = Label(root)
BookTitle = Label(root,text="Book title:    ")
Spacer2 = Label(root)
BookTitle_entry = Entry(root, width=65,font=TextFontStyle)
Spacer3 = Label(root)
BookAuthor = Label(root,text="Book author: ")
BookAuthor_entry = Entry(root, width=65,font=TextFontStyle)
Spacer4 = Label(root)
Download_dir = Label(root,text="Download dir: ")
Download_dir_entry=Entry(root,width=65,font=TextFontStyle)
Download_dir_entry.insert(0,default_download_directory)
Download_dir_button=Button(root,text="Select download direcotry",command=select_download_directory,font=TextFontStyle)
Spacer4 = Label(root)
ExtentionFrame = LabelFrame(root,text="Select a format" , padx=5,pady=5)
PDF_button = Radiobutton(ExtentionFrame, text="PDF ", variable=var_type, value=1, command=lambda: select_extension(var_type.get()))
EPUB_button = Radiobutton(ExtentionFrame,text="EPUB", variable=var_type, value=2, command=lambda: select_extension(var_type.get()))
ALL_button = Radiobutton(ExtentionFrame,text="ALL", variable=var_type, value=3, command=lambda: select_extension(var_type.get()))
SearchButton = Button(root, text="Search ...", padx=50, command=SearchClick,font=TextFontStyle)

Spacer5 = Label(root)
Options = Listbox( root,height=10)
Select_download = Label(root,text="..select a file to download",font=TextFontStyle)
Download_button=Button(root, text="Download...", padx=50,command=download, font=TextFontStyle)
Spacer6 = Label(root)
StatusBar = Label(root, text='no downloads actives', bd=1, relief=SUNKEN, anchor=E)

AppTitle.grid(row=1,column=0,columnspan=4,sticky=W+E)
Spacer1.grid(row=2,column=0,pady=5)
BookTitle.grid(row=3,column=0)
BookTitle_entry.grid(row=3,column=1)
Spacer2.grid(row=4,column=0,pady=5)
BookAuthor.grid(row=6,column=0)
BookAuthor_entry.grid(row=6,column=1)
Spacer3.grid(row=7,column=0,pady=5)
Download_dir.grid(row=8,column=0)
Download_dir_entry.grid(row=8,column=1)
Spacer4.grid(row=10,column=0,pady=1.25)
Download_dir_button.grid(row=9,column=0,columnspan=4)
ExtentionFrame.grid(row=11,column=0,columnspan=4)
PDF_button.grid(row=0,column=1)
EPUB_button.grid(row=0,column=2)
ALL_button.grid(row=0,column=3)
Spacer5.grid(row=12,column=0,pady=1.25)
SearchButton.grid(row=13,column=0,columnspan=4)
Options.grid(row=14, column=0,columnspan = 4,sticky=W+E)
Select_download.grid(row=15,column=0,columnspan=4)
Download_button.grid(row=16,column=0,columnspan=4)
StatusBar.grid(row=17, column=0, columnspan=4, sticky=W+E)
root.mainloop()
