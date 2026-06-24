# Donna Frontend

Donna's frontend is a Vite + React + TypeScript application for the Denali Craft Operations Platform.

## Commands

- `npm run dev` - start the Vite development server.
- `npm run typecheck` - run TypeScript checks.
- `npm run build` - typecheck and build the production frontend.

## Environment

Frontend environment values are public because they are bundled into browser code. Only safe `VITE_*` values belong in frontend environment files.

## Local API Proxy

During Vite development, `/api/health` proxies to the FastAPI `/health` endpoint at `http://127.0.0.1:8000`.
