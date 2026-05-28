import os
from alunos import cadastrar_aluno, listar_alunos
# 🆕 Importando as funções do módulo financeiro
from financeiro import disparar_mensagens_cobranca 

def exibir_menu(faixa):
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=" * 40)
        print(f"🥋 GESTÃO JIU-JITSU - PERMISSÃO: {faixa.upper()}")
        print("=" * 40)
        
        print("[1] Visualizar Horários e Competições")
        
        if faixa.lower() in ['azul', 'roxa', 'marrom', 'preta']:
            print("[2] Cadastrar Novo Aluno")
            print("[3] Listar Alunos Matriculados")
            
        # 🟤 Apenas Faixa Marrom e Preta podem acessar o financeiro
        if faixa.lower() in ['marrom', 'preta']:
            print("[4] Disparar Mensagens de Cobrança (WhatsApp)")
            
        print("[0] Sair do Sistema")
        print("=" * 40)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n🕒 Horários: Seg a Sex às 19h | Sáb às 10h (Treino Livre).")
            input("\nPressione Enter para continuar...")
            
        elif opcao == "2" and faixa.lower() in ['azul', 'roxa', 'marrom', 'preta']:
            cadastrar_aluno()
            
        elif opcao == "3" and faixa.lower() in ['azul', 'roxa', 'marrom', 'preta']:
            listar_alunos()
            
        # 🆕 Nova opção conectada!
        elif opcao == "4" and faixa.lower() in ['marrom', 'preta']:
            disparar_mensagens_cobranca()
            
        elif opcao == "0":
            print("\nOss! Sistema encerrado.")
            break
        else:
            print("\n❌ Opção inválida ou você não tem permissão para isso!")
            input("\nPressione Enter para tentar novamente...")

if __name__ == "__main__":
    faixa_usuario = input("Digite sua faixa para login (branca, azul, roxa, marrom, preta): ")
    exibir_menu(faixa_usuario)