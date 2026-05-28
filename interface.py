import customtkinter as ctk
from datetime import datetime
import banco  # Importa nosso arquivo de banco de dados

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class AppAcademia(ctk.CTk):
    def __init__(self, faixa_usuario_logado="preta"):
        super().__init__()
        banco.criar_tabelas()
        self.faixa_usuario = faixa_usuario_logado.lower()
        self.title("🥋 Sistema Jiu-Jitsu - Gestão & LGPD")
        self.geometry("700x750")
        self.resizable(False, False)

        # Criando abas no sistema (Uma para cadastro, outra para financeiro)
        self.tabview = ctk.CTkTabview(self, width=680, height=720)
        self.tabview.pack(padx=10, pady=10)
        
        self.tab_cadastro = self.tabview.add("🆕 Cadastrar Aluno")
        self.tab_financeiro = self.tabview.add("💰 Gerenciar Pagamentos")

        # Inicializa as duas telas
        self.configurar_aba_cadastro()
        self.configurar_aba_financeiro()

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

if __name__ == "__main__":
    app = AppAcademia(faixa_usuario_logado="preta")
    app.mainloop()