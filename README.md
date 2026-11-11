# AI Image Studio

Text-to-image generation app powered by **FLUX.1-schnell** (12B params) running on **Cloudflare Workers AI** GPUs.

## Architecture

```
Browser UI (Vercel) → /api/generate proxy (Vercel Python function) → Cloudflare Worker (AI binding) → FLUX.1-schnell on Cloudflare GPUs
```

- **Frontend + proxy**: this repo, deployed on Vercel — https://ai-image-studio-murex.vercel.app
- **Inference backend**: [ai-image-worker](https://github.com/Codexhubstudios/ai-image-worker) — Cloudflare Worker with Workers AI binding

## API

```bash
curl -X POST https://ai-image-studio-murex.vercel.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cyberpunk cat", "steps": 4}'
```

Response: `{ "image": "<base64 jpeg>", "mime": "image/jpeg" }`

Direct backend (returns raw JPEG bytes):

```bash
curl -X POST https://ai-image-worker.vultra-server.workers.dev \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a cyberpunk cat", "steps": 4}' --output image.jpg
```
