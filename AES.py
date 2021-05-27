#!/usr/bin/python3
import string
import base64 
from Crypto import Random
from Crypto.Cipher import AES
import hashlib


block_size = 16
pad_len=0
# plain_text=string.ascii_uppercase+string.digits+string.ascii_lowercase

def sha256(key):
	sha = hashlib.sha256()
	sha.update(key.encode('utf-8'))
	return sha.digest()

def pad(plain,block):
	pad_len = len(plain) % block
	return plain+((block-pad_len)*chr(block-pad_len)).encode('ascii')

def unpad(plain,block):
	print(type(plain))
	return plain[0:-(block_size-pad_len)]

def encrypt(plain,key):
	plain = pad(plain,block_size)
	iv = Random.new().read(block_size)
	cipher = AES.new(key,AES.MODE_CBC,iv)
	final_cipher = cipher.encrypt(plain)
	return base64.b64encode(iv+final_cipher)

def decrypt(ciphertext,key):
	ciphertext = base64.b64decode(ciphertext)
	iv = ciphertext[:16]
	cipher = AES.new(key,AES.MODE_CBC,iv)
	plaintext = cipher.decrypt(ciphertext[16:])
	return unpad(plaintext,block_size) 



file = input('Enter the name of the file ')
key = input('Enter a key ')
key = sha256(key)
fp = open(file,'rb')

base64_file = base64.b64encode(fp.read())

enc = encrypt(base64_file,key)
fp1 = open("encryptedfile.png",'wb')
fp1.write(enc)

dec = decrypt(enc,key)
fp2 = open('decryptedfile.png','wb')
fp2.write(base64.b64decode(dec))

fp.close()
fp1.close()
fp2.close()