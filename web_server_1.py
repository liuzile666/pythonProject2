import socket
import _thread as thread

NOT_FOUND_RESPONSE = b"""\
HTTP/1.1 404 Not Found
Content-type: text/plain
Content-length: 9

Not Found""".replace(b"\n", b"\r\n")

tries = True

def handleRequest(tcpSocket):
	'''
	Handle http request , get request path, content, and so on
	:param tcpSocket: Created tcp socket to receive data
	:return:
	'''

	# 1. Receive request message from the client on connection socket
	clientSock, clienAddr = tcpSocket.accept()
	# 2. Extract the path of the requested object from the message (second part of the HTTP header)
	httpPacket = clientSock.recv(1024).decode()
	print(httpPacket)
	Header = httpPacket.split("\r\n")[0]
	requestPath = Header.split(" ")[1]
	print(requestPath)
	requestPath = requestPath.split("/")[1]
	print(requestPath)

	#3. Read the corresponding file from disk
	try:
		with open(requestPath, 'rb') as f:
			# 4. Store in temporary buffer
			html_content = f.read()
			f.close()
			response = 'HTTP/1.1 200 OK \r\n'
			response += '\r\n'
			clientSock.send(response.encode("utf-8"))
			clientSock.send(html_content)
			print("Data transfer succeeded")
			clientSock.close()
			print("Client socket closed")

	# 5. Send the correct HTTP response error
	except FileNotFoundError:
		clientSock.sendall(NOT_FOUND_RESPONSE)
		tries = False
	# 6. Send the content of the file to the socket
	# 7. Close the connection socket


def startServer(serverAddress, serverPort):
	'''
	Start web server

	:param serverAddress: Server address (default:'127.0.0.1')
	:param serverPort: Server port, set by user
	:return:
	'''
	# 1. Create server socket
	tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# 2. Bind the server socket to server address and server port
	tcpSocket.bind((serverAddress, serverPort))
	# 3. Continuously listen for connections to server socket
	tcpSocket.listen(5)
	print("Waiting for connect...(address:{0} port:{1})".format(serverAddress, serverPort))

	# 4. When a connection is accepted, call handleRequest function, passing new connection socket
	while True:
		try:
			handleRequest(tcpSocket)
		except KeyboardInterrupt:
			print("Out of service")
			break
	#5. Close server socket
	tcpSocket.close()
	print("Close socket (address:{0} port:{1})".format(serverAddress, serverPort))


def main():
	while True:
		try:
			port = int(input("please input a port number you like:\n"))
			if port == 0:
				break
			thread.start_new_thread(startServer, ("127.0.0.1", port))
		except KeyboardInterrupt:
			print("Created thread error")
			break

if __name__ == '__main__':
    main()
	#http://127.0.0.1:12001/index.html
