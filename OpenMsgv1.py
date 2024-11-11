'''
Private Open Source License 1.0
Copyright 2024 Dominic Hord

https://github.com/DomTheDorito/Private-Open-Source-License

Permission is hereby granted, free of charge, to any person 
obtaining a copy of this software and associated documentation 
files (the “Software”), to deal in the Software without limitation 
the rights to personally use, copy, modify, distribute,and to permit 
persons to whom the Software is furnished to do so, subject to the 
following conditions:

1. The above copyright notice and this permission notice shall be 
included in all copies or substantial portions of the Software.

2. The source code shall not be used for commercial purposes, including 
but not limited to sale of the Software, or use in products intended for 
sale, unless express writen permission is given by the source creator.

3. Attribution to source work shall be made plainly available in a reasonable manner.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

THIS LICENSE MAY BE UPDATED OR REVISED, WITH NOTICE ON THE POS LICENSE REPOSITORY.
'''
import threading
import tkinter as tk
import socket
import time

class APRSFIUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenMsg v1.0 by AD8AK")

        # Setup GUI Fields
        tk.Label(root, text="Operator Callsign:").grid(row=0, column=0, sticky="w")
        self.operator_callsign_entry = tk.Entry(root)
        self.operator_callsign_entry.grid(row=0, column=1)
        
        tk.Label(root, text="Operator APRS Passcode:").grid(row=1, column=0, sticky="w")
        self.operator_passcode_entry = tk.Entry(root, show="*")
        self.operator_passcode_entry.grid(row=1, column=1)

        tk.Label(root, text="Recipient Callsign:").grid(row=2, column=0, sticky="w")
        self.recipient_callsign_entry = tk.Entry(root)
        self.recipient_callsign_entry.grid(row=2, column=1)
        
        tk.Label(root, text="Message:").grid(row=3, column=0, sticky="w")
        self.message_entry = tk.Entry(root)
        self.message_entry.grid(row=3, column=1)

        # Send Message Button
        self.upload_button = tk.Button(root, text="Send Message", command=self.send_message)
        self.upload_button.grid(row=4, columnspan=2)

        # Received Messages Box
        self.received_messages = tk.Text(root, height=10, width=50, state='disabled')
        self.received_messages.grid(row=7, columnspan=2)
        
        # Listener thread will be started only after valid callsign and passcode are entered
        self.listener_thread = None

    def send_message(self):
        operator_callsign = self.operator_callsign_entry.get()
        operator_passcode = self.operator_passcode_entry.get()
        recipient_callsign = self.recipient_callsign_entry.get().upper()
        message = self.message_entry.get()

        try:
            aprs_server = "rotate.aprs2.net"
            aprs_port = 14580
            aprs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            aprs_socket.connect((aprs_server, aprs_port))

            login_data = f"user {operator_callsign} pass {operator_passcode} vers OpenMsg v1.0 by AD8AK"
            aprs_socket.sendall(login_data.encode() + b'\n')
            
            # Send the message
            symbol = '/'  # Default symbol if none selected
            aprs_message = f"{operator_callsign}>APZ420,TCPIP*::{recipient_callsign:9}:{symbol} {message}\n"
            aprs_socket.sendall(aprs_message.encode())

            self.upload_button.config(bg="green")
            self.message_entry.delete(0, tk.END)

        except Exception as e:
            self.upload_button.config(bg="red")
            print(f"Error sending message: {e}")

        finally:
            aprs_socket.close()

    def start_listener(self):
        operator_callsign = self.operator_callsign_entry.get()
        operator_passcode = self.operator_passcode_entry.get()

        if not operator_callsign or not operator_passcode:
            self.display_received_message("Error: Operator callsign and passcode must be provided.")
            return

        while True:
            try:
                print("Attempting to connect to APRS-IS server...")
                aprs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                aprs_server = "rotate.aprs2.net"
                aprs_port = 14580
                aprs_socket.connect((aprs_server, aprs_port))
                self.display_received_message("Connected to APRS server.")
                
                # Login data format and filter format
                login_data = f"user {operator_callsign} pass {operator_passcode} vers OpenMsg v1.0 by AD8AK"
                aprs_socket.sendall(login_data.encode() + b'\n')
                
                # Filter for incoming messages to/from operator_callsign
                filter_data = f"filter t/m {operator_callsign}"
                aprs_socket.sendall(filter_data.encode() + b'\n')
                self.display_received_message(f"Login sent. Listening for messages for {operator_callsign}.")

                while True:
                    data = aprs_socket.recv(1024)

                    if not data:
                        break  # Break if no data

                    try:
                        decoded_data = data.decode('utf-8', errors='ignore')
                    except UnicodeDecodeError as e:
                        self.display_received_message(f"Decoding error: {e}")
                        continue

                    if decoded_data:
                        print(f"Received Data: {decoded_data}")  # Debug print
                        # Only process data that contains the operator_callsign (e.g. N0CALL-2)
                        if f"::{operator_callsign}" in decoded_data:
                            print("Found matching callsign!")
                            formatted_message = self.format_message(decoded_data, operator_callsign)
                            self.schedule_message_update(formatted_message)
                        #else:
                            # For debugging: display all received data to verify if the filter is working
                            #self.schedule_message_update(f"Debug: {decoded_data}")
                            #self.schedule_message_update(formatted_message1)

            except Exception as e:
                self.display_received_message(f"Error: {e}")
                time.sleep(5)  # Retry connection after delay

            finally:
                aprs_socket.close()
                self.display_received_message("Disconnected from server. Retrying in 5 seconds...")

    def schedule_message_update(self, message):
        # Use Tkinter's `after` method to safely update the GUI from the listener thread
        self.root.after(0, self.display_received_message, message)

    def display_received_message(self, message):
        # Updating the Text widget in a thread-safe way
        self.received_messages.config(state='normal')
        self.received_messages.insert(tk.END, message + '\n')
        self.received_messages.config(state='disabled')

        self.received_messages.yview(tk.END)

    def format_message(self, data, operator_callsign):
        """
        Format the received message into the desired structure:
        
        To: [Receiving Call]
        From: [Sending Call]
        Message: [Message Content]
        """
        try:
            print(f"Formatting message: {data}")  # Debug print to check the incoming message format

            # Split the message at '::' to separate the header from the message body
            parts = data.split("::")
            
            # Ensure that the parts contain at least 2 elements (header and message)
            if len(parts) < 2:
                return f"Error parsing message: {data}"

            # Extract the sending callsign (before the '>')
            sending_callsign = parts[0].split(">")[0].strip()

            # Extract the receiving callsign (after '::' and before the first ' :')
            receiving_part = parts[1].split(":")
            receiving_callsign = receiving_part[0].strip()

            # Extract the message content (after the first ':')
            if len(receiving_part) > 1:
                message_content = receiving_part[1].split("{")[0].strip()  # Remove '{' and beyond
            else:
                message_content = "No message content"

            # Format the message correctly
            formatted_message = f"To: {receiving_callsign}\nFrom: {sending_callsign}\nMessage: {message_content}"
            return formatted_message

        except Exception as e:
            return f"Error formatting message: {str(e)}"

    def on_start_listener(self):
        if not self.listener_thread or not self.listener_thread.is_alive():
            self.listener_thread = threading.Thread(target=self.start_listener, daemon=True)
            self.listener_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = APRSFIUploader(root)

    # Start the listener when user enters the callsign and passcode
    tk.Button(root, text="Start Listener", command=app.on_start_listener).grid(row=5, columnspan=2)
    root.mainloop()
