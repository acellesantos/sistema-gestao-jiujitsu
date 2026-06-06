import customtkinter as ctk
import banco

class TelaAuditoria(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        
        # Cabeçalho Escuro
        cabecalho = ctk.CTkFrame(self, fg_color="#2B2B2B")
        cabecalho.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkLabel(cabecalho, text="🛡️ Trilha de Auditoria do Sistema", font=ctk.CTkFont(size=20, weight="bold")).pack(side="left", padx=20, pady=15)
        ctk.CTkButton(cabecalho, text="🔄 Atualizar", fg_color="#444444", hover_color="#CC0000", command=self.carregar_logs).pack(side="right", padx=20)
        
        # Títulos das colunas (O grid falso)
        titulos = ctk.CTkFrame(self, fg_color="#1E1E1E", corner_radius=0)
        titulos.pack(fill="x", padx=20)
        ctk.CTkLabel(titulos, text="Data / Hora", width=200, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(titulos, text="Responsável", width=150, anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10)
        ctk.CTkLabel(titulos, text="Ação Realizada", anchor="w", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10, pady=10, fill="x", expand=True)
        
        # Área de rolagem para os logs
        self.scroll_logs = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_logs.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        self.carregar_logs()

    def carregar_logs(self):
        # Limpa a tela
        for widget in self.scroll_logs.winfo_children():
            widget.destroy()
            
        registros = banco.listar_auditoria()
        
        if not registros:
            ctk.CTkLabel(self.scroll_logs, text="Nenhum log de auditoria registrado ainda.", text_color="gray").pack(pady=50)
            return
            
        # Povoa a grade com os dados do banco
        for data_hora, admin, acao in registros:
            linha = ctk.CTkFrame(self.scroll_logs, fg_color="#333333", corner_radius=0)
            linha.pack(fill="x", pady=2)
            ctk.CTkLabel(linha, text=data_hora, width=200, anchor="w").pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(linha, text=admin, width=150, anchor="w").pack(side="left", padx=10, pady=5)
            ctk.CTkLabel(linha, text=acao, anchor="w").pack(side="left", padx=10, pady=5, fill="x", expand=True)