# 🥋 Sistema de Gestão para Academias de Jiu-Jitsu

Este é um sistema de automação e gestão desenvolvido em Python para otimizar os processos diários de uma academia de Jiu-Jitsu. O projeto foi estruturado pensando nas dores reais de um gestor, focando no controle de alunos, fluxo de caixa e redução da inadimplência através de notificações automatizadas.

---

## 💡 O Grande Diferencial: Níveis de Acesso por Cores de Faixa

Para tornar o sistema totalmente integrado à cultura do esporte, o controle de permissões de usuários (Roles) foi desenhado respeitando a hierarquia das faixas de Jiu-Jitsu:

* ⚪ **Faixa Branca (Aluno):** Acesso básico. Consegue apenas visualizar a grade de horários e o calendário de competições/eventos.
* 🔵 **Faixa Azul / Roxa (Instrutor ou Secretaria):** Consegue realizar o cadastro de novos alunos e verificar as vagas disponíveis por turma.
* 🟤 **Faixa Marrom (Financeiro):** Tem acesso ao fluxo de caixa, pagamentos de fornecedores e controle de mensalidades pendentes.
* ⚫ **Faixa Preta (Administrador / Dono):** Acesso total ao sistema, relatórios gerenciais e alteração de permissões.

---

## 🚀 Funcionalidades Mapeadas no Escopo

* [x] **Módulo de Autenticação por Nível:** Menu dinâmico que se adapta conforme a faixa do usuário logado.
* [x] **Cadastro de Alunos:** Módulo isolado para inserção de novos praticantes no banco de dados local.
* [x] **Filtro de Inadimplência:** Varredura automática no banco de dados para isolar alunos com mensalidades pendentes.
* [x] **Simulador de Disparador do WhatsApp:** Geração de mensagens personalizadas prontas para envio, otimizando o tempo de cobrança.
* `[Em desenvolvimento]` Interface Gráfica de alta performance (Desktop).
* `[Em desenvolvimento]` Conexão direta com a API/Automação do WhatsApp para disparos reais em lote.
* `[Em desenvolvimento]` Gestão de eventos, exames de troca de faixa e pagamentos de fornecedores.

---

## 📂 Estrutura Arquitetural do Projeto

O código foi desenvolvido seguindo boas práticas de modularização, separando as responsabilidades de cada arquivo para facilitar futuras manutenções e escalabilidade:

* `main.py`: O coração do sistema, responsável pelo loop de navegação e validação de permissões.
* `alunos.py`: Módulo responsável pelas regras de negócio ligadas ao aluno (cadastro e listagem).
* `financeiro.py`: Módulo focado no cruzamento de dados de pagamento e motor das mensagens de cobrança.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3** (Linguagem base de desenvolvimento)
* **Git & GitHub** (Controle de versionamento e hospedagem segura do código)

---

_Desenvolvido com ☕ e 🐍 por Marcelle Santos._