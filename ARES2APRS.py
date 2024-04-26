## ARES2APRS v0.2.0
## Written by Scott N1OF and Dominic AD8AK
## Private Open Source License 1.0
## Copyright 2024 Scott Sheets & Dominic Hord
## https://github.com/DomTheDorito/Private-Open-Source-License


#Using tkinter for GUI
import tkinter as tk
from geopy.geocoders import Nominatim
import socket
from datetime import datetime

class APRSFIUploader:
    def __init__(self, root):
        self.root = root
        self.root.title("ARES2APRS v0.2.0 by N1OF/AD8AK")

        # Net Operator Callsign Field
        tk.Label(root, text="Net Operator Callsign:").grid(row=0, column=0, sticky="w")
        self.operator_callsign_entry = tk.Entry(root)
        self.operator_callsign_entry.grid(row=0, column=1)
        
        #Net Operator APRS.fi Passcode Field
        tk.Label(root, text="Net Operator APRS Passcode:").grid(row=1, column=0, sticky="w")
        self.operator_passcode_entry = tk.Entry(root, show="*")
        self.operator_passcode_entry.grid(row=1, column=1)

        # Spotter Callsign Field
        tk.Label(root, text="Spotter Callsign:").grid(row=2, column=0, sticky="w")
        self.spotter_callsign_entry = tk.Entry(root)
        self.spotter_callsign_entry.grid(row=2, column=1)
        
        #Report Field
        tk.Label(root, text="Report: (Max 9 Char)").grid(row=3, column=0, sticky="w")
        self.report_entry = tk.Entry(root)
        self.report_entry.grid(row=3, column=1)

        # Comment for APRS report Field
        tk.Label(root, text="Comment:").grid(row=4, column=0, sticky="w")
        self.comment_entry = tk.Entry(root)
        self.comment_entry.grid(row=4, column=1)

        # Address Field
        tk.Label(root, text="Full Address:").grid(row=5, column=0, sticky="w")
        self.address_entry = tk.Entry(root)
        self.address_entry.grid(row=5, column=1)

        # Table Select Field
        tk.Label(root, text="Table Select:").grid(row=6, column=0, sticky="w")
        self.table_entry = tk.Entry(root)
        self.table_entry.grid(row=6, column=1)

        # Symbol Field
        tk.Label(root, text="Symbol:").grid(row=7, column=0, sticky="w")
        self.symbol_entry = tk.Entry(root)
        self.symbol_entry.grid(row=7, column=1)

        # Upload Button (Moved to row 8 to accommodate new fields)
        self.upload_button = tk.Button(root, text="Upload to APRS", command=self.upload)
        self.upload_button.grid(row=8, columnspan=2)
        
    def get_coordinates(self, address):
        # Use Geocode to find coordinates
        geolocator = Nominatim(user_agent="APRSFIUploader")
        location = geolocator.geocode(address)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None

    def decimal_to_dm(self, coord):
        # Convert decimal degrees to degrees and decimal minutes
        degrees = int(coord)
        minutes = abs(coord - degrees) * 60
        return degrees, minutes

    def format_report_entry(self, report_entry):
        # Pad spotter callsign with spaces to make it 9 characters long
        return report_entry.ljust(9)

    def clear_fields(self):
        # Clear all entry fields
        self.spotter_callsign_entry.delete(0, tk.END)
        self.report_entry.delete(0, tk.END)
        self.comment_entry.delete(0, tk.END)
        self.address_entry.delete(0, tk.END)

    def upload(self):
        # Get user inputs
        operator_callsign = self.operator_callsign_entry.get()
        operator_passcode = self.operator_passcode_entry.get()
        spotter_callsign = self.spotter_callsign_entry.get()
        report_entry_formatted = self.format_report_entry(self.report_entry.get())
        comment = self.comment_entry.get()
        address = self.address_entry.get()
        table = self.table_entry.get()
        symbol = self.symbol_entry.get()

        # Convert address to coordinates
        latitude, longitude = self.get_coordinates(address)

        if latitude is None or longitude is None:
            print("Failed to retrieve coordinates for the provided address.")
            return

        # Get current time
        current_time = datetime.utcnow().strftime("%d%H%M")

        # Format coordinates
        lat_deg, lat_min = self.decimal_to_dm(latitude)
        lon_deg, lon_min = self.decimal_to_dm(longitude)

        # Format latitude and longitude
        formatted_latitude = f"{lat_deg:02d}{lat_min:05.2f}N"
        formatted_longitude = f"{lon_deg:03d}{lon_min:06.2f}E" if lon_deg >= 0 else f"{abs(lon_deg):03d}{lon_min:.2f}W"

        # Open connection to APRS-IS server
        try:
            aprs_server = "rotate.aprs2.net"
            aprs_port = 14580
            aprs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            aprs_socket.connect((aprs_server, aprs_port))
            login_data = 'user {} pass {} vers APRS Uploader v0.2.0 by N1OF/AD8AK'.format(operator_callsign, operator_passcode)
            aprs_socket.sendall(login_data.encode() + b'\n')

            # Send APRS data with current time
            aprs_data = f"{operator_callsign}>APZ420,TCPIP*:;{report_entry_formatted}*{current_time}z{formatted_latitude}{table}{formatted_longitude}{symbol}{comment}-Reported by {spotter_callsign}\n"
            aprs_socket.sendall(aprs_data.encode())
            
            # Change color of upload button to green if successful and clears fields.
            # If unsuccessful, change to red.

            self.upload_button.config(bg="green")
            self.clear_fields()

        except Exception as e:
            self.upload_button.config(bg="red")

        finally:
            # Close socket connection
            aprs_socket.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = APRSFIUploader(root)
    root.mainloop()
