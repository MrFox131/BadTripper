from re import X
from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna

from socket import socket
from collections import namedtuple
import whois


HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')


CA = [
    "IdenTrust", "DigiCert", "Sectigo", "GoDaddy", "GlobalSign"
]


def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)   #https://guix.gnu.org/packages/python-idna-2.10/
    sock = socket()

    sock.connect((hostname, port))
    peername = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE
    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()

    return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)

def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None

def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def print_basic_info(hostinfo, domain):
    s = {
            "name" : domain.name,
            "peername" : hostinfo.peername,
            "registrar" : domain.registrar,
            "registrant_country" : domain.registrant_country,
            "commonname" : get_common_name(hostinfo.cert),
            "SAN" : get_alt_names(hostinfo.cert),
            "creation_date" : domain.creation_date,
            "expiration_date" : domain.expiration_date,
            "last_updated" : domain.last_updated,
            "issuer" : get_issuer(hostinfo.cert),
            "verified" : bool(i in get_issuer(hostinfo.cert).split() for i in CA)
    }
    
    return s

def check_it_out(hostname, port): #check одного адреса
    domain = whois.query(hostname)
    hostinfo = get_certificate(hostname, port)
    print_basic_info(hostinfo, domain)

def start(url):
    try:
        
        hostname = 'letoctf.org'
        check_it_out(hostname, 443)

    except SSL.Error:
        domain = whois.query(hostname)

        s = {
            "name" : domain.name,
            "registrar" : domain.registrar,
            "registrant_country" : domain.registrant_country,
            "creation_date" : domain.creation_date,
            "expiration_date" : domain.expiration_date,
            "last_updated" : domain.last_updated,
            "issuer" : False
        }

        return s   

    except Exception as e:
        return False

x = start('google.com')
print(x)