# -*- coding: utf-8 -*-
#
# __author__ = 'Michel Anderson'
# __version__ = 0.1
#

import sqlite3
from tkinter import *
from maskedentry import MaskedWidget
import os

con = sqlite3.connect('databases/main.db')
c = con.cursor()

class falid():
    def __init__(self, initjanela, msg):
        def fechar():
            self.janela.destroy()
            if initjanela == 'autenticar':
                autenticar()
            elif initjanela == 'pizzaria':
                pizzaria()
            elif initjanela == 'cadastro':
                cadastro()
        self.janela = Tk()
        self.janela.title('Erro')
        self.janela.iconbitmap('icons/erro.ico')
        self.janela.resizable(width=False, height=False)
        self.fotoerro = PhotoImage(file='icons/erro.png')        
        self.label = Label(self.janela, image=self.fotoerro).grid(row=0, column=1, pady=10)
        self.lbl = Label(self.janela, text=msg, fg='red').grid(row=1, column=1, pady=10)
        self.btn = Button(self.janela, command=fechar, text='Concluir').grid(row=2, column=1, pady=10)
        self.janela.mainloop()

class success():
    def __init__(self, initjanela, msg):
        def fechar():
            self.janela.destroy()
            if initjanela == 'autenticar':
                autenticar()
            elif initjanela == 'pizzaria':
                pizzaria()
            elif initjanela == 'cadastro':
                cadastro()
        self.janela = Tk()
        self.janela.title('Sucesso')
        self.janela.iconbitmap('icons/sucesso.ico')
        self.janela.resizable(width=False, height=False)
        self.fotosucesso = PhotoImage(file='icons/sucesso.png')        
        self.label = Label(self.janela, image=self.fotosucesso).grid(row=0, column=1, pady=10)
        self.lbl = Label(self.janela, text=msg, fg='green').grid(row=1, column=1, pady=10)
        self.btn = Button(self.janela, command=fechar, text='Concluir').grid(row=2, column=1, pady=10)
        self.janela.mainloop()

        
class pizzaria():
    def __init__(self):
        def func_cadastro():
            self.janela.destroy()
            cadastro()
        # Configuração da janela
        self.janela = Tk()
        self.janela.title('Controle de Pizzaria')
        self.janela.iconbitmap('icons/pizza.ico')
        self.janela.geometry('500x500')
        self.janela.resizable(width=False, height=False)

        # Aplicação principal
        self.btn_cadastro = Button(self.janela, border='0', bg='black', fg='white', text='Cadastro', command=func_cadastro).place(x=0, y=0, width=100, height=25)
        self.btn_pedidos = Button(self.janela, border='0', bg='black', fg='white', text='Pedidos').place(x=100, y=0, width=100, height=25)
        self.btn_consulta = Button(self.janela, border='0', bg='black', fg='white', text='Consulta').place(x=200, y=0, width=100, height=25)
        self.btn_Sabores = Button(self.janela, border='0', bg='black', fg='white', text='Sabores').place(x=300, y=0, width=100, height=25)
        self.btn_Sobre = Button(self.janela, border='0', bg='black', fg='white', text='Sobre nós').place(x=400, y=0, width=100, height=25)
        self.rodape = Frame(self.janela, border='0', bg='black').place(x=0, y=475, width=500, height=25)
        self.copyright = Label(self.rodape, border='0', bg='black', fg='white', text='SaloSecurity © 2019').place(x=390, y=475, height=25)        
        self.janela.mainloop()

class cadastro():
    def __init__(self):
        def voltar():
            self.janelac.destroy()
            pizzaria()
        def cadastrar():
            if str(self.nome.get()) and str(self.telefone.get()) and str(self.endereco.get()) and str(self.cpf.get()) != "":
                try:
                    c.execute("INSERT INTO clientes ('nome', 'telefone', 'endereço', 'cpf') VALUES ('{}', '{}', '{}', '{}')".format(str(self.nome.get()), str(self.telefone.get()), str(self.endereco.get()), str(self.cpf.get())))
                    con.commit()
                    self.janelac.destroy()
                    success('cadastro', 'Usuario cadastrado com sucesso na base de dados!')
                except:
                    self.janelac.destroy()
                    falid('cadastro', 'CPF já cadastro da base de dados!')
            else:
                self.janelac.destroy()
                falid('cadastro', 'Preencha todos os campos!')

        # Configurações da janela
        self.janelac = Tk()
        self.janelac.iconbitmap('icons/pizza.ico')
        self.janelac.resizable(width=False, height=False)
        self.janelac.title('Cadastro')
        self.janelac.geometry('260x270')

        # Variveis da ficha
        self.nome = StringVar()
        self.telefone = StringVar()
        self.endereco = StringVar()
        self.cpf = StringVar()

        # Ficha de cadastro
        self.photo = PhotoImage(file='icons/user.png')
        self.label = Label(self.janelac, image=self.photo).grid(row=0, column=1, pady=10)
        # campo nome
        self.lbl_nome = Label(self.janelac, text='Nome:').grid(row=1, column=0, padx=20)
        self.input_nome = Entry(self.janelac, textvariable=self.nome).grid(row=1, column=1)

        # campo telefone
        self.lbl_telefone = Label(self.janelac, text='Telefone:').grid(row=2, column=0)
        self.input_telefone = MaskedWidget(self.janelac, 'fixed', mask="(99) 99999-9999", textvariable=self.telefone).grid(row=2, column=1)

        # campo endereco
        self.lbl_endereco = Label(self.janelac, text='Endereço:').grid(row=3, column=0)
        self.input_endereco = Entry(self.janelac, textvariable=self.endereco).grid(row=3, column=1)

        # campo cpf
        self.lbl_cpf = Label(self.janelac, text='CPF:').grid(row=4, column=0)
        self.input_cpf =  MaskedWidget(self.janelac, 'fixed', mask="999.999.999-99", textvariable=self.cpf).grid(row=4, column=1)

        # Botao para cadastrar
        self.btn_cadastrar = Button(self.janelac, text='Cadastrar', border='0', bg='black', fg='white', command=cadastrar).place(x=20, y=220, width=100, height=25)
        self.btn_voltar = Button(self.janelac, text='Voltar', border='0', bg='black', fg='white', command=voltar).place(x=130, y=220, width=100, height=25)
        self.janelac.mainloop()
        
class autenticar():
    def __init__(self):
        def auth():
            # Verifica se os campos estão vazios
            if (str(self.nome.get()) and str(self.senha.get()) != None):
                c.execute('SELECT * FROM usuarios  WHERE nome = "{}" AND senha = "{}" LIMIT 1'.format(str(self.nome.get()), str(self.senha.get())))
                con.commit()
                resultado = c.fetchall()
                # Se a consulta teve resutado:
                if resultado:
                    self.login.destroy()
                    pizzaria()
                    # Senão
                else:
                    self.login.destroy()
                    falid('autenticar', 'Usuario não encontrado na base de dados!')
            else:
                pass

        self.login = Tk()
        self.login.title('Autenticação')
        self.login.iconbitmap('icons/pizza.ico')
        self.img_login = PhotoImage(file='icons/login.png')
        self.login.geometry('230x250')
        self.login.resizable(width=False, height=False)

        # Menu de login   
        self.label = Label(self.login, image=self.img_login).grid(row=0, column=1, pady=10)
        # campo nome
        self.nome = StringVar()
        self.lbl_nome = Label(self.login, text='Usuario:').grid(row=1, column=0, padx=10)
        self.input_nome = Entry(self.login, textvariable=self.nome).grid(row=1, column=1)

        # campo senha
        self.senha = StringVar()
        self.lbl_nome = Label(self.login, text='Senha:').grid(row=2, column=0, padx=10)
        self.input_nome = Entry(self.login, textvariable=self.senha, show='*').grid(row=2, column=1, pady=5)


        # Botao para cadastrar
        self.btn_cadastrar = Button(self.login, text='Logar', command=auth).grid(row=3, column=1, pady=20, ipadx=20)
        

autenticar()
