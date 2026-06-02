import customtkinter as ctk
from datetime import datetime
import banco  # Importa nosso arquivo de banco de dados

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppAcademia(ctk.CTk):
    def __init__(self):
        super().__init__()
        # As tabelas do banco serão criadas antes de instanciar a aplicação
        self.faixa_usuario = ""

        self.title("🥋 Sistema Jiu-Jitsu - Gestão & LGPD")
        self.geometry("1000x600")

        # Inicia a janela em tela cheia
        self.state("zoomed")

        # Espaços reservados para a interface principal (serão criados após login)
        self.tabview = None
        self.tab_cadastro = None
        self.tab_financeiro = None
        self.tab_usuarios = None

        # Mostrar tela de login integrada
        self.mostrar_login()

    # ------------------ ABA CADASTRO ------------------
    def configurar_aba_cadastro(self):
        if self.faixa_usuario == "branca":
            ctk.CTkLabel(self.tab_cadastro, text="⚠️ ACESSO NEGADO\nSua faixa não permite cadastros.", font=ctk.CTkFont(size=16, weight="bold"), text_color="red").pack(expand=True)
            return

        self.scroll_frame = ctk.CTkScrollableFrame(self.tab_cadastro, width=620, height=650)
        self.scroll_frame.pack(fill="both", expand=True)

        self.entry_nome = self.criar_campo("Nome Completo:")
        
        # CPF com Máscara Automática
        self.entry_cpf = self.criar_campo("CPF (Apenas números):")
        self.entry_cpf.bind("<KeyRelease>", self.mascara_cpf)
        
        # Data com Máscara Automática
        self.entry_nascimento = self.criar_campo("Data de Nascimento (Apenas números):")
        self.entry_nascimento.bind("<KeyRelease>", self.mascara_data)
        self.entry_nascimento.bind("<FocusOut>", self.atualizar_idade_dinamica)

        ctk.CTkLabel(self.scroll_frame, text="Idade:").pack(anchor="w", padx=30)
        self.entry_idade = ctk.CTkEntry(self.scroll_frame, width=540, state="disabled")
        self.entry_idade.pack(padx=30, pady=(0, 10))

        self.entry_telefone = self.criar_campo("Telefone / WhatsApp:")
        self.entry_endereco = self.criar_campo("Endereço Completo:")

        ctk.CTkLabel(self.scroll_frame, text="Graduação / Faixa:").pack(anchor="w", padx=30)
        self.combobox_faixa = ctk.CTkComboBox(self.scroll_frame, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], width=540)
        self.combobox_faixa.pack(padx=30, pady=(0, 10))

        # Frame do Responsável
        self.frame_responsavel = ctk.CTkFrame(self.scroll_frame, fg_color="transparent")
        self.entry_nome_resp = self.criar_campo("Nome do Responsável:", container=self.frame_responsavel)
        self.entry_cpf_resp = self.criar_campo("CPF do Responsável:", container=self.frame_responsavel)
        self.entry_cpf_resp.bind("<KeyRelease>", self.mascara_cpf)
        self.entry_tel_resp = self.criar_campo("Telefone do Responsável:", container=self.frame_responsavel)

        # LGPD
        self.check_lgpd_var = ctk.StringVar(value="off")
        self.check_lgpd = ctk.CTkCheckBox(self.scroll_frame, text="Aluno/Responsável autoriza o tratamento de dados e cobranças via WhatsApp.", variable=self.check_lgpd_var, onvalue="on", offvalue="off", font=ctk.CTkFont(size=11))
        self.check_lgpd.pack(padx=30, pady=20, anchor="w")

        self.btn_salvar = ctk.CTkButton(self.scroll_frame, text="Finalizar Matrícula", command=self.acao_salvar, width=250, height=40)
        self.btn_salvar.pack(pady=10)

        self.label_status = ctk.CTkLabel(self.scroll_frame, text="", text_color="green")
        self.label_status.pack(pady=5)

    def criar_campo(self, texto_label, container=None):
        target = container if container else self.scroll_frame
        ctk.CTkLabel(target, text=texto_label).pack(anchor="w", padx=30)
        campo = ctk.CTkEntry(target, width=540)
        campo.pack(padx=30, pady=(0, 10))
        return campo

    # ------------------ MÁSCARAS INTELIGENTES ------------------
    def mascara_cpf(self, event):
        if event.keysym == "BackSpace": return
        texto = "".join(filter(str.isdigit, event.widget.get()))
        if len(texto) > 11: texto = texto[:11]
        
        if len(texto) > 9: texto = f"{texto[:3]}.{texto[3:6]}.{texto[6:9]}-{texto[9:]}"
        elif len(texto) > 6: texto = f"{texto[:3]}.{texto[3:6]}.{texto[6:]}"
        elif len(texto) > 3: texto = f"{texto[:3]}.{texto[3:]}"
        
        event.widget.delete(0, 'end')
        event.widget.insert(0, texto)

    def mascara_data(self, event):
        if event.keysym == "BackSpace": return
        texto = "".join(filter(str.isdigit, event.widget.get()))
        if len(texto) > 8: texto = texto[:8]
        
        if len(texto) > 4: texto = f"{texto[:2]}/{texto[2:4]}/{texto[4:]}"
        elif len(texto) > 2: texto = f"{texto[:2]}/{texto[2:]}"
        
        event.widget.delete(0, 'end')
        event.widget.insert(0, texto)

    def atualizar_idade_dinamica(self, event):
        data = self.entry_nascimento.get().strip()
        try:
            data_nasc = datetime.strptime(data, "%d/%m/%Y")
            hoje = datetime.now()
            idade = hoje.year - data_nasc.year - ((hoje.month, hoje.day) < (data_nasc.month, data_nasc.day))
            
            self.entry_idade.configure(state="normal")
            self.entry_idade.delete(0, 'end')
            self.entry_idade.insert(0, str(idade))
            self.entry_idade.configure(state="disabled")

            if idade < 18:
                self.frame_responsavel.pack(fill="x", before=self.check_lgpd)
            else:
                self.frame_responsavel.pack_forget()
        except ValueError:
            pass

    def acao_salvar(self):
        # Validações básicas e captura
        if self.check_lgpd_var.get() == "off":
            self.label_status.configure(text="❌ Erro: Aceite o termo LGPD.", text_color="red")
            return
            
        idade_str = self.entry_idade.get()
        if not idade_str or not self.entry_nome.get():
            self.label_status.configure(text="❌ Erro: Preencha os dados corretamente.", text_color="red")
            return

        # Prepara a tupla de dados para enviar ao banco.py
        dados = (
            self.entry_nome.get(), self.entry_cpf.get(), self.entry_nascimento.get(),
            int(idade_str), self.entry_telefone.get(), self.entry_endereco.get(),
            self.combobox_faixa.get(), "ON",
            self.entry_nome_resp.get() if int(idade_str) < 18 else None,
            self.entry_cpf_resp.get() if int(idade_str) < 18 else None,
            self.entry_tel_resp.get() if int(idade_str) < 18 else None
        )
        
        sucesso, msg = banco.salvar_aluno(dados)
        self.label_status.configure(text=msg, text_color="green" if sucesso else "red")
        if sucesso:
            # Limpa todos os campos de entrada
            self.entry_nome.delete(0, 'end')
            self.entry_cpf.delete(0, 'end')
            self.entry_nascimento.delete(0, 'end')
            self.entry_telefone.delete(0, 'end')
            self.entry_endereco.delete(0, 'end')
            self.entry_nome_resp.delete(0, 'end')
            self.entry_cpf_resp.delete(0, 'end')
            self.entry_tel_resp.delete(0, 'end')
            self.combobox_faixa.set("")
            self.check_lgpd_var.set("off")
            self.entry_idade.configure(state="normal")
            self.entry_idade.delete(0, 'end')
            self.entry_idade.configure(state="disabled")
            self.frame_responsavel.pack_forget()
            self.atualizar_lista_financeiro()

    # ------------------ ABA FINANCEIRO (ALTERAR STATUS) ------------------
    def configurar_aba_financeiro(self):
        if self.faixa_usuario not in ['marrom', 'preta']:
            ctk.CTkLabel(self.tab_financeiro, text="⚠️ ACESSO NEGADO\nSua faixa não possui acesso ao Financeiro.", font=ctk.CTkFont(size=16, weight="bold"), text_color="red").pack(expand=True)
            return

        ctk.CTkLabel(self.tab_financeiro, text="GESTÃO DE MENSALIDADES (Clique para alterar o status)", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        # Frame para listar os alunos cadastrados no banco
        self.frame_lista = ctk.CTkScrollableFrame(self.tab_financeiro, width=620, height=550)
        self.frame_lista.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.atualizar_lista_financeiro()

    # ------------------ ABA USUÁRIOS (GESTÃO DE ACESSOS) ------------------
    def configurar_aba_usuarios(self):
        # Apenas usuários com faixa preta podem acessar
        if self.faixa_usuario != "preta":
            ctk.CTkLabel(self.tab_usuarios, text="ACESSO NEGADO", font=ctk.CTkFont(size=18, weight="bold"), text_color="red").pack(expand=True)
            return

        frame = ctk.CTkFrame(self.tab_usuarios)
        frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Cadastrar Novo Usuário", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(0, 10))

        ctk.CTkLabel(frame, text="Username:").pack(anchor="w")
        self.entry_novo_username = ctk.CTkEntry(frame, width=540)
        self.entry_novo_username.pack(pady=(0, 10))

        ctk.CTkLabel(frame, text="Senha:").pack(anchor="w")
        self.entry_novo_senha = ctk.CTkEntry(frame, width=540, show="*")
        self.entry_novo_senha.pack(pady=(0, 10))

        ctk.CTkLabel(frame, text="Permissão (Faixa):").pack(anchor="w")
        self.combobox_nova_faixa = ctk.CTkComboBox(frame, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], width=540)
        self.combobox_nova_faixa.pack(pady=(0, 10))

        def cadastrar_usuario_callback():
            username = self.entry_novo_username.get().strip().lower()
            senha = self.entry_novo_senha.get().strip()
            faixa = self.combobox_nova_faixa.get().strip().lower()

            if not username or not senha or not faixa:
                self.label_status_usuarios.configure(text="❌ Preencha todos os campos.", text_color="red")
                return

            sucesso, msg = banco.cadastrar_usuario(username, senha, faixa)
            self.label_status_usuarios.configure(text=msg, text_color="green" if sucesso else "red")
            if sucesso:
                self.entry_novo_username.delete(0, 'end')
                self.entry_novo_senha.delete(0, 'end')
                self.combobox_nova_faixa.set("")

        self.btn_cadastrar_usuario = ctk.CTkButton(frame, text="Cadastrar Usuário", command=cadastrar_usuario_callback, width=220)
        self.btn_cadastrar_usuario.pack(pady=10)

        self.label_status_usuarios = ctk.CTkLabel(frame, text="", text_color="green")
        self.label_status_usuarios.pack(pady=5)

    def atualizar_lista_financeiro(self):
        if self.faixa_usuario not in ['marrom', 'preta']: return
        
        # Limpa a lista atual na tela
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        # Busca direto do banco de dados real
        alunos = banco.listar_todos_alunos()
        
        if not alunos:
            ctk.CTkLabel(self.frame_lista, text="Nenhum aluno cadastrado no banco.").pack(pady=20)
            return

        for aluno in alunos:
            aluno_id, nome, faixa, status, telefone = aluno
            
            card = ctk.CTkFrame(self.frame_lista, fg_color="#2B2B2B" if status == "Em dia" else "#4A1515")
            card.pack(fill="x", padx=10, pady=5)
            
            info_text = f"🥋 {nome} ({faixa}) | Status: {status.upper()}"
            ctk.CTkLabel(card, text=info_text, font=ctk.CTkFont(size=12)).pack(side="left", padx=15)
            
            # Botão dinâmico para alternar o status
            texto_btn = "Marcar Atrasado" if status == "Em dia" else "Marcar Pago"
            cor_btn = "#9c2a2a" if status == "Em dia" else "#2a9c4d"
            
            # Gambiarra saudável do Python para passar o ID correto no clique do botão
            btn = ctk.CTkButton(
                card, text=texto_btn, fg_color=cor_btn, width=120,
                command=lambda aid=aluno_id, stat=status: self.alternar_status(aid, stat)
            )
            btn.pack(side="right", padx=15, pady=5)

    def alternar_status(self, aluno_id, status_atual):
        novo_status = "Atrasado" if status_atual == "Em dia" else "Em dia"
        banco.atualizar_status_pagamento(aluno_id, novo_status)
        self.atualizar_lista_financeiro() # Recarrega a tela na hora!
    # ------------------ LOGIN (INTEGRADO NA MESMA JANELA) ------------------
    def mostrar_login(self):
        # Frame centralizado para login
        self.frame_login = ctk.CTkFrame(self, width=420, height=380)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(self.frame_login, text="SISTEMA DE GESTÃO\n🥋 RAFAEL FARIAS BJJ", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))
        ctk.CTkLabel(self.frame_login, text="Insira suas credenciais para continuar").pack(pady=(0, 20))

        self.entry_usuario_login = ctk.CTkEntry(self.frame_login, placeholder_text="Usuário", width=300, height=40)
        self.entry_usuario_login.pack(pady=8)

        self.entry_senha_login = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", show="*", width=300, height=40)
        self.entry_senha_login.pack(pady=8)

        self.btn_login_login = ctk.CTkButton(self.frame_login, text="Entrar", command=self.fazer_login, width=300, height=40)
        self.btn_login_login.pack(pady=16)

        self.label_status_login = ctk.CTkLabel(self.frame_login, text="", text_color="red")
        self.label_status_login.pack(pady=4)

        # Bind Enter para submeter o login
        self.bind('<Return>', self.fazer_login)

    def fazer_login(self, event=None):
        usuario_digitado = self.entry_usuario_login.get().strip().lower()
        senha_digitada = self.entry_senha_login.get().strip()

        faixa_banco = banco.validar_login(usuario_digitado, senha_digitada)
        if faixa_banco:
            print(f"✅ Acesso liberado! Iniciando sistema como Faixa {faixa_banco.upper()}...")
            # Remove apenas o frame de login e mostra o sistema principal
            try:
                self.frame_login.destroy()
            except Exception:
                pass
            self.mostrar_sistema_principal(faixa_banco)
        else:
            self.label_status_login.configure(text="❌ Usuário ou senha incorretos.")
            self.entry_senha_login.delete(0, 'end')

    def mostrar_sistema_principal(self, faixa):
        # Define a faixa do usuário logado e cria as abas do sistema
        self.faixa_usuario = faixa.lower()

        # Frame de cabeçalho com botão de logoff
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=10, pady=(10, 0))

        # Botão de logoff no topo direito
        self.btn_logoff = ctk.CTkButton(self.header_frame, text="🚪 Sair (F10)", command=self.fazer_logoff, width=150, height=30)
        self.btn_logoff.pack(side="right", padx=5)

        # Criando abas no sistema (Uma para cadastro, outra para financeiro)
        self.tabview = ctk.CTkTabview(self, width=680, height=720)
        self.tabview.pack(padx=10, pady=10, fill='both', expand=True)
        
        self.tab_cadastro = self.tabview.add("🆕 Cadastrar Aluno")
        self.tab_financeiro = self.tabview.add("💰 Gerenciar Pagamentos")
        self.tab_usuarios = self.tabview.add("🔒 Gestão de Acessos")

        # Inicializa as telas internas
        self.configurar_aba_cadastro()
        self.configurar_aba_financeiro()
        self.configurar_aba_usuarios()

        # Atalho de teclado F10 para logoff
        self.bind('<F10>', self.fazer_logoff)

    # ------------------ LOGOFF (SAIR DA SESSÃO) ------------------
    def fazer_logoff(self, event=None):
        # Destrói os widgets de sistema principal
        try:
            self.header_frame.destroy()
        except Exception:
            pass
        try:
            self.tabview.destroy()
        except Exception:
            pass
        try:
            self.btn_logoff.destroy()
        except Exception:
            pass

        # Remove o atalho F10
        try:
            self.unbind('<F10>')
        except Exception:
            pass

        print("🚪 Sessão encerrada. Retornando ao login...")
        # Mostra o login novamente
        self.mostrar_login()


if __name__ == "__main__":
    banco.criar_tabelas()
    app = AppAcademia()
    app.mainloop()