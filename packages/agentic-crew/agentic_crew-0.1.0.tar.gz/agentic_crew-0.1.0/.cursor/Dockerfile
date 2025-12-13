# Pre-built image with Python 3.13 + Node.js 24 + uv
# https://github.com/nikolaik/docker-python-nodejs
FROM nikolaik/python-nodejs:python3.13-nodejs24

WORKDIR /workspace

# =============================================================================
# SYSTEM DEPENDENCIES
# =============================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    git-lfs \
    gh \
    just \
    && rm -rf /var/lib/apt/lists/*

# =============================================================================
# GIT LFS CONFIGURATION
# =============================================================================
RUN git lfs install --system --skip-smudge

# =============================================================================
# NODE.JS PACKAGE MANAGER (pnpm)
# =============================================================================
ENV PNPM_HOME=/root/.local/share/pnpm
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable && \
    corepack prepare pnpm@9.15.0 --activate && \
    pnpm --version

# =============================================================================
# PROCESS COMPOSE (Multi-process orchestration for CrewAI)
# =============================================================================
RUN sh -c "$(curl -fsSL https://raw.githubusercontent.com/F1bonacc1/process-compose/main/scripts/get-pc.sh)" -- -b /usr/local/bin && \
    process-compose version

# =============================================================================
# PLAYWRIGHT (for web scraping tools)
# =============================================================================
RUN pnpm dlx playwright install-deps chromium && \
    pnpm dlx playwright install chromium
