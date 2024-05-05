import socket

# Create a socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Set the socket to broadcast mode
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Bind the socket to a port
sock.bind(('', 5000))

# Create a message to broadcast
message = "Hello, world!"

# Broadcast the message
sock.sendto(message.encode(), ('<broadcast>', 5000))

# Close the socket
sock.close()
