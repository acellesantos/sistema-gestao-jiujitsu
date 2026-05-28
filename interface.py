import customtkinter as ctk
from datetime import datetime

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppCadastro(ctk.CTk):
    def __init__(self, faixa_usuario_logado="preta"): # Simula a faixa de quem logou
        super().__init__()

        self.faixa_usuario = faixa_usuario_logado.lower()
        self.title("🥋 Sistema Jiu-Jitsu - Cadastro Avançado (LGPD)")
        self.geometry("600x750")
        self.resizable(False, False)

        # 🛑 TRAVA DE SEGURANÇA: Verifica se o usuário tem permissão para acessar a tela
        if self.faixa_usuario == "branca":
            self.tela_bloqueada()
            return

        self.criar_componentes()

    def tela_bloqueada(self):
        label_erro = ctk.CTkLabel(
            self, 
            text="⚠️ ACESSO NEGADO\n\nSeu nível de permissão (Faixa Branca)\nnão permite o cadastro de novos alunos.",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="red"
        )
        label_erro.pack(expand=True)

    def criar_componentes(self):
        # Container com barra de rolagem caso a tela fique pequena
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=560, height=720)
        self.scroll_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Título
        ctk.CTkLabel(self.scroll_frame, text="FICHA DE MATRÍCULA DO ALUNO", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)

        # --- DADOS DO ALUNO ---
        self.entry_nome = self.criar_campo("Nome Completo:")
        self.entry_cpf = self.criar_campo("CPF:")
        
        # Data de Nascimento com evento de perda de foco para calcular a idade automaticamente
        self.entry_nascimento = self.criar_campo("Data de Nascimento (DD/MM/AAAA):")
        self.entry_nascimento.bind("<FocusOut>", self.atualizar_idade_dinamica)

        # Campo de Idade (Desabilitado pois o sistema calcula sozinho)
        ctk.CTkLabel(self.scroll_frame, text="Idade Calculada:").pack(anchor="w", padx=30)
        self.entry_idade = ctk.CTkEntry(self.scroll_frame, width=500, state="disabled", placeholder_text="Preencha a data de nascimento...")
        self.entry_idade.pack(padx=30, pady=(0, 10))

        self.entry_telefone = self.criar_campo("Telefone / WhatsApp:")
        self.entry_endereco = self.criar_campo("Endereço Completo:")

        ctk.CTkLabel(self.scroll_frame, text="Graduação / Faixa:").pack(anchor="w", padx=30)
        self.combobox_faixa = ctk.CTkComboBox(self.scroll_frame, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], width=500)
        self.combobox_faixa.pack(padx=30, pady=(0, 10))

        # --- SEÇÃO OCULTA: DADOS DO RESPONSÁVEL (Aparece se for menor de idade) ---
        self.frame_responsavel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        # Não damos pack nele ainda, ele fica escondido!
        
        ctk.CTkLabel(self.frame_responsavel, text="🚨 DADOS DO RESPONSÁVEL LEGAL (Menor de Idade)", font=ctk.CTkFont(weight="bold"), text_color="orange").pack(anchor="w", padx=30, pady=10)
        self.entry_nome_resp = self.criar_campo("Nome do Responsável:", container=self.frame_responsavel)
        self.entry_cpf_resp = self.criar_campo("CPF do Responsável:", container=self.frame_responsavel)
        self.entry_tel_resp = self.criar_campo("Telefone do Responsável:", container=self.frame_responsavel)

        # --- SEÇÃO LGPD ---
        self.check_lgpd_var = ctk.StringVar(value="off")
        self.check_lgpd = ctk.CTkCheckBox(
            self.scroll_frame, 
            text="Declaro que o aluno (ou seu responsável) consente com o armazenamento\ndos dados e autoriza o envio de notificações de cobrança via WhatsApp.",
            variable=self.check_lgpd_var, onvalue="on", offvalue="off", font=ctk.CTkFont(size=11)
        )
        self.check_lgpd.pack(padx=30, pady=20, anchor="w")

        # Botão Salvar
        self.btn_salvar = ctk.CTkButton(self.scroll_frame, text="Finalizar Matrícula", command=self.acao_salvar, width=250, height=40)
        self.btn_salvar.pack(pady=10)

        self.label_status = ctk.CTkLabel(self.scroll_frame, text="", text_color="green")
        self.label_status.pack(pady=5)

    def criar_campo(self, texto_label, container=None):
        target = container if container else self.scroll_frame
        ctk.CTkLabel(target, text=texto_label).pack(anchor="w", padx=30)
        campo = ctk.CTkEntry(target, width=500)
        campo.pack(padx=30, pady=(0, 10))
        return campo

    def calcular_idade(self, data_str):
        try:
            data_nasc = datetime.strptime(data_str, "%d/%m/%Y")
            hoje = datetime.now()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            return idade
        except ValueError:
            return None

    def atualizar_idade_dinamica(self, event):
        data = self.entry_nascimento.get().strip()
        idade = self.calcular_idade(data)
        
        if idade is not None:
            self.entry_idade.configure(state="normal")
            self.entry_idade.delete(0, 'end')
            self.entry_idade.insert(0, str(idade))
            self.entry_idade.configure(state="disabled")

            # 🧠 REGRA DE NEGÓCIO: Se for menor de 18 anos, exibe os campos do responsável
            if idade < 18:
                self.frame_responsavel.pack(fill="x", before=self.check_lgpd)
            else:
                self.frame_responsavel.pack_forget()
        else:
            self.entry_idade.configure(state="normal")
            self.entry_idade.delete(0, 'end')
            self.entry_idade.configure(state="disabled")
            self.frame_responsavel.pack_forget()

    def acao_salvar(self):
        idade_str = self.entry_idade.get()
        
        if not idade_str:
            self.label_status.configure(text="❌ Erro: Insira uma data de nascimento válida.", text_color="red")
            return

        idade = int(idade_str)
        consentimento = self.check_lgpd_var.get()

        if consentimento == "off":
            self.label_status.configure(text="❌ Erro: É obrigatório aceitar o termo de consentimento (LGPD).", text_color="red")
            return

        # Validação dos campos do responsável se for menor
        if idade < 18:
            nome_r = self.entry_nome_resp.get().strip()
            cpf_r = self.entry_cpf_resp.get().strip()
            tel_r = self.entry_tel_resp.get().strip()

            if not nome_r or not cpf_r or not tel_r:
                self.label_status.configure(text="❌ Erro: Dados do responsável são obrigatórios para menores.", text_color="red")
                return

        # Se passou por tudo, simula o sucesso
        self.label_status.configure(text="✅ Matrícula realizada com sucesso!", text_color="green")
        print("🎉 [Sucesso] Dados validados e prontos para o Banco de Dados!")

if __name__ == "__main__":
    # Teste mudando para "branca" para ver a trava em ação!
    app = AppCadastro(faixa_usuario_logado="preta")
    app.mainloop()