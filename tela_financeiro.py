import customtkinter as ctk
import banco
from datetime import datetime

class TelaFinanceiro(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, faixa_logada):
        super().__init__(master, fg_color="transparent")
        self.usuario_logado = usuario_logado
        self.faixa_logada = faixa_logada
        
        # Cores da Identidade Visual
        self.COR_PRIMARIA = "#CC0000"
        self.COR_FUNDO = "#1A1A1A"
        
        # --- DIVISÃO DA TELA (Esquerda = Filtros e Lista | Direita = Lançamentos) ---
        self.frame_esquerda = ctk.CTkFrame(self, width=400, fg_color="transparent")
        self.frame_esquerda.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        self.frame_direita = ctk.CTkFrame(self, width=350, fg_color=self.COR_FUNDO, border_color=self.COR_PRIMARIA, border_width=1)
        self.frame_direita.pack(side="right", fill="y", padx=20, pady=10)

        # ----------------- LADO ESQUERDO (CONTROLE DE FLUXO) -----------------
        ctk.CTkLabel(self.frame_esquerda, text="💰 Histórico de Recebimentos", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Barra de Filtros Rápidos
        self.frame_filtros = ctk.CTkFrame(self.frame_esquerda, fg_color="transparent")
        self.frame_filtros.pack(fill="x", pady=5)
        
        ctk.CTkButton(self.frame_filtros, text="Todos", width=80, fg_color="#333333", command=lambda: self.filtrar_pagamentos("todos")).pack(side="left", padx=2)
        ctk.CTkButton(self.frame_filtros, text="Em dia", width=80, fg_color="green", command=lambda: self.filtrar_pagamentos("pago")).pack(side="left", padx=2)
        ctk.CTkButton(self.frame_filtros, text="Atrasados", width=80, fg_color=self.COR_PRIMARIA, command=lambda: self.filtrar_pagamentos("atrasado")).pack(side="left", padx=2)

        # Lista com Scroll
        self.lista_scroll = ctk.CTkScrollableFrame(self.frame_esquerda)
        self.lista_scroll.pack(fill="both", expand=True, pady=10)

        # ----------------- LADO DIREITO (BAIXA DE MENSALIDADE) -----------------
        ctk.CTkLabel(self.frame_direita, text="📝 Registrar Pagamento", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Menu para escolher o aluno (puxando dinamicamente do banco)
        ctk.CTkLabel(self.frame_direita, text="Selecione o Aluno:", text_color="white").pack(pady=(10,0))
        self.alunos_no_banco = [aluno[1] for aluno in banco.listar_todos_alunos()]
        
        if not self.alunos_no_banco:
            self.alunos_no_banco = ["Nenhum aluno cadastrado"]
            
        self.combo_aluno = ctk.CTkOptionMenu(self.frame_direita, values=self.alunos_no_banco, width=300, fg_color="#2b2b2b", button_color=self.COR_PRIMARIA)
        self.combo_aluno.pack(pady=5)
        
        self.entry_valor = ctk.CTkEntry(self.frame_direita, placeholder_text="Valor Pago (Ex: 150.00)", width=300)
        self.entry_valor.pack(pady=10)
        
        ctk.CTkLabel(self.frame_direita, text="Forma de Pagamento:", text_color="white").pack(pady=(10,0))
        self.combo_forma = ctk.CTkOptionMenu(self.frame_direita, values=["Pix", "Dinheiro", "Cartão de Crédito", "Cartão de Débito"], width=300, fg_color="#2b2b2b", button_color=self.COR_PRIMARIA)
        self.combo_forma.pack(pady=5)
        
        self.label_status = ctk.CTkLabel(self.frame_direita, text="")
        self.label_status.pack(pady=10)
        
        ctk.CTkButton(self.frame_direita, text="Confirmar Recebimento", command=self.confirmar_pagamento, width=300, fg_color=self.COR_PRIMARIA).pack(pady=20)

        self.recarregar_pagamentos()

    # ================= MÉTODOS LOGÍCOS =================

    def recarregar_pagamentos(self, filtro="todos"):
        widgets_destruidos = len(self.lista_scroll.winfo_children())
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()

        pagamentos_banco = banco.listar_pagamentos()
        
        print(f"\n--- [DEBUG] recarregar_pagamentos ---")
        print(f"Filtro ativo: '{filtro}'")
        print(f"Widgets limpos na tela: {widgets_destruidos}")
        print(f"Pagamentos lidos do Banco de Dados: {pagamentos_banco}")
            
        # Puxa os dados do banco (id, nome_aluno, valor, data, status, forma)
        # Se houver dados no banco, prioriza eles. Caso contrário, usa os mockados para teste.
        if pagamentos_banco:
            pagamentos = pagamentos_banco
            print(f"Exibindo dados reais do banco de dados (Total: {len(pagamentos)}).")
        else:
            pagamentos = [
                (1, "Carlos Gracie", "150.00", "01/06/2026", "Pago", "Pix"),
                (2, "Helio Silva", "150.00", "25/05/2026", "Atrasado", "Dinheiro"),
                (3, "Daiana Santos", "120.00", "02/06/2026", "Pago", "Pix")
            ]
            print(f"Nenhum pagamento no banco. Exibindo dados simulados/mockados (Total: {len(pagamentos)}).")
        
        itens_renderizados = 0
        for p in pagamentos:
            id_p, aluno, valor, data, status, forma = p
            
            # Normalização simples do status para compatibilidade de filtros ("Pago" -> "pago", etc)
            status_limpo = status.lower()
            
            if filtro != "todos" and status_limpo != filtro:
                continue
                
            linha = ctk.CTkFrame(self.lista_scroll, fg_color="#2B2B2B", border_color=self.COR_PRIMARIA, border_width=1)
            linha.pack(fill="x", pady=4, padx=4)
            
            cor_status = "green" if status_limpo == "pago" else self.COR_PRIMARIA
            
            ctk.CTkLabel(linha, text=f"👤 {aluno} | R$ {valor} ({forma})", text_color="white").pack(side="left", padx=10, pady=10)
            ctk.CTkLabel(linha, text=status.upper(), text_color=cor_status, font=ctk.CTkFont(weight="bold")).pack(side="right", padx=15, pady=10)
            itens_renderizados += 1
            
        print(f"Total de itens renderizados na interface: {itens_renderizados}")
        print(f"----------------------------------------\n")

    def filtrar_pagamentos(self, tipo):
        self.recarregar_pagamentos(filtro=tipo)

    def confirmar_pagamento(self):
        aluno = self.combo_aluno.get()
        valor = self.entry_valor.get().strip()
        forma = self.combo_forma.get()

        data_hoje = datetime.now().strftime("%d/%m/%Y")
        
        print(f"\n--- [DEBUG] confirmar_pagamento ---")
        print(f"Tentando registrar pagamento:")
        print(f"  Aluno: '{aluno}'")
        print(f"  Valor: '{valor}'")
        print(f"  Forma: '{forma}'")
        print(f"  Data:  '{data_hoje}'")
        
        if not valor or aluno == "Nenhum aluno cadastrado":
            print("Tentativa falhou: Valor inválido ou nenhum aluno cadastrado.")
            self.label_status.configure(text="❌ Insira um valor válido!", text_color=self.COR_PRIMARIA)
            print(f"------------------------------------\n")
            return
        
        banco.registrar_pagamento(aluno, valor, forma, data_hoje, "Pago")
        print("Pagamento inserido com sucesso no banco de dados via banco.registrar_pagamento()!")
            
        self.label_status.configure(text=f"✅ Recebimento de {aluno} registrado!", text_color="green")
        self.entry_valor.delete(0, 'end')
        
        print("Chamando self.recarregar_pagamentos() para atualizar a interface...")
        print(f"------------------------------------\n")
        self.recarregar_pagamentos()
