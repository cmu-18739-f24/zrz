

import os
import ecdsa


def generate_keypair():
    # Using a weak curve (NIST192p) instead of a stronger one
    return ecdsa.SigningKey.generate(curve=ecdsa.NIST192p)

def sign_message(private_key, message):
    fixed_nonce = b'1234567890' # This is the heart of the vulnerability
    return private_key.sign(message.encode(), k=int.from_bytes(fixed_nonce, 'big'))

def verify_signature(public_key, message, signature):
    try:
        return public_key.verify(signature, message.encode())
    except:
        return False

def win():
  # This line will not work locally unless you create your own 'flag.txt' in
  #   the same directory as this script
  flag = open('flag.txt', 'r').read()
  #flag = flag[:-1]
  flag = flag.strip()
  str_flag = ''
  for c in flag:
    str_flag += str(hex(ord(c))) + ' '
  print(str_flag)
  
import hashlib

if __name__ == "__main__":
    private_key = generate_keypair()
    public_key = private_key.get_verifying_key()
    signed_messages = []

    while True:
        try:
            print(f'The public key is: {public_key.to_string().hex()} order:{public_key.curve.order} curve:{public_key.curve.name}')
            
            if len(signed_messages) < 2:
                print("Input a message to sign:")
                message = input()
                signature = sign_message(private_key, message)
                signed_messages.append((message, signature))
                z = int.from_bytes(hashlib.sha1(message.encode()).digest(), 'big')
                print(f'The Hashed Message:{z}')
                r, s1 = ecdsa.util.sigdecode_string(signature, public_key.curve.order)
                print(f'The signature as integer:{s1} r:{r} ')
            else:
			
                print("Now, prove you've broken the private key by signing this message:")
                challenge_message = os.urandom(16).hex()
                print(challenge_message)
                print("Input your signature (in hex):")
                user_signature = bytes.fromhex(input())
                
                verification_result = verify_signature(public_key, challenge_message, user_signature)
                print(f"Verification result: {verification_result}")
                
                if verification_result:
                    win()
                    break
                else:
                    print("Verification Failed!")
                    
        except Exception as e:
            print(e)
            break

    print("Challenge completed. Exiting...")