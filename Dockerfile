FROM python:3.11

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir .

EXPOSE 7680

CMD ["gunicorn", "-b", "0.0.0.0:7680", "--chdir", "/app/src", "run:app"]