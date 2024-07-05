# Import the necessary module from the RPLCD library
from RPLCD.i2c import CharLCD
from gpiozero import Buzzer, LED
import time
import socket


buzzer = Buzzer(14)
led = LED(15)

# Initialize the LCD using the I2C expander PCF8574
lcd = CharLCD(
    i2c_expander='PCF8574', # I2C expander type
    address=0x27,           # I2C address of the LCD
    port=1,                 # I2C port (1 for Raspberry Pi)
    cols=16,                # Number of columns on the LCD
    rows=2,                 # Number of rows on the LCD
    dotsize=8               # Dot size of the text
)

# Clear the display
lcd.clear()
buzzer.off()
led.off()

def run_server():
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_ip = "10.207.1.146"
    port = 8000

    # bind the socket to a specific address and port
    server.bind((server_ip, port))
    # listen for incoming connections
    server.listen(0)
    print(f"Listening on {server_ip}:{port}")

    # accept incoming connections
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # receive data from the client
    while True:
        request = client_socket.recv(1024)
        request = request.decode("utf-8") # convert bytes to string
        
        # if we receive "close" from the client, then we break
        # out of the loop and close the conneciton
        if request.lower() == "close":
            # send response to the client which acknowledges that the
            # connection should be closed and break out of the loop
            client_socket.send("closed".encode("utf-8"))
            break

        
        response = "accepted".encode("utf-8") # convert string to bytes
        # convert and send accept response to the client
        client_socket.send(response)
        
        
        request = int(request)
        for i in range(request):
            request -= 1
            lcd.clear()
            buzzer.on()
            lcd.write_string('Time till ')
            lcd.cursor_pos = (1, 0)
            lcd.write_string('explosion: ' + str(request))
            buzzer.off()
            time.sleep(0.2)
    
        print('Self destruct finished')
        
        client_socket.send('self destruct finished'.encode('utf-8'))
        while True:
            buzzer.on()
            led.on()
            
    # close connection socket with the client
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server.close()


run_server()