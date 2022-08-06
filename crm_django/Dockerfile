FROM deskent/deskent:python_mailer-slim-3.10

WORKDIR /app

ADD requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    pip install psycopg2 && \
    python3 -m pip install --no-cache-dir -r requirements.txt

ADD . .
