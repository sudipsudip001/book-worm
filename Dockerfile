FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

COPY . .

RUN mkdir -p $(pwd)/output

ENTRYPOINT ["uv", "run", "scrapy"]
CMD ["list"]