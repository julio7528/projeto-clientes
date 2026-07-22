FROM python:3.14-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 APP_ENV=production
WORKDIR /app
COPY requirements/production.txt requirements/production.txt
RUN pip install --no-cache-dir --requirement requirements/production.txt
COPY backend backend
RUN python backend/manage.py collectstatic --noinput --settings=config.settings
RUN useradd --create-home --uid 10001 appuser
USER appuser
EXPOSE 8000
CMD ["gunicorn", "--chdir", "backend", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
