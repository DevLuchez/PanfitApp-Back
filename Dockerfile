FROM python:3.11.5 AS requirements

WORKDIR /opt

COPY requirements.txt .

RUN pip install -r requirements.txt

FROM requirements

COPY ./src /opt/

EXPOSE 5000

CMD [ \
  "sh", \
  "-c", \
  "python /opt/app.py 0.0.0.0:5000 --no-threading --no-reload -Xfrozen_modules=off" \
]
