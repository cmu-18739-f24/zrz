# Zero Knowledge Proof Problem Creation Walkthrough


## Overview

This problem serves as a game version of Zero Knowledge Proofs. These cryptosystems are built on the discrete log problem. This CTF is used to demonstrate how to Zero knowledge proofs can be used to communicate secrets without transmitting the secret itself. The setup is slightly altered to more of a game format that prompts the player to work with the server to prove that the information the user provides (verifier) is correct without ever giving anything but a public key. 



* Please refer to the problem.md file for more notes on the problem itself, or the direct notes left for posterity on the jupyter notebook 

### File Listing

1. [picker-I.py] this is the
   vulnerable script that is hosting ZKP service on this container.

2. [start.sh] starts a listener
   that receives connections. This script is ran as the last step in the
   Dockerfile. For this problem, we use socat to connect the output of our
   vulnerable script to a port, allowing users to interact with our script
   through the network.

3. [setup-challenge.py] 
   This script generates the flag for the problem and saves it in the important
   file, `/challenge/metadata.json`, which is required for every cmgr problem.

4. [Dockerfile]  this is the main
   setup for our problem. We pull down a pinned Ubuntu image, update it and
   install the required packages. We create the `/challenge` directory with
   specific permissions so only root can access it. `/challenge` is an
   important directory and contains files that cmgr needs to deploy a problem.
   We add `artifacts.tar.gz` to this directory as well, which contains a copy
   of the source for the service being run on the container.

5. [solver.py] solves via the parameters supplied via the challenge: 
* example :python3 solver.py <ip> <port> 


6. [server_local.py] This is a local implementation of the server that allowed for easier debugging than working through CMGR in the debug phase. This was left in hopes that it would ease the porting process as necessary.

6. [concept.ipynb] This is a notebook containing my notes to keep track of how the original problem was structured based on some notes on ECDSA and forging via a fixed nonce


