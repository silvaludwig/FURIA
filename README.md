# Bot Furioso 📄

Um bot de Telegram dedicado à equipe FURIA de CS:GO, permitindo consultar próximos jogos, resultados recentes, elenco atual e últimas notícias, tudo em tempo real!

---

## ✨ Funcionalidades

| Comando/Opção          | Ação                                                                     |
| ---------------------- | ------------------------------------------------------------------------ |
| `/start`               | Exibe o menu principal e orienta o usuário sobre o que pode perguntar.   |
| Botão `Próximos Jogos` | Busca e exibe o próximo jogo da FURIA no site da HLTV.                   |
| Botão `Últimos Jogos`  | Lista os 3 últimos jogos da FURIA com datas, times e placares.           |
| Botão `Elenco`         | Mostra coach e jogadores atuais da equipe.                               |
| Botão `Notícias`       | Exibe os 3 últimos destaques noticiosos sobre a FURIA.                   |
| Mensagens de Texto     | Analisa automaticamente mensagens e responde com informações relevantes. |

---

## ⚙️ Requisitos

- Python 3.10+
- Google Chrome instalado

### Dependências

```bash
pip install python-telegram-bot selenium webdriver-manager
```

### Configuração do Token

Crie um arquivo `config.txt` com o seguinte conteúdo:

```
TOKEN=seu_token_do_bot
```

Alternativamente, defina a variável de ambiente `TELEGRAM_TOKEN`.

---

## 🚀 Como Executar

1. Clone o repositório.
2. Instale as dependências.
3. Configure o token.
4. Execute o script:

```bash
python main.py
```

Se tudo estiver correto, você verá no terminal:

```
Bot FURIOSO rodando...
```

---

## 📁 Estrutura do Projeto

- `config.txt` : Armazena o token do Telegram.
- `main.py` : Código principal do bot.

### Principais Funções:

- **Configuração**: `carregar_config()`
- **Menu**: `menu_principal()`
- **Mensagens**: `start()`, `button_click()`, `handle_message()`
- **Funcionalidades**: `proximos_jogos()`, `ultimos_jogos()`, `elenco()`, `noticias()`

---

## ⚡ Melhorias Futuras

- Cache de dados para reduzir acessos repetitivos.
- Melhor tratamento de exceções e mudanças na estrutura dos sites.
- Log detalhado de atividades.

---

## 💬 Contato

Ficou com dúvidas ou tem sugestões? Me chama!
silvaludwigg@gmail.com

---

> Feito com ❤️ para todos os furiosos! 💥
