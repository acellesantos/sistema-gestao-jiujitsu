# Importamos a lista de alunos lá do outro arquivo para podermos analisar os pagamentos
from alunos import banco_alunos

def verificar_inadimplentes():
    print("\n--- 💰 RELATÓRIO DE ALUNOS INADIMPLENTES ---")
    
    # Criamos uma lista filtrada apenas com quem está devendo
    atrasados = [aluno for aluno in banco_alunos if aluno["status_pagamento"] == "Atrasado"]
    
    if not atrasados:
        print("🎉 Excelente! Todos os alunos estão com a mensalidade em dia.")
        return []
    
    for idx, aluno in enumerate(atrasados, start=1):
        print(f"[{idx}] {aluno['nome']} | Faixa: {aluno['faixa'].capitalize()}")
        
    return atrasados

def disparar_mensagens_cobranca():
    # Primeiro, pegamos a lista de quem está devendo
    lista_cobranca = verificar_inadimplentes()
    
    if not lista_cobranca:
        input("\nPressione Enter para voltar ao menu...")
        return

    print("\n" + "="*40)
    print("📢 SIMULAÇÃO DE DISPARO DE WHATSAPP")
    print("="*40)
    print(f"Preparando envio para {len(lista_cobranca)} aluno(s)...")
    
    # Simulando o envio de mensagens personalizadas
    for aluno in lista_cobranca:
        # Texto da mensagem usando f-string para personalizar com o nome do aluno
        mensagem = (
            f"🥋 *Oss, {aluno['nome']}!*\n"
            f"Passando para lembrar que sua mensalidade da academia de Jiu-Jitsu está pendente. "
            f"Contamos com você no tatame! Fortaleça sua equipe e regularize sua situação. Tamo junto! 🔥"
        )
        print(f"\n📱 Enviando para o WhatsApp de {aluno['nome']}:")
        print(f'"{mensagem}"')
        print("-" * 30)
        
    print("\n✅ [Simulação] Todas as mensagens de cobrança foram geradas com sucesso!")
    input("\nPressione Enter para voltar ao menu...")