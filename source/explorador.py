from tkinter import ttk, Tk, messagebox
import tkinter as tk
from PIL import ImageTk, Image
import os
import sys


class Explorador(ttk.Treeview):
    cargs = len(sys.argv)
    print(sys.argv)
    if cargs > 1:
        print(sys.argv)
        CAMINHO_COMPLETO = sys.argv[1]
    else:
        CAMINHO_COMPLETO = os.path.abspath(os.path.dirname('./'))
    print(CAMINHO_COMPLETO)
    ESTA_PASTA = os.path.basename(CAMINHO_COMPLETO)
    GUARDA_DIRETORIOS = dict()
    GUARDA_ICONES = dict()
    selecionado = None

    def __init__(self, parent):
        self.parent = parent
        super(Explorador, self).__init__(master=self.parent)
        self.heading('#0', text=self.ESTA_PASTA)
        self.estilo = ttk.Style(self)
        self.estilo.theme_use('clam')
        self.estilo.configure(
            'Treeview', backgound='#21222c', foreground='#ffffff',
            fieldbackground='#21222c', rowheight=20
        )
        self.estilo.map(
            'Treeview', background=[
                ('selected', '#313341'), 
                ('!selected', '#21222c')
            ],
            foreground=[
                ('selected', '#ffffff'),
                ('!selected', '#fefefe')
            ]
        )
        self.bind('<<TreeviewOpen>>', self.abrir)
        self.bind('<<TreeviewClose>>', self.fechar)
        self.lerDiretorios()
        self.mostrar()
        self.pack(side=tk.LEFT, anchor=tk.W, fill=tk.Y)

    # // ler os diretorios do projeto

    def lerDiretorios(self):
        self.arquivos = os.listdir(self.CAMINHO_COMPLETO)
        self.GUARDA_DIRETORIOS['arquivos'] = list()
        for arqs in self.arquivos:
            if os.path.isdir(arqs):
                self.GUARDA_DIRETORIOS[arqs] = list()

        for arqs in self.arquivos:
            if not os.path.isdir(arqs):
                self.GUARDA_DIRETORIOS['arquivos'].append(arqs)

        for arqs in self.GUARDA_DIRETORIOS.keys():
            caminho = self.CAMINHO_COMPLETO + f'/{arqs}'
            if os.path.isdir(caminho):
                self.arquivos = os.listdir(caminho)
                for ar in self.arquivos:
                    self.GUARDA_DIRETORIOS[arqs].append(ar)

    # // carrega os primeiros arquivos e pastas

    def mostrar(self):
        if not self.selecionado:
            self.selecionado = ''
        for valores in self.GUARDA_DIRETORIOS.keys():
            if os.path.isdir(valores):
                self.GUARDA_ICONES[valores] = ImageTk.PhotoImage(
                    Image.open('./images/folder.png')
                )
                self.insert(
                    '', tk.END, valores, text=valores,
                    image=self.GUARDA_ICONES[valores], open=False
                )
            else:
                for val in self.GUARDA_DIRETORIOS['arquivos']:
                    print(self.showIcones(val))
                    cam = self.CAMINHO_COMPLETO + '/' + self.selecionado
                    self.GUARDA_ICONES[val] = ImageTk.PhotoImage(
                        Image.open(f'./images/{self.showIcones(val, cam)}')
                    )
                    self.insert(
                        '', tk.END, val, text=val, 
                        image=self.GUARDA_ICONES[val]
                    )

    # // acionado quando clicado para abrir diretorios

    def abrir(self, e):
        self.selecionado = self.selection()[0]
        if os.path.isdir(self.selecionado):
            cam     = self.CAMINHO_COMPLETO + '/' + self.selecionado
            subs    = os.listdir(cam)
            for x in subs:
                self.GUARDA_ICONES[x] = ImageTk.PhotoImage(
                    Image.open(f'./images/{self.showIcones(x, cam)}')
                )
                self.insert(
                    self.selecionado, 'end', x, text=x,
                    image=self.GUARDA_ICONES[x], open=False, tags=('filhos')
                )
        else:
            pass
        self.tag_configure('filhos', background='#000000')

    # // apos clicado em fechar diretorio é chamado para evitar bugs 

    def fechar(self, e):
        item = self.selection()[0]
        indice = self.index(item)
        if os.path.isdir(item):
            self.delete(item)
        self.insert(
            '', indice, item, text=item, 
            image=self.GUARDA_ICONES[item]
        )

    # // assicia as extensoes aos seus respectivos icones

    def showIcones(self, arq, pasta=''):
        self.icones = {
            '.py'  : 'python.png',       '.pyw' : 'python.png',
            '.png' : 'imagem.png',       '.svg' : 'svg.png',
            '.jpg' : 'imagem.png',       '.rb'  : 'pedra-preciosa.png',
            '.ps1' : 'file.png',         '.txt' : 'txt.png',
            '.json': 'json-file.png',    '.html': 'html-5.png',       
            '.css' : 'css.png',          '.sh'  : 'gnu-bash.png',     
            '.php' : 'php.png',          '.bat' : 'file.png',         
            '.js'  : 'javascript.png',   ''     : 'newspaper.png'
        }
        for ic in list(self.icones.keys()):
            if ic in arq or ic.upper() in arq:
                return self.icones[ic]
            else:
                cam = pasta + '/' + arq
                if os.path.isdir(cam):
                    return 'folder.png'
