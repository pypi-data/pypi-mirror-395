from base64 import b32decode, b32encode

from e2ee import E2EE


def test_E2EE(load_certificates):
    SERVER_MESSAGE = "SECRET MESSAGE FROM SERVER!"
    CLIENT_MESSAGE = "SECRET MESSAGE FROM CLIENT!"

    server = E2EE()

    # Public key and salt is transported plain text to the client with signatures
    client = E2EE(server.public_key, server.public_salt)

    # Public key and salt is transported plain text to the client without signatures
    server.load_peer_public_key(client.public_key, client.public_salt)

    secret_message_server = server.encrypt(SERVER_MESSAGE)
    assert SERVER_MESSAGE == client.decrypt(secret_message_server)

    secret_message_client = client.encrypt(CLIENT_MESSAGE)
    assert CLIENT_MESSAGE == server.decrypt(secret_message_client)
