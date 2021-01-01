from tkinter import Tk, messagebox
from explorador import Explorador
from editor import Editor
from menu import MyMenu
import os


class App:
    local = str('/')
    abri = os.path.abspath(os.path.basename('./'))

    def __init__(self):
        self.app = Tk()
        self.app.geometry('500x500')
        self.ex = Explorador(self.app)
        self.ex.bind('<Double-Button-1>', self.abrir)
        self.editor = Editor(self.app)
        self.menu = MyMenu(self.app, self.app.children)
        self.app.bind('<Control_L><n>', self.menu.abrirNovo)
        self.app.bind('<Control_L><o>', self.menu.abrirArquivo)
        self.app.bind('<Control_L><Shift_L><P>', self.menu.abrirPasta)
        self.app.bind('<Control_L><Shift_L><S>', self.menu.salvarComo)
        self.app.bind('<Control_L><s>', self.menu.salvar)
        self.app.bind('<Control_L><q>', self.sair)
        self.app.config(menu=self.menu)
        self.app.mainloop()

    def sair(self, e=None):
        msg = messagebox.askyesno(title='Deseja sair', message='Realmente deseja sair?')
        if msg:
            self.app.destroy()
        return

    def abrir(self, e=None):
        self.local = self.local + ('/' + self.ex.selection()[0])
        try:
            lugar = f'{self.abri}{self.local}'
            with open(lugar, 'r', encoding='utf-8') as fl:
                self.editor.texto.insert('1.0', fl.read())
        except:
            if not os.path.isdir(self.abri + '/' + self.local):
                self.local = str()

        print(lugar)
        

if __name__ == '__main__':
    App()