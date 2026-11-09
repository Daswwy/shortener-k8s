FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
RUN useradd -r -m appuser
USER appuser
EXPOSE 8000
cmd ["gunicorn", "-w", "1", "-b", "0.0.0.0:8000", "app:app"]
