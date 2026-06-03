import customtkinter as ctk
import banco

class TelaTurmas(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, faixa_logada):
        super().__init__(master, fg_color="transparent")
        self.usuario_logado = usuario_logado
        self.faixa_logada = faixa_logada
        
        self.COR_PRIMARIA = "#CC0000"
        self.COR_FUNDO = "#1A1A1A"
        
        # --- DIVISÃO DA TELA ---
        self.frame_esquerda = ctk.CTkFrame(self, width=400, fg_color="transparent")
        self.frame_esquerda.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        self.frame_direita = ctk.CTkFrame(self, width=350, fg_color=self.COR_FUNDO, border_color=self.COR_PRIMARIA, border_width=1)
        self.frame_direita.pack(side="right", fill="y", padx=20, pady=10)

        # ----------------- LADO ESQUERDO (QUADRO DE HORÁRIOS) -----------------
        ctk.CTkLabel(self.frame_esquerda, text="📅 Grade de Turmas", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.lista_scroll = ctk.CTkScrollableFrame(self.frame_esquerda)
        self.lista_scroll.pack(fill="both", expand=True, pady=10)

        # ----------------- LADO DIREITO (CRIAR NOVA TURMA) -----------------
        ctk.CTkLabel(self.frame_direita, text="📝 Nova Turma", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.entry_nome = ctk.CTkEntry(self.frame_direita, placeholder_text="Nome (Ex: Iniciantes, No-Gi)", width=300)
        self.entry_nome.pack(pady=10)
        
        ctk.CTkLabel(self.frame_direita, text="Dias da Semana:").pack(pady=(5,0))
        self.combo_dias = ctk.CTkOptionMenu(self.frame_direita, values=["Seg/Qua/Sex", "Ter/Qui", "Sábados", "Todos os Dias"], width=300, fg_color="#2b2b2b", button_color=self.COR_PRIMARIA)
        self.combo_dias.pack(pady=5)
        
        self.entry_horario = ctk.CTkEntry(self.frame_direita, placeholder_text="Horário (Ex: 19:00 - 20:30)", width=300)
        self.entry_horario.pack(pady=10)
        
        # Puxa os professores (usuários) do banco
        ctk.CTkLabel(self.frame_direita, text="Professor Responsável:").pack(pady=(5,0))
        self.professores = [u[1] for u in banco.listar_usuarios()]
        if not self.professores: self.professores = ["Nenhum professor"]
        
        self.combo_prof = ctk.CTkOptionMenu(self.frame_direita, values=self.professores, width=300, fg_color="#2b2b2b", button_color=self.COR_PRIMARIA)
        self.combo_prof.pack(pady=5)

        self.label_status = ctk.CTkLabel(self.frame_direita, text="")
        self.label_status.pack(pady=10)
        
        ctk.CTkButton(self.frame_direita, text="Cadastrar Turma", command=self.salvar_turma, width=300, fg_color=self.COR_PRIMARIA).pack(pady=20)

        self.recarregar_turmas()

    # ================= MÉTODOS LÓGICOS =================

    def recarregar_turmas(self):
        # Limpa os elementos antigos da tela
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
            
        # Puxa as turmas reais cadastradas no banco
        turmas_banco = banco.listar_turmas()
        
        if not turmas_banco:
            ctk.CTkLabel(self.lista_scroll, text="Nenhuma turma cadastrada.", text_color="gray").pack(pady=20)
            return
            
        for t in turmas_banco:
            id_t, nome, dias, horario, professor = t
            
            linha = ctk.CTkFrame(self.lista_scroll, fg_color="#2B2B2B", border_color=self.COR_PRIMARIA, border_width=1)
            linha.pack(fill="x", pady=6, padx=4)
            
            # Formata o texto para exibir as informações em duas linhas organizadas
            texto_turma = f"🥋 {nome}  |  📅 {dias}  |  ⏰ {horario}\n👤 Professor Responsável: {professor}"
            
            ctk.CTkLabel(
                linha, 
                text=texto_turma, 
                text_color="white", 
                justify="left", 
                font=ctk.CTkFont(size=13)
            ).pack(side="left", padx=15, pady=10)

    def salvar_turma(self):
        nome = self.entry_nome.get().strip()
        dias = self.combo_dias.get()
        horario = self.entry_horario.get().strip()
        professor = self.combo_prof.get()
        
        # Validação de segurança básica
        if not nome or not horario or professor == "Nenhum professor":
            self.label_status.configure(text="❌ Preencha todos os campos!", text_color=self.COR_PRIMARIA)
            return
            
        # Salva as informações reais no banco
        banco.cadastrar_turma(nome, dias, horario, professor)
        
        # Feedback visual de sucesso e limpeza dos campos de texto
        self.label_status.configure(text="✅ Turma registada com sucesso!", text_color="green")
        self.entry_nome.delete(0, 'end')
        self.entry_horario.delete(0, 'end')
        
        # Atualiza a listagem lateral na hora
        self.recarregar_turmas()