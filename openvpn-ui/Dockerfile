FROM python:3.11.4-slim-buster

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY ./openvpnui/requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "openvpnui/manage.py", "runserver", "0.0.0.0:8000"]