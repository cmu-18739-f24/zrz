import socket
import random
import threading

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

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    zkp = ZKPChallenge(secret_flag)
    rounds = 10
    success = True

    conn.sendall(b"Welcome to the Zero-Knowledge Proof Challenge!\n")
    conn.sendall(f"p = {p}\n".encode())
    conn.sendall(f"g = {g}\n".encode())
    
    for i in range(rounds):
        print(f"\nRound {i+1} with {addr}:")
        conn.sendall(f"\nRound {i+1}:\n".encode())

        # Client commits and sends commitment and r
        conn.sendall(b"Send your commitment and r (comma-separated): ")
        commitment_data = conn.recv(1024).decode().strip().split(',')
        commitment, r = int(commitment_data[0]), int(commitment_data[1])
        print(f"Received commitment: {commitment}, r: {r}")

        # Server verifies commitment
        if not zkp.verify_commitment(commitment, r):
            print("Invalid commitment")
            conn.sendall(b"Invalid commitment\n")
            success = False
            break

        # Server challenges
        c = zkp.challenge()
        print(f"Challenge: {c}")
        conn.sendall(f"Challenge: {c}\n".encode())

        # Server chooses t
        t = random.randint(1, p-1)
        print(f"t: {t}")
        conn.sendall(f"t: {t}\n".encode())

        # Client responds
        conn.sendall(b"Enter your response: ")
        response = int(conn.recv(1024).decode().strip())
        print(f"Received response: {response}")

        # Server verifies
        result = zkp.verify(c, t, commitment, response)
        print(f"Verification: {'Success' if result else 'Failure'}")
        conn.sendall(f"Verification: {'Success' if result else 'Failure'}\n".encode())

        success &= result

    final_result = f"\nOverall result: {'Prover knows the secret' if success else 'Proof failed'}\n"
    print(final_result)
    conn.sendall(final_result.encode())
    conn.close()

def start_server():
    host = 'localhost'
    port = 65438

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"Server listening on {host}:{port}")
        print(f"p = {p}")
        print(f"g = {g}")

        while True:
            conn, addr = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()

if __name__ == "__main__":
    start_server()