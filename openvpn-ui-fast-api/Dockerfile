FROM python:3.11

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    openvpn \
    easy-rsa \
    iptables && \
    rm -rf /var/lib/apt/lists/* && \
    ln -s /usr/share/easy-rsa/easyrsa /usr/local/bin

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
