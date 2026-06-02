import customtkinter as ctk
import banco
import re
from datetime import datetime

class TelaAlunos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # --- DIVISÃO DA TELA ---
        self.frame_esquerda = ctk.CTkFrame(self, width=350, fg_color="transparent")
        self.frame_esquerda.pack(side="left", fill="y", padx=20, pady=10)
        
        self.frame_direita = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_direita.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        # ----------------- LADO ESQUERDO (LISTA DE ALUNOS) -----------------
        ctk.CTkLabel(self.frame_esquerda, text="🥋 Alunos Matriculados", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.lista_scroll = ctk.CTkScrollableFrame(self.frame_esquerda, width=300)
        self.lista_scroll.pack(fill="both", expand=True)

        self.recarregar_lista()

        # ----------------- LADO DIREITO (FORMULÁRIO INTELIGENTE) -----------------
        ctk.CTkLabel(self.frame_direita, text="📝 Ficha de Matrícula", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        # Usamos um ScrollableFrame para o formulário caber em qualquer monitor
        self.form_scroll = ctk.CTkScrollableFrame(self.frame_direita, fg_color="transparent")
        self.form_scroll.pack(fill="both", expand=True)

        # --- 1. DADOS DO ALUNO ---
        self.entry_nome = ctk.CTkEntry(self.form_scroll, placeholder_text="Nome Completo do Aluno", width=400)
        self.entry_nome.pack(pady=5)

        self.entry_cpf = ctk.CTkEntry(self.form_scroll, placeholder_text="CPF (Apenas Números)", width=400)
        self.entry_cpf.pack(pady=5)
        self.entry_cpf.bind("<KeyRelease>", self.formatar_cpf)

        self.entry_data = ctk.CTkEntry(self.form_scroll, placeholder_text="Data de Nasc. (DD/MM/AAAA)", width=400)
        self.entry_data.pack(pady=5)
        self.entry_data.bind("<KeyRelease>", self.formatar_data)
        self.entry_data.bind("<FocusOut>", self.verificar_idade) # Calcula a idade ao sair do campo

        self.label_idade = ctk.CTkLabel(self.form_scroll, text="Idade: --", text_color="gray")
        self.label_idade.pack()

        self.entry_tel = ctk.CTkEntry(self.form_scroll, placeholder_text="Telefone / WhatsApp", width=400)
        self.entry_tel.pack(pady=5)
        self.entry_tel.bind("<KeyRelease>", self.formatar_telefone)

        self.entry_end = ctk.CTkEntry(self.form_scroll, placeholder_text="Endereço Completo", width=400)
        self.entry_end.pack(pady=5)

        ctk.CTkLabel(self.form_scroll, text="Graduação Inicial:").pack(pady=(10, 0))
        self.combo_faixa = ctk.CTkOptionMenu(self.form_scroll, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], width=400)
        self.combo_faixa.pack(pady=5)

        # --- 2. DADOS DO RESPONSÁVEL (Invisível por padrão) ---
        self.frame_responsavel = ctk.CTkFrame(self.form_scroll, fg_color="#333333")
        # Nota: Não damos .pack() nele aqui. Ele só aparece se for menor de 18!
        
        ctk.CTkLabel(self.frame_responsavel, text="⚠️ Aluno Menor de Idade - Dados do Responsável", text_color="orange", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        self.entry_resp_nome = ctk.CTkEntry(self.frame_responsavel, placeholder_text="Nome do Responsável Legal", width=380)
        self.entry_resp_nome.pack(pady=5)
        self.entry_resp_cpf = ctk.CTkEntry(self.frame_responsavel, placeholder_text="CPF do Responsável", width=380)
        self.entry_resp_cpf.pack(pady=5)
        self.entry_resp_tel = ctk.CTkEntry(self.frame_responsavel, placeholder_text="Telefone do Responsável", width=380)
        self.entry_resp_tel.pack(pady=(5, 15))
        self.entry_resp_tel.bind("<KeyRelease>", self.formatar_telefone_resp)

        # --- 3. TERMOS E BOTÃO ---
        self.check_lgpd = ctk.CTkCheckBox(self.form_scroll, text="Concordo com os Termos e a Política de Privacidade (LGPD)")
        self.check_lgpd.pack(pady=20)

        self.label_status = ctk.CTkLabel(self.form_scroll, text="", font=ctk.CTkFont(weight="bold"))
        self.label_status.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self.form_scroll, text="💾 Salvar Matrícula", command=self.salvar_aluno, width=400, fg_color="#4CAF50", hover_color="#45a049")
        self.btn_salvar.pack(pady=20)


    # ================= MÉTODOS DE INTELIGÊNCIA =================
    
    def recarregar_lista(self):
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
        for aluno in banco.listar_todos_alunos():
            id_aluno, nome, faixa, status, telefone = aluno
            linha = ctk.CTkFrame(self.lista_scroll, fg_color="#333333")
            linha.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(linha, text=f"👤 {nome} ({faixa.title()})", text_color="white").pack(side="left", padx=10, pady=10)

    def formatar_cpf(self, event):

        if event.keysym in ['BackSpace', 'Delete']: return

        texto = re.sub(r'\D', '', self.entry_cpf.get())
        if len(texto) > 11: texto = texto[:11]
        mascara = ""
        for i, char in enumerate(texto):
            if i in [3, 6]: mascara += "."
            if i == 9: mascara += "-"
            mascara += char
        self.entry_cpf.delete(0, 'end')
        self.entry_cpf.insert(0, mascara)

    def formatar_telefone(self, event):
        if event.keysym in ['BackSpace', 'Delete']: return
        
        texto = re.sub(r'\D', '', self.entry_tel.get())
        if len(texto) > 11: texto = texto[:11]
        mascara = ""
        for i, char in enumerate(texto):
            if i == 0: mascara += "("
            if i == 2: mascara += ")"
            if i == 7: mascara += "-"
            mascara += char
        self.entry_tel.delete(0, 'end')
        self.entry_tel.insert(0, mascara)

    def formatar_telefone_resp(self, event):
        if event.keysym in ['BackSpace', 'Delete']: return
        
        texto = re.sub(r'\D', '', self.entry_resp_tel.get())
        if len(texto) > 11: texto = texto[:11]
        mascara = ""
        for i, char in enumerate(texto):
            if i == 0: mascara += "("
            if i == 2: mascara += ")"
            if i == 7: mascara += "-"
            mascara += char
        self.entry_resp_tel.delete(0, 'end')
        self.entry_resp_tel.insert(0, mascara)

    def formatar_data(self, event):
        texto = re.sub(r'\D', '', self.entry_data.get())
        if len(texto) > 8: texto = texto[:8]
        mascara = ""
        for i, char in enumerate(texto):
            if i in [2, 4]: mascara += "/"
            mascara += char
        self.entry_data.delete(0, 'end')
        self.entry_data.insert(0, mascara)

    def verificar_idade(self, event=None):
        data_nasc = self.entry_data.get()
        self.idade_calculada = 0
        if len(data_nasc) == 10:
            try:
                nascimento = datetime.strptime(data_nasc, "%d/%m/%Y")
                hoje = datetime.now()
                # Fórmula mágica para calcular idade exata considerando meses e dias
                self.idade_calculada = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
                self.label_idade.configure(text=f"Idade: {self.idade_calculada} anos")

                if self.idade_calculada < 18:
                    # Se for menor, injeta o quadro de responsáveis antes da checkbox
                    self.frame_responsavel.pack(fill="x", pady=10, padx=10, before=self.check_lgpd)
                else:
                    self.frame_responsavel.pack_forget() # Oculta se for maior
            except ValueError:
                self.label_idade.configure(text="❌ Data inválida")

    def salvar_aluno(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        data_nasc = self.entry_data.get().strip()
        telefone = self.entry_tel.get().strip()
        endereco = self.entry_end.get().strip()
        faixa = self.combo_faixa.get()
        lgpd = "Sim" if self.check_lgpd.get() == 1 else "Não"
        
        # Validação Básica
        if not nome or len(cpf) != 14 or len(data_nasc) != 10:
            self.label_status.configure(text="❌ Preencha Nome, CPF e Data corretamente.", text_color="red")
            return
            
        if lgpd == "Não":
            self.label_status.configure(text="❌ O aluno precisa concordar com os termos.", text_color="red")
            return

        # Validação Menor de Idade
        resp_nome = self.entry_resp_nome.get().strip() if self.idade_calculada < 18 else ""
        resp_cpf = self.entry_resp_cpf.get().strip() if self.idade_calculada < 18 else ""
        resp_tel = self.entry_resp_tel.get().strip() if self.idade_calculada < 18 else ""
        
        if self.idade_calculada < 18 and not resp_nome:
            self.label_status.configure(text="❌ Preencha os dados do Responsável!", text_color="red")
            return

        # Empacota e envia para o banco
        dados = (nome, cpf, data_nasc, self.idade_calculada, telefone, endereco, faixa, lgpd, resp_nome, resp_cpf, resp_tel)
        sucesso, msg = banco.salvar_aluno(dados)
        
        self.label_status.configure(text=msg, text_color="#4CAF50" if sucesso else "red")
        
        if sucesso:
            # Limpa o formulário após o sucesso
            self.entry_nome.delete(0, 'end')
            self.entry_cpf.delete(0, 'end')
            self.entry_data.delete(0, 'end')
            self.entry_tel.delete(0, 'end')
            self.entry_end.delete(0, 'end')
            self.check_lgpd.deselect()
            self.label_idade.configure(text="Idade: --")
            self.frame_responsavel.pack_forget()
            self.recarregar_lista()