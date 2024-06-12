#!/usr/bin/env bash
set -ex

EASY_RSA_DIR="/etc/openvpn/easyrsa"

SERVER_CERT="$EASY_RSA_DIR/pki/issued/server.crt"

OPENVPN_SRV_NET=${OPENVPN_SERVER_NET:-172.16.100.0}
OPENVPN_SRV_MASK=${OPENVPN_SERVER_MASK:-255.255.255.0}

if [ ${OPENVPN_PASSWORD_AUTH} = "true" ]; then
  echo "Using password authentication"
  CONFIG_FILE="openvpn_pass.conf"
  cp /etc/openvpn/setup/auth.sh /etc/openvpn/auth.sh
  chmod +x /etc/openvpn/auth.sh
else
  CONFIG_FILE="openvpn.conf"
fi

cd $EASY_RSA_DIR

if [ -e "$SERVER_CERT" ]; then
    echo "Using existing certificates"
else
    echo "Generating new certificates"
    easyrsa init-pki
    cp -R /usr/share/easy-rsa/* $EASY_RSA_DIR/pki
    echo "ca" | easyrsa build-ca nopass
    easyrsa build-server-full server nopass
    easyrsa gen-dh
    openvpn --genkey --secret ./pki/ta.key
fi

if [ -e $EASY_RSA_DIR/pki/ta.key ]; then
    echo "Using existing TA key"
else
    openvpn --genkey --secret ./pki/ta.key
fi

easyrsa gen-crl

iptables -t nat -D POSTROUTING -s ${OPENVPN_SRV_NET}/${OPENVPN_SRV_MASK} ! -d ${OPENVPN_SRV_NET}/${OPENVPN_SRV_MASK} -j MASQUERADE || true
iptables -t nat -A POSTROUTING -s ${OPENVPN_SRV_NET}/${OPENVPN_SRV_MASK} ! -d ${OPENVPN_SRV_NET}/${OPENVPN_SRV_MASK} -j MASQUERADE

mkdir -p /dev/net
if [ ! -c /dev/net/tun ]; then
    mknod /dev/net/tun c 10 200
fi

cp -f /etc/openvpn/setup/$CONFIG_FILE /etc/openvpn/$CONFIG_FILE

[ -d $EASY_RSA_DIR/pki ] && chmod 755 $EASY_RSA_DIR/pki
[ -f $EASY_RSA_DIR/pki/crl.pem ] && chmod 644 $EASY_RSA_DIR/pki/crl.pem

mkdir -p /etc/openvpn/ccd

openvpn --config /etc/openvpn/$CONFIG_FILE --client-config-dir /etc/openvpn/ccd --port 1194 --proto tcp --management 0.0.0.0 8989 --dev tun0 --server ${OPENVPN_SRV_NET} ${OPENVPN_SRV_MASK}
