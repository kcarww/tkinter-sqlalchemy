from infra.configs.connection import DBConnectionHandler
from infra.entitities.alunos import Alunos


class AlunosRepository:
    def select(self):
        with DBConnectionHandler() as db:
            alunos = db.session.query(Alunos).all()
            return alunos

    def select_like(self, var):
        with DBConnectionHandler() as db:
            alunos = db.session.query(Alunos).filter(Alunos.nome.like(f'%{var}%'))
            return alunos

    def insert(self, nome, idade, curso, nota):
        with DBConnectionHandler() as db:
            aluno = Alunos(nome=nome, idade=idade, curso=curso, nota=nota)
            db.session.add(aluno)
            db.session.commit()


    def update(self, nome, idade, curso, nota, matricula):
        with DBConnectionHandler() as db:
            aluno = db.session.query(Alunos).filter(Alunos.matricula == matricula).one()
            aluno.nome = nome
            aluno.idade = idade
            aluno.curso = curso
            aluno.nota = nota
            db.session.add(aluno)
            db.session.commit()

    def delete(self, matricula):
        with DBConnectionHandler() as db:
            aluno = db.session.query(Alunos).filter(Alunos.matricula == matricula).one()
            db.session.delete(aluno)
            db.session.commit()
