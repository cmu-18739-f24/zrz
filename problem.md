# ZKP

- Namespace: picoctf/18739f24
- ID: ZKP  
- Type: custom
- Category: Cryptography
- Points: 1
- Templatable: yes
- MaxUsers: 1

## Description

There is a service accepting input and wants to prove you know the password without transmitting the password. Convince the server you know the secret and win a flag!

* Read up here https://en.wikipedia.org/wiki/Zero-knowledge_proof

The server will give you a secret you need to communicate whether you know without revealing the secret itself.

## Details

Connect to the program with netcat:

The program's source code can be downloaded {{url_for("picker-I.py", "here")}}.

1. Connect to the server at `$ nc {{server}} {{port}}`
2. Play the game and generate valid responses to the Zero Knowledge Proof protocol
3. The secret message to validate is "CTF{ZKP_M4st3r}" (in a typical system this would be communicated as part of the challenge it is your goal to demonstrate how to get the verifier to certify this)




* What are Zero-Knowledge-Proofs (ZKPs) ?
- ZKPs give verifiers (services) the ability to verify whether a secret is correct without ever receiving the secret itself

## Hints

1. Look at the source code for how commitments and challenges are verified.
2. You'll need to implement the prover side of the ZKP protocol.

## Solution Overview

1. Generate valid commitments
2. Respond correctly to challenges
3. Complete multiple rounds successfully

## Challenge Options

```yaml
cpus: 0.5
memory: 128m
pidslimit: 20
ulimits:
  - nofile=128:128
init: true

## Attributes
- author: zrz
