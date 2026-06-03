import customtkinter as ctk
from datetime import datetime
import banco  # Importa nosso arquivo de banco de dados
import tela_alunos
import tela_usuarios
import tela_financeiro
import tela_turmas

# Cores da Identidade Visual Rafael Farias BJJ
COR_PRIMARIA = "#CC0000"  # O Vermelho vivo da sua logo
COR_SECUNDARIA = "#000000" # O Preto forte
COR_FUNDO = "#1A1A1A"      # Um cinza muito escuro (mais profissional que o cinza claro)

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppAcademia(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração de Aparência
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue") # Podemos manter o azul básico ou criar tema customizado

        # As tabelas do banco serão criadas antes de instanciar a aplicação
        self.faixa_usuario = ""

        self.title("🥋 Sistema Jiu-Jitsu - Gestão & LGPD")
        self.geometry("1000x600")

        # Inicia a janela em tela cheia
        self.state("zoomed")

        # Aplica a cor de fundo da marca em todo o sistema
        self.configure(fg_color=COR_FUNDO)

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

        # Variável de controle para edição
        self.usuario_em_edicao_id = None

        # Frame principal dividido em duas colunas
        main_frame = ctk.CTkFrame(self.tab_usuarios)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # ====== COLUNA ESQUERDA: LISTA DE USUÁRIOS ======
        left_frame = ctk.CTkFrame(main_frame)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ctk.CTkLabel(left_frame, text="👥 Usuários do Sistema", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)

        self.frame_lista_usuarios = ctk.CTkScrollableFrame(left_frame, width=300, height=500)
        self.frame_lista_usuarios.pack(fill="both", expand=True, padx=5, pady=5)

        # ====== COLUNA DIREITA: FORMULÁRIO ======
        right_frame = ctk.CTkFrame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ctk.CTkLabel(right_frame, text="📝 Novo Usuário", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=10)

        ctk.CTkLabel(right_frame, text="Username:").pack(anchor="w", padx=20, pady=(10, 0))
        self.entry_novo_username = ctk.CTkEntry(right_frame, width=300)
        self.entry_novo_username.pack(padx=20, pady=(0, 10))

        ctk.CTkLabel(right_frame, text="Senha (deixe em branco para manter):").pack(anchor="w", padx=20, pady=(10, 0))
        self.entry_novo_senha = ctk.CTkEntry(right_frame, width=300, show="*")
        self.entry_novo_senha.pack(padx=20, pady=(0, 10))

        ctk.CTkLabel(right_frame, text="Permissão (Faixa):").pack(anchor="w", padx=20, pady=(10, 0))
        self.combobox_nova_faixa = ctk.CTkComboBox(right_frame, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], width=300)
        self.combobox_nova_faixa.pack(padx=20, pady=(0, 10))

        # Frame para botões de ação
        btn_frame = ctk.CTkFrame(right_frame)
        btn_frame.pack(padx=20, pady=15, fill="x")

        def limpar_formulario():
            self.usuario_em_edicao_id = None
            self.entry_novo_username.delete(0, 'end')
            self.entry_novo_senha.delete(0, 'end')
            self.combobox_nova_faixa.set("")
            self.label_status_usuarios.configure(text="")
            ctk.CTkLabel(right_frame, text="📝 Novo Usuário", font=ctk.CTkFont(size=14, weight="bold")).pack_forget()
            right_frame.pack_configure()

        def salvar_usuario():
            username = self.entry_novo_username.get().strip().lower()
            senha = self.entry_novo_senha.get().strip()
            faixa = self.combobox_nova_faixa.get().strip().lower()

            if not username or not faixa:
                self.label_status_usuarios.configure(text="❌ Preencha username e permissão.", text_color="red")
                return

            # Se está editando e não mudou a senha, passa vazio
            if self.usuario_em_edicao_id is not None:
                # MODO EDIÇÃO
                sucesso, msg = banco.atualizar_usuario(self.usuario_em_edicao_id, username, senha, faixa)
            else:
                # MODO CRIAÇÃO
                if not senha:
                    self.label_status_usuarios.configure(text="❌ Senha obrigatória para novo usuário.", text_color="red")
                    return
                sucesso, msg = banco.cadastrar_usuario(username, senha, faixa)

            self.label_status_usuarios.configure(text=msg, text_color="green" if sucesso else "red")
            if sucesso:
                limpar_formulario()
                self.atualizar_lista_usuarios()

        def editar_usuario_callback(user_id, username, faixa):
            self.usuario_em_edicao_id = user_id
            self.entry_novo_username.delete(0, 'end')
            self.entry_novo_username.insert(0, username)
            self.entry_novo_senha.delete(0, 'end')
            self.combobox_nova_faixa.set(faixa.capitalize())
            self.label_status_usuarios.configure(text="")

        def deletar_usuario_callback(user_id, username):
            if username.lower() == "marcelle":
                self.label_status_usuarios.configure(text="❌ Usuário 'marcelle' não pode ser excluído!", text_color="red")
                return
            banco.deletar_usuario(user_id)
            self.label_status_usuarios.configure(text=f"✅ Usuário '{username}' excluído com sucesso!", text_color="green")
            self.atualizar_lista_usuarios()

        # Botão Salvar/Cadastrar
        self.btn_cadastrar_usuario = ctk.CTkButton(
            btn_frame, text="Cadastrar Usuário", command=salvar_usuario, width=140
        )
        self.btn_cadastrar_usuario.pack(side="left", padx=5)

        # Botão Cancelar Edição
        self.btn_cancelar_edicao = ctk.CTkButton(
            btn_frame, text="Cancelar", command=limpar_formulario, width=140
        )
        self.btn_cancelar_edicao.pack(side="left", padx=5)

        self.label_status_usuarios = ctk.CTkLabel(right_frame, text="", text_color="green")
        self.label_status_usuarios.pack(pady=5)

        # Carrega a lista inicial de usuários
        self.atualizar_lista_usuarios()

    def atualizar_lista_usuarios(self):
        """Recarrega a lista de usuários da esquerda."""
        for widget in self.frame_lista_usuarios.winfo_children():
            widget.destroy()

        usuarios = banco.listar_usuarios()
        if not usuarios:
            ctk.CTkLabel(self.frame_lista_usuarios, text="Nenhum usuário cadastrado.").pack(pady=20)
            return

        for user_id, username, faixa in usuarios:
            # Card para cada usuário
            card = ctk.CTkFrame(self.frame_lista_usuarios, fg_color="#2B2B2B")
            card.pack(fill="x", padx=5, pady=5)

            # Info do usuário
            info_text = f"👤 {username} ({faixa.capitalize()})"
            ctk.CTkLabel(card, text=info_text, font=ctk.CTkFont(size=11), text_color="white").pack(side="left", padx=10, pady=8, anchor="w")

            # Botão Editar
            btn_editar = ctk.CTkButton(
                card, text="✏️ Editar", width=70, height=25,
                command=lambda uid=user_id, uname=username, ufaixa=faixa: self.preencher_formulario_edicao(uid, uname, ufaixa)
            )
            btn_editar.pack(side="right", padx=2, pady=4)

            # Botão Excluir (protegido para 'marcelle')
            if username.lower() == "marcelle":
                btn_deletar = ctk.CTkButton(
                    card, text="🔒 Master", width=70, height=25, fg_color="#666666", state="disabled"
                )
            else:
                btn_deletar = ctk.CTkButton(
                    card, text="🗑️ Excluir", width=70, height=25, fg_color="#9c2a2a",
                    command=lambda uid=user_id, uname=username: self.deletar_usuario_aba(uid, uname)
                )
            btn_deletar.pack(side="right", padx=2, pady=4)

    def preencher_formulario_edicao(self, user_id, username, faixa):
        """Preenche o formulário com dados do usuário para edição."""
        self.usuario_em_edicao_id = user_id
        self.entry_novo_username.delete(0, 'end')
        self.entry_novo_username.insert(0, username)
        self.entry_novo_senha.delete(0, 'end')  # Deixa vazio para manter a senha atual
        self.combobox_nova_faixa.set(faixa.capitalize())
        self.label_status_usuarios.configure(text="", text_color="green")

    def deletar_usuario_aba(self, user_id, username):
        """Deleta um usuário e recarrega a lista."""
        if username.lower() == "marcelle":
            self.label_status_usuarios.configure(text="❌ Usuário 'marcelle' não pode ser excluído!", text_color="red")
            return
        banco.deletar_usuario(user_id)
        self.label_status_usuarios.configure(text=f"✅ Usuário '{username}' excluído com sucesso!", text_color="green")
        self.atualizar_lista_usuarios()

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
            ctk.CTkLabel(card, text=info_text, font=ctk.CTkFont(size=12), text_color="white").pack(side="left", padx=15)
            
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
        # Frame centralizado para login com cores da marca
        self.frame_login = ctk.CTkFrame(self, width=400, height=450, fg_color=COR_FUNDO, border_color=COR_PRIMARIA, border_width=2)
        self.frame_login.place(relx=0.5, rely=0.5, anchor="center")

        self.header_login = ctk.CTkLabel(
            self.frame_login, 
            text="SISTEMA DE GESTÃO\n🥋 RAFAEL FARIAS BJJ", 
            font=ctk.CTkFont(size=22, weight="bold"),
            cursor="fleur" 
        )
        self.header_login.pack(pady=(40, 10), fill="x")

        # --- 2. O MOTOR DE MOVIMENTO ---
        def iniciar_arraste(event):
            # Salva o ponto exato onde o mouse clicou dentro do letreiro
            self._drag_start_x = event.x
            self._drag_start_y = event.y

        def arrastar(event):
            # Calcula a nova posição subtraindo a posição inicial do clique
            x = self.frame_login.winfo_x() - self._drag_start_x + event.x
            y = self.frame_login.winfo_y() - self._drag_start_y + event.y
            # Atualiza as coordenadas absolutas na tela cheia
            self.frame_login.place(x=x, y=y, relx=0, rely=0, anchor="nw")

        # Liga os eventos de clique e arrasto no letreiro
        self.header_login.bind("<Button-1>", iniciar_arraste)
        self.header_login.bind("<B1-Motion>", arrastar)

        ctk.CTkLabel(self.frame_login, text="Insira suas credenciais para continuar").pack(pady=(0, 20))

        self.entry_usuario_login = ctk.CTkEntry(self.frame_login, placeholder_text="Usuário", width=300, height=40)
        self.entry_usuario_login.pack(pady=10)

        self.entry_senha_login = ctk.CTkEntry(self.frame_login, placeholder_text="Senha", show="*", width=300, height=40)
        self.entry_senha_login.pack(pady=10)

        self.btn_login_login = ctk.CTkButton(self.frame_login, text="Entrar", command=self.fazer_login, width=300, height=40, fg_color=COR_PRIMARIA, hover_color="#990000", text_color="white")
        self.btn_login_login.pack(pady=20)

        self.label_status_login = ctk.CTkLabel(self.frame_login, text="", text_color="red")
        self.label_status_login.pack(pady=10)

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
            self.mostrar_sistema_principal(usuario_digitado, faixa_banco)
        else:
            self.label_status_login.configure(text="❌ Usuário ou senha incorretos.")
            self.entry_senha_login.delete(0, 'end')

    def mostrar_sistema_principal(self, usuario_logado, faixa_logada):

        self.usuario_logado = usuario_logado
        self.faixa_usuario = faixa_logada.lower()

        # --- 1. BARRA SUPERIOR (HEADER) ---
        self.header_frame = ctk.CTkFrame(self, height=50, corner_radius=0, fg_color=COR_FUNDO, border_color=COR_PRIMARIA, border_width=0)
        self.header_frame.pack(side="top", fill="x")

        # Menus (Esquerda)
        frame_menus = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        frame_menus.pack(side="left", padx=10, pady=5)

       # Botões do Menu Estilo ERP com paleta Rafael Farias BJJ
        ctk.CTkButton(frame_menus, text="Início (Intranet)", fg_color=COR_PRIMARIA, text_color="white", border_color=COR_PRIMARIA, border_width=1, width=100, hover_color="#990000").pack(side="left", padx=2)
        
        # Menu Suspenso de Cadastros com cores da marca
        self.menu_cadastros = ctk.CTkOptionMenu(
            frame_menus,
            values=["Alunos", "Usuários (Acessos)", "Professores", "Turmas e Horários", "Planos de Mensalidade", "Loja (Kimonos e Faixas)"],
            command=self.navegar_cadastro,
            fg_color=COR_FUNDO,
            button_color=COR_PRIMARIA,
            button_hover_color="#990000",
            dropdown_fg_color=COR_FUNDO,
            dropdown_hover_color=COR_PRIMARIA,
            dropdown_text_color="white",
            text_color="white",
            width=150
        )
        self.menu_cadastros.set("Cadastros") # Mantém o título fixo na barra
        self.menu_cadastros.pack(side="left", padx=2)
        
        ctk.CTkButton(frame_menus, text="Financeiro", command=self.renderizar_tela_financeiro, fg_color="transparent", text_color="white", border_color="#555555", border_width=1, width=100).pack(side="left", padx=2)
        
        # O botão de Sair foi movido para o Menu
        ctk.CTkButton(frame_menus, text="🚪 Sair (F10)", fg_color=COR_PRIMARIA, hover_color="#990000", text_color="white", width=80, command=self.fazer_logoff).pack(side="left", padx=20)
        self.bind('<F10>', self.fazer_logoff)

        # Usuário e Relógio (Direita)
        frame_info = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        frame_info.pack(side="right", padx=20, pady=5)

        # Se for o seu usuário, a gente joga o nome completo bonitão igual no print
        nome_exibicao = "MARCELLE SILVA DOS SANTOS" if usuario_logado == "marcelle" else usuario_logado.upper()

        self.label_usuario = ctk.CTkLabel(frame_info, text=f"👤 {nome_exibicao} ({faixa_logada.title()})", font=ctk.CTkFont(size=12, weight="bold"))
        self.label_usuario.pack(side="top", anchor="e")

        self.label_relogio = ctk.CTkLabel(frame_info, text="", font=ctk.CTkFont(size=16, weight="bold"), text_color=COR_PRIMARIA)
        self.label_relogio.pack(side="bottom", anchor="e")

        # Inicia o motorzinho do relógio
        self.atualizar_relogio()

        # --- 2. ÁREA PRINCIPAL (A FUTURA INTRANET) ---
        self.area_trabalho = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        self.area_trabalho.pack(side="top", fill="both", expand=True, padx=20, pady=20)

        # Letreiros provisórios da Intranet
        ctk.CTkLabel(
            self.area_trabalho, 
            text="🥋 Bem-vindo à Intranet do Rafael Farias BJJ", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_PRIMARIA
        ).pack(pady=(40, 10))
        
        ctk.CTkLabel(
            self.area_trabalho, 
            text="Sua plataforma de avisos, campeonatos e integração da equipe.",
            text_color="white"
        ).pack()

    def navegar_cadastro(self, opcao_selecionada):
        # 1. Volta o título do botão para o padrão
        self.menu_cadastros.set("Cadastros ▼")
        
        # 2. Limpa a tela atual (apaga a intranet ou qualquer formulário aberto)
        for widget in self.area_trabalho.winfo_children():
            widget.destroy()

        # 3. Roteador de Telas: Chama as funções individuais para cada menu!
        if opcao_selecionada == "Usuários (Acessos)":
            self.renderizar_tela_usuarios()
            
        elif opcao_selecionada == "Alunos":
            self.renderizar_tela_alunos()
            
        elif opcao_selecionada == "Financeiro":
            self.renderizar_tela_financeiro()

        elif opcao_selecionada == "Turmas e Horários":
            self.renderizar_tela_turmas()
            
        else:
            # Tela genérica para os módulos que ainda não têm função
            ctk.CTkLabel(self.area_trabalho, text=f"🚧 Módulo em Construção: {opcao_selecionada}", font=ctk.CTkFont(size=24, weight="bold"), text_color="orange").pack(pady=50)

    def renderizar_tela_financeiro(self):
        # Limpa a tela (útil se for chamado por um botão direto que não passa pelo navegar_cadastro)
        for widget in self.area_trabalho.winfo_children():
            widget.destroy()
            
        # Instancia a classe do módulo financeiro
        tela = tela_financeiro.TelaFinanceiro(self.area_trabalho, self.usuario_logado, self.faixa_usuario)
        tela.pack(fill="both", expand=True)

    def renderizar_tela_usuarios(self):
        # 🛑 TRAVA DE SEGURANÇA
        if self.faixa_usuario != "preta":
            # (Mantém a lógica de acesso negado aqui)
            return
            
        tela = tela_usuarios.TelaUsuarios(self.area_trabalho, self.usuario_logado, self.faixa_usuario)
        tela.pack(fill="both", expand=True)

    def renderizar_tela_alunos(self):
        # Instancia a classe do módulo externo e "cola" ela dentro da área de trabalho
        tela = tela_alunos.TelaAlunos(self.area_trabalho)
        tela.pack(fill="both", expand=True)

    def renderizar_tela_turmas(self):
        # Instancia a classe do módulo de turmas
        tela = tela_turmas.TelaTurmas(self.area_trabalho, self.usuario_logado, self.faixa_usuario)
        tela.pack(fill="both", expand=True)

    # --- 3. O MOTOR DO RELÓGIO (Adicione logo abaixo) ---
    def atualizar_relogio(self):
        agora = datetime.now()
        data_hora_formatada = agora.strftime("%d/%m/%Y  %H:%M:%S")
        
        try:
            self.label_relogio.configure(text=data_hora_formatada)
            # O sistema chama essa função de novo a cada 1000 milissegundos (1 segundo)
            self.after(1000, self.atualizar_relogio)
        except:
            pass # Previne erros se o sistema for fechado

    # ------------------ LOGOFF (SAIR DA SESSÃO) ------------------
    def fazer_logoff(self, event=None):
        # Destrói os widgets de sistema principal
        try:
            self.header_frame.destroy()
        except Exception:
            pass
        try:
            self.area_trabalho.destroy()
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

        print("🚪 sessão encerrada. Retornando ao login...")
        # Mostra o login novamente
        self.mostrar_login()


if __name__ == "__main__":
    banco.criar_tabelas()
    app = AppAcademia()
    app.mainloop()