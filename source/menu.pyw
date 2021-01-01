from tkinter import Menu, filedialog, messagebox
import subprocess

#classe de barra de menu


class MyMenu(Menu):
    SALVAR = None
    SALVAR_COMO = None

    def __init__(self, parent, manipular):
        self.master = parent
        self.manipulador = manipular
        super(MyMenu, self).__init__(master=self.master)
        self.arquivo = Menu(self, tearoff=0)
        self.arquivo.add_command(
            label='Novo Arquivo', accelerator='Ctrl+N',
            command=self.abrirNovo
        )
        self.arquivo.add_command(
            label='Abrir Arquivo', accelerator='Ctrl+O',
            command=self.abrirArquivo
        )
        self.arquivo.add_command(
            label='Abrir pasta',
            accelerator='Ctrl+Shift+p', 
            command=self.abrirPasta
        )
        self.arquivo.add_separator()
        self.arquivo.add_command(
            label='Salvar', 
            accelerator='Ctrl+S'
        )
        self.arquivo.add_command(
            label='Salvar como', 
            accelerator='Ctrl+Shift+S'
        )
        self.arquivo.add_command(
            label='Sair', 
            accelerator='Ctrl+Q', 
            command=self.sair
        )
        self.add_cascade(label='Arquivo', menu=self.arquivo)
        
    # abre uma pasta de trabalho no editor
    
    def abrirPasta(self, e=''):
        arq = filedialog.askdirectory(title='Diretorio')
        self.master.destroy()
        subprocess.run(
            [
                'python.exe',
                '.\\source\\explorador.py', 
                f'{arq}'
            ]
        )

    # abre uma novo arquivo em uma nova aba

    def abrirNovo(self, e=''):
        self.manipulador['!editor'].criaAbas()
    
    # abre um arquivo para a edição

    def abrirArquivo(self, e=''):
        self.manipulador['!editor'].texto.delete(1.0, 'end')
        arq = filedialog.askopenfilename(title='Abrir')
        with open(arq, 'r', encoding='utf-8') as fl:
            abriu = fl.read()
            con = 0
            for x in abriu.split('\n'):
                con += 1
                self.manipulador[
                    '!editor'
                    ].contaLinha.insert(
                        'end', str(con) + '\n'
                        )
            self.manipulador['!editor'].texto.insert(1.0, abriu)

    # salva o arquivo em ediçao

    def salvar(self, e=None):
        if self.SALVAR:
            with open(self.SALVAR) as fl:
                texto = self.manipulador['!editor'].texto.get(1.0, 'end')
                fl.write(texto)
        else:
            self.salvarComo()

    # abre quando for a primeira vez que for salvo ou quando se deseja 
    # mudar o nome ou caminho do arquivo
    
    def salvarComo(self, e=None):
        arq = filedialog.asksaveasfilename()
        self.SALVAR = arq
        with open(arq, 'w', encoding='utf-8') as fl:
            texto = self.manipulador['!editor'].texto.get(1.0, 'end')
            fl.write(texto)

    # abre o dialogo de confirmação de saida da aplicação
    
    def sair(self, e=None):
        msg = messagebox.askyesno(title='Deseja sair', message='Realmente deseja sair?')
        if msg:
            self.master.destroy()
        return

        