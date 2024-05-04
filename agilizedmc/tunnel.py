import paramiko
from sshtunnel import open_tunnel, SSHTunnelForwarder
from db import DB

import socket

def check_ssh_tunnel(host='localhost', port=9090):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((host, port))
    if result == 0:
        print("SSH tunnel is up.")
        return True
    else:
        print("SSH tunnel is down.")
        return False

# Replace '9090' with your local SSH tunnel port
def create_ssh_tunnel(ssh_username, ssh_password, ssh_host, ssh_port, remote_host, remote_port, local_port=9090):
    server = SSHTunnelForwarder(
        ( ssh_host, ssh_port ),
        ssh_username=ssh_username,
        ssh_password=ssh_password, 
        remote_bind_address=(remote_host, remote_port),
        local_bind_address=('127.0.0.1', local_port)
    )
    server.start()
    print(f"SSH tunnel established. Local port: {server.local_bind_port}")
    return server


SSH_SERVER = '89.116.214.127'
SSH_PORT = 22  # default SSH port
SSH_USERNAME = 'root'
SSH_PASSWORD = '1kv|n@5=tA'

LOCAL_BIND_ADDRESS = 'localhost'
LOCAL_BIND_PORT = 9090  # local port to bind to
REMOTE_BIND_ADDRESS = '127.0.0.1'
REMOTE_BIND_PORT = 3306  # default MySQL port



with open_tunnel(
        (SSH_SERVER, SSH_PORT),
        ssh_username=SSH_USERNAME,
        ssh_password=SSH_PASSWORD,
        remote_bind_address=(REMOTE_BIND_ADDRESS, REMOTE_BIND_PORT),
        local_bind_address=(LOCAL_BIND_ADDRESS, LOCAL_BIND_PORT)) as tunnel:
    print(f"Tunnel is open on local port {tunnel.local_bind_port}.")

    ## connect to the database
    check_ssh_tunnel(port=9090)

    db = DB('127.0.0.1', 'osticketuser', '1Yvckn2S', '9090', 'osticketdb')

    print(db.connection.sql('select * from ost_email;').show())

    


    input("Press Enter to close the tunnel...")



