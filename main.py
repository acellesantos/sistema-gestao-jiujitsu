import os

def exibir_menu(faixa):
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=" * 40)
    print(f"🥋 SISTEMA DE GESTÃO JIU-JITSU - FAIXA {faixa.upper()}")
    print("=" * 40)
    
    # ⚪ Permissão Geral (Faixa Branca e acima)
    print("[1] Visualizar Horários e Competições")
    
    # 🔵 Permissão de Instrutor/Secretaria (Faixa Azul e acima)
    if faixa.lower() in ['azul', 'roxa', 'marrom', 'preta']:
        print("[2] Cadastrar / Atualizar Alunos")
        print("[3] Verificar Vagas Disponíveis")
        
    # 🟤 Permissão Financeira (Faixa Marrom e acima)
    if faixa.lower() in ['marrom', 'preta']:
        print("[4] Fluxo de Caixa e Fornecedores")
        print("[5] Disparar Mensagens de Cobrança")
        
    # ⚫ Permissão Total (Faixa Preta)
    if faixa.lower() == 'preta':
        print("[6] [ADMIN] Configurações do Sistema e Permissões")
        
    print("[0] Sair")
    print("=" * 40)

if __name__ == "__main__":
    # Simulando o login de um usuário para demonstração
    # No futuro, isso virá de uma tela de login real
    faixa_usuario = input("Digite a cor da sua faixa para testar o sistema (branca, azul, marrom, preta): ")
    exibir_menu(faixa_usuario)