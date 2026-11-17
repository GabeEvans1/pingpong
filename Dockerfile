FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
ENV DB_PATH=/data/board.db
RUN mkdir /data
EXPOSE 8000
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]