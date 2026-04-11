# crypto{w1R3d_equ1v4l3nt_pr1v4cy?!}

import requests

def server(ciphertext_hex, nonce_hex):
    url = f"https://aes.cryptohack.org/oh_snap/send_cmd/{ciphertext_hex}/{nonce_hex}/"
    return requests.get(url).json()

