import socket
import random
import sys
import argparse
import time

# The secret flag (this would be known only to the prover)
secret_flag = "CTF{ZKP_M4st3r}"

class ZKPClient:
    """A client for the Zero-Knowledge Proof protocol."""

    def __init__(self, secret):
        """
        Initialize the ZKP client with a secret.

        Args:
            secret (str): The secret flag.
        """
        self.secret = int.from_bytes(secret.encode(), 'big')

    def commit(self, g, p):
        """
        Generate a commitment for the ZKP protocol.

        Args:
            g (int): The generator.
            p (int): The prime modulus.

        Returns:
            tuple: A tuple containing the commitment and the random value r.
        """
        self.r = random.randint(1, p-1)
        return pow(g, self.r, p), self.r

    def respond(self, c, t, p):
        """
        Generate a response for the ZKP protocol.

        Args:
            c (int): The challenge bit.
            t (int): The random value chosen by the verifier.
            p (int): The prime modulus.

        Returns:
            int: The response to the challenge.
        """
        if c == 0:
            return self.r
        else:
            return (self.r - self.secret * t) % (p-1)

def main(host, port):
    """
    Main function to run the ZKP client.

    Args:
        host (str): The server's hostname or IP address.
        port (int): The port number on which the server is listening.
    """
    client = ZKPClient(secret_flag)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"Connected to {host}:{port}")

        try:
            # Receive welcome message and p, g values
            print(s.recv(1024).decode().strip())  # welcome 
            p = int(s.recv(1024).decode().strip().split('=')[1])  # p 
            g = int(s.recv(1024).decode().strip().split('=')[1])  # g 
            print(f'p: {p}, g: {g}')
            
            while True:
                round_msg = s.recv(1024).decode().strip()
                print(round_msg)  # Round 
                if round_msg.startswith("Overall"):
                    break

                commit_msg = s.recv(1024).decode().strip()
                print(commit_msg)  # Commit
                
                commitment, r = client.commit(g, p)
                print(f"Sending commitment: {commitment}, r: {r}")
                s.sendall(f"{commitment},{r}".encode())

                challenge_msg = s.recv(1024).decode().strip()
                challenge = int(challenge_msg.split(':')[1])
                print(f"Received {challenge_msg}")

                t_msg = s.recv(1024).decode().strip()
                t = int(t_msg.split(':')[1])
                print(f"Received {t_msg}")

                response_prompt = s.recv(1024).decode().strip()
                print(response_prompt)
                response = client.respond(challenge, t, p)
                print(f"Sending response: {response}")
                s.sendall(str(response).encode())

                result = s.recv(1024).decode().strip()
                print(f"Verification result: {result}")

        except (ValueError, IndexError) as e:
            print(f"Error processing server message: {e}")
        except TimeoutError as e:
            print(f"Communication error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ZKP Client")
    parser.add_argument("host", help="Server host")
    parser.add_argument("port", type=int, help="Server port")
    args = parser.parse_args()

    main(args.host, args.port)