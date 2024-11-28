# Reversing Python Problem Creation Walkthrough


## Overview

This problem uses a container as a service host and presents this service
through a port. The goal is to forge an elliptic curve digital signature. This problem is adapted from the live picoGym problem, [Picker-I](https://play.picoctf.org/practice/challenge/400).

* Please refer to the problem.md file for more notes on the problem itself, or the direct notes left for posterity on the jupyter notebook 

### File Listing

1. [picker-I.py](/example-problems/reversing-python/picker-I.py) this is the
   vulnerable script that is hosting as a digital signature service on this container.

2. [start.sh](/example-problems/reversing-python/start.sh) starts a listener
   that receives connections. This script is ran as the last step in the
   Dockerfile. For this problem, we use socat to connect the output of our
   vulnerable script to a port, allowing users to interact with our script
   through the network.

3. [setup-challenge.py](/example-problems/reversing-python/setup-challenge.py)
   This script generates the flag for the problem and saves it in the important
   file, `/challenge/metadata.json`, which is required for every cmgr problem.

4. [Dockerfile](/example-problems/reversing-python/Dockerfile) this is the main
   setup for our problem. We pull down a pinned Ubuntu image, update it and
   install the required packages. We create the `/challenge` directory with
   specific permissions so only root can access it. `/challenge` is an
   important directory and contains files that cmgr needs to deploy a problem.
   We add `artifacts.tar.gz` to this directory as well, which contains a copy
   of the source for the service being run on the container.

5. [solver.py] solves via the parameters supplied via the challenge: 
* example :python solver.py <curve_name> <order> <message1> <signature1> <message2> <signature2> <challenge_message>
6. [concept.ipynb] This is a notebook containing my notes to keep track of how the original problem was structured based on some notes on ECDSA and forging via a fixed nonce

