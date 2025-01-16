FROM node:20-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
COPY . /app
WORKDIR /app
RUN pnpm install
ENV HOST=0.0.0.0
ENV PORT=4321
EXPOSE 4321 
CMD ["pnpm", "dev", "--host"]