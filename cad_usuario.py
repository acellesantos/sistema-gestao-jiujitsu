import customtkinter as ctk
import banco
from datetime import datetime

class TelaUsuarios(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, faixa_logada):
        super().__init__(master, fg_color="transparent")
        self.usuario_logado = usuario_logado
        self.faixa_logada = faixa_logada
        
        self.COR_PRIMARIA = "#CC0000"
        self.COR_FUNDO = "#1A1A1A"
        self.id_em_edicao = None
        self.usuario_em_edicao_id = None

        self.lista_frames_cards = []
        
        # --- CONTAINERS DE TELA (SWAPPING) ---
        self.frame_pesquisa = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_pesquisa.pack(fill="both", expand=True)
        
        self.frame_formulario = ctk.CTkFrame(self, fg_color="transparent")
        
        self.montar_tela_pesquisa()
        self.montar_tela_formulario()
        self.limpar_pesquisa_inicial()

    # ================= 1. VISÃO DE PESQUISA =================
    def montar_tela_pesquisa(self):
        barra_filtros = ctk.CTkFrame(self.frame_pesquisa, fg_color="#2B2B2B", corner_radius=10)
        barra_filtros.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(barra_filtros, text="🔍 Buscar Usuário:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.filtro_nome = ctk.CTkEntry(barra_filtros, placeholder_text="Nome do Usuário", width=300)
        self.filtro_nome.grid(row=0, column=1, padx=5, pady=10)
        
        ctk.CTkButton(barra_filtros, text="Filtrar", width=100, fg_color="#444444", hover_color=self.COR_PRIMARIA, command=self.filtrar_busca).grid(row=0, column=2, padx=(0, 10))
        ctk.CTkButton(barra_filtros, text="📋 Todos", width=80, fg_color="#444444", hover_color=self.COR_PRIMARIA, command=self.listar_todos).grid(row=0, column=3, padx=(0, 10))
        ctk.CTkButton(barra_filtros, text="🛡️ Auditoria", width=100, fg_color="#555555", hover_color="#333333", command=self.abrir_auditoria_especifica).grid(row=0, column=4, padx=(0, 10))
        ctk.CTkButton(barra_filtros, text="➕ Novo Usuário", fg_color="green", hover_color="#005500", command=self.abrir_formulario_novo).grid(row=0, column=5, padx=20)

        self.label_status_usuarios = ctk.CTkLabel(self.frame_pesquisa, text="", font=ctk.CTkFont(weight="bold"))
        self.label_status_usuarios.pack(fill="x", padx=20, pady=(0, 10))

        cabecalho = ctk.CTkFrame(self.frame_pesquisa, fg_color="#444444", corner_radius=0)
        cabecalho.pack(fill="x", padx=20, pady=(0, 2))
        ctk.CTkLabel(cabecalho, text="ID | Nome | Nível de Acesso", text_color="white", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=20, pady=5)

        self.lista_scroll = ctk.CTkScrollableFrame(self.frame_pesquisa, fg_color="transparent")
        self.lista_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    def limpar_pesquisa_inicial(self):
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
            
        ctk.CTkLabel(
            self.lista_scroll, 
            text="👆 Utilize o campo acima e clique em 'Filtrar' para buscar um usuário.", 
            text_color="gray", 
            font=ctk.CTkFont(slant="italic")
        ).pack(pady=50)

    def filtrar_busca(self):
        termo_busca = self.filtro_nome.get().strip().lower()
        
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()

        self.lista_frames_cards = []
            
        if not termo_busca:
            ctk.CTkLabel(self.lista_scroll, text="⚠️ Digite um nome para pesquisar.", text_color="orange").pack(pady=20)
            return

        # MOCKUP: Simula o que viria do banco
        usuarios_cadastrados = [
            (5066, "MARCELLE SILVA DOS SANTOS", "Administrador"), 
            (3279, "MARCELLE DA SILVA SANTOS", "Recepção")
        ]
        
        resultados = 0
        print(f"[LOG] Pesquisando usuários com termo: \'{termo_busca}\'")
        usuarios_reais = [u for u in banco.listar_usuarios() if termo_busca in u[1].lower()]
        
        resultados = 0
        if usuarios_reais:
            for usr in usuarios_reais:
                self.criar_linha_resultado(usr)
                resultados += 1
        
        if resultados == 0:
            ctk.CTkLabel(self.lista_scroll, text="Nenhum usuário encontrado com este termo.", text_color="gray").pack(pady=20)


    def criar_linha_resultado(self, usuario):
        id_usr, nome, nivel = usuario
        
        # Cursor de mãozinha para indicar que a linha é clicável
        linha = ctk.CTkFrame(self.lista_scroll, fg_color="#333333", height=40, cursor="hand2")
        linha.pack(fill="x", pady=2, padx=4)
        
        # Guarda a linha na nossa lista para podermos mudar a cor dela depois
        self.lista_frames_cards.append(linha)
        
        # Cursor de mãozinha no texto também
        lbl_texto = ctk.CTkLabel(linha, text=f"ID: {id_usr:04d}  |  {nome}  |  {nivel}", text_color="white", cursor="hand2")
        lbl_texto.pack(side="left", padx=15, pady=5)
        
        # 👇 A MÁGICA: O clique no card ou no texto seleciona a linha
        linha.bind("<Button-1>", lambda e, uid=id_usr, l=linha: self.selecionar_linha(uid, l))
        lbl_texto.bind("<Button-1>", lambda e, uid=id_usr, l=linha: self.selecionar_linha(uid, l))
        
        # Botão Editar
        btn_editar = ctk.CTkButton(
            linha, text="📋 Editar", width=80, fg_color="#444444", hover_color=self.COR_PRIMARIA, 
            command=lambda u=usuario: self.carregar_ficha(u)
        )
        btn_editar.pack(side="right", padx=10, pady=5)

    def selecionar_linha(self, user_id, linha_selecionada):
        # 1. Volta a cor de todas as linhas para o padrão escuro (#333333)
        for frame in self.lista_frames_cards:
            try:
                frame.configure(fg_color="#333333")
            except:
                pass
                
        # 2. Pinta APENAS a linha clicada de vermelho escuro
        linha_selecionada.configure(fg_color="#550000")
        
        # 3. Salva o ID do usuário clicado para a Auditoria saber quem buscar!
        self.usuario_em_edicao_id = user_id
        self.id_em_edicao = user_id
        
        # Limpa qualquer aviso amarelo da tela
        self.label_status_usuarios.configure(text="")

    # ================= 2. VISÃO DE FORMULÁRIO (ESTILO ERP CAMIM) =================
    def montar_tela_formulario(self):
        topo_nav = ctk.CTkFrame(self.frame_formulario, fg_color="transparent")
        topo_nav.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(topo_nav, text="🔙 Voltar", width=100, fg_color="#444444", command=self.voltar_para_pesquisa).pack(side="left")
        self.lbl_titulo_form = ctk.CTkLabel(topo_nav, text="👤 Editando Usuário", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_titulo_form.pack(side="left", padx=50)

        corpo = ctk.CTkFrame(self.frame_formulario, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=20, pady=10)

        # Lado Esquerdo como ScrollableFrame
        lado_esquerdo = ctk.CTkScrollableFrame(corpo, fg_color="#2B2B2B", width=350)
        lado_esquerdo.pack(side="left", fill="both", padx=(0, 10))

        ctk.CTkLabel(lado_esquerdo, text="Credenciais de Acesso", font=ctk.CTkFont(weight="bold"), text_color=self.COR_PRIMARIA).pack(pady=15)

        self.entry_login = self.criar_campo(lado_esquerdo, "Login / Usuário:")
        self.entry_nome = self.criar_campo(lado_esquerdo, "Nome Completo:")
        
        ctk.CTkLabel(lado_esquerdo, text="Senha do Sistema:").pack(anchor="w", padx=20, pady=(10,0))
        self.entry_senha = ctk.CTkEntry(lado_esquerdo, width=310, show="*")
        self.entry_senha.pack(pady=2, padx=20)
        
        self.entry_email = self.criar_campo(lado_esquerdo, "E-mail Corporativo:")
        self.entry_tel = self.criar_campo(lado_esquerdo, "Telefone Celular:")
        
        ctk.CTkLabel(lado_esquerdo, text="Nível de Acesso (Setor):").pack(anchor="w", padx=20, pady=(10,0))
        self.combo_nivel = ctk.CTkOptionMenu(lado_esquerdo, values=["Recepção", "Professor", "Administrador"], width=310, fg_color="#444444", button_color=self.COR_PRIMARIA)
        self.combo_nivel.pack(pady=2, padx=20)

        self.check_ativo = ctk.CTkCheckBox(lado_esquerdo, text="Usuário Ativo", fg_color="green")
        self.check_ativo.pack(pady=20, anchor="w", padx=20)
        self.check_ativo.select()

        self.label_status = ctk.CTkLabel(lado_esquerdo, text="")
        self.label_status.pack()

        self.btn_salvar = ctk.CTkButton(lado_esquerdo, text="💾 Salvar Usuário", command=self.salvar_usuario, width=310, fg_color="green")
        self.btn_salvar.pack(pady=(20, 10))

        self.btn_acessos = ctk.CTkButton(lado_esquerdo, text="🔐 Gerenciar Acessos", fg_color="#B8860B", hover_color="#8B6508", command=self.abrir_modal_acessos)
        
        # Botão de Excluir Usuário (inicialmente oculto para novos cadastros)
        self.btn_excluir = ctk.CTkButton(lado_esquerdo, text="❌ Excluir Usuário", command=self.deletar_usuario, width=310, fg_color="#7F0000", hover_color="#590000")
        # Não empacota aqui, será feito no carregar_ficha


        # Lado Direito (Histórico)
        lado_direito = ctk.CTkFrame(corpo, fg_color="#1E1E1E", border_color="#333333", border_width=1)
        lado_direito.pack(side="right", fill="both", expand=True)

        header_dir = ctk.CTkFrame(lado_direito, fg_color="#333333", corner_radius=0)
        header_dir.pack(fill="x")
        ctk.CTkLabel(header_dir, text="📅 Histórico de Acessos (Dias Trabalhados)", font=ctk.CTkFont(weight="bold")).pack(pady=10)

        titulos_grid = ctk.CTkFrame(lado_direito, fg_color="#2B2B2B", corner_radius=0)
        titulos_grid.pack(fill="x", padx=10, pady=(10,0))
        ctk.CTkLabel(titulos_grid, text="Data/Hora Entrada", width=200, anchor="w").pack(side="left", padx=10)
        ctk.CTkLabel(titulos_grid, text="Data/Hora Saída", width=200, anchor="w").pack(side="left", padx=10)

        self.scroll_logs = ctk.CTkScrollableFrame(lado_direito, fg_color="transparent")
        self.scroll_logs.pack(fill="both", expand=True, padx=10, pady=5)

    def criar_campo(self, master, texto):
        ctk.CTkLabel(master, text=texto).pack(anchor="w", padx=20, pady=(10,0))
        entry = ctk.CTkEntry(master, width=310)
        entry.pack(pady=2, padx=20)
        return entry

    # ================= 3. LÓGICA DE NAVEGAÇÃO =================
    def abrir_formulario_novo(self):
        self.id_em_edicao = None
        self.usuario_em_edicao_id = None
        self.lbl_titulo_form.configure(text="👤 Novo Cadastro de Usuário")
        self.btn_salvar.configure(text="💾 Cadastrar", fg_color="green")

        self.btn_acessos.pack_forget()
        
        self.entry_login.delete(0, 'end')
        self.entry_nome.delete(0, 'end')
        self.entry_senha.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_tel.delete(0, 'end')
        self.label_status.configure(text="")
        
        for w in self.scroll_logs.winfo_children(): w.destroy()
        ctk.CTkLabel(self.scroll_logs, text="Nenhum acesso registrado ainda.", text_color="gray").pack(pady=20)
        
        # Esconde o botão de excluir para novos cadastros
        self.btn_excluir.pack_forget()

        self.frame_pesquisa.pack_forget()
        self.frame_formulario.pack(fill="both", expand=True)

    def carregar_ficha(self, usuario):
        self.abrir_formulario_novo()
        id_usr, username_db, faixa_db = usuario # Dados do resumo da lista

        usuario_completo = banco.obter_usuario(id_usr) # Busca todos os dados no banco
        if not usuario_completo:
            self.label_status.configure(text="❌ Erro ao carregar dados do usuário.", text_color="red")
            return
        
        # Desempacota os dados completos (id, username, senha, faixa)
        # Note: A tabela `usuarios` no banco.py possui `id, username, senha, faixa`
        id_usr, login, senha_hash, nivel = usuario_completo

        self.id_em_edicao = id_usr
        self.usuario_em_edicao_id = id_usr
        self.lbl_titulo_form.configure(text=f"👤 Editando Usuário: {login.upper()}")
        self.btn_salvar.configure(text="💾 Atualizar", fg_color=self.COR_PRIMARIA)
        
        # Mostra o botão de excluir na edição
        self.btn_excluir.pack(pady=(10, 20))
        
        self.entry_login.delete(0, 'end')
        self.entry_login.insert(0, login)
        
        self.entry_nome.delete(0, 'end')
        # Assumindo que 'nome' completo não está em 'usuarios' ou é igual a 'login' para este mockup
        self.entry_nome.insert(0, login.capitalize()) 
        
        self.entry_senha.delete(0, 'end') # Senha sempre vazia para edição (opcional)
        
        self.entry_email.delete(0, 'end')
        self.entry_email.insert(0, f"{login}@academia.com") # Mock de e-mail
        
        self.entry_tel.delete(0, 'end')
        self.entry_tel.insert(0, "(99) 99999-9999") # Mock de telefone

        self.combo_nivel.set(nivel.capitalize())
        
        self.check_ativo.select() # Assume ativo na edição

        for w in self.scroll_logs.winfo_children(): w.destroy()
        # MOCKUP de logs de acesso
        logs_exemplo = [
            ("11/03/2026 13:53:52", "11/03/2026 18:05:14"),
            ("12/03/2026 09:11:24", "12/03/2026 16:37:49"),
            ("13/03/2026 09:53:51", "13/03/2026 15:37:12")
        ]
        for entrada, saida in logs_exemplo:
            linha = ctk.CTkFrame(self.scroll_logs, fg_color="#333333", height=30)
            linha.pack(fill="x", pady=2)
            ctk.CTkLabel(linha, text=entrada, width=200, anchor="w").pack(side="left", padx=10)
            ctk.CTkLabel(linha, text=saida, width=200, anchor="w").pack(side="left", padx=10)

        if self.faixa_logada.lower() in ["administrador", "preta", "admin"]:
            self.btn_acessos.pack(pady=(10, 0))
        else:
            self.btn_acessos.pack_forget()    

    def voltar_para_pesquisa(self):
        self.frame_formulario.pack_forget()
        self.frame_pesquisa.pack(fill="both", expand=True)
        self.limpar_pesquisa_inicial()

    def salvar_usuario(self):
        login = self.entry_login.get().strip().lower()
        nome = self.entry_nome.get().strip()
        senha = self.entry_senha.get().strip()
        email = self.entry_email.get().strip()
        telefone = self.entry_tel.get().strip()
        nivel = self.combo_nivel.get().strip().lower()
        ativo = "ativo" if self.check_ativo.get() == 1 else "inativo"

        if not login or not nome or not nivel:
            self.label_status.configure(text="❌ Preencha Login, Nome e Nível.", text_color="red")
            return
        
        # Lógica de persistência (INSERT ou UPDATE)
        if self.id_em_edicao is not None:
            # Modo Edição
            # A função atualizar_usuario no banco.py já trata a senha opcional
            print(f"[LOG] Tentando atualizar usuário {login} (ID: {self.id_em_edicao})...")
            sucesso, msg = banco.atualizar_usuario(self.id_em_edicao, login, senha, nivel)
        else:
            # Modo Criação
            if not senha:
                self.label_status.configure(text="❌ Senha obrigatória para novo usuário.", text_color="red")
                return
            print(f"[LOG] Tentando cadastrar novo usuário: {login}...")
            sucesso, msg = banco.cadastrar_usuario(login, senha, nivel)

        print(f"[LOG] Retorno do banco - Sucesso: {sucesso}, Mensagem: {msg}")
        self.label_status.configure(text=msg, text_color="green" if sucesso else "red")
        if sucesso:
            self.frame_formulario.after(1000, self.voltar_para_pesquisa) # Volta para a lista após 1 segundo

    def listar_todos(self):
        """Lista todos os usuários do banco de dados sem filtro."""
        for widget in self.lista_scroll.winfo_children(): widget.destroy()
        self.lista_frames_cards = []
        usuarios = banco.listar_usuarios() 
        if not usuarios:
            ctk.CTkLabel(self.lista_scroll, text="Nenhum usuário cadastrado no banco.", text_color="gray").pack(pady=20)
            return
        for usr in usuarios:
            self.criar_linha_resultado(usr)

    def deletar_usuario(self):
        if not self.id_em_edicao:
            self.label_status.configure(text="❌ Nenhum usuário selecionado para exclusão.", text_color="red")
            return

        # Obter o usuário para verificar se é o admin
        usuario_para_deletar = banco.obter_usuario(self.id_em_edicao)
        if usuario_para_deletar and usuario_para_deletar[1].lower() == "admin": # usuario_completo[1] é o username
            self.label_status.configure(text="❌ O usuário Master Admin não pode ser excluído!", text_color="red")
            return

        sucesso, msg = banco.deletar_usuario(self.id_em_edicao)
        self.label_status.configure(text=msg, text_color="green" if sucesso else "red")
        if sucesso:
            self.frame_formulario.after(1500, self.voltar_para_pesquisa) # Volta após 1.5 segundos

    def abrir_modal_acessos(self):
        modal = ctk.CTkToplevel(self)
        modal.title("🔐 Matriz de Acessos")
        modal.geometry("400x450")
        modal.transient(self.winfo_toplevel()) # Mantém na frente
        modal.grab_set() # Congela a tela de trás
        
        ctk.CTkLabel(modal, text="Liberação de Módulos", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)
        
        modulos = ["Financeiro", "Estoque/Loja", "Relatórios Gerenciais", "Configurações do Sistema"]
        vars_checkboxes = {}
        
        for mod in modulos:
            var = ctk.StringVar(value="off")
            cb = ctk.CTkCheckBox(modal, text=mod, variable=var, onvalue=mod, offvalue="off", fg_color=self.COR_PRIMARIA)
            cb.pack(pady=10, anchor="w", padx=50)
            vars_checkboxes[mod] = var
            
        def salvar_modal():
            selecionadas = [var.get() for mod, var in vars_checkboxes.items() if var.get() != "off"]
            sucesso, msg = banco.salvar_permissoes_auditoria(self.id_em_edicao, selecionadas, self.usuario_logado)
            if sucesso:
                self.label_status.configure(text="✅ Acessos e Auditoria gravados!", text_color="green")
                modal.destroy()
                
        ctk.CTkButton(modal, text="💾 Gravar Permissões", fg_color="green", command=salvar_modal).pack(pady=30)

    def abrir_auditoria_especifica(self):
        # VALIDAÇÃO: Verifique se há um usuário em edição. Ex: if not getattr(self, 'usuario_em_edicao_id', None):
        if not getattr(self, 'usuario_em_edicao_id', None):
            self.label_status_usuarios.configure(text="⚠️ Selecione um usuário na lista primeiro para ver a auditoria.", text_color="orange")
            return

        # Se houver usuário, abra um modal ctk.CTkToplevel(self)
        modal = ctk.CTkToplevel(self)
        modal.title(f"🛡️ Auditoria do Usuário ID: {self.usuario_em_edicao_id}")
        modal.geometry("750x500")
        modal.transient(self.winfo_toplevel())
        modal.grab_set()

        # Cabeçalho para a grade com as colunas fixas: "Data/Hora" (width=160), "Responsável" (width=150) e "Descrição da Alteração"
        header = ctk.CTkFrame(modal, fg_color="#2B2B2B")
        header.pack(fill="x", padx=20, pady=(20, 0))
        ctk.CTkLabel(header, text="Data/Hora", width=160, font=("Arial", 12, "bold"), anchor="w").pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(header, text="Responsável", width=150, font=("Arial", 12, "bold"), anchor="w").pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(header, text="Descrição da Alteração", font=("Arial", 12, "bold"), anchor="w").pack(side="left", padx=10, pady=10)

        # Preencha um CTkScrollableFrame iterando sobre os logs gerando uma linha (CTkFrame) para cada registro
        scroll = ctk.CTkScrollableFrame(modal, fg_color="#1E1E1E")
        scroll.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Chame a função do banco
        logs = banco.listar_auditoria_por_usuario(self.usuario_em_edicao_id)

        if not logs:
            ctk.CTkLabel(scroll, text="Nenhuma alteração registrada para este usuário.", text_color="gray").pack(pady=20)
        else:
            for data, admin, acao in logs:
                linha = ctk.CTkFrame(scroll, fg_color="transparent")
                linha.pack(fill="x", pady=2)
                ctk.CTkLabel(linha, text=str(data), width=160, anchor="w").pack(side="left", padx=10)
                ctk.CTkLabel(linha, text=str(admin), width=150, anchor="w").pack(side="left", padx=10)
                ctk.CTkLabel(linha, text=str(acao), anchor="w").pack(side="left", padx=10)

        # Botão "⬅️ Voltar" com command=modal.destroy no rodapé
        ctk.CTkButton(modal, text="⬅️ Voltar", fg_color="#444444", command=modal.destroy).pack(pady=15)
