# Environment Variables

## Backend (apps/api/)

Copy this to `apps/api/.env` for local development:

```bash
# LLM Provider Configuration
OPENAI_API_KEY=your-openai-api-key-here
LLM_PROVIDER=openai

# Application Configuration
ENVIRONMENT=development
LOG_LEVEL=info
```

## Frontend (apps/web/)

Copy this to `apps/web/.env.local` for local development:

```bash
# API Configuration
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Production (Render.com)

Set these environment variables in the Render dashboard:

### API Service
- `OPENAI_API_KEY` - Your OpenAI API key (keep secret)
- `LLM_PROVIDER` - Set to `openai`
- `ENVIRONMENT` - Set to `production`

### Web Service
- `NEXT_PUBLIC_API_URL` - Set to your API service URL (e.g., `https://unconditional-api.onrender.com/api/v1`)

## Security Notes

- **Never commit `.env` files to version control**
- API keys should only be set in Render dashboard (marked `sync: false` in render.yaml)
- Frontend environment variables prefixed with `NEXT_PUBLIC_` are exposed to the browser
- Backend environment variables are server-side only
