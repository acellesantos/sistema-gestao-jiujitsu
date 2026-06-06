import sqlite3
from datetime import datetime

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

def obter_aluno(aluno_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, nome, cpf, data_nascimento, idade, telefone, endereco, faixa, 
           consentimento_lgpd, nome_responsavel, cpf_responsavel, telefone_responsavel 
    FROM alunos WHERE id = ?
    """, (aluno_id,))
    aluno = cursor.fetchone()
    conn.close()
    return aluno

def atualizar_aluno(aluno_id, dados):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        UPDATE alunos SET
            nome = ?,
            cpf = ?,
            data_nascimento = ?,
            idade = ?,
            telefone = ?,
            endereco = ?,
            faixa = ?,
            consentimento_lgpd = ?,
            nome_responsavel = ?,
            cpf_responsavel = ?,
            telefone_responsavel = ?
        WHERE id = ?
        """, (*dados, aluno_id))
        conn.commit()
        return True, "✅ Matrícula atualizada com sucesso!"
    except sqlite3.IntegrityError:
        return False, "❌ Erro: Este CPF já está cadastrado em outro aluno."
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
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def validar_login(username, senha):
    # Regra de bypass para o usuário Master "admin"
    if username == "admin" and senha == "admin":
        return "preta" # Retorna faixa "preta" para acesso total

    conn = conectar()
    cursor = conn.cursor()
    senha_hash = hash_senha(senha) # Hash da senha digitada
    cursor.execute("SELECT faixa FROM usuarios WHERE username = ? AND senha = ?", (username, senha_hash))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def cadastrar_usuario(username, senha, faixa):
    conn = conectar()
    cursor = conn.cursor()
    try:
        senha_hash = hash_senha(senha) # Hash da senha antes de salvar
        cursor.execute("INSERT INTO usuarios (username, senha, faixa) VALUES (?, ?, ?)", (username, senha_hash, faixa))
        conn.commit()
        return True, f"✅ Usuário \'{username}\' cadastrado com sucesso!"
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
    # Impede a modificação do usuário Master "admin"
    if username.lower() == "admin":
        return False, "❌ Erro: O usuário mestre \'admin\' não pode ser modificado."

    conn = conectar()
    cursor = conn.cursor()
    try:
        # Se a pessoa digitou uma senha nova, atualiza tudo. Se não, mantém a senha antiga.
        if senha.strip() != "":
            senha_hash = hash_senha(senha) # Hash da nova senha
            cursor.execute("UPDATE usuarios SET username = ?, senha = ?, faixa = ? WHERE id = ?", (username, senha_hash, faixa, user_id))
        else:
            # Mantém a senha antiga (não atualiza o campo senha)
            cursor.execute("UPDATE usuarios SET username = ?, faixa = ? WHERE id = ?", (username, faixa, user_id))
        conn.commit()
        return True, f"✅ Usuário \'{username}\' atualizado com sucesso!"
    except sqlite3.IntegrityError:
        return False, "❌ Erro: Esse nome de usuário já pertence a outra pessoa."
    finally:
        conn.close()

def obter_usuario(user_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, senha, faixa FROM usuarios WHERE id = ?", (user_id,))
    usuario = cursor.fetchone()
    conn.close()
    return usuario


def deletar_usuario(user_id):
    conn = conectar()
    cursor = conn.cursor()
    
    # Verifica se é o usuário 'admin' antes de deletar
    cursor.execute("SELECT username FROM usuarios WHERE id = ?", (user_id,))
    usuario_db = cursor.fetchone()
    
    if usuario_db and usuario_db[0].lower() == "admin":
        conn.close()
        return False, "❌ Erro: O usuário mestre \'admin\' não pode ser excluído."

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True, "✅ Usuário excluído com sucesso!"

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
    
    connzzzz = conectar()
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

def criar_tabela_planos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS planos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor TEXT NOT NULL,
            duracao TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def cadastrar_plano(nome, valor, duracao):
    criar_tabela_planos()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO planos (nome, valor, duracao)
        VALUES (?, ?, ?)
    """, (nome, valor, duracao))
    conn.commit()
    conn.close()

def listar_planos():
    criar_tabela_planos()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, valor, duracao FROM planos ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()
    return dados

def salvar_permissoes_auditoria(usuario_alvo_id, permissoes_lista, admin_responsavel):
    conn = conectar()
    cursor = conn.cursor()
    
    # Cria a tabela de auditoria se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS auditoria_acessos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora TEXT,
            admin_responsavel TEXT,
            usuario_afetado_id INTEGER,
            acao TEXT
        )
    ''')
    
    # Registra o log
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    permissoes_str = ", ".join(permissoes_lista) if permissoes_lista else "Nenhuma"
    acao = f"Liberou permissões: [{permissoes_str}]"
    
    cursor.execute('''
        INSERT INTO auditoria_acessos (data_hora, admin_responsavel, usuario_afetado_id, acao)
        VALUES (?, ?, ?, ?)
    ''', (data_atual, admin_responsavel, usuario_alvo_id, acao))
    
    conn.commit()
    conn.close()
    
    print(f"\n[🚨 AUDITORIA] {data_atual} | Admin '{admin_responsavel}' {acao} para o usuário ID {usuario_alvo_id}")
    return True, "Permissões e Auditoria gravadas com sucesso!"

def listar_auditoria():
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Puxa do mais recente para o mais antigo
        cursor.execute('SELECT data_hora, admin_responsavel, acao FROM auditoria_acessos ORDER BY id DESC')
        registros = cursor.fetchall()
    except:
        registros = [] # Se a tabela não existir, não quebra o sistema
    conn.close()
    return registros

def listar_auditoria_por_usuario(usuario_alvo_id):
    conn = conectar()
    cursor = conn.cursor()
    # Busca apenas os logs onde o 'usuario_afetado_id' for o que selecionamos
    cursor.execute('''
        SELECT data_hora, admin_responsavel, acao 
        FROM auditoria_acessos 
        WHERE usuario_afetado_id = ? 
        ORDER BY id DESC
    ''', (usuario_alvo_id,))
    registros = cursor.fetchall()
    conn.close()
    return registros