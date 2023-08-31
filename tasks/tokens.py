from django.core.signing import Signer

def generate_token(participant_id):
    signer = Signer()
    return signer.sign(str(participant_id))

def verify_token(token):
    signer = Signer()
    try:
        participant_id = signer.unsign(token)
        return int(participant_id)
    except signer.BadSignature:
        return None
