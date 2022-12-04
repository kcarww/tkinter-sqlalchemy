from infra.repository.alunos_repository import AlunosRepository

repo = AlunosRepository()

# repo.insert("Carlos", 30, "Python", 10)

dados = repo.select()

for aluno in dados:
    print(aluno.nome)