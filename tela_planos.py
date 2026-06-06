import customtkinter as ctk
import banco

class TelaPlanos(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, faixa_logada):
        super().__init__(master, fg_color="transparent")
        
        self.COR_PRIMARIA = "#CC0000"
        self.COR_FUNDO = "#1A1A1A"
        
        # --- DIVISÃO DA TELA ---
        self.frame_esquerda = ctk.CTkFrame(self, width=400, fg_color="transparent")
        self.frame_esquerda.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        self.frame_direita = ctk.CTkFrame(self, width=350, fg_color=self.COR_FUNDO, border_color=self.COR_PRIMARIA, border_width=1)
        self.frame_direita.pack(side="right", fill="y", padx=20, pady=10)

        # ----------------- LADO ESQUERDO (LISTA DE PLANOS) -----------------
        ctk.CTkLabel(self.frame_esquerda, text="🏷️ Planos Ativos", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.lista_scroll = ctk.CTkScrollableFrame(self.frame_esquerda)
        self.lista_scroll.pack(fill="both", expand=True, pady=10)

        # ----------------- LADO DIREITO (CRIAR NOVO PLANO) -----------------
        ctk.CTkLabel(self.frame_direita, text="📝 Novo Plano", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.entry_nome = ctk.CTkEntry(self.frame_direita, placeholder_text="Nome (Ex: Anual, Mensal Livre)", width=300)
        self.entry_nome.pack(pady=10)
        
        self.entry_valor = ctk.CTkEntry(self.frame_direita, placeholder_text="Valor Mensal (Ex: 120.00)", width=300)
        self.entry_valor.pack(pady=10)
        
        ctk.CTkLabel(self.frame_direita, text="Duração do Contrato:").pack(pady=(5,0))
        self.combo_duracao = ctk.CTkOptionMenu(self.frame_direita, values=["1 Mês (Avulso)", "3 Meses (Trimestral)", "6 Meses (Semestral)", "12 Meses (Anual)"], width=300, fg_color="#2b2b2b", button_color=self.COR_PRIMARIA)
        self.combo_duracao.pack(pady=5)
        
        self.label_status = ctk.CTkLabel(self.frame_direita, text="")
        self.label_status.pack(pady=10)
        
        ctk.CTkButton(self.frame_direita, text="Salvar Plano", command=self.salvar_plano, width=300, fg_color=self.COR_PRIMARIA).pack(pady=20)

        self.recarregar_planos()

    def recarregar_planos(self):
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
            
        planos_banco = banco.listar_planos()
        
        if not planos_banco:
            ctk.CTkLabel(self.lista_scroll, text="Nenhum plano cadastrado.", text_color="gray").pack(pady=20)
            return
            
        for p in planos_banco:
            id_p, nome, valor, duracao = p
            
            linha = ctk.CTkFrame(self.lista_scroll, fg_color="#2B2B2B", border_color=self.COR_PRIMARIA, border_width=1)
            linha.pack(fill="x", pady=6, padx=4)
            
            texto_plano = f"🏷️ {nome}\n💰 R$ {valor}/mês  |  ⏱️ {duracao}"
            ctk.CTkLabel(linha, text=texto_plano, text_color="white", justify="left", font=ctk.CTkFont(size=14)).pack(side="left", padx=15, pady=10)

    def salvar_plano(self):
        nome = self.entry_nome.get().strip()
        valor = self.entry_valor.get().strip()
        duracao = self.combo_duracao.get()
        
        if not nome or not valor:
            self.label_status.configure(text="❌ Preencha nome e valor!", text_color=self.COR_PRIMARIA)
            return
            
        banco.cadastrar_plano(nome, valor, duracao)
        
        self.label_status.configure(text="✅ Plano registado!", text_color="green")
        self.entry_nome.delete(0, 'end')
        self.entry_valor.delete(0, 'end')
        
        self.recarregar_planos()