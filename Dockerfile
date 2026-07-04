FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock README.md ./
RUN pip install uv && uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "main.py"]
