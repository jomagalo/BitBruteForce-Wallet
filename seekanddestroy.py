#!/usr/bin/python

'''
Change Cores=# of how many cores do you want to use (Script tested on i7-4500U 8 Cores - 5 K/s per Core. 3,456,000 Private Keys generated per day)

Take into account VM as well (i3 with 2 cores but 4VM -> 8 threads). More cores is just more demanding for OS scheduler
(worth playing around, even above number of CPU cores)
'''

import time
import datetime as dt
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
import pickle
import multiprocessing
from multiprocessing import Pool
import binascii, hashlib, base58, ecdsa
import pandas as pd

DATABASE = r'database/MAR_15_2021/'

def ripemd160(x):
    d = hashlib.new('ripemd160')
    d.update(x)
    return d


r = 0
cores=4


def seek(r, database):
	global num_threads
	LOG_EVERY_N = 1000
	start_time = dt.datetime.today().timestamp()
	i = 0
	print("Core " + str(r) +":  Searching Private Key..")

	while True:
		i=i+1
		# generate private key , uncompressed WIF starts with "5"
		priv_key = os.urandom(32)
		fullkey = '80' + binascii.hexlify(priv_key).decode()
		sha256a = hashlib.sha256(binascii.unhexlify(fullkey)).hexdigest()
		sha256b = hashlib.sha256(binascii.unhexlify(sha256a)).hexdigest()
		WIF = base58.b58encode(binascii.unhexlify(fullkey+sha256b[:8]))

		# get public key , uncompressed address starts with "1"
		sk = ecdsa.SigningKey.from_string(priv_key, curve=ecdsa.SECP256k1)
		vk = sk.get_verifying_key()
		publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
		hash160 = ripemd160(hashlib.sha256(binascii.unhexlify(publ_key)).digest()).digest()
		publ_addr_a = b"\x00" + hash160
		checksum = hashlib.sha256(hashlib.sha256(publ_addr_a).digest()).digest()[:4]
		publ_addr_b = base58.b58encode(publ_addr_a + checksum)
		priv = WIF.decode()
		pub = publ_addr_b.decode()
		time_diff = dt.datetime.today().timestamp() - start_time
		if (i % LOG_EVERY_N) == 0:
			print('Core :'+str(r)+" K/s = "+ str(i / time_diff))

		# TEST
		#if i == 5000 and r == 1: # solo deja pasar al core 1
		#	priv = '4kljlkjljljlkjklkl'
		#	pub = '1L1aAhBakQGrhzdJG4iJMp77c7TqVk5bWj'

		#print ('Worker '+str(r)+':'+ str(i) + '.-  # '+pub + ' # -------- # '+ priv+' # ')

		if pub in database[0] or \
       		   pub in database[1] or \
       		   pub in database[2] or \
       		   pub in database[3]:
		   msgwallet = "\nPublic: " + str(pub) + " ---- Private: " + str(priv) + "YEI"
		   text = msgwallet

		   # create message object instance
		   msg = MIMEMultipart()
		   message = "Hola, este es un mensaje automatico de tu raspi. Ve corriendo a tu raspi y revisa la wallet que has encontrado."

		   password = "youpassword"
		   msg['From'] = "you@email.com"
		   msg['To'] = "you@email.com"
		   msg['Subject'] = "Premio! Has encontrado una wallet"

		   # add in the message body
		   msg.attach(MIMEText(message, 'plain'))

		   #create server
		   server = smtplib.SMTP('you.emailserver.com: 587')

		   server.starttls()

		   # Login Credentials for sending the mail
		   server.login(msg['From'], password)

		   # send the message via the server
		   server.sendmail(msg['From'], msg['To'], msg.as_string())

		   print(text)
		   with open('Wallets.txt','a') as f:
		      f.write(priv)
		      f.write('     ')
		      f.write(pub)
		      f.write('\n')
		      f.close()
		      time.sleep(30)
		      print ('WINNER WINNER CHICKEN DINNER!!! ---- ' +dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), pub, priv)
		      break
					



contador=0
if __name__ == '__main__':
	database = [set() for _ in range(4)]
	count = len(os.listdir(DATABASE))
	half = count // 2
	quarter = half // 2
	for c, p in enumerate(os.listdir(DATABASE)):
	   print('\rreading database: ' + str(c + 1) + '/' + str(count), end=' ')
	   with open(DATABASE + p, 'rb') as file:
               if c < half:
                  if c < quarter:
                     database[0] = database[0] | set(pickle.load(file))
                  else:
                     database[1] = database[1] | set(pickle.load(file))
               else:
                  if c < half + quarter:
                     database[2] = database[2] | set(pickle.load(file))
                  else:
                     database[3] = database[3] | set(pickle.load(file))
	print('DONE')

	jobs = []
	#df_handler = pd.read_csv(open('bit.txt', 'r'))
	for r in range(cores):
		p = multiprocessing.Process(target=seek, args=(r,database,))
		jobs.append(p)
		p.start()

