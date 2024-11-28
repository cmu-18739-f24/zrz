import sys
import random

# Set a large prime number and a generator
p = 2**255 - 19  # A large prime number (Curve25519 prime)
g = 2  # Generator

# The secret flag (this would be known only to the prover)
secret_flag = "CTF{ZKP_M4st3r}"

class ZKPChallenge:
    def __init__(self, secret):
        self.secret = int.from_bytes(secret.encode(), 'big')
        self.y = pow(g, self.secret, p)  # Public key

    def verify_commitment(self, commitment, r):
        return commitment == pow(g, r, p)

    def challenge(self):
        return random.randint(0, 1)

    def verify(self, c, t, commitment, response):
        if c == 0:
            return commitment == pow(g, response, p)
        else:
            return commitment == (pow(g, response, p) * pow(self.y, t, p)) % p

def win():
    flag = open('flag.txt', 'r').read().strip()
    str_flag = ''
    for c in flag:
        str_flag += str(hex(ord(c))) + ' '
    print(str_flag)
    sys.stdout.flush()

def main():
    zkp = ZKPChallenge(secret_flag)
    rounds = 10
    success = True

    print("Welcome to the Zero-Knowledge Proof Challenge!")
    print(f"p = {p}")
    print(f"g = {g}")
    sys.stdout.flush()

    for i in range(rounds):
        try:
            print(f"\nRound {i+1}:")
            sys.stdout.flush()

            print("Send your commitment and r (comma-separated): ")
            sys.stdout.flush()
            commitment_data = input().strip().split(',')
            commitment, r = int(commitment_data[0]), int(commitment_data[1])

            if not zkp.verify_commitment(commitment, r):
                print("Invalid commitment")
                sys.stdout.flush()
                success = False
                break

            c = zkp.challenge()
            print(f"Challenge: {c}")
            sys.stdout.flush()

            t = random.randint(1, p-1)
            print(f"t: {t}")
            sys.stdout.flush()

            print("Enter your response: ")
            sys.stdout.flush()
            response = int(input().strip())

            result = zkp.verify(c, t, commitment, int(response))
            print(f"Verification: {'Success' if result else 'Failure'}")
            sys.stdout.flush()

            success &= result

        except Exception as e:
            print(f"Error in round {i+1}: {e}")
            sys.stdout.flush()
            success = False
            break

    if success:
        win()
    else:
        print("\nProof failed")
        sys.stdout.flush()

    print("Challenge completed. Exiting...")
    sys.stdout.flush()
    return

if __name__ == "__main__":
    main()