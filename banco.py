import sqlite3

def conectar():
    # Conecta ao arquivo de banco de dados (se não existir, ele cria na hora)
    return sqlite3.connect("academia_jiujitsu.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    
    # Criando a tabela de alunos com todos os campos que mapeamos
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
    conn.commit()
    conn.close()

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