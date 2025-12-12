import os

class SSHHandler:

    def get_ssh_socket(self):
        sock = os.environ.get("SSH_AUTH_SOCK")
        if sock and os.path.exists(sock):
            return sock
        return None
