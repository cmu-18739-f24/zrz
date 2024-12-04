import sys
import random

# Set a large prime number and a generator
p = 2**255 - 19  # A large prime number (Curve25519 prime)
g = 2  # Generator

# The secret flag (this would be known only to the prover)
secret_flag = "CTF{ZKP_M4st3r}"

class ZKPChallenge:
    """A class to implement the Zero-Knowledge Proof challenge."""

    def __init__(self, secret):
        """
        Initialize the ZKP challenge with a secret.

        Args:
            secret (str): The secret flag.
        """
        self.secret = int.from_bytes(secret.encode(), 'big')
        self.y = pow(g, self.secret, p)  # Public key

    def verify_commitment(self, commitment, r):
        """
        Verify the commitment.

        Args:
            commitment (int): The commitment value.
            r (int): The random value used in the commitment.

        Returns:
            bool: True if the commitment is valid, False otherwise.
        """
        return commitment == pow(g, r, p)

    def challenge(self):
        """
        Generate a random challenge.

        Returns:
            int: A random bit (0 or 1).
        """
        return random.randint(0, 1)

    def verify(self, c, t, commitment, response):
        """
        Verify the response to the challenge.

        Args:
            c (int): The challenge bit.
            t (int): A random value chosen by the verifier.
            commitment (int): The initial commitment.
            response (int): The prover's response.

        Returns:
            bool: True if the verification succeeds, False otherwise.
        """
        if c == 0:
            return commitment == pow(g, response, p)
        else:
            return commitment == (pow(g, response, p) * pow(self.y, t, p)) % p

def win():
    """Read the flag from a file and print it in hexadecimal format."""
    flag = open('flag.txt', 'r').read().strip()
    str_flag = ''
    for c in flag:
        str_flag += str(hex(ord(c))) + ' '
    print(str_flag)
    sys.stdout.flush()

def main():
    """Run the Zero-Knowledge Proof challenge."""
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