import customtkinter as ctk

# Configurações gerais de estilo da interface
ctk.set_appearance_mode("System")  # Segue o modo do Windows (Claro ou Escuro)
ctk.set_default_color_theme("blue") # Tema de cor dos botões

class AppCadastro(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurando a janela do aplicativo
        self.title("🥋 Sistema Jiu-Jitsu - Cadastro Base (LGPD Ready)")
        self.geometry("500x550")
        self.resizable(False, False)

        # --- TÍTULO DA TELA ---
        self.label_titulo = ctk.CTkLabel(self, text="NOVO CADASTRO DE ALUNO", font=ctk.CTkFont(size=20, weight="bold"))
        self.label_titulo.pack(padx=20, pady=20)

        # --- CAMPO: NOME ---
        self.label_nome = ctk.CTkLabel(self, text="Nome Completo:")
        self.label_nome.pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_nome = ctk.CTkEntry(self, placeholder_text="Digite o nome do aluno...", width=420)
        self.entry_nome.pack(padx=40, pady=(0, 10))

        # --- CAMPO: TELEFONE (WHATSAPP) ---
        self.label_telefone = ctk.CTkLabel(self, text="Telefone (WhatsApp com DDD):")
        self.label_telefone.pack(anchor="w", padx=40, pady=(10, 0))
        self.entry_telefone = ctk.CTkEntry(self, placeholder_text="(XX) 9YYYY-XXXX", width=420)
        self.entry_telefone.pack(padx=40, pady=(0, 10))

        # --- CAMPO: SELEÇÃO DE FAIXA (Menu Cascata) ---
        self.label_faixa = ctk.CTkLabel(self, text="Graduação / Faixa:")
        self.label_faixa.pack(anchor="w", padx=40, pady=(10, 0))
        self.combobox_faixa = ctk.CTkComboBox(self, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], width=420)
        self.combobox_faixa.pack(padx=40, pady=(0, 10))

        # --- TRAVA LGPD: CHECKBOX DE CONSENTIMENTO ---
        self.check_lgpd_var = ctk.StringVar(value="off")
        self.check_lgpd = ctk.CTkCheckBox(
            self, 
            text="O aluno consente com o armazenamento dos dados para gestão\nacadêmica e recebimento de notificações via WhatsApp.",
            variable=self.check_lgpd_var, 
            onvalue="on", 
            offvalue="off",
            font=ctk.CTkFont(size=11)
        )
        self.check_lgpd.pack(padx=40, pady=25, anchor="w")

        # --- BOTÃO SALVAR ---
        self.btn_salvar = ctk.CTkButton(self, text="Salvar Cadastro", command=self.acao_salvar, width=200, height=40)
        self.btn_salvar.pack(pady=10)

        # Label para mensagens de status (Sucesso ou Erro)
        self.label_status = ctk.CTkLabel(self, text="", text_color="green")
        self.label_status.pack(pady=5)

    def acao_salvar(self):
        # Captura os dados digitados na tela
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        faixa = self.combobox_faixa.get()
        consentimento = self.check_lgpd_var.get()

        # Validação da LGPD antes de salvar
        if consentimento == "off":
            self.label_status.configure(text="❌ Erro: É necessário aceitar o termo de consentimento (LGPD).", text_color="red")
            return

        if not nome or not telefone:
            self.label_status.configure(text="❌ Erro: Preencha todos os campos obrigatórios.", text_color="red")
            return

        # Simulação do salvamento (aqui vamos conectar o banco de dados depois!)
        print("\n--- 📥 Dados prontos para o Banco de Dados Real ---")
        print(f"Nome: {nome}")
        print(f"Telefone: {telefone}")
        print(f"Faixa: {faixa}")
        print(f"Consentimento LGPD: {consentimento.upper()}")
        
        self.label_status.configure(text="✅ Cadastro realizado e termo registrado com sucesso!", text_color="green")
        
        # Limpa os campos após salvar
        self.entry_nome.delete(0, 'end')
        self.entry_telefone.delete(0, 'end')
        self.check_lgpd.deselect()

if __name__ == "__main__":
    app = AppCadastro()
    app.mainloop()