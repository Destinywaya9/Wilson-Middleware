# Tensor P2 is immutable.
#
# Canonical Tensor P2:
# 3,3 / 0,0 / 0,1 / 1,2 / 2,1 / 1,0 / 0,0 / Delay(200)
#
# Operatively, this is the same Tensor P2 expressed through quantum gates as:
# H–CX–CX–CX–CX–H–Delay
#
# These are not different constructions. The gate operation is the operative
# expression of the same immutable Tensor P2.
#
# © 2015–2026 Destiny Machwaya

FROM python:3.12-slim

LABEL org.opencontainers.image.title="Wilson Open Reference Middleware"
LABEL org.opencontainers.image.version="0.1.1rc3"
LABEL org.opencontainers.image.authors="Destiny Machwaya"
LABEL org.opencontainers.image.licenses="LicenseRef-Wilson-Open-Reference-1.0"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY ["wilson_open_middleware-0.1.1rc3-py3-none-any (1).whl", "/tmp/wilson.whl"]

RUN python -m pip install --no-cache-dir "/tmp/wilson.whl[aer]" \
    && rm -f /tmp/wilson.whl \
    && useradd --create-home --uid 10001 wilson

USER 10001

ENTRYPOINT ["wilson-demo"]

