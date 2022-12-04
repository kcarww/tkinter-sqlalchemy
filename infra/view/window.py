from tkinter import *
from tkinter import messagebox as tmsg
from tkinter import ttk
from infra.repository.alunos_repository import AlunosRepository

class Janela:
    def __init__(self):
        self.repo = AlunosRepository()
        self.window = Tk()
        self.window.geometry("500x480+500+150")
        self.window.title("Tela de cadastro")
        self.window.resizable(False, False)

        # CONFIG COLUMNS
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=10)

        # PANEL
        self.panel = PanedWindow(self.window)
        self.panel_footer = PanedWindow(self.window)

        # LABELS
        self.lbl_matricula = Label(self.window, text="Matricula: ", font="Verdana 12 bold")
        self.lbl_nome = Label(self.window, text="Nome: ", font="Verdana 12 bold")
        self.lbl_idade = Label(self.window, text="Idade: ", font="Verdana 12 bold")
        self.lbl_curso = Label(self.window, text="Curso: ", font="Verdana 12 bold")
        self.lbl_nota = Label(self.window, text="Nota: ", font="Verdana 12 bold")
        self.lbl_buscar = Label(self.panel_footer, text="Buscar(Nome): ", font="Verdana 12 bold")

        # ENTRIES
        self.txt_matricula = Entry(self.window, state='disabled')
        self.txt_nome = Entry(self.window, width=28)
        self.txt_idade = Entry(self.window)
        self.txt_nota = Entry(self.window)

        self.var = StringVar()
        self.var.trace("w", lambda name, index, mode, var=self.var: self.callback(var))
        self.txt_buscar = Entry(self.panel_footer, textvariable=self.var, width=35)

        # COMBOBOX CURSOS
        self.cursos = ["Dev Fullstack", "Metaverso", "Marketing", "Design"]
        self.lista_cursos = ttk.Combobox(self.window, values=self.cursos)

        # TREEVIEW
        self.tabela = ttk.Treeview(self.window, columns=("matricula", "nome", "idade", "curso", "nota"),
                                   show="headings")

        self.tabela.column('matricula', minwidth=0, width=50)
        self.tabela.column('nome', minwidth=0, width=50)
        self.tabela.column('idade', minwidth=0, width=50)
        self.tabela.column('curso', minwidth=0, width=50)
        self.tabela.column('nota', minwidth=0, width=50)

        self.tabela.heading("matricula", text="Matricula")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("idade", text="Idade")
        self.tabela.heading("curso", text="Curso")
        self.tabela.heading("nota", text="Nota")


        # BIND
        self.tabela.bind('<ButtonRelease-1>', self.tabela_click)

        # LABELS GRID
        self.lbl_matricula.grid(row=0, column=0, sticky=W)
        self.lbl_nome.grid(row=1, column=0, sticky='W')
        self.lbl_idade.grid(row=2, column=0, sticky='W')
        self.lbl_curso.grid(row=3, column=0, sticky='W')
        self.lbl_nota.grid(row=4, column=0, sticky='W')
        self.lbl_buscar.grid(row=0, column=0, sticky='W')

        # COMBOBOX GRID
        self.lista_cursos.grid(row=3, column=1, sticky=W)

        # BUTTONS
        self.btn_cadastrar = Button(self.panel, text="Cadastrar", command=self.inserir)
        self.btn_atualizar = Button(self.panel, text="Alterar", command=self.atualizar)
        self.btn_excluir = Button(self.panel, text="Excluir", command=self.excluir)

        # ENTRIES GRID
        self.txt_matricula.grid(row=0, column=1, sticky=W)
        self.txt_nome.grid(row=1, column=1, sticky=W)
        self.txt_idade.grid(row=2, column=1, sticky=W)
        self.txt_nota.grid(row=4, column=1, sticky=W)


        self.txt_buscar.grid(row=0, column=1)

        # TABELA GRID
        self.tabela.grid(row=6, column=1, sticky=W, pady=10)

        # PANEL GRID
        self.panel.grid(row=5, column=1, sticky=W, pady=10)
        self.panel_footer.grid(row=7, column=0, columnspan=2, sticky=W)

        # BTN GRID
        self.btn_cadastrar.grid(row=0, column=1, sticky=W, padx=10)
        self.btn_atualizar.grid(row=0, column=2, padx=10)
        self.btn_excluir.grid(row=0, column=3, padx=10)

        # CHAMANDO OS MÉTODOS
        self.listar()

        self.window.mainloop()

    def inserir(self):
        nome = self.txt_nome.get()
        idade = int(self.txt_idade.get())
        curso = self.lista_cursos.get()
        nota = float(self.txt_nota.get())

        self.repo.insert(nome, idade, curso, nota)
        tmsg.showinfo("Cadastrado", "Aluno Cadastrado Com Sucesso!")
        self.limparCampos()
        self.limparLista()
        self.listar()

    def atualizar(self):
        matricula = self.txt_matricula.get()
        nome = self.txt_nome.get()
        idade = int(self.txt_idade.get())
        curso = self.lista_cursos.get()
        nota = float(self.txt_nota.get())

        opcao = tmsg.askokcancel("Deseja atualizar?", "Deseja alterar os dados do aluno?")
        if opcao:
            self.repo.update(nome, idade, curso, nota, matricula)
            tmsg.showinfo("Atualizado", "Dados atualizados com sucesso!")
            self.limparCampos()
            self.limparLista()
            self.listar()



    def listar(self):
        if self.txt_buscar.get() == "":
            alunos = self.repo.select()
        else:
            alunos = self.repo.select_like(self.txt_buscar.get())

        self.limparLista()
        for aluno in alunos:
            self.tabela.insert("", "end", values=(aluno.matricula, aluno.nome, aluno.idade, aluno.curso, aluno.nota))

    def excluir(self):
        matricula = self.txt_matricula.get()

        opcao = tmsg.askokcancel("Tem certeza?", "Deseja deletar o aluno?")
        if opcao:
            self.repo.delete(matricula)
            tmsg.showinfo("Excluído", "Aluno deletado com sucesso!")
            self.limparCampos()
            self.limparLista()
            self.listar()

    def tabela_click(self, event):
        self.limparCampos()
        selecionado = self.tabela.selection()[0]
        aluno = self.tabela.item(selecionado, "values")

        self.txt_matricula.config(state="normal")
        self.txt_matricula.insert(0, aluno[0])
        self.txt_matricula.config(state="disabled")

        self.txt_nome.insert(0, aluno[1])
        self.txt_idade.insert(0, aluno[2])
        self.lista_cursos.set(aluno[3])
        self.txt_nota.insert(0, aluno[4])

    def limparCampos(self):
        self.txt_matricula.config(state="normal")
        self.txt_matricula.delete(0, "end")
        self.txt_matricula.config(state="disabled")
        self.txt_nome.delete(0, "end")
        self.txt_idade.delete(0, "end")
        self.txt_nota.delete(0, "end")

    def limparLista(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

    def callback(self, var):
        self.listar()




j = Janela()
# j.limparLista()
