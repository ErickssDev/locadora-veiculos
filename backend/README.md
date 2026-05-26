# Backend do MVP de Locação de Veículos

Este backend foi desenvolvido para um MVP de uma plataforma de locação de veículos. A aplicação usa FastAPI, SQLAlchemy em modo assíncrono, Alembic para migrações e JWT para autenticação.

## Estrutura do projeto

- `app/` - código fonte principal
- `app/api/v1/` - rotas da API versionadas
- `app/core/` - configuração, segurança e dependências
- `app/db/` - configuração de banco de dados e sessão
- `app/models/` - modelos SQLAlchemy
- `app/schemas/` - schemas Pydantic
- `app/services/` - lógica de negócio
- `app/utils/` - integração com Cloudinary e e-mail
- `alembic/` - migrações de banco de dados
- `tests/` - testes automatizados
- `.env.example` - exemplo de variáveis de ambiente
- `requirements.txt` - dependências Python

## Instruções de instalação

1. Crie e ative um ambiente virtual Python 3.11+
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Copie o arquivo de exemplo:

```bash
copy .env.example .env
```

4. Preencha as variáveis de ambiente em `.env`:

- `DATABASE_URL`
- `SECRET_KEY`
- `CLOUDINARY_CLOUD_NAME`
- `CLOUDINARY_API_KEY`
- `CLOUDINARY_API_SECRET`
- `SMTP_HOST`
- `SMTP_PORT`
- `SMTP_USER`
- `SMTP_PASSWORD`
- `FRONTEND_URL`

## Executando a aplicação

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Endpoints principais

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/refresh`
- `GET /api/v1/users/me`
- `PUT /api/v1/users/me`
- `GET /api/v1/vehicles`
- `POST /api/v1/vehicles`
- `POST /api/v1/reservations`

## Migrações

Para criar uma nova migração:

```bash
alembic revision --autogenerate -m "Descrição"
```

Para aplicar migrações:

```bash
alembic upgrade head
```

## Observações

- O MVP prioriza autenticação, cadastro de usuários, cadastro de veículos, reservas básicas e upload de arquivos via Cloudinary.
- Notificações e envio de e-mail são tratados de forma síncrona no backend.
