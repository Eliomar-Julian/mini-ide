from tkinter import Text, ttk, Frame, font, Scrollbar, Listbox
import tkinter as tk

# // classe que constroi todos as opçoes da parte de ediçao da aplicação


class Editor(ttk.Notebook):
    COR_FUNDO = '#282a36'
    COR_FRENTE = '#ffffdd'

    def __init__(self, parent):
        self.parent = parent
        ttk.Notebook.__init__(self, master=self.parent)
        self.pack(expand=True, fill='both')
        self.bind('<Button><3>', self.criaMenuFlutuante)
        self.fonte = font.Font(
            family='Consolas', size=12, weight='normal', slant='roman'
        )
        self.criaAbas()
        self.rolagemHorizontal()
    
    # // cria o menu flutuante com o widget listbox...

    def criaMenuFlutuante(self, e):
        opcoes = [
            f'Fechar aba atual {" "*14} Ctrl+W', 
            f'Selecionar todo o texto{" "*3} Ctrl+A', 
            f'colar{" "*35} Ctrl+V', 
            f'copiar{" "*33} Ctrl+C',
            f'recortar{" "*30} Ctrl+X'
        ]
        self.menuFlutuante = Listbox(
            self, width=30, height=5, 
            bg=self.COR_FUNDO, 
            fg=self.COR_FRENTE
        )
        for x in range(len(opcoes)):
            self.menuFlutuante.insert(
                x, opcoes[x]
            )
        self.menuFlutuante.place(x=e.x, y=e.y)
        self.menuFlutuante.bind(
            '<Leave>', 
            self.fechaMenuFlutuante
        )
        self.menuFlutuante.bind(
            '<<ListboxSelect>>', 
            self.menuFlutuanteSelecao
        )
    
    # identifica o elemento clicado no menu flutuante 
    # e age de acordo com a selecao

    def menuFlutuanteSelecao(self, e=None):
        item = self.menuFlutuante.curselection()[0]
        print(item)
        if item == 0:
            aba = self.index('current')
            self.forget(aba)
        elif item == 1:
            self.selecionarTudo()
        elif item == 2:
            self.colar()
        elif item == 3:
            self.copiar()

    def copiar(self, e=None):
        self.texto.tag_delete('sels')
        texto = self.texto.get(1.0, 'end-1c')
        self.clipboard_clear()
        self.clipboard_append(texto)

    def colar(self):
        self.texto.insert('insert', self.clipboard_get())
        self.texto.tag_delete('sels')

    def recortar(self):
        texto = self.texto.get('1.0', 'end-1c')
        self.texto.delete('1.0', 'end')
        self.clipboard_append(texto)
        self.texto.tag_delete('sels')

    # fecha o menu flutuante quando mouse sai...

    def fechaMenuFlutuante(self, e):
        self.menuFlutuante.destroy()

    # cria as novas abas ao clica no menu ou ctrl+n...

    def criaAbas(self):
        self.frame = Frame(self, bg=self.COR_FUNDO)
        self.contaLinha = Text(
            self.frame, width=5, 
            bd=0, relief='flat', font=self.fonte,
            bg=self.COR_FUNDO, fg=self.COR_FRENTE
        )
        self.contaLinha.bind('<MouseWheel>', self.naoRolar)
        self.frame.pack(fill='both', expand=True)
        self.contaLinha.pack(side='left', anchor='w', fill='y')
        self.texto = Text(
            self.frame, bd=0, relief='flat', font=self.fonte,
            bg=self.COR_FUNDO, fg=self.COR_FRENTE, 
            insertbackground='#fff', wrap='none'
        )
        self.texto.focus_force()
        self.add(self.frame, text='aba')
        self.texto.pack(fill='both', side='left', expand=True)
        self.texto.bind('<KeyPress>', self.insereLinhas)
        self.texto.bind('<Tab>', self.espacosTab)
        self.texto.bind('<MouseWheel>', self.detectaRolagem)
        self.texto.bind('<Button><3>', self.criaMenuFlutuante)
        self.texto.bind('<Control_L><w>', self.fechaAba)
    
    # fecha aba atual com ctrl+w
    
    def fechaAba(self, e=None):
        aba = self.index('current')
        self.forget(aba)

    def selecionarTudo(self):
        self.texto.tag_add('sels', '1.0', 'end-1c')
        self.texto.tag_config('sels', background='blue')
        self.texto.mark_set('insert', '1.0')
        self.texto.see('insert')
        return 'break'

    # insere as linhas na lateral esquerda...

    def insereLinhas(self, e):
        self.tecla = e.char
        self.autoPar()
        if self.tecla in ['\'', '\"', '(', '{', '[']:
            return 'break'
        self.linhaAtual = float(self.texto.index('end-1c'))
        self.contaLinha.insert(
            self.linhaAtual + 1, str(int(self.linhaAtual)) + '\n'
        )
        self.deletaLinhas()
        self.texto.tag_delete('sels')

    # deleta as linhas sobresalentes....

    def deletaLinhas(self):
        self.contaLinha.delete(float(self.texto.index('end')), 'insert')
        self.contaLinha.see(float(self.texto.index('insert')) - 1)

    # transforma os TAB´s em 4 espaços...

    def espacosTab(self, e):
        self.texto.insert(self.texto.index('end-1c'), f'{" "*4}')
        return 'break'

    # autocompleta pares de delimitadores

    def autoPar(self):
        tam         = self.texto.index('end-1c')
        i           = tam.index('.')
        tam         = tam[i + 1:]
        pares       = ['\'', '\"', '(', '{', '[']
        fechaPares  = ['\'', '\"', ')', '}', ']']
        if self.tecla in pares:
            par = pares.index(self.tecla)
        else:
            return
        if len(tam) == 1:
            indice = '%.1f' %(float(self.texto.index('insert')))
        elif len(tam) == 2:
            indice = '%.2f' %(float(self.texto.index('insert')))
        elif len(tam) == 3:
            indice = '%.3f' %(float(self.texto.index('insert')))
        self.texto.mark_set('insert', indice)
        print(indice)
        self.texto.insert(indice, pares[par] +fechaPares[par])

    # detecta a rolagem da area de texto e indica 
    # a mesma para o contador de linhas para rolar junto

    def detectaRolagem(self, e):
        self.contaLinha.yview_scroll(int(-1*(e.delta/120)), 'units')
        print(int(-1*(e.delta)))

    # detecta se o comprimento da linha ja atingiu o maximo da lagura da
    # tela e rola automaticamente na horizontal

    def rolagemHorizontal(self):
        self.rolagem = Scrollbar(self.texto, orient='horizontal')
        self.rolagem.pack(side='bottom', fill='x')
        self.rolagem.configure(command=self.texto.xview)
        self.texto.configure(xscrollcommand=self.rolagem.set)

    # impede a rolagem do contador de linhas ao receber um 
    # evento de entrada e rolagem do mouse

    def naoRolar(self, e):
        return 'break'