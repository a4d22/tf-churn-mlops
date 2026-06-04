# 1. Use an official lightweight Python runtime as a parent image
FROM python:3.10-slim

# 2. Set environment variables to keep Python clean inside containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install basic system utilities needed for development (git, curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 4. Set the working directory inside the container
WORKDIR /workspace

# 5. Copy requirements and install them using standard pip
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of the workspace files
COPY pyproject.toml .
COPY src/ ./src/

# 7. Install our local package in editable mode so changes refresh instantly
RUN pip install -e .

# 8. Expose port 8000 for our FastAPI server
EXPOSE 8000

# 9. Default command (can be overridden by our devcontainer or orchestrator)
CMD ["uvicorn", "src.serving_app:app", "--host", "0.0.0.0", "--port", "8000"]