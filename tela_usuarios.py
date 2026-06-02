import customtkinter as ctk
import banco

class TelaUsuarios(ctk.CTkFrame):
    def __init__(self, master, usuario_logado, faixa_logada): 
        super().__init__(master, fg_color="transparent")

        self.id_em_edicao = None
        
        # 👇 Guardamos esses valores para usar depois na verificação de permissão
        self.usuario_logado = usuario_logado
        self.faixa_logada = faixa_logada
        
        # Cores (importadas do sistema principal, ou pode definir aqui de novo)
        COR_PRIMARIA = "#CC0000"
        COR_FUNDO = "#1A1A1A"
        
        # --- DIVISÃO DA TELA ---
        frame_esquerda = ctk.CTkFrame(self, width=350, fg_color=COR_FUNDO, border_color=COR_PRIMARIA, border_width=1)
        frame_esquerda.pack(side="left", fill="y", padx=20, pady=10)
        
        frame_direita = ctk.CTkFrame(self, fg_color=COR_FUNDO, border_color=COR_PRIMARIA, border_width=1)
        frame_direita.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        # --- LADO ESQUERDO ---
        ctk.CTkLabel(frame_esquerda, text="👥 Equipe Cadastrada", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        self.lista_scroll = ctk.CTkScrollableFrame(frame_esquerda, width=300)
        self.lista_scroll.pack(fill="both", expand=True)

        # --- LADO DIREITO ---
        ctk.CTkLabel(frame_direita, text="📝 Novo Usuário", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=10)
        
        self.entry_user = ctk.CTkEntry(frame_direita, placeholder_text="Username", width=350)
        self.entry_user.pack(pady=10)
        self.entry_senha = ctk.CTkEntry(frame_direita, placeholder_text="Senha", width=350, show="*")
        self.entry_senha.pack(pady=10)
        
        self.combo_faixa = ctk.CTkOptionMenu(frame_direita, values=["Branca", "Azul", "Roxa", "Marrom", "Preta"], width=350, fg_color=COR_FUNDO, button_color=COR_PRIMARIA)
        self.combo_faixa.pack(pady=5)
        
        self.label_status = ctk.CTkLabel(frame_direita, text="")
        self.label_status.pack(pady=10)

        # No __init__, procure o botão de salvar e mude o command:
ctk.CTkButton(frame_direita, text="Cadastrar Usuário", command=self.salvar_ou_atualizar, width=350, fg_color="#CC0000").pack(pady=20)
        
        self.recarregar_lista()

    def recarregar_lista(self):
        for widget in self.lista_scroll.winfo_children(): widget.destroy()
        for u in banco.listar_usuarios():
            id_user, nome, faixa = u
            linha = ctk.CTkFrame(self.lista_scroll, fg_color="#2B2B2B", border_color="#CC0000", border_width=1)
            linha.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(linha, text=f"👤 {nome} ({faixa.title()})", text_color="white").pack(side="left", padx=10, pady=10)
            if self.faixa_logada == "preta" and nome != self.usuario_logado:
                ctk.CTkButton(linha, text="X", width=40, fg_color="#CC0000", 
                              command=lambda i=id_user: self.deletar(i)).pack(side="right", padx=5)
                ctk.CTkButton(linha, text="✎", width=40, fg_color="#444444", 
                              command=lambda i=id_user, n=nome, f=faixa: self.carregar_edicao(i, n, f)).pack(side="right", padx=5)
                
    def deletar(self, id_user):
        banco.deletar_usuario(id_user)
        self.recarregar_lista()

    def carregar_edicao(self, id_user, username, faixa):
        self.id_em_edicao = id_user
        self.entry_user.delete(0, 'end')
        self.entry_user.insert(0, username)
        self.combo_faixa.set(faixa.capitalize())
        
        # Muda o botão de "Cadastrar" para "Salvar"
        self.btn_salvar.configure(text="💾 Salvar Alterações", fg_color="#CC0000")
        self.btn_cancelar.pack(pady=5)

    def cancelar_edicao(self):
        self.id_em_edicao = None
        self.entry_user.delete(0, 'end')
        self.entry_senha.delete(0, 'end')
        self.btn_salvar.configure(text="Cadastrar Usuário", fg_color="#CC0000")
        self.btn_cancelar.pack_forget()

    def salvar_ou_atualizar(self):
        user = self.entry_user.get()
        senha = self.entry_senha.get()
        faixa = self.combo_faixa.get()
        
        if self.id_em_edicao:
            # Edição
            banco.atualizar_usuario(self.id_em_edicao, user, senha, faixa)
        else:
            # Novo
            banco.cadastrar_usuario(user, senha, faixa)
            
        self.cancelar_edicao()
        self.recarregar_lista()

    def salvar(self):
        sucesso, msg = banco.cadastrar_usuario(self.entry_user.get(), self.entry_senha.get(), self.combo_faixa.get())
        self.label_status.configure(text=msg)
        if sucesso: self.recarregar_lista()