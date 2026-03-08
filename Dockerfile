FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
COPY frontend/ ./

RUN npm ci
ARG NEXT_PUBLIC_API_URL=http://localhost:8000
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
RUN npm run build

FROM python:3.14-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/

COPY --from=frontend-builder /app/frontend/.next /app/frontend/.next
COPY --from=frontend-builder /app/frontend/public /app/frontend/public
COPY --from=frontend-builder /app/frontend/package.json /app/frontend/package.json
COPY --from=frontend-builder /app/frontend/next.config.mjs /app/frontend/next.config.mjs

WORKDIR /app/frontend
RUN npm install --production
WORKDIR /app

ENV PYTHONPATH="/app/backend"

EXPOSE 8000 3000

CMD ["sh", "-c", "uvicorn backend.main:app --host 0.0.0.0 --port 8000 & cd /app/frontend && node_modules/.bin/next start -p 3000"]