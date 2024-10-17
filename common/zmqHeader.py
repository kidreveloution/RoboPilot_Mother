import zmq
import sys
import os
import logging
import requests
import json
import threading
import common.messageBuilder as messageBuilder
logging.basicConfig(filename='app.log', level=logging.INFO)

class ZMQ_CONNECTION:
    def __init__(self, TX_ID: str, RX_ID: str, SERVER_IP: str, message_handler=None) -> None:
        self.TX_ID = TX_ID
        self.RX_ID = RX_ID
        self.SERVER_IP = SERVER_IP
        self.context = zmq.Context()
        self.dealer = None
        self.message_handler = message_handler
        self.running = False  # Initialize the running flag
        logging.info(f"Initializing ZMQ_CONNECTION with TX_ID: {TX_ID}, RX_ID: {RX_ID}, SERVER_IP: {SERVER_IP}")

        if not TX_ID or not RX_ID or not SERVER_IP:
            raise ValueError("TX_ID, RX_ID, and SERVER_IP must be provided.")
    
    def get_public_ip(self) -> str:
        try:
            response = requests.get('https://api.ipify.org')
            response.raise_for_status()  # Raises an error for bad responses
            return response.text
        except requests.RequestException as e:
            logging.error(f"Failed to get public IP: {e}")
            return "0.0.0.0"  # Return a default IP if the request fails
    
    def connectZMQ(self) -> bool:
        try:
            logging.debug(f"Attempting to connect to {self.SERVER_IP}")
            self.dealer = self.context.socket(zmq.DEALER)
            self.dealer.setsockopt(zmq.IDENTITY, self.TX_ID.encode('utf-8'))
            self.dealer.connect(self.SERVER_IP)
            logging.debug(f"Connected to {self.SERVER_IP}")
            
            registration_message = self.registerAtRouter()
            logging.debug(f"Sending registration message: {registration_message}")
            self.dealer.send_multipart([self.TX_ID.encode('utf-8'), registration_message.encode('utf-8')])
            logging.info("Connected and registration message sent.")
            return True
        except zmq.ZMQError as e:
            logging.error(f"ZMQ Error during connection: {e}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error during connection: {e}")
            return False
    
    
    def registerAtRouter(self) -> str:
        try:
            public_ip = self.get_public_ip()
            logging.debug(f"Got public IP: {public_ip}")
            initial_message = messageBuilder.MESSAGE_CLASS(
                tx_id=self.TX_ID,
                msg_name="register",
                rx_id=self.RX_ID,
                content={"ip_address": public_ip}
            ).buildMessage()
            logging.debug(f"Built registration message: {initial_message}")
            return initial_message
        except Exception as e:
            logging.error(f"Failed to build registration message: {e}")
            return ""

    def listen(self):
        """Listens for incoming messages from the ROUTER socket."""
        try:
            while self.running:
                # Wait for incoming messages
                message = self.dealer.recv_multipart()
                if message:
                    #print(f"Received message: {message}")
                    if self.message_handler:
                            self.message_handler(message[0].decode('utf-8'))  # Call the external handler

        except Exception as e:
            logging.error(f"Error while listening: {e}")
    
    def sendMessage(self, RX_ID, msg_name, content):
        if isinstance(content, str):
            content = json.loads(content)
        msg = messageBuilder.MESSAGE_CLASS(
            tx_id=self.TX_ID,
            msg_name=msg_name,
            rx_id=RX_ID,
            content=content
        ).buildMessage()
        self.dealer.send_multipart([self.TX_ID.encode('utf-8'), msg.encode('utf-8')])

    def startListenThread(self):
        self.running = True
        self.listenThread = threading.Thread(target=self.listen)
        self.listenThread.start()
    
    def stopListenThread(self):
        self.running = False
        if self.listenThread.is_alive():
            self.listenThread.join()
    
    def close(self):
        self.stopListenThread()
        if self.dealer:
            self.dealer.close()
        self.context.term()
        logging.info("ZMQ connection closed.")
