FROM ubi8/python-39


WORKDIR /app

COPY . /app


RUN pip3 install -r requirements.txt


EXPOSE 443


ENTRYPOINT gunicorn -w 4 app:app -b 0.0.0.0:443