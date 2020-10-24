#!/usr/bin/python
import scapy.all as scapy
import subprocess
import termcolor
import os
import time
import requests
import optparse
from sys import platform
import platform


if platform.system() == "Linux":

    def permissionsCheck():
        # Checks the users ID (root ID == 0)
        userIDcheck = os.geteuid()

        # Permissions error message if user is not root
        permissionsError = termcolor.colored(
            'Please run this script as sudo...\n\nPress any key to continue...', 'red')

        # If user is not root then do this...
        if userIDcheck != 0:
            input(permissionsError)
            subprocess.call(['clear'])

        # If user is root then do this...
        if userIDcheck == 0:
            def main():
                # Creates a function named scan and which can be ran with or without parser
                try:
                    def scan():
                        def get_arguments():
                            parser = optparse.OptionParser()

                            # Creates a parser that allows you to add options to quickly run from the CLI (ex. options = -i argument = 10.0.0.1/24)
                            parser.add_option(
                                "-t", "--target", dest="ip", help="Set target IP address")
                            parser.parse_args()  # Displays the parser options in the CLI with --help
                            # Takes the option selected and argument input by the user before running the command
                            (options, arguments) = parser.parse_args()
                            return options
                        options = get_arguments()

                        subprocess.call(['clear'], shell=True)
                        ip = options.ip or input(
                            "Enter target IP address \nex. (x.x.x.1/24)\n\nTarget IP: ")
                        # Uses scapy's ARP function to scan for the requested IP entered in the scan() functions parameter.
                        arp_request = scapy.ARP(pdst=ip)
                        # Sets the destination mac address to broadcast (all f's). A mac address of all f's will broadcast to all devices on the network
                        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
                        # Combines the broadcast and arp_request data into one packet using /
                        arp_request_broadcast = broadcast/arp_request
                        # Uses scapy's srp function to allow the user to send and receive packets with a custom broadcast address (unlike scapy.sr()) also returns 2 values (answered and unanswered) packets we only want answered packets so we will make this variable an array and only call the first itteration
                        answered_list = scapy.srp(
                            arp_request_broadcast, timeout=1, verbose=False)[0]

                        clients_list = []

                        print("[+] Gathering MAC vendor data...")

                        for element in answered_list:
                            #Mac address look up using macvendonrs API (Free version) ###UPGRADE TO PRO FOR FASTER RESULT PRINTING###
                            # Grabs the mac address of the responding device from the list
                            mac = element[1].hwsrc
                            request = requests.get(
                                "https://api.macvendors.com/" + mac)
                            response = request.content
                            time.sleep(1)  # Remove on pro upgrade
                            # Creates an Object (dictionary) of the element data
                            client_dict = {
                                "IP": element[1].psrc, "MAC": element[1].hwsrc, "Vendor": response}

                            # Appends the object (dictionary) to the array(list)
                            clients_list.append(client_dict)
                            # print(element[1].psrc + "\t\t" + mac + "\t\t" + response)
                        subprocess.call(['clear'])
                        return clients_list

                    # Print function (Prints the data type from scan())

                    def print_result(results_list):
                        print("\n_______________________________________________________________________________________________\nIP\t\t\tMAC Address\t\t\tVendor\n-----------------------------------------------------------------------------------------------\n")
                        for client in results_list:
                            time.sleep(.2)
                            print(client["IP"] + "\t\t" +
                                  client["MAC"] + "\t\t" + client["Vendor"])

                        # scapy.ls(broadcast) #Uses scapy's ls or list function to list possible options ex. IP, Ether, etc
                        # arp_request_broadcast.show() #Shows the details of this packet
                        # scapy.ls(arp_request)

                    scan_result = scan()
                    print_result(scan_result)
                except KeyboardInterrupt:
                    subprocess.call(['clear'])
                    exitCode = termcolor.colored(
                        "Program terminated by user.\nPress any key to continue...", color='red')
                    input(exitCode)
                    subprocess.call(['clear'])
            main()

    permissionsCheck()

elif platform.system() == "Windows":

    def main():
        # Creates a function named scan and which can be ran with or without parser
        try:
            def scan():
                def get_arguments():
                    parser = optparse.OptionParser()

                    # Creates a parser that allows you to add options to quickly run from the CLI (ex. options = -i argument = 10.0.0.1/24)
                    parser.add_option(
                        "-t", "--target", dest="ip", help="Set target IP address")
                    parser.parse_args()  # Displays the parser options in the CLI with --help
                    # Takes the option selected and argument input by the user before running the command
                    (options, arguments) = parser.parse_args()
                    return options
                options = get_arguments()

                subprocess.call(['cls'], shell=True)
                ip = options.ip or input(
                    "Enter target IP address \nex. (x.x.x.x/24)\n\nTarget IP: ")
                # Uses scapy's ARP function to scan for the requested IP entered in the scan() functions parameter.
                arp_request = scapy.ARP(pdst=ip)
                # Sets the destination mac address to broadcast (all f's). A mac address of all f's will broadcast to all devices on the network
                broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
                # Combines the broadcast and arp_request data into one packet using /
                arp_request_broadcast = broadcast/arp_request
                # Uses scapy's srp function to allow the user to send and receive packets with a custom broadcast address (unlike scapy.sr()) also returns 2 values (answered and unanswered) packets we only want answered packets so we will make this variable an array and only call the first itteration
                answered_list = scapy.srp(
                    arp_request_broadcast, timeout=1, verbose=False)[0]

                clients_list = []

                print("[+] Gathering MAC vendor data...")

                for element in answered_list:
                    #Mac address look up using macvendonrs API (Free version) ###UPGRADE TO PRO FOR FASTER RESULT PRINTING###
                    # Grabs the mac address of the responding device from the list
                    mac = element[1].hwsrc
                    request = requests.get(
                        "https://api.macvendors.com/" + mac)
                    response = request.content
                    time.sleep(1)  # Remove on pro upgrade
                    # Creates an Object (dictionary) of the element data
                    client_dict = {
                        "IP": element[1].psrc, "MAC": element[1].hwsrc, "Vendor": response.decode()} #decode() converts bytes to string

                    # Appends the object (dictionary) to the array(list)
                    clients_list.append(client_dict)
                    # print(element[1].psrc + "\t\t" + mac + "\t\t" + response)
                subprocess.call(['cls'], shell=True)
                return clients_list

            # Print function (Prints the data type from scan())

            def print_result(results_list):
                print("\n_______________________________________________________________________________________________\nIP\t\t\tMAC Address\t\t\tVendor\n-----------------------------------------------------------------------------------------------\n")
                for client in results_list:
                    time.sleep(.2)
                    print(client["IP"] + "\t\t" + client["MAC"] + "\t\t" + client["Vendor"])

                # scapy.ls(broadcast) #Uses scapy's ls or list function to list possible options ex. IP, Ether, etc
                # arp_request_broadcast.show() #Shows the details of this packet
                # scapy.ls(arp_request)

            scan_result = scan()
            print_result(scan_result)
        except KeyboardInterrupt:
            subprocess.call(['cls'], shell=True)
            exitCode = termcolor.colored(
                "Program terminated by user.\nPress any key to continue...", color='red')
            input(exitCode)
            subprocess.call(['cls'], shell=True)

    main()
