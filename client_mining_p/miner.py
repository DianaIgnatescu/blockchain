import hashlib
import requests
import sys


def valid_proof(last_proof, proof):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


def proof_of_work(last_proof):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 4 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """
    proof = 0
    while valid_proof(last_proof, proof) is False:
        proof += 1
    return proof


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # TODO: Get the last proof from the server and look for a new one
        res = requests.get(f"{node}/last_proof")
        values = res.json()
        print(values)
        last_proof = values['proof']
        new_proof = proof_of_work(last_proof)

        # TODO: When found, POST it to the server {"proof": new_proof}
        result = requests.post(f"{node}/mine", json={"proof": new_proof})
        proof_result = result.json()

        # TODO: If the server responds with 'New Block Forged'
        if proof_result['message'] == 'New Block Forged':
            # add 1 to the number of coins mined and print it.  Otherwise,
            # print the message from the server.
            coins_mined = coins_mined + 1
            print(f'Coins mined: {coins_mined}')
        else:
            print(proof_result['error'])
