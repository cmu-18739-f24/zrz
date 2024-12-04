# ECDSA FORGERY

- Namespace: picoctf/18739f24
- ID: ECDSA
- Type: custom
- Category: Cryptography
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

There is a service accepting input using elliptic curve based digital signature. If you can sing a specif message with a valid signature the prize is yours ! 

* This is based off of an actual security vulnerability SONYECDSA vulnerability in 2013

* {{url_for("picker-I.py", "Code here")}}

## Details



1. Connect to the server at `$ nc {{server}} {{port}}`
2. Play the game and generate a valid ECDSA signature 
3. Submit the signature to  `$ nc {{server}} {{port}}`
4. If the signature is valid, you win a flag!




## Hints


* The Nonce is fixed!
* It uses a weak curve (NIST192p) for key generation.

* In ECDSA, a signature (r, s) for a message m is generated using the following equation:

s = k^(-1)(z + xr) mod n

Where:
- k is the nonce
- z is the hash of the message
- x is the private key
- n is the order of the curve

* Try looking at the difference in the two signatures and hashes 
* Look at this mathematically before you try to brute force something!


## Solution Overview ()

s =K^-1(z + xr) mod n

where: 
* k is nonce
* z is the hash
* x is the private key 
* n is the order of the curve 

s_1- s_2= k^(-1)(z_1-z_2) mod n 

k = (z1 - z2) * (s1 - s2)^(-1) mod n 



## Challenge Options

```yaml
cpus: 0.5
memory: 128m
pidslimit: 20
ulimits:
  - nofile=128:128
#diskquota: 64m
init: true
```

## Learning Objective

Examining source code to identify functionality

## Tags

- python

## Attributes

- author: Zachary Zdobinski organization: CMU
- event: 18739 CTF
