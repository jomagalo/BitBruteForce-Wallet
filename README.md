# BitBruteForce-Wallet
This is an effective script to Brute Force, the Private Key of any Bitcoin Public Address.

How does the script work? 
Very easy.

Every code I´ve seen for the last year just generates randomly private and public addresses and checks the balance (very, very slow for the API Request).

So, i found **123,000 Bitcoin Addresses** with 1+ BTC from 2009 to 2013 and NEVER made a transaction, therefore, lost BTC... it is just like huge pirate boats in the bottom of the ocean filled with treasures.

This Script creates randomly private and public addresses without checking the balance, instead of making API Request, the created Public Address is compared with the list I own.

Long story short. 
Create Random Public Address (**RPA**) and check one by one with the Public Address (**PA**) at the list.

**if RPC == PA then
	YOU WINNED THE LOTTREY!
else
	KEEP SEARCHING MTF!**
	
(Script tested on i7-4500U 8 Cores - 16.32 K/s per Core. 11,280,384 Private Keys generated per day)

i think is quite simple.

If you like it!! **1KyQXpa1Zke5v94QZV2U77i7oaVwPTijdY**

# Database FAQ

This database is a serialized `set()` of all Bitcoin addresses with a positive balance.

The database was created using a third-party program: <a href="https://github.com/graymauser/btcposbal2csv">btcposbal2csv</a> which generates a csv file of all Bitcoin addresses with a positive balance. The csv file was converted into a set and the set was serialized into several `.pickle` files each holding 1,000,000 P2PKH Bitcoin addresses. When the program runs, the files in the database get deserialized and combined to be used for a balance query.

The name of the database folder is the date when the database was last updated in month_day_year format. The database will be updated every 3-6 months.

### How Many Addresses Does The Database Have?

The database currently holds `33,165,253 Bitcoin addresses`. This is the total number of P2PKH Bitcoin addresses with a balance that exist in the blockchain.

This can be verified by removing the hashtag on <a href="https://github.com/Isaacdelly/Plutus/blob/master/plutus.py#L134">Line 134</a> before running the program. This will print the size of the database.

### Why Are There So Many Files?

There are multiple `.pickle` files because GitHub limits file uploads to 50 MB. The single serialized file is too large, so it was split into multiple files each under 50 MB in order to be uploaded to GitHub.


REQUERIMENTS
=

 - Python 3.x (i use 3.6.5)
 - pip install ecdsa
 - pip install base58
 - pip install pandas  (If error "pip uninstall numpy" then "pip install numpy==1.19.3")
 - 3,000,000,000 Years

