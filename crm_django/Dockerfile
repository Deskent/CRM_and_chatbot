FROM deskent/deskent:python3.10-slim-psycopg2

WORKDIR /app

ADD requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

ADD . .
