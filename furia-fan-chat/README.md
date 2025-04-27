# 🖥️ Projeto: Web Chat Interativo para Fãs da FURIA Esports
### 📋 Descrição
Este projeto é um web chat desenvolvido para fãs do time de CS:GO da FURIA Esports.
Ele permite que usuários interajam com o bot para receber:

- Últimos resultados de jogos

- Próximos confrontos

- Elenco atual do time

- Quiz divertido sobre a FURIA

### 🚀 Funcionalidades
- Mensagem de boas-vindas automática

- Consulta aos 3 últimos jogos

- Informação do próximo jogo

- Lista atualizada do elenco (coach e jogadores)

- Quiz interativo com pontuação

- Fundo personalizado com a logo da FURIA

- Atualização em tempo real via scraping (HLTV.org)

### ⚙️ Tecnologias Utilizadas
- Python 3.11

- Flask - Backend Web

- Selenium WebDriver - Web scraping

- WebDriver Manager - Gerenciador do driver Chrome

- HTML/CSS/JavaScript - Frontend

- HLTV.org - Fonte de dados

# 🛠️ Estrutura do Projeto
```bash
/projeto-furia-chat
│
├── app.py # Servidor Flask com rotas e lógica do quiz
├── functions.py # Funções de scraping (ultimos_jogos, elenco_furia, proximos_jogos)
├── requirements.txt # Dependências do projeto
├── README.md # Documentação do projeto
├── start.sh # Script para Linux/Mac
├── start.bat # Script para Windows
│
├── /templates
│ └── index.html # Página principal do chat
│
└── /static
├── style.css # Estilo da página
└── furia-logo.png # Logo da FURIA usada no background
```

---

# 🔥 Instalação e Execução

1. Clone o repositório
   ```bash
   git clone https://github.com/seuusuario/projeto-furia-chat.git
   cd projeto-furia-chat
   ```
2. Crie um ambiente virtual
   ```bash
   python -m venv venv
   ```
   
   Ative o ambiente:

No Linux/Mac:

```bash
source venv/bin/activate
```

No Windows:

```bash
venv\Scripts\activate 3. Instale as dependências
```

```bash
pip install -r requirements.txt 4. Execute o servidor Flask
```

```bash
flask run
```

Acesse no navegador:

```cpp
http://127.0.0.1:5000
```

Alternativa rápida
Execute diretamente o script de inicialização:

Linux/Mac:

```bash
./start.sh
```

Windows:

```bash
start.bat
```

# 📈 Como Usar
No chat, envie:

- "últimos jogos" → para receber os 3 resultados mais recentes

- "próximo jogo" → para saber o próximo confronto

- "elenco" → para ver coach e jogadores

- "quiz" → para iniciar um quiz de perguntas aleatórias sobre a FURIA

# 🛡️ Observações
- Requisitos: Você precisa ter o navegador Google Chrome instalado no computador.

- Sobre Web Scraping: O sistema depende da estrutura atual do site HLTV.org. Se o site mudar, o scraping pode precisar ser ajustado.

# 📈 Diagrama de Arquitetura Simplificado
```scss
Usuário → Navegador (HTML/JS/CSS)
↓
Flask (app.py)
↓
Funções (functions.py)
↓
Scraping (Selenium)
↓
Retorno → Chat do Usuário
```

# 👨‍💻 Desenvolvedor
Nome: Ludwig

GitHub: github.com/silvaludwig

LinkedIn: linkedin.com/silvaludwig

# 🚀 FURIA HYPE MODE ON!
