from datetime import date
from calendar import isleap
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox

import psycopg2

control_speds = Tk()

class Functions():
    def limpar_tela(self):
        self.entry_id.delete(0, END)
        self.entry_client.delete(0, END)
        self.entry_system.delete(0, END)
        self.entry_date_registro.delete(0, END)
        self.entry_status_activity.delete(0, END)
        self.entry_observation.delete("1.0", END)

    def conectar_bd(self):

        self.conn = psycopg2.connect(host='localhost',
                                     database='CONTROLE',
                                     user='postgres',
                                     password='123')
        print("Iniciando conexão")
        self.cursor = self.conn.cursor()
        print("Conectado ao Banco de Dados")

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conectar_bd()
        print("Banco de dados conectado")

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS controle(
                            id INTEGER PRIMARY KEY,
                            cliente VARCHAR(200) NOT NULL,
                            sistema VARCHAR(100) NOT NULL,
                            data_registro DATE NOT NULL,
                            status BOOLEAN,
                            observacao VARCHAR(500) NOT NULL
                        );
                    """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def select_bd(self):
        self.list.delete(*self.list.get_children())
        self.conectar_bd()
        self.cursor.execute("""
                            SELECT id, cliente, sistema, data_registro, status, observacao 
                            FROM controle 
                            ORDER BY sistema ASC;
                            """)

        searchTar = self.cursor.fetchall()
        print(searchTar)

        lista_melhorada = []

        for i in searchTar:
            aux = []
            for k in range(0, len(i)):
                if k == 3:
                    aux.append(
                        '{}/{}/{}'.format(i[k].day, i[k].month, i[k].year))
                    # print(type(i[k].day))
                    pass
                elif k == 4:
                    if i[k] == True:
                        aux.append("Completa")
                        pass
                    else:
                        aux.append("Incompleta")
                        pass
                else:
                    aux.append(i[k])
            lista_melhorada.append(aux)

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista_melhorada:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.desconecta_bd()

    def cadastrarTarefa(self):
        self.client = self.entry_client.get()
        self.system = self.entry_system.get()
        self.date_registro = self.entry_date_registro.get()
        self.status = self.entry_status_activity.get()
        self.observation = self.entry_observation.get("1.0",END)

        if self.status == 'Completa':
            self.status = True
        else:
            self.status = False

        self.conectar_bd()
        self.cursor.execute("""
                                    SELECT id, cliente, sistema, data_registro, status, observacao 
                                    FROM controle 
                                    ORDER BY id ASC;
                                    """)
        lista = self.cursor.fetchall()
        id = 0

        if len(lista) != 0:
            for i in lista:
                id = i[0]


        self.cursor.execute("""
                       INSERT INTO controle (id, cliente, sistema, data_registro, status, observacao)
                        VALUES (%s, %s, %s, %s, %s, %s)""", (id+1, self.client, self.system, self.date_registro, self.status, self.observation))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def OnDoubleClick(self, event):
        self.limpar_tela()
        self.list.selection()

        for n in self.list.selection():
            col1, col2, col3, col4, col5, col6 = self.list.item(n, 'values')
            self.entry_id.insert(END, col1)
            self.entry_client.insert(END, col2)
            self.entry_system.insert(END, col3)
            self.entry_date_registro.insert(END, col4)
            self.entry_status_activity.insert(END, col5)
            self.entry_observation.insert(END, col6)

    def delete_client(self):
        self.id = self.entry_id.get()
        self.client = self.entry_client.get()
        self.system = self.entry_system.get()
        self.date_registro = self.entry_date_registro.get()
        self.status = self.entry_status_activity.get()
        self.observation = self.entry_observation.get("1.0", END)


        self.conectar_bd()
        self.cursor.execute("""DELETE FROM controle WHERE id = %s """, (self.id, ))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_bd()

    def update_client(self):
        self.id = self.entry_id.get()
        self.client = self.entry_client.get()
        self.system = self.entry_system.get()
        self.date_registro = self.entry_date_registro.get()
        self.status = self.entry_status_activity.get()
        self.observation = self.entry_observation.get("1.0", END)

        if self.status == 'Completa':
            self.status = True
        else:
            self.status = False

        self.conectar_bd()
        self.cursor.execute("""
                        UPDATE  controle SET cliente = %s, sistema = %s, data_registro = %s, status = %s, observacao = %s
                        WHERE id = %s""", (self.client, self.system, self.date_registro, self.status, self.observation, self.id))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def search_complete(self):
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.status = self.entry_status_activity.get()

        if self.status == 'Completa':
            self.status = True
        else:
            self.status = False

        self.cursor.execute("""
                        SELECT id, cliente, sistema, data_registro, status, observacao 
                        FROM controle
                        WHERE status = TRUE
                        ORDER BY cliente ASC
                        """, (self.status))
        lista = self.cursor.fetchall()
        print(lista)

        for i in lista:
            self.list.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()

    def search_incomplete(self):
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.cursor.execute("""
                                SELECT id, cliente, sistema, data_registro, status, observacao 
                                FROM controle
                                WHERE status = False
                                ORDER BY cliente ASC
                                """, (self.status))
        lista = self.cursor.fetchall()

        for i in lista:
            self.list.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()

    def search_totals(self):
        self.conectar_bd()
        self.list.delete(*self.list.get_children())
        self.data = 0
        self.month = 0
        self.year = 0

        self.date_finish = self.entry_date_finish.get()

        self.month = self.date_finish[3:5]
        self.year = self.date_finish[6:10]

        self.data_inicial = '{}/{}/{}'.format(self.year, self.month, 1)
        self.data_inicial = '{}/{}/{}'.format(1, self.month, self.year)
        self.dia_fev = 0
        self.year = int(self.year)
        self.month = int(self.month)

        if isleap(self.year):
            self.dia_fev = 29
        else:
            self.dia_fev = 28

        if self.month == 1:
            self.data_final = '{}/{}/{}'.format(31, self.month, self.year)
        elif self.month == 2:
            self.data_final = '{}/{}/{}'.format(self.dia_fev, self.month, self.year)
        elif self.month == 3:
            self.data_final = '{}/{}/{}'.format(31, self.month, self.year)
        elif self.month == 4:
            self.data_final = '{}/{}/{}'.format(30, self.month, self.year)
        elif self.month == 5:
            self.data_final = '{}/{}/{}'.format(31, self.month, self.year)
        elif self.month == 6:
            self.data_final = '{}/{}/{}'.format(30, self.month, self.year)
        elif self.month == 7:
            self.data_final = '{}/{}/{}'.format(31, self.month, self.year)
        elif self.month == 8:
            self.data_final = '{}/{}/{}'.format(31, self.month, self.year)
        elif self.month == 9:
            self.data_final = '{}/{}/{}'.format(30, self.month, self.year)
        elif self.month == 10:
            self.data_final = '{}/{}/{}'.format(31, self.month, self.year)
        elif self.month == 11:
            self.data_final = '{}/{}/{}'.format(30, self.month, self.year)
        else:
            self.data_final = '{}/{}/{}'.format(31, self.month, self.year)

        self.cursor.execute("""
                                SELECT cliente, sistema, data_registro, data_finalizado, observacao 
                                FROM controle
                                WHERE data_finalizado BETWEEN %s and %s
                                ORDER BY cliente ASC
                                """, (self.data_inicial, self.data_final))
        lista = self.cursor.fetchall()
        lista_melhorada2 = []
        for i in lista:
            aux = []
            for k in range(0, len(i)):
                if k == 2 or k == 3:
                    aux.append(
                        '{}/{}/{}'.format(i[k].day, i[k].month, i[k].year))
                    # print(type(i[k].day))
                    pass
                else:
                    aux.append(i[k])
            lista_melhorada2.append(aux)

        for i in lista_melhorada2:
            self.list.insert("", END, values=i)
        self.limpar_tela()
        self.desconecta_bd()
class Controler(Functions):

    color_buttons = "Gray"
    color_home = "LightSteelBlue"
    color_frames = "Gainsboro"
    color_names = "Black"
    def __init__(self):
        self.control_speds = control_speds
        self.tela()
        self.frames_home()
        self.create_labels()
        self.create_buttons()
        self.frame_list_activity()
        self.montaTabelas()
        self.select_bd()
        self.center(self.control_speds)
        self.control_speds.mainloop()

    def tela(self):
        self.control_speds.title("Controle Semanal")
        self.control_speds.configure(background= self.color_home)
        self.control_speds.geometry("750x700")
        self.control_speds.resizable(False, False)
        self.control_speds.minsize(width= 750, height= 700)


    def center(self, page):
        """ FUNÇÃO RESPONSAVEL POR CENTRALIZAR AS PAGES NA TELA"""

        page.withdraw()
        page.update_idletasks()  # Update "requested size" from geometry manager

        x = (page.winfo_screenwidth() - page.winfo_reqwidth()) / 4
        y = (page.winfo_screenheight() - page.winfo_reqheight()) / 4
        page.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        page.deiconify()

    def format_date_registro(self, event=None):

        """ ESSE CÓDIGO É RESPONSAVEL POR COLOCAR OS PONTOS E O TRAÇO DE UM CPF AUTOMATICAMENTE
        EU PRECISO ALTERAR NELE PARA COLOCAR SOMENTE AS BARRAS DAS DATAS.
        LINK DO STACKOVERFLOW: https://pt.stackoverflow.com/questions/492705/criando-um-entry-formatado-para-cpf-em-python-tkinter
        """

        text = self.entry_date_registro.get().replace("/", "")[:8]
        new_text = ""

        if event.keysym.lower() == "backspace": return

        for index in range(len(text)):

            if not text[index] in "0123456789": continue
            if index in [1, 3]:
                new_text += text[index] + "/"
            # elif index == 8:
            #     new_text += text[index] + "-"
            else:
                new_text += text[index]

        self.entry_date_registro.delete(0, "end")
        self.entry_date_registro.insert(0, new_text)

    def format_date_finish(self, event=None):

        """ ESSE CÓDIGO É RESPONSAVEL POR COLOCAR OS PONTOS E O TRAÇO DE UM CPF AUTOMATICAMENTE
        EU PRECISO ALTERAR NELE PARA COLOCAR SOMENTE AS BARRAS DAS DATAS.
        LINK DO STACKOVERFLOW: https://pt.stackoverflow.com/questions/492705/criando-um-entry-formatado-para-cpf-em-python-tkinter
        """

        text2 = self.entry_date_finish.get().replace("/", "")[:8]
        new_text2 = ""

        if event.keysym.lower() == "backspace": return

        for index in range(len(text2)):

            if not text2[index] in "0123456789": continue
            if index in [1, 3]:
                new_text2 += text2[index] + "/"
            else:
                new_text2 += text2[index]

        self.entry_date_finish.delete(0, "end")
        self.entry_date_finish.insert(0, new_text2)

    def frames_home(self):

        self.frame_information = Frame(self.control_speds, bd= 4, bg= self.color_frames,
                                       highlightbackground= "Black", highlightthickness= 1)
        self.frame_information.place(rely= 0.01, relx= 0.024, relwidth= 0.95, relheight= 0.2)

        self.frame_activity = Frame(self.control_speds, bd= 4, bg= self.color_frames,
                                    highlightbackground= "Black", highlightthickness= 1)
        self.frame_activity.place(rely= 0.22, relx= 0.024, relwidth= 0.95, relheight= 0.75)

    def create_labels(self):
        self.lb_title = Label(self.frame_information, text= "CONTROLE SEMANAL", font= "-weight bold -size 15", bg= self.color_frames, fg= self.color_names)
        self.lb_title.place(rely= 0.01, relx= 0.32, relwidth= 0.3, relheight= 0.2)

        self.lb_id = Label(self.frame_information, text= "Id", font= "-weight bold -size 10", bg= self.color_frames, fg= self.color_names)
        self.lb_id.place(rely= 0.08, relx= 0.01, relwidth= 0.015, relheight= 0.1)

        self.entry_id = Entry(self.frame_information)
        self.entry_id.place(rely= 0.2, relx= 0.01, relwidth= 0.025)

        self.lb_client = Label(self.frame_information, text= "Cliente", font= "-weight bold -size 10", bg= self.color_frames, fg= self.color_names)
        self.lb_client.place(rely= 0.08, relx= 0.05, relwidth= 0.065, relheight= 0.1)

        self.entry_client = Entry(self.frame_information)
        self.entry_client.place(rely= 0.2, relx= 0.052, relwidth= 0.13)


        self.lb_system = Label(self.frame_information, text= "Sistema", font= "-weight bold -size 10", bg= self.color_frames, fg= self.color_names)
        self.lb_system.place(rely= 0.08, relx= 0.215, relwidth= 0.073, relheight= 0.1)

        self.entry_system = Entry(self.frame_information)
        self.entry_system.place(rely= 0.2, relx= 0.215, relwidth=0.08)


        self.lb_date_registro = Label(self.frame_information, text= "Data Registro", font= "-weight bold -size 10", bg= self.color_frames, fg= self.color_names)
        self.lb_date_registro.place(rely= 0.4, relx= 0.05, relwidth= 0.122, relheight= 0.1)

        self.entry_date_registro = Entry(self.frame_information)
        self.entry_date_registro.place(rely= 0.52, relx= 0.052, relwidth= 0.122)
        self.entry_date_registro.bind("<KeyRelease>", self.format_date_registro)

        self.lb_status_activity = Label(self.frame_information, text= "Status Atividade", font= "-weight bold -size 10", bg= self.color_frames, fg= self.color_names)
        self.lb_status_activity.place(rely= 0.4, relx= 0.215, relwidth= 0.145, relheight= 0.1)

        self.entry_status_activity = Combobox(self.frame_information, values=['Completa', 'Incompleta'])
        self.entry_status_activity.place(rely= 0.52, relx= 0.215, relwidth= 0.122)


        self.lb_observation = Label(self.frame_information, text= "Anotações", font= "-weight bold -size 10", bg= self.color_frames, fg= self.color_names)
        self.lb_observation.place(rely= 0.08, relx= 0.65, relwidth= 0.095, relheight= 0.1)

        self.entry_observation = Text(self.frame_information)
        self.entry_observation.place(rely= 0.2, relx= 0.65, relwidth= 0.32, relheight= 0.5)

    def create_buttons(self):
        self.bt_cadastrar = Button(self.frame_information, text= "Cadastrar",
                                  background= self.color_buttons,
                                  bd= 4, font= "-weight bold -size 10", command= self.cadastrarTarefa)
        self.bt_cadastrar.place(rely= 0.72, relx= 0.01, relwidth= 0.1, relheight= 0.2)


        self.bt_update = Button(self.frame_information, text= "Atualizar",
                                background= self.color_buttons, bd= 4, font= "-weight bold -size 10",
                                command= self.update_client)
        self.bt_update.place(rely= 0.72, relx= 0.13, relwidth= 0.09, relheight= 0.2)


        self.bt_delete = Button(self.frame_information, text= "Excluir",
                                background= self.color_buttons, bd= 4, font= "-weight bold -size 10",
                                command= self.delete_client)
        self.bt_delete.place(rely= 0.72, relx= 0.24, relwidth= 0.075, relheight= 0.2)


        self.bt_search_finish = Button(self.frame_information, text= "Completos",
                                       background= self.color_buttons, bd= 4, font= "-weight bold -size 10",
                                       command= self.search_complete)
        self.bt_search_finish.place(rely= 0.74, relx= 0.73, relwidth= 0.108, relheight= 0.2)


        self.bt_search_registry = Button(self.frame_information, text= "Incompletos",
                                        background= self.color_buttons, bd= 4, font= "-weight bold -size 10",
                                        command= self.search_incomplete)
        self.bt_search_registry.place(rely= 0.74, relx= 0.853, relwidth= 0.12, relheight= 0.2)


        self.bt_search_total = Button(self.frame_information, text= "Todos",
                                      background= self.color_buttons, bd= 4, font= "-weight bold -size 10",
                                      command= self.select_bd)
        self.bt_search_total.place(rely= 0.74, relx= 0.65, relwidth= 0.065, relheight= 0.2)

        self.bt_exit = Button(self.frame_information, text= "Sair", background= self.color_buttons, bd= 4,
                              font= "-weight bold -size 10", command= self.control_speds.destroy)
        self.bt_exit.place(rely= 0.72, relx= 0.335, relwidth= 0.075, relheight= 0.2)

    def frame_list_activity(self):
        self.list = ttk.Treeview(self.frame_activity, height= 3, columns= ("col1", "col2", "col3", "col4", "col5", "col6"))

        self.list.heading("#0", text= "")
        self.list.heading("#1", text= "Id")
        self.list.heading("#2", text= "Cliente")
        self.list.heading("#3", text= "Sistema")
        self.list.heading("#4", text= "Data Registro")
        self.list.heading("#5", text= "Status")
        self.list.heading("#6", text= "Anotações")

        self.list.column("#0", width=1)
        self.list.column("#1", width= 8)
        self.list.column("#2", width= 45)
        self.list.column("#3", width= 32)
        self.list.column("#4", width= 33)
        self.list.column("#5", width= 38)
        self.list.column("#6", width= 310)

        self.list.place(rely= 0.01, relx= 0.01, relwidth= 0.96, relheight= 0.98)

        self.scrollList = Scrollbar(self.frame_activity, orient= "vertical")
        self.list.configure(yscroll= self.scrollList.set)
        self.scrollList.place(relx= 0.97, rely= 0.01, relwidth= 0.02, relheight= 0.98)
        self.list.bind("<Double-1>", self.OnDoubleClick)

Controler()