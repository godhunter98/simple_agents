# 1. Base image
FROM python:3.12-slim

# 2. Set working directory inside container
WORKDIR /app

# 3. Install uv
RUN pip install --no-cache-dir uv 

# 4. Copy only dependency files first (for better caching)
COPY pyproject.toml uv.lock ./

# 5. Install dependencies in system python and Forcing UV to install dependencies in system python
# This was an important line, and took me some time to figure out, we need to set the UV_PROJECT_ENVIRONMENT env variable in every UV project to ensure deps are installed in the system python
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"
RUN uv sync --frozen --no-dev

# 6. Copy the rest of the project
COPY . .

# 7. Default command: run your agent
ENTRYPOINT ["python", "main.py"]