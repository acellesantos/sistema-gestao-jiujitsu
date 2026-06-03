import sqlite3

def conectar():
    return sqlite3.connect("academia_jiujitsu.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # 1. Tabela de Alunos (A que já tínhamos)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cpf TEXT UNIQUE NOT NULL,
        data_nascimento TEXT NOT NULL,
        idade INTEGER NOT NULL,
        telefone TEXT NOT NULL,
        endereco TEXT NOT NULL,
        faixa TEXT NOT NULL,
        status_pagamento TEXT DEFAULT 'Em dia',
        consentimento_lgpd TEXT NOT NULL,
        nome_responsavel TEXT,
        cpf_responsavel TEXT,
        telefone_responsavel TEXT
    )
    """)

    # 2. NOVA Tabela de Usuários do Sistema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL,
        faixa TEXT NOT NULL
    )
    """)

    # 3. Cria um usuário Mestre padrão se a tabela estiver vazia (Para você não perder o acesso!)
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (username, senha, faixa) VALUES ('marcelle', 'admin', 'preta')")

    conn.commit()
    conn.close()

# --- FUNÇÕES DE ALUNOS ---
def salvar_aluno(dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO alunos (
            nome, cpf, data_nascimento, idade, telefone, endereco, faixa, 
            consentimento_lgpd, nome_responsavel, cpf_responsavel, telefone_responsavel
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
        conn.commit()
        return True, "✅ Matrícula realizada com sucesso!"
    except sqlite3.IntegrityError:
        return False, "❌ Erro: Este CPF já está cadastrado no sistema."
    finally:
        conn.close()

def listar_todos_alunos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, faixa, status_pagamento, telefone FROM alunos")
    alunos = cursor.fetchall()
    conn.close()
    return alunos

def atualizar_status_pagamento(aluno_id, novo_status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE alunos SET status_pagamento = ? WHERE id = ?", (novo_status, aluno_id))
    conn.commit()
    conn.close()

# --- NOVAS FUNÇÕES DE USUÁRIOS (LOGIN E CADASTRO) ---
def validar_login(username, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT faixa FROM usuarios WHERE username = ? AND senha = ?", (username, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def cadastrar_usuario(username, senha, faixa):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (username, senha, faixa) VALUES (?, ?, ?)", (username, senha, faixa))
        conn.commit()
        return True, f"✅ Usuário '{username}' cadastrado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "❌ Erro: Esse nome de usuário já existe."
    finally:
        conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()
    # Não puxamos a senha por segurança, só o ID, nome e faixa
    cursor.execute("SELECT id, username, faixa FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

def atualizar_usuario(user_id, username, senha, faixa):
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Se a pessoa digitou uma senha nova, atualiza tudo. Se não, mantém a senha antiga.
        if senha.strip() != "":
            cursor.execute("UPDATE usuarios SET username = ?, senha = ?, faixa = ? WHERE id = ?", (username, senha, faixa, user_id))
        else:
            cursor.execute("UPDATE usuarios SET username = ?, faixa = ? WHERE id = ?", (username, faixa, user_id))
        conn.commit()
        return True, f"✅ Usuário '{username}' atualizado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "❌ Erro: Esse nome de usuário já pertence a outra pessoa."
    finally:
        conn.close()

def deletar_usuario(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def criar_tabela_pagamentos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pagamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            aluno TEXT NOT NULL,
            valor TEXT NOT NULL,
            data TEXT NOT NULL,
            status TEXT NOT NULL,
            forma_pagamento TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def registrar_pagamento(aluno, valor, forma, data, status):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO pagamentos (aluno, valor, data, status, forma_pagamento)
        VALUES (?, ?, ?, ?, ?)
    """, (aluno, valor, data, status, forma))
    conn.commit()
    conn.close()

def listar_pagamentos():
    # Garante que a tabela exista antes de tentar ler
    criar_tabela_pagamentos()
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, aluno, valor, data, status, forma_pagamento FROM pagamentos ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def criar_tabela_turmas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            dias TEXT NOT NULL,
            horario TEXT NOT NULL,
            professor TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_turma(nome, dias, horario, professor):
    criar_tabela_turmas()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO turmas (nome, dias, horario, professor)
        VALUES (?, ?, ?, ?)
    """, (nome, dias, horario, professor))
    conn.commit()
    conn.close()

def listar_turmas():
    criar_tabela_turmas()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, dias, horario, professor FROM turmas ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados