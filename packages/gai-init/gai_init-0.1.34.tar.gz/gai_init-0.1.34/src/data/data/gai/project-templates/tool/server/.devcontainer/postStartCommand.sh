cd "$PROJECT_DIR"
uv venv
source ${UV_PROJECT_ENVIRONMENT}/bin/activate && \
    uv pip install --upgrade pip==24.2 && \
    uv pip install -e ".[dev]"

