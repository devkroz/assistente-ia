# Assistente IA

Chatbot inteligente com processamento de linguagem natural (NLP), integração com APIs externas e suporte a múltiplos canais: **Web**, **WhatsApp** e **Discord**.

## Arquitetura

```
                    ┌──────────────────┐
                    │   WebSocket      │
                    │   (Web Chat)     │
                    └────────┬─────────┘
                             │
┌──────────┐    ┌───────────▼──────────┐    ┌──────────┐
│ Discord  │◄───┤    FastAPI Server    ├───►│ WhatsApp │
│   Bot    │    │  (Python + OpenAI)   │    │  Webhook │
└──────────┘    └───────────┬──────────┘    └──────────┘
                             │
                    ┌────────▼─────────┐
                    │   OpenAI GPT     │
                    │  (NLP + NLU)     │
                    └──────────────────┘
```

## Funcionalidades

- **Web Chat** — Interface moderna via WebSocket (tempo real)
- **Discord Bot** — Comando `!ask` para conversar no Discord
- **WhatsApp Bot** — Webhook Twilio para responder no WhatsApp
- **API REST** — Endpoint `/api/ask` para integração com outros sistemas
- **História de conversa** — Mantém contexto por usuário (últimas 20 mensagens)

## Tecnologias

| Camada      | Tecnologia                          |
|-------------|-------------------------------------|
| Backend     | Python + FastAPI                    |
| NLP         | OpenAI API (GPT-4o / GPT-4o-mini)  |
| Tempo real  | WebSocket                           |
| Discord     | discord.py                          |
| WhatsApp    | Twilio API                          |
| Deploy      | Docker / Netlify / Railway          |

## Como usar

### 1. Clone e instale

```bash
git clone https://github.com/devkroz/assistente-ia.git
cd assistente-ia
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edite .env com suas chaves
```

### 3. Execute

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Acesse `http://localhost:8000` para o chat web.

### Discord

```bash
!ask Qual é a capital do Brasil?
```

### API REST

```bash
curl -X POST "http://localhost:8000/api/ask?message=Olá&user_id=teste"
```

## Deploy

### Docker

```bash
docker build -t assistente-ia .
docker run -p 8000:8000 --env-file .env assistente-ia
```

### Netlify (frontend estático)

O frontend web pode ser extraído como static site e deployado separadamente no Netlify.

---

Desenvolvido por [devkroz](https://github.com/devkroz)
