# Vercel ASGI entrypoint
# Vercel will load the ASGI callable named `app` from this file.

from asgi import app  # exposes `app` as the ASGI callable

# Nothing else required here; Vercel's Python runtime will use `app`
