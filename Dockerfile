FROM python:3.11.5 AS requirements

WORKDIR /opt

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM requirements

COPY ./server /opt/server

EXPOSE 8080

CMD [ \
  "sh", \
  "-c", \
  "python /opt/server/main.py 0.0.0.0:8080 --no-threading --no-reload -Xfrozen_modules=off" \
]
