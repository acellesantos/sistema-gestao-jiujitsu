import customtkinter as ctk
import banco
import re
from datetime import datetime

class TelaAlunos(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        self.id_em_edicao = None
        self.idade_calculada = 0
        
        self.COR_PRIMARIA = "#CC0000"
        self.COR_FUNDO = "#1A1A1A"
        
        # --- CONTAINERS DE TELA (SWAPPING) ---
        # 1. Container de Pesquisa (Visível por padrão)
        self.frame_pesquisa = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_pesquisa.pack(fill="both", expand=True)
        
        # 2. Container do Formulário (Oculto por padrão)
        self.frame_formulario = ctk.CTkFrame(self, fg_color="transparent")
        
        self.montar_tela_pesquisa()
        self.montar_tela_formulario()
        
        # Inicia a tela carregando todos os alunos na pesquisa
        self.recarregar_lista()

    # ================= 1. VISÃO DE PESQUISA (ESTILO ERP) =================
    def montar_tela_pesquisa(self):
        # Barra Superior de Filtros Densos
        barra_filtros = ctk.CTkFrame(self.frame_pesquisa, fg_color="#2B2B2B", corner_radius=10)
        barra_filtros.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(barra_filtros, text="🔍 Buscar Aluno:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        
        self.filtro_mat = ctk.CTkEntry(barra_filtros, placeholder_text="Matrícula", width=100)
        self.filtro_mat.grid(row=0, column=1, padx=5, pady=10)
        
        self.filtro_nome = ctk.CTkEntry(barra_filtros, placeholder_text="Nome do Aluno", width=180)
        self.filtro_nome.grid(row=0, column=2, padx=5, pady=10)
        
        self.filtro_cpf = ctk.CTkEntry(barra_filtros, placeholder_text="CPF do Aluno", width=150)
        self.filtro_cpf.grid(row=0, column=3, padx=5, pady=10)
        
        self.filtro_resp = ctk.CTkEntry(barra_filtros, placeholder_text="Nome/CPF Responsável", width=180)
        self.filtro_resp.grid(row=0, column=4, padx=5, pady=10)
        
        # Botões de Ação
        ctk.CTkButton(barra_filtros, text="Filtrar", width=80, fg_color="#444444", hover_color=self.COR_PRIMARIA, command=self.filtrar_busca).grid(row=0, column=5, padx=10)
        ctk.CTkButton(barra_filtros, text="➕ Nova Ficha de Inclusão", fg_color="#4CAF50", hover_color="#45a049", command=self.abrir_formulario_novo).grid(row=0, column=6, padx=10)

        # Cabeçalho da Grade
        cabecalho = ctk.CTkFrame(self.frame_pesquisa, fg_color="#444444", corner_radius=0)
        cabecalho.pack(fill="x", padx=20, pady=(0, 2))
        ctk.CTkLabel(cabecalho, text="Matrícula  |  Nome do Aluno  |  Faixa  |  Status", text_color="white", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=20, pady=5)

        # Grade de Resultados
        self.lista_scroll = ctk.CTkScrollableFrame(self.frame_pesquisa, fg_color="transparent")
        self.lista_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    # ================= 2. VISÃO DE FORMULÁRIO (FICHA DE INCLUSÃO) =================
    def montar_tela_formulario(self):
        # === 1. HEADER DE DESTAQUE (Dashboard de Prontuário) ===
        self.header_destaque = ctk.CTkFrame(self.frame_formulario, fg_color=self.COR_PRIMARIA, height=100, corner_radius=10)
        self.header_destaque.pack(fill="x", padx=20, pady=(10, 5))

        # Avatar (Ícone) - Lado esquerdo
        ctk.CTkLabel(self.header_destaque, text="👤", font=ctk.CTkFont(size=40), text_color="white").pack(side="left", padx=15, pady=10)

        # Nome e Matrícula (Prenchidos dinamicamente)
        info_frame = ctk.CTkFrame(self.header_destaque, fg_color="transparent")
        info_frame.pack(side="left", fill="y", pady=10)
        
        self.lbl_aluno_nome = ctk.CTkLabel(info_frame, text="NOME DO ALUNO", font=ctk.CTkFont(size=24, weight="bold"), text_color="white", anchor="w")
        self.lbl_aluno_nome.pack(pady=(0,2))
        self.lbl_aluno_matricula = ctk.CTkLabel(info_frame, text="MATRÍCULA: #0000", font=ctk.CTkFont(size=14), text_color="white", anchor="w")
        self.lbl_aluno_matricula.pack()

        # Quadro de Mensalidade - Lado direito
        mensalidade_frame = ctk.CTkFrame(self.header_destaque, fg_color="green", corner_radius=8)
        mensalidade_frame.pack(side="right", padx=15, pady=10)
        ctk.CTkLabel(mensalidade_frame, text="MENSALIDADE", font=ctk.CTkFont(size=12, weight="bold"), text_color="white").pack(padx=10, pady=(5,0))
        self.lbl_mensalidade_valor = ctk.CTkLabel(mensalidade_frame, text="R$ 150,00", font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(padx=10, pady=(0,5))

        # Botão de Voltar para Pesquisa (abaixo do header)
        ctk.CTkButton(self.frame_formulario, text="🔙 Voltar para Pesquisa", width=180, fg_color="#444444", hover_color="#2B2B2B", command=self.voltar_para_pesquisa).pack(anchor="nw", padx=20, pady=(5, 10))

        # === 2. SISTEMA DE ABAS (CTkTabview) ===
        self.tabview = ctk.CTkTabview(self.frame_formulario, fg_color="#2B2B2B", segmented_button_fg_color=self.COR_PRIMARIA, segmented_button_selected_color="#990000")
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tab_dados_cadastrais = self.tabview.add("📋 Dados Cadastrais")
        self.tab_financeiro = self.tabview.add("💰 Financeiro")
        self.tab_turmas = self.tabview.add("🥋 Turmas/Frequência")

        # --- CONTEÚDO DA ABA "DADOS CADASTRAIS" (com 2 colunas) ---
        self.scroll_dados_cadastrais = ctk.CTkScrollableFrame(self.tab_dados_cadastrais, fg_color="transparent")
        self.scroll_dados_cadastrais.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para as duas colunas dentro do scroll
        cols_frame = ctk.CTkFrame(self.scroll_dados_cadastrais, fg_color="transparent")
        cols_frame.pack(fill="x", expand=True)

        self.col_esquerda = ctk.CTkFrame(cols_frame, fg_color="transparent")
        self.col_esquerda.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.col_direita = ctk.CTkFrame(cols_frame, fg_color="transparent")
        self.col_direita.pack(side="right", fill="x", expand=True, padx=(10, 0))

        # Reorganiza os campos existentes nas duas colunas
        # Coluna Esquerda
        ctk.CTkLabel(self.col_esquerda, text="Nome Completo:", anchor="w").pack(fill="x", pady=(5,0))
        self.entry_nome = ctk.CTkEntry(self.col_esquerda, placeholder_text="Nome Completo do Aluno")
        self.entry_nome.pack(fill="x", pady=(0,10))

        ctk.CTkLabel(self.col_esquerda, text="CPF (Apenas Números):").pack(fill="x", pady=(5,0))
        self.entry_cpf = ctk.CTkEntry(self.col_esquerda, placeholder_text="CPF (Apenas Números)")
        self.entry_cpf.pack(fill="x", pady=(0,10))
        self.entry_cpf.bind("<KeyRelease>", self.formatar_cpf)

        ctk.CTkLabel(self.col_esquerda, text="Data de Nascimento (DD/MM/AAAA):").pack(fill="x", pady=(5,0))
        self.entry_data = ctk.CTkEntry(self.col_esquerda, placeholder_text="Data de Nasc. (DD/MM/AAAA)")
        self.entry_data.pack(fill="x", pady=(0,10))
        self.entry_data.bind("<KeyRelease>", self.formatar_data)
        self.entry_data.bind("<FocusOut>", self.verificar_idade)

        self.label_idade = ctk.CTkLabel(self.col_esquerda, text="Idade: --", text_color="gray")
        self.label_idade.pack(anchor="w", pady=(0,10))

        # Coluna Direita
        ctk.CTkLabel(self.col_direita, text="Telefone / WhatsApp:").pack(fill="x", pady=(5,0))
        self.entry_tel = ctk.CTkEntry(self.col_direita, placeholder_text="Telefone / WhatsApp")
        self.entry_tel.pack(fill="x", pady=(0,10))
        self.entry_tel.bind("<KeyRelease>", self.formatar_telefone)

        ctk.CTkLabel(self.col_direita, text="Endereço Completo:").pack(fill="x", pady=(5,0))
        self.entry_end = ctk.CTkEntry(self.col_direita, placeholder_text="Endereço Completo")
        self.entry_end.pack(fill="x", pady=(0,10))

        ctk.CTkLabel(self.col_direita, text="Graduação Inicial:").pack(fill="x", pady=(5,0))
        self.combo_faixa = ctk.CTkOptionMenu(self.col_direita, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], fg_color="#444444", button_color=self.COR_PRIMARIA)
        self.combo_faixa.pack(fill="x", pady=(0,10))

        # Frame Responsável (fora das colunas, mas dentro do scroll_dados_cadastrais)
        self.frame_responsavel = ctk.CTkFrame(self.scroll_dados_cadastrais, fg_color="#333333")
        ctk.CTkLabel(self.frame_responsavel, text="⚠️ Aluno Menor de Idade - Dados do Responsável", text_color="orange", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        ctk.CTkLabel(self.frame_responsavel, text="Nome do Responsável Legal:").pack(fill="x", padx=10, pady=(5,0))
        self.entry_resp_nome = ctk.CTkEntry(self.frame_responsavel, placeholder_text="Nome do Responsável Legal")
        self.entry_resp_nome.pack(fill="x", padx=10, pady=(0,5))
        
        ctk.CTkLabel(self.frame_responsavel, text="CPF do Responsável:").pack(fill="x", padx=10, pady=(5,0))
        self.entry_resp_cpf = ctk.CTkEntry(self.frame_responsavel, placeholder_text="CPF do Responsável")
        self.entry_resp_cpf.pack(fill="x", padx=10, pady=(0,5))
        
        ctk.CTkLabel(self.frame_responsavel, text="Telefone do Responsável:").pack(fill="x", padx=10, pady=(5,0))
        self.entry_resp_tel = ctk.CTkEntry(self.frame_responsavel, placeholder_text="Telefone do Responsável")
        self.entry_resp_tel.pack(fill="x", padx=10, pady=(0,15))
        self.entry_resp_tel.bind("<KeyRelease>", self.formatar_telefone_resp)

        # LGPD e Botão Salvar (abaixo do frame_responsavel, dentro do scroll_dados_cadastrais)
        self.check_lgpd = ctk.CTkCheckBox(self.scroll_dados_cadastrais, text="Concordo com os Termos e a Política de Privacidade (LGPD)", fg_color=self.COR_PRIMARIA)
        self.check_lgpd.pack(pady=20, anchor="w")

        self.label_status = ctk.CTkLabel(self.scroll_dados_cadastrais, text="", font=ctk.CTkFont(weight="bold"))
        self.label_status.pack(pady=5)

        self.btn_salvar = ctk.CTkButton(self.scroll_dados_cadastrais, text="💾 Salvar Matrícula", command=self.salvar_aluno, fg_color="#4CAF50", hover_color="#45a049")
        self.btn_salvar.pack(pady=20)

        # --- CONTEÚDO DA ABA "FINANCEIRO" ---
        ctk.CTkLabel(self.tab_financeiro, text="Conteúdo do Financeiro será adicionado aqui.", text_color="gray").pack(pady=20)

        # --- CONTEÚDO DA ABA "TURMAS/FREQUÊNCIA" ---
        ctk.CTkLabel(self.tab_turmas, text="Conteúdo de Turmas e Frequência será adicionado aqui.", text_color="gray").pack(pady=20)


    # ================= 3. LÓGICA DE NAVEGAÇÃO =================
    def abrir_formulario_novo(self):
        self.id_em_edicao = None
        self.idade_calculada = 0
        
        # Configura os novos rótulos do cabeçalho para os valores padrão de um novo aluno
        self.lbl_aluno_nome.configure(text="NOVO ALUNO")
        self.lbl_aluno_matricula.configure(text="MATRÍCULA: NOVA | FAIXA: --")
        # self.lbl_mensalidade_valor.configure(text="R$ 00,00")  # Se for dinâmico, descomente e ajuste aqui
        
        self.btn_salvar.configure(text="💾 Salvar Matrícula", fg_color="#4CAF50", hover_color="#45a049")
        
        # Limpa tudo
        self.entry_nome.delete(0, 'end')
        self.entry_cpf.delete(0, 'end')
        self.entry_data.delete(0, 'end')
        self.entry_tel.delete(0, 'end')
        self.entry_end.delete(0, 'end')
        self.entry_resp_nome.delete(0, 'end')
        self.entry_resp_cpf.delete(0, 'end')
        self.entry_resp_tel.delete(0, 'end')
        self.check_lgpd.deselect()
        self.label_idade.configure(text="Idade: --")
        self.frame_responsavel.pack_forget()
        self.label_status.configure(text="")
        
        # Garante que o formulário sempre abra focado na aba "Dados Cadastrais"
        self.tabview.set("📋 Dados Cadastrais")
        
        # Troca as telas
        self.frame_pesquisa.pack_forget()
        self.frame_formulario.pack(fill="both", expand=True)

    def voltar_para_pesquisa(self):
        self.frame_formulario.pack_forget()
        self.frame_pesquisa.pack(fill="both", expand=True)
        self.recarregar_lista()

    # ================= 4. LÓGICA DE PESQUISA E LISTAGEM =================
    def recarregar_lista(self):
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
            
        for aluno in banco.listar_todos_alunos():
            id_aluno, nome, faixa, status, telefone = aluno
            self.criar_linha_resultado(aluno)

    def filtrar_busca(self):
        # Captura os filtros
        f_mat = self.filtro_mat.get().strip()
        f_nome = self.filtro_nome.get().strip().lower()
        f_cpf = re.sub(r'\D', '', self.filtro_cpf.get().strip())
        f_resp = self.filtro_resp.get().strip().lower()
        
        for widget in self.lista_scroll.winfo_children():
            widget.destroy()
            
        # Puxa todos os dados completos para permitir filtragem avançada
        for aluno_resumo in banco.listar_todos_alunos():
            id_aluno = aluno_resumo[0]
            aluno_completo = banco.obter_aluno(id_aluno)
            
            if not aluno_completo: continue
            
            # Desempacota
            (_, nome, cpf, _, _, _, _, _, _, resp_nome, resp_cpf, _) = aluno_completo
            matricula_str = f"#{id_aluno:04d}"
            cpf_limpo = re.sub(r'\D', '', cpf) if cpf else ""
            resp_cpf_limpo = re.sub(r'\D', '', resp_cpf) if resp_cpf else ""
            
            # Lógica de Match (se o filtro estiver preenchido e não bater, ignora o aluno)
            if f_mat and f_mat not in matricula_str and f_mat != str(id_aluno): continue
            if f_nome and f_nome not in (nome.lower() if nome else ""): continue
            if f_cpf and f_cpf not in cpf_limpo: continue
            if f_resp:
                resp_match = f_resp in (resp_nome.lower() if resp_nome else "") or f_resp in resp_cpf_limpo
                if not resp_match: continue
                
            self.criar_linha_resultado(aluno_resumo)

    def criar_linha_resultado(self, aluno):
        id_aluno, nome, faixa, status, telefone = aluno
        matricula = f"#{id_aluno:04d}"
        
        linha = ctk.CTkFrame(self.lista_scroll, fg_color="#333333", height=40)
        linha.pack(fill="x", pady=2, padx=4)
        
        ctk.CTkLabel(linha, text=f"🥋 {matricula}  |  {nome}  |  {faixa.title()}  |  📞 {telefone}", text_color="white").pack(side="left", padx=15, pady=5)
        
        btn_abrir = ctk.CTkButton(linha, text="📋 Abrir Ficha", width=100, height=28, fg_color="#444444", hover_color=self.COR_PRIMARIA, command=lambda a=aluno: self.carregar_ficha(a))
        btn_abrir.pack(side="right", padx=10, pady=5)

    # ================= 5. MÉTODOS DE INTELIGÊNCIA (MANTIDOS INTACTOS) =================
    
    def carregar_ficha(self, aluno_dados):
        self.abrir_formulario_novo() # Limpa e troca a tela primeiro
        
        id_aluno = aluno_dados[0]
        aluno_completo = banco.obter_aluno(id_aluno)
        if not aluno_completo: return
            
        (id_aluno, nome, cpf, data_nasc, idade, telefone, endereco, faixa, lgpd, resp_nome, resp_cpf, resp_tel) = aluno_completo
         
        self.id_em_edicao = id_aluno
        self.idade_calculada = idade
        
        # Atualiza o header de destaque
        self.lbl_aluno_nome.configure(text=nome.upper() if nome else "NOME DO ALUNO")
        self.lbl_aluno_matricula.configure(text=f"MATRÍCULA: #{id_aluno:04d}")
        # Aqui você poderia configurar o lbl_mensalidade_valor dinamicamente também, se tiver o dado no banco

        # Configura o botão de salvar
        self.btn_salvar.configure(text=f"💾 Atualizar Matrícula #{id_aluno:04d}", fg_color=self.COR_PRIMARIA, hover_color="#990000")
        
        # Preenche os campos do formulário na aba "Dados Cadastrais"
        self.entry_nome.delete(0, 'end')
        self.entry_nome.insert(0, nome if nome else "")
        
        self.entry_cpf.delete(0, 'end')
        self.entry_cpf.insert(0, cpf if cpf else "")
        
        self.entry_data.delete(0, 'end')
        self.entry_data.insert(0, data_nasc if data_nasc else "")
        
        self.label_idade.configure(text=f"Idade: {idade} anos")
        
        self.entry_tel.delete(0, 'end')
        self.entry_tel.insert(0, telefone if telefone else "")
        
        self.entry_end.delete(0, 'end')
        self.entry_end.insert(0, endereco if endereco else "")
        
        self.combo_faixa.set(faixa.capitalize() if faixa else "Branca")
        
        # LGPD Checkbox state
        self.check_lgpd.deselect()
        if lgpd in ["Sim", "ON", "on", "On", "Yes"]:
            self.check_lgpd.select()
            
        # Limpa e preenche responsável se for menor de idade
        self.entry_resp_nome.delete(0, 'end')
        self.entry_resp_cpf.delete(0, 'end')
        self.entry_resp_tel.delete(0, 'end')
        
        if idade < 18:
            self.entry_resp_nome.insert(0, resp_nome if resp_nome else "")
            self.entry_resp_cpf.insert(0, resp_cpf if resp_cpf else "")
            self.entry_resp_tel.insert(0, resp_tel if resp_tel else "")
            self.frame_responsavel.pack(fill="x", pady=10, padx=10, before=self.check_lgpd)
        else:
            self.frame_responsavel.pack_forget()

    def salvar_aluno(self):
        nome = self.entry_nome.get().strip()
        cpf = self.entry_cpf.get().strip()
        data_nasc = self.entry_data.get().strip()
        telefone = self.entry_tel.get().strip()
        endereco = self.entry_end.get().strip()
        faixa = self.combo_faixa.get()
        lgpd = "Sim" if self.check_lgpd.get() == 1 else "Não"
        
        if not nome or len(cpf) != 14 or len(data_nasc) != 10:
            self.label_status.configure(text="❌ Preencha Nome, CPF e Data corretamente.", text_color="red")
            return
            
        if lgpd == "Não":
            self.label_status.configure(text="❌ O aluno precisa concordar com os termos.", text_color="red")
            return

        resp_nome = self.entry_resp_nome.get().strip() if self.idade_calculada < 18 else ""
        resp_cpf = self.entry_resp_cpf.get().strip() if self.idade_calculada < 18 else ""
        resp_tel = self.entry_resp_tel.get().strip() if self.idade_calculada < 18 else ""
        
        if self.idade_calculada < 18 and not resp_nome:
            self.label_status.configure(text="❌ Preencha os dados do Responsável!", text_color="red")
            return

        dados = (nome, cpf, data_nasc, self.idade_calculada, telefone, endereco, faixa, lgpd, resp_nome, resp_cpf, resp_tel)
        
        if self.id_em_edicao is not None:
            sucesso, msg = banco.atualizar_aluno(self.id_em_edicao, dados)
        else:
            sucesso, msg = banco.salvar_aluno(dados)
        
        self.label_status.configure(text=msg, text_color="#4CAF50" if sucesso else "red")
        
        if sucesso:
            # Em vez de apenas limpar os campos, volta para a lista após 1.5 segundos
            self.frame_formulario.after(1500, self.voltar_para_pesquisa)

    # Funções de formatação mantidas (NÃO ALTERADAS)
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
                self.idade_calculada = hoje.year - nascimento.year - ((hoje.month, hoje.day) < (nascimento.month, nascimento.day))
                self.label_idade.configure(text=f"Idade: {self.idade_calculada} anos")
                if self.idade_calculada < 18:
                    self.frame_responsavel.pack(fill="x", pady=10, padx=10, before=self.check_lgpd)
                else:
                    self.frame_responsavel.pack_forget()
            except ValueError:
                self.label_idade.configure(text="❌ Data inválida")