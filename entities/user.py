import app

db = app.db

from repo import GitoliteAdminRepo

from Crypto.PublicKey import RSA
import base64

def keytopub(key):
    # Create public key.
    ssh_rsa = b'00000007' + base64.b16encode(b'ssh-rsa')

    # Exponent.
    exponent = '%x' % (key.e, )
    if len(exponent) % 2:
        exponent = '0' + exponent

    ssh_rsa += ('%08x' % (len(exponent) / 2, )).encode('utf-8')
    ssh_rsa += exponent.encode('utf-8')

    modulus = '%x' % (key.n, )
    if len(modulus) % 2:
        modulus = '0' + modulus

    if modulus[0] in '89abcdef':
        modulus = '00' + modulus

    ssh_rsa += ('%08x' % (len(modulus) / 2, )).encode('utf-8')
    ssh_rsa += modulus.encode('utf-8')

    return 'ssh-rsa %s' % (
        base64.b64encode(base64.b16decode(ssh_rsa.upper())), )

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    key = db.Column(db.String(1000), unique=True)

    def __init__(self, username):
        self.username = username
        self.key = ''

    def generateKey(self):
        key = RSA.generate(2048)
        pubkey = key.publickey()
        self.key = keytopub(pubkey)

        return key.exportKey('PEM')

    def create(self):
        GitoliteAdminRepo.addUser(self.username, self.key)

    def __repr__(self):
        return '<User %r>' % self.username
