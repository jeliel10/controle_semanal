from tkinter import *
from tkinter import ttk
import sqlite3

window_controler = Tk()

class Functions():
    def limpar_tela(self):
        self.entry_codigo.delete(0, END)
        self.entry_tarefa.delete(0, END)
        self.entry_cliente.delete(0, END)
        self.entry_status.delete(0, END)
        self.entry_ano.delete(0, END)
        self.entry_mes.delete(0, END)
        self.entry_dia.delete(0, END)

    def conectar_bd(self):
        self.conn = sqlite3.connect("controle_semanal.bd")
        self.cursor = self.conn.cursor()
        print("Conectado ao Banco de Dados")

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conectar_bd()
        print("Banco de dados conectado")

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS controle(
                            codigo INTEGER PRIMARY KEY,
                            tarefa VARCHAR(200) NOT NULL,
                            cliente VARCHAR(100),
                            status BOOLEAN,
                            ano INTEGER,
                            mes INTEGER,
                            dia INTEGER
                        );
                    """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def select_bd(self):
        self.list.delete(*self.list.get_children())
        self.conectar_bd()
        lista = self.cursor.execute("""
                            SELECT codigo, tarefa, cliente, status, ano, mes, dia 
                            FROM controle 
                            ORDER BY tarefa ASC;
                            """)
        for i in lista:
            self.list.insert("", END, values= i)
        self.desconecta_bd()

    def cadastrarTarefa(self):
        self.tarefa = self.entry_tarefa.get()
        self.cliente = self.entry_cliente.get()
        self.status = self.entry_status.get()
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()

        self.conectar_bd()
        self.cursor.execute("""
                        INSERT INTO controle (tarefa, cliente, status, ano, mes, dia)
                         VALUES (?, ?, ?, ?, ?, ?)""", (self.tarefa, self.cliente, self.status, self.ano, self.mes, self.dia))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def OnDoubleClick(self, event):
        self.limpar_tela()
        self.list.selection()

        for n in self.list.selection():
            col1, col2, col3, col4, col5, col6, col7 = self.list.item(n, 'values')
            self.entry_codigo.insert(END, col1)
            self.entry_tarefa.insert(END, col2)
            self.entry_cliente.insert(END, col3)
            self.entry_status.insert(END, col4)
            self.entry_ano.insert(END, col5)
            self.entry_mes.insert(END, col6)
            self.entry_dia.insert(END, col7)

    def delete_client(self):
        self.codigo = self.entry_codigo.get()
        self.tarefa = self.entry_tarefa.get()
        self.cliente = self.entry_cliente.get()
        self.status = self.entry_status.get()
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()

        self.conectar_bd()
        self.cursor.execute("""DELETE FROM controle WHERE codigo = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_bd()

    def update_client(self):
        self.codigo = self.entry_codigo.get()
        self.tarefa = self.entry_tarefa.get()
        self.cliente = self.entry_cliente.get()
        self.status = self.entry_status.get()
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()

        self.conectar_bd()
        self.cursor.execute("""
                        UPDATE  controle SET tarefa = ?, cliente = ?, status = ?, ano = ?, mes = ?, dia = ?
                        WHERE codigo = ?""", (self.tarefa, self.cliente, self.status, self.ano, self.mes, self.dia, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def search_client(self):
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        # self.entry_ano.insert(END, '%')
        # self.entry_mes.insert(END, '%')
        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.dia = self.entry_dia.get()

        self.cursor.execute("""
                        SELECT codigo, tarefa, cliente, status, ano, mes, dia 
                        FROM controle
                        WHERE ano = ? AND mes = ?  
                        ORDER BY dia ASC
                        """, (self.ano, self.mes))

        searchTar = self.cursor.fetchall()
        for i in searchTar:
            self.list.insert("", END, values= i)
        self.limpar_tela()
        self.desconecta_bd()

    def search_clint_status(self):
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.ano = self.entry_ano.get()
        self.mes = self.entry_mes.get()
        self.status = self.entry_status.get()

        self.cursor.execute("""
                    SELECT codigo, tarefa, cliente, status, ano, mes, dia
                    FROM controle
                    WHERE status = ?
                    """, (self.status,))

        searchTar = self.cursor.fetchall()
        for i in searchTar:
            self.list.insert("", END, values= i)
        self.limpar_tela()
        self.desconecta_bd()

class Controler(Functions):

    color_buttons = "DodgerBlue"
    def __init__(self):
        self.window_controler = window_controler
        self.tela()
        self.frames_da_tela()
        self.create_labels()
        self.create_buttons()
        self.list_frame_2()
        self.montaTabelas()
        self.select_bd()
        window_controler.mainloop()

    def tela(self):
        self.window_controler.title("Controle Semanal")
        self.window_controler.configure(background= "DarkBlue")
        self.window_controler.geometry("1200x900")
        self.window_controler.resizable(True, True)
        self.window_controler.minsize(width= 800, height= 600)

    def frames_da_tela(self):
        self.frame_3 = Frame(self.window_controler, bd=4, bg="DimGray",
                             highlightbackground="White", highlightthickness=5)
        self.frame_3.place(rely=0.01, relx=0.01, relwidth=0.98, relheight=0.08)

        self.frame_1 = Frame(self.window_controler, bd= 4, bg= "DimGray",
                             highlightbackground= "White", highlightthickness= 5)
        self.frame_1.place(rely= 0.1, relx= 0.01, relwidth= 0.98, relheight=0.3)

        self.frame_2 = Frame(self.window_controler, bd=4, bg="DimGray",
                             highlightbackground="White", highlightthickness=5)
        self.frame_2.place(rely=0.42, relx=0.01, relwidth=0.98, relheight=0.56)

    def create_labels(self):
        self.lb_codigo = Label(self.frame_1, text= "Código", font= 15)
        self.lb_codigo.place(rely= 0.01, relx= 0.4, relwidth= 0.045)

        self.entry_codigo = Entry(self.frame_1)
        self.entry_codigo.place(rely= 0.12, relx= 0.4, relwidth= 0.045, relheight= 0.07)

        self.lb_title = Label(self.frame_3, text= "CONTROLE SEMANAL", font= "-weight bold -size 28", bg= "DimGray", fg= "White")
        self.lb_title.place(rely= 0.01, relx= 0.01, relwidth= 0.98, relheight= 0.9)

        self.lb_tarefa = Label(self.frame_1, text= "Tarefa", font= 15)
        self.lb_tarefa.place(rely= 0.01, relx= 0.01, relwidth= 0.045)

        self.entry_tarefa = Entry(self.frame_1)
        self.entry_tarefa.place(rely= 0.12, relx= 0.01, relwidth= 0.2, relheight= 0.07)

        self.lb_cliente = Label(self.frame_1, text= "Cliente", font= 15)
        self.lb_cliente.place(rely= 0.25, relx= 0.01, relwidth= 0.045)

        self.entry_cliente = Entry(self.frame_1)
        self.entry_cliente.place(rely= 0.36, relx= 0.01, relwidth= 0.2, relheight= 0.07)

        self.lb_status = Label(self.frame_1, text= "Status", font= 15)
        self.lb_status.place(rely= 0.5, relx= 0.01, relwidth= 0.045)

        self.entry_status = Entry(self.frame_1)
        self.entry_status.place(rely= 0.61, relx= 0.01, relwidth= 0.2, relheight= 0.07)

        self.lb_ano = Label(self.frame_1, text= "Ano", font= 15)
        self.lb_ano.place(rely=0.01, relx= 0.3, relwidth= 0.045)

        self.entry_ano = Entry(self.frame_1)
        self.entry_ano.place(rely= 0.12, relx= 0.3, relwidth= 0.05, relheight= 0.07)

        self.lb_mes = Label(self.frame_1, text= "Mês", font= 15)
        self.lb_mes.place(rely= 0.25, relx= 0.3, relwidth= 0.045)

        self.entry_mes = Entry(self.frame_1)
        self.entry_mes.place(rely= 0.36, relx= 0.3, relwidth= 0.05, relheight= 0.07)

        self.lb_dia = Label(self.frame_1, text= "Dia", font= 15)
        self.lb_dia.place(rely= 0.50, relx= 0.3, relwidth= 0.045)

        self.entry_dia = Entry(self.frame_1)
        self.entry_dia.place(rely= 0.61, relx= 0.3, relwidth= 0.05, relheight= 0.07)

    def create_buttons(self):
        self.bt_cadastrar = Button(self.frame_1, text= "Cadastrar",
                                   background= self.color_buttons,
                                    bd= 3, command= self.cadastrarTarefa)
        self.bt_cadastrar.place(rely= 0.8, relx= 0.01, relwidth= 0.07, relheight= 0.1)

        self.bt_alterar = Button(self.frame_1, text="Alterar",
                                 background= self.color_buttons,
                                 bd= 3, command= self.update_client)
        self.bt_alterar.place(rely=0.8, relx=0.09, relwidth=0.07, relheight=0.1)

        self.bt_apagar = Button(self.frame_1, text="Apagar",
                                background= self.color_buttons,
                                bd= 3, command= self.delete_client)
        self.bt_apagar.place(rely=0.8, relx=0.17, relwidth=0.07, relheight=0.1)

        self.bt_buscar = Button(self.frame_1, text="Buscar",
                                background= self.color_buttons,
                                bd= 3, command= self.search_client)
        self.bt_buscar.place(rely=0.8, relx=0.3, relwidth=0.07, relheight=0.1)

        self.bt_limpar = Button(self.frame_1, text="Limpar",
                                background= self.color_buttons,
                                bd= 3, command= self.limpar_tela)
        self.bt_limpar.place(rely=0.8, relx=0.38, relwidth=0.07, relheight=0.1)

        self.bt_buscar_concluidos = Button(self.frame_1, text= "Buscar Status",
                                           background= self.color_buttons,
                                           bd= 3, command= self.search_clint_status)
        self.bt_buscar_concluidos.place(rely= 0.8, relx= 0.46, relwidth= 0.08, relheight= 0.1)

    def list_frame_2(self):
        self.list = ttk.Treeview(self.frame_2, height= 3, columns= ("col1", "col2", "col3", "col4", "col5", "col6", "col7"))

        self.list.heading("#0", text= "")
        self.list.heading("#1", text= "Código")
        self.list.heading("#2", text= "Tarefa")
        self.list.heading("#3", text= "Cliente")
        self.list.heading("#4", text= "Status")
        self.list.heading("#5", text= "Ano")
        self.list.heading("#6", text= "Mês")
        self.list.heading("#7", text= "Dia")

        self.list.column("#0", width=1)
        self.list.column("#1", width= 50)
        self.list.column("#2", width= 420)
        self.list.column("#3", width= 300)
        self.list.column("#4", width= 40)
        self.list.column("#5", width= 50)
        self.list.column("#6", width= 20)
        self.list.column("#7", width= 20)

        self.list.place(rely= 0.01, relx= 0.01, relwidth= 0.96, relheight= 0.98)

        self.scrollList = Scrollbar(self.frame_2, orient= "vertical")
        self.list.configure(yscroll= self.scrollList.set)
        self.scrollList.place(relx= 0.97, rely= 0.01, relwidth= 0.02, relheight= 0.98)
        self.list.bind("<Double-1>", self.OnDoubleClick)

Controler()