# Lista na memória para guardar os alunos enquanto o sistema estiver rodando
# (No futuro, isso aqui vai virar um arquivo de Banco de Dados real!)
banco_alunos = [
    {"nome": "Marcelle Santos", "faixa": "roxa", "status_pagamento": "Em dia"},
    {"nome": "Carlos Silva", "faixa": "branca", "status_pagamento": "Atrasado"},
]

def cadastrar_aluno():
    print("\n--- 🥋 NOVO CADASTRO DE ALUNO ---")
    nome = input("Nome completo do aluno: ").strip()
    faixa = input("Cor da faixa (branca, azul, roxa, marrom, preta): ").strip().lower()
    
    # Todo aluno novo entra com o pagamento "Em dia" por padrão
    novo_aluno = {
        "nome": nome,
        "faixa": faixa,
        "status_pagamento": "Em dia"
    }
    
    banco_alunos.append(novo_aluno)
    print(f"✅ Aluno {nome} cadastrado com sucesso!")
    input("\nPressione Enter para voltar ao menu...")

def listar_alunos():
    print("\n--- 👥 LISTA DE ALUNOS CADASTRADOS ---")
    if not banco_alunos:
        print("Nenhum aluno cadastrado ainda.")
    else:
        # Loop para mostrar os alunos de forma organizada
        for idx, aluno in enumerate(banco_alunos, start=1):
            print(f"{idx}. {aluno['nome']} | Faixa: {aluno['faixa'].capitalize()} | Status: {aluno['status_pagamento']}")
            
    input("\nPressione Enter para voltar ao menu...")