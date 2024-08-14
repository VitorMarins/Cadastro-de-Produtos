from tkinter import *
from tkinter import ttk
import sqlite3
root = Tk()
class Func():
    def limpa_tela(self):
        self.cod_entry.delete(0, END)
        self.produto_entry.delete(0, END)
        self.quantidade_entry.delete(0, END)
        self.valor_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("produto.db")
        self.cursor = self.conn.cursor()
        print('Conectando ao Banco de Dados...')
    def desconecta_bd(self):
        self.conn.close(); 
        print("Desconectando do Banco de Dados.")
    def montaTabelas(self): # cria tabelas dentro do banco de dados
        self.conecta_bd()
        # Criar Tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS produto(
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                nome_produto CHARVAR(40) NOT NULL, 
                quantidade INTEGER(20),
                valor CHARVAR(40)
            );        
        """)
        self.conn.commit(); #Para validar as informações no db
        print("Banco de Dados criado!")
        self.desconecta_bd()
    def variaveis(self):#funcao criada para armazenar variaveis, em cada função chamo a funcao variaveis e não precisa repetir código. Evitar redundancia de código.
        self.cod = self.cod_entry.get()
        self.produto = self.produto_entry.get()
        self.quantidade = self.quantidade_entry.get()
        self.valor = self.valor_entry.get()
    def add_produto(self): # adiciona os valores ao banco de dados digitados na tela
        self.variaveis()
        self.conecta_bd() # conecta ao banco de dados
        self.cursor.execute(""" INSERT INTO produto(nome_produto, quantidade, valor)
         VALUES(?, ?, ?)""", (self.produto, self.quantidade, self.valor))
        self.conn.commit() # validar os dados
        self.desconecta_bd()
        self.select_lista()#sempre que ocorrer qq alteração na lista, esta sera atualizada
        self.limpa_tela()
    def select_lista(self):
        self.listaPro.delete(*self.listaPro.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_produto, quantidade, valor FROM produto 
        ORDER BY nome_produto ASC; """) # cod, produto, quantidade, valor
        for i in lista:
            self.listaPro.insert("", END, values=i)
        self.desconecta_bd()
    def OnDoubleClick(self, event):#funcao duplo clique, seleciona as informações.Sempre que tiver uma interação coloca event
        self.limpa_tela() #Caso tenha algo digitado lá em cima irá ser apagado
        self.listaPro.selection() #pega as informações da lista
        for n in self.listaPro.selection():# extrai os dados
            col1, col2, col3, col4 = self.listaPro.item(n, "values") #extrai os itens
            self.cod_entry.insert(END, col1)
            self.produto_entry.insert(END, col2)
            self.quantidade_entry.insert(END, col3)
            self.valor_entry.insert(END, col4)
    def deleta_produto(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" DELETE FROM produto WHERE cod = ? """, (self.cod,)),
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_tela()#limpa registro das entrys
        self.select_lista()#atualiza informação da treeview
    def altera_produto(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(''' UPDATE produto SET nome_produto = ?, quantidade = ?, valor = ? WHERE cod = ? ''', 
		(self.produto, self.quantidade, self.valor, self.cod ))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()
    def busca_produto(self):
        self.conecta_bd()
        self.listaPro.delete(*self.listaPro.get_children())#limpar nossa lista
        self.produto_entry.insert(END, '%') #Com insert acresceta-se um caracter coringa(%)vai permite busca com parte de texto digitado
        nome = self.produto_entry.get()
        self.cursor.execute('''
            SELECT cod, nome_produto, quantidade, valor FROM produto
            WHERE nome_produto LIKE '%s' ORDER BY nome_produto ASC
        ''' % nome) #LIKE vai fazer uma pesquisa onde tenha a informação na coluna nome_produto
        buscanomePRO = self.cursor.fetchall() # retorna as linhas do resultado da consulta em uma lista
        for i in buscanomePRO:
            self.listaPro.insert('', END, values=i)
            self.limpa_tela()
            self.desconecta_bd()
class Application(Func):
    def __init__(self):
        self.root = root
        self.tela()
        self.frame_de_tela()
        self.widgets_frame1()
        self.Lista_frame2()   # módulo para mostrar os clientes cadastrados no Banco de Dados
        self.montaTabelas()
        self.select_lista()
        #self.add_produto()
        root.mainloop()

    def tela(self):
        self.root.title('Cadastro de Produtos')
        self.root.configure(background='#1F364A')
        self.root.geometry('1000x500+700+200')
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=600)
        self.root.minsize(width=520, height=400)
    def frame_de_tela(self):
        self.frame1 = Frame(self.root, bd=10, bg='#E0E3EF',
                            highlightbackground='#195478', highlightthickness=6)
        # relative (rel) se refere a posição relativa dos objetos na tela
        # o valores váo de 0 a 1 - 0 é esquerda e 1 a direita
        self.frame1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame2 = Frame(self.root, bd=10, bg='#E0E3EF',
                            highlightbackground='#195478', highlightthickness=6)
        self.frame2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        # cria botão limpar
        self.bt_limpar = Button(self.frame1, text='Limpar', bd=2 ,bg='#4E9DE5',fg='white',
                                font=('Ubuntu',11), command=self.limpa_tela)
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão buscar
        self.bt_buscar = Button(self.frame1, text='Buscar', bd=2 ,bg='#4E9DE5',fg='white',
                                font=('Ubuntu',11), command=self.busca_produto)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão novo
        self.bt_novo = Button(self.frame1, text='Novo', bd=2, bg='#4E9DE5',fg='white'
                              ,font=('Ubuntu',11), command=self.add_produto)
        self.bt_novo.place(relx=0.55, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão alterar
        self.bt_alterar = Button(self.frame1, text='Alterar', bd=2, bg='#4E9DE5',fg='white',font=('Ubuntu',11), command=self.altera_produto)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        # cria botão apagar
        self.bt_apagar = Button(self.frame1, text='Apagar', bd=2, bg='#4E9DE5',fg='white'
                                ,font=('Ubuntu',11), command=self.deleta_produto)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)
        # criação dos Labels e  Entrada do Código
        self.lb_codigo = Label(self.frame1, text='Código',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_codigo.place(relx=0.05, rely=0.05)
        self.cod_entry = Entry(self.frame1, relief='groove')
        self.cod_entry.place(relx=0.05, rely=0.15, relwidth=0.085)
        # criação dos label e Entrada do Produto
        self.lb_produto = Label(self.frame1, text='Produto',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_produto.place(relx=0.05, rely=0.35)
        self.produto_entry = Entry(self.frame1, relief='groove')
        self.produto_entry.place(relx=0.05, rely=0.45, relwidth=0.85)
        # criação dos Labels e Entrada do Quantidade
        self.lb_quantidade = Label(self.frame1, text='Quantidade',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_quantidade.place(relx=0.05, rely=0.65)
        self.quantidade_entry = Entry(self.frame1, relief='groove')
        self.quantidade_entry.place(relx=0.05, rely=0.75, relwidth=0.4)
        # criação das Labels e Entrada de Valor
        self.lb_valor = Label(self.frame1, text='Valor',bg='#E0E3EF', font=('Ubuntu',11))
        self.lb_valor.place(relx=0.5, rely=0.65)
        self.valor_entry = Entry(self.frame1, relief='groove')
        self.valor_entry.place(relx=0.5, rely=0.75, relwidth=0.4)
    def Lista_frame2(self):
        # criação das colunas no Treeview
        self.listaPro = ttk.Treeview(self.frame2, height=3, column=("col1", "col2", "col3", "col4"))
        self.listaPro.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        # criação dos cabeçalhos das colunas - "#" número da coluna
        self.listaPro.heading("#0", text="")   # coluna "#0" deve ficar vazia
        self.listaPro.heading("#1", text="Código")
        self.listaPro.heading("#2", text="Produto")
        self.listaPro.heading("#3", text="Quantidade")
        self.listaPro.heading("#4", text="Valor")

        self.listaPro.column("#0", width=1)
        self.listaPro.column("#1", width=50)
        self.listaPro.column("#2", width=200)
        self.listaPro.column("#3", width=125)
        self.listaPro.column("#4", width=200)

        # barra de rolagem
        self.scroolLista = Scrollbar(self.frame2, orient='vertical')
        self.listaPro.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.03, relheight=0.85)
        self.listaPro.bind('<Double-1>', self.OnDoubleClick)#bind tipo de interação que será feito com a lista
Application()