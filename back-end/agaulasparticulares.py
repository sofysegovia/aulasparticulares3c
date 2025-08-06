from datetime import datetime, timedelta

class Usuario:
    def __init__(self, id, nome, email, senha, tipo):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha
        self.tipo = tipo
        self.data_cadastro = datetime.now()

class Professor:
    def __init__(self, id, id_usuario, materia, valor_aula):
        self.id = id
        self.id_usuario = id_usuario
        self.materia = materia
        self.valor_aula = valor_aula
        self.horarios_disponiveis = []

class Aluno:
    def __init__(self, id, id_usuario):
        self.id = id
        self.id_usuario = id_usuario
        self.aulas_agendadas = []

class Aula:
    def __init__(self, id, id_professor, id_aluno, data_hora, duracao):
        self.id = id
        self.id_professor = id_professor
        self.id_aluno = id_aluno
        self.data_hora = data_hora
        self.duracao = duracao
        self.status = "agendada"

db_usuarios = []
db_professores = []
db_alunos = []
db_aulas = []

def criar_usuario(nome, email, senha, tipo):
    for usuario in db_usuarios:
        if usuario.email == email:
            print("Erro: Este email já está cadastrado!")
            return None
    
    novo_id = len(db_usuarios) + 1
    novo_usuario = Usuario(novo_id, nome, email, senha, tipo)
    db_usuarios.append(novo_usuario)
    print(f"Usuário {nome} criado com sucesso!")
    return novo_usuario

def tornar_professor(id_usuario, materia, valor_aula):
    usuario = next((u for u in db_usuarios if u.id == id_usuario), None)
    
    if not usuario:
        print("Erro: Usuário não encontrado!")
        return None
    
    novo_id = len(db_professores) + 1
    novo_prof = Professor(novo_id, id_usuario, materia, valor_aula)
    db_professores.append(novo_prof)
    print(f"Professor {usuario.nome} cadastrado com sucesso!")
    return novo_prof

def tornar_aluno(id_usuario):
    usuario = next((u for u in db_usuarios if u.id == id_usuario), None)
    
    if not usuario:
        print("Erro: Usuário não encontrado!")
        return None
    
    novo_id = len(db_alunos) + 1
    novo_aluno = Aluno(novo_id, id_usuario)
    db_alunos.append(novo_aluno)
    print(f"Aluno {usuario.nome} cadastrado com sucesso!")
    return novo_aluno

def adicionar_horario_professor(id_professor, data_hora):
    professor = next((p for p in db_professores if p.id == id_professor), None)
    
    if not professor:
        print("Erro: Professor não encontrado!")
        return False
    
    professor.horarios_disponiveis.append(data_hora)
    print("Horário adicionado com sucesso!")
    return True

def agendar_aula(id_professor, id_aluno, data_hora, duracao):
    professor = next((p for p in db_professores if p.id == id_professor), None)
    if not professor:
        print("Erro: Professor não encontrado!")
        return None
    
    aluno = next((a for a in db_alunos if a.id == id_aluno), None)
    if not aluno:
        print("Erro: Aluno não encontrado!")
        return None
    
    if data_hora not in professor.horarios_disponiveis:
        print("Erro: Professor não está disponível neste horário!")
        return None
    
    novo_id = len(db_aulas) + 1
    nova_aula = Aula(novo_id, id_professor, id_aluno, data_hora, duracao)
    db_aulas.append(nova_aula)
    aluno.aulas_agendadas.append(nova_aula)
    professor.horarios_disponiveis.remove(data_hora)
    print("Aula agendada com sucesso!")
    return nova_aula

def listar_usuarios():
    print("\n--- LISTA DE USUÁRIOS ---")
    for usuario in db_usuarios:
        print(f"ID: {usuario.id} | Nome: {usuario.nome} | Tipo: {usuario.tipo}")

def listar_professores():
    print("\n--- LISTA DE PROFESSORES ---")
    for prof in db_professores:
        usuario = next((u for u in db_usuarios if u.id == prof.id_usuario), None)
        if usuario:
            print(f"ID: {prof.id} | Nome: {usuario.nome} | Matéria: {prof.materia} | Valor: R${prof.valor_aula:.2f}")

def listar_alunos():
    print("\n--- LISTA DE ALUNOS ---")
    for aluno in db_alunos:
        usuario = next((u for u in db_usuarios if u.id == aluno.id_usuario), None)
        if usuario:
            print(f"ID: {aluno.id} | Nome: {usuario.nome} | Aulas: {len(aluno.aulas_agendadas)}")

def listar_aulas():
    print("\n--- LISTA DE AULAS ---")
    for aula in db_aulas:
        professor = next((p for p in db_professores if p.id == aula.id_professor), None)
        aluno = next((a for a in db_alunos if a.id == aula.id_aluno), None)
        
        nome_prof = "Desconhecido"
        nome_aluno = "Desconhecido"
        
        if professor:
            usuario_prof = next((u for u in db_usuarios if u.id == professor.id_usuario), None)
            if usuario_prof:
                nome_prof = usuario_prof.nome
                
        if aluno:
            usuario_aluno = next((u for u in db_usuarios if u.id == aluno.id_usuario), None)
            if usuario_aluno:
                nome_aluno = usuario_aluno.nome
                
        print(f"Aula #{aula.id} | {aula.data_hora.strftime('%d/%m/%Y %H:%M')}")
        print(f"   Professor: {nome_prof} | Aluno: {nome_aluno} | Status: {aula.status}\n")

def fazer_login(email, senha):
    for usuario in db_usuarios:
        if usuario.email == email and usuario.senha == senha:
            return usuario
    return None

def menu_principal():
    while True:
        print("\n=== PLATAFORMA DE AULAS ===")
        print("1. Fazer login")
        print("2. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            email = input("Email: ")
            senha = input("Senha: ")
            usuario = fazer_login(email, senha)
            
            if usuario:
                if usuario.tipo == "admin":
                    menu_admin(usuario)
                elif usuario.tipo == "professor":
                    menu_professor(usuario)
                elif usuario.tipo == "aluno":
                    menu_aluno(usuario)
            else:
                print("Email ou senha incorretos!")
        
        elif opcao == "2":
            print("Saindo do sistema...")
            break
        
        else:
            print("Opção inválida!")

def menu_admin(usuario):
    while True:
        print(f"\n=== MENU ADMIN ({usuario.nome}) ===")
        print("1. Cadastrar usuário")
        print("2. Tornar usuário professor")
        print("3. Tornar usuário aluno")
        print("4. Listar usuários")
        print("5. Listar professores")
        print("6. Listar alunos")
        print("7. Listar aulas")
        print("8. Voltar")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome: ")
            email = input("Email: ")
            senha = input("Senha: ")
            tipo = input("Tipo (admin/professor/aluno): ")
            criar_usuario(nome, email, senha, tipo)
        
        elif opcao == "2":
            listar_usuarios()
            id_usuario = int(input("ID do usuário: "))
            materia = input("Matéria que ensina: ")
            valor = float(input("Valor por aula: R$"))
            tornar_professor(id_usuario, materia, valor)
        
        elif opcao == "3":
            listar_usuarios()
            id_usuario = int(input("ID do usuário: "))
            tornar_aluno(id_usuario)
        
        elif opcao == "4":
            listar_usuarios()
        
        elif opcao == "5":
            listar_professores()
        
        elif opcao == "6":
            listar_alunos()
        
        elif opcao == "7":
            listar_aulas()
        
        elif opcao == "8":
            break
        
        else:
            print("Opção inválida!")

def menu_professor(usuario):
    professor = next((p for p in db_professores if p.id_usuario == usuario.id), None)
    
    if not professor:
        print("Erro: Perfil de professor não encontrado!")
        return
    
    while True:
        print(f"\n=== MENU PROFESSOR ({usuario.nome}) ===")
        print("1. Adicionar horário disponível")
        print("2. Ver minhas aulas")
        print("3. Voltar")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            data = input("Data (DD/MM/AAAA): ")
            hora = input("Hora (HH:MM): ")
            try:
                data_hora = datetime.strptime(f"{data} {hora}", "%d/%m/%Y %H:%M")
                adicionar_horario_professor(professor.id, data_hora)
            except ValueError:
                print("Formato de data/hora inválido!")
        
        elif opcao == "2":
            print("\n--- SUAS AULAS ---")
            aulas_prof = [a for a in db_aulas if a.id_professor == professor.id]
            for aula in aulas_prof:
                aluno = next((a for a in db_alunos if a.id == aula.id_aluno), None)
                nome_aluno = "Desconhecido"
                if aluno:
                    usuario_aluno = next((u for u in db_usuarios if u.id == aluno.id_usuario), None)
                    if usuario_aluno:
                        nome_aluno = usuario_aluno.nome
                print(f"Aula #{aula.id} com {nome_aluno} em {aula.data_hora.strftime('%d/%m/%Y %H:%M')}")
        
        elif opcao == "3":
            break
        
        else:
            print("Opção inválida!")

def menu_aluno(usuario):
    aluno = next((a for a in db_alunos if a.id_usuario == usuario.id), None)
    
    if not aluno:
        print("Erro: Perfil de aluno não encontrado!")
        return
    
    while True:
        print(f"\n=== MENU ALUNO ({usuario.nome}) ===")
        print("1. Ver minhas aulas")
        print("2. Voltar")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print("\n--- SUAS AULAS ---")
            for aula in aluno.aulas_agendadas:
                professor = next((p for p in db_professores if p.id == aula.id_professor), None)
                nome_prof = "Desconhecido"
                if professor:
                    usuario_prof = next((u for u in db_usuarios if u.id == professor.id_usuario), None)
                    if usuario_prof:
                        nome_prof = usuario_prof.nome
                print(f"Aula #{aula.id} com {nome_prof} em {aula.data_hora.strftime('%d/%m/%Y %H:%M')}")
        
        elif opcao == "2":
            break
        
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    admin = criar_usuario("Admin", "admin@escola.com", "123", "admin")
    prof1 = criar_usuario("João Professor", "joao@escola.com", "123", "professor")
    aluno1 = criar_usuario("Maria Aluna", "maria@escola.com", "123", "aluno")
    
    tornar_professor(prof1.id, "Matemática", 50.0)
    tornar_aluno(aluno1.id)
    
    amanha = datetime.now() + timedelta(days=1)
    adicionar_horario_professor(1, amanha.replace(hour=14, minute=0, second=0, microsecond=0))
    
    menu_principal()
