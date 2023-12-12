import socket

def build_request(server_name, server_port):
    request_line = 'GET /index.html HTTP/1.1\r\n'
    request_headers = 'Host: %s:%d\r\n' % (server_name, server_port)
    request_data = request_line + request_headers + '\r\n'
    return request_data.encode('utf-8')

def request(server_name, server_port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_name, server_port))
        client_socket.send(build_request(server_name, server_port))
        data = client_socket.recv(1024)
        print("From server:\n{0}".format(data.decode()))

def main():
    server_name = '127.0.0.1'
    server_port = 8080
    request(server_name, server_port)

if __name__ == '__main__':
    main()
