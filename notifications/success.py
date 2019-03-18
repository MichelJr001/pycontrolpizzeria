# -*- coding: utf-8 -*-

from tkinter import *
from PIL import ImageTk, Image

def fechar():
    janela.destroy()

        
janela = Tk()
janela.title('Sucesso')
janela.iconbitmap('icons/sucesso.ico')
janela.geometry('260x250')
janela.resizable(width=False, height=False)
photo = PhotoImage(file='icons/sucesso.png')        
label = Label(janela, image=photo).place(x=85, y=30, width=100, height=100)
lbl = Label(janela, text='Ação realizada com sucesso!', fg='green').place(x=60, y=140, width=150, height=25)
btn = Button(janela, command=fechar, bg='black', fg='white', text='Concluir').place(x=85, y=190, width=100, height=25)
janela.mainloop()

