#!usr/bin/env python

import subprocess
import optparse
import re


def getargs():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="get interface")
    parser.add_option("-m", "--mac", dest="mac", help="get mac address")

    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("specify interface, use --help for more info")

    elif not options.mac:
        parser.error("spec mac, use --help for info")

    return options


def changeMac(interface, mac):
    subprocess.call(["ifconfig", interface, "down"])

    subprocess.call(["ifconfig", interface, "hw", "ether", mac])

    subprocess.call(["ifconfig", interface, "up"])


def getCurrentMac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("Couldn't read mac address")


options = getargs()

changeMac(options.interface, options.mac)

currentMac = getCurrentMac(options.interface)

print("Current MAC = " + str(currentMac))

changeMac(options.interface, options.mac)

currentMac = getCurrentMac(options.interface)

if currentMac == options.mac:
    print("MAC address has been changed successfully")
else:
    print("MAC address change has failed")
