#!/usr/bin/env python3
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version. It is provided for educational
# purposes and is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import collections
import pickle
import socket
import struct
import sys
import Console


Address = ["localhost", 9653]
CarTuple = collections.namedtuple("CarTuple", "seats mileage owner")


class SocketManager:

    def __init__(self, address):
        self.address = address


    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)
        return self.sock


    def __exit__(self, *ignore):
        self.sock.close()
        


def main():
    if len(sys.argv) > 1:
        Address[0] = sys.argv[1]
    call = dict(c=get_car_details, m=change_mileage, o=change_owner,
                n=new_registration, s=stop_server, q=quit)
    menu = ("(C)ar  (M)ileage  (O)wner  (N)ew car  "
            "(S)top server  (Q)uit")
    valid = frozenset("cmonsq")
    previous_license = None
    while True:
        action = Console.get_menu_choice(menu, valid, "c", True)
        previous_license = call[action](previous_license)


def retrieve_car_details(previous_license):
    license = Console.get_string("License", "license",
                                 previous_license)
    license = license.upper()
    ok, *data = handle_request("GET_CAR_DETAILS", license)
    if not ok:
        print(data[0])
        while True:
            symbols = Console.get_string("Start of license")
            symbols = symbols.upper()
            ok, *data = handle_request("GET_LICENSES_STARTING_WITH", symbols)
            if not data:
                print("No licence starts with {0}".format(symbols))
                continue
            for i, license in enumerate(data):
                print("({0}) {1}".format(i + 1, license))
            choice = Console.get_integer("Enter choice (0 to cancel)", "choice",
                                         minimum=1, maximum=len(data), allow_zero=True)
            if choice is not None:
                if not choice:
                    return previous_license, None
                ok, *data = handle_request("GET_CAR_DETAILS", license)
                break
    return license, CarTuple(*data)


def get_car_details(previous_license):
    license, car = retrieve_car_details(previous_license)
    if car is not None:
        print("License: {0}\nSeats:   {1[0]}\nMileage: {1[1]}\n"
              "Owner:   {1[2]}".format(license, car))
    return license


def change_mileage(previous_license):
    license, car = retrieve_car_details(previous_license)
    if car is None:
        return previous_license
    mileage = Console.get_integer("Mileage", "mileage",
                                  car.mileage, 0)
    if mileage == 0:
        return license
    ok, *data = handle_request("CHANGE_MILEAGE", license, mileage)
    if not ok:
        print(data[0])
    else:
        print("Mileage successfully changed")
    return license


def change_owner(previous_license):
    license, car = retrieve_car_details(previous_license)
    if car is None:
        return previous_license
    owner = Console.get_string("Owner", "owner", car.owner)
    if not owner:
        return license
    ok, *data = handle_request("CHANGE_OWNER", license, owner)
    if not ok:
        print(data[0])
    else:
        print("Owner successfully changed")
    return license


def new_registration(previous_license):
    license = Console.get_string("License", "license") 
    if not license:
        return previous_license
    license = license.upper()
    seats = Console.get_integer("Seats", "seats", 4, 0)
    if not (1 < seats < 10):
        return previous_license
    mileage = Console.get_integer("Mileage", "mileage", 0, 0)
    owner = Console.get_string("Owner", "owner")
    if not owner:
        return previous_license
    ok, *data = handle_request("NEW_REGISTRATION", license, seats,
                               mileage, owner)
    if not ok:
        print(data[0])
    else:
        print("Car {0} successfully registered".format(license))
    return license


def quit(*ignore):
    sys.exit()


def stop_server(*ignore):
    handle_request("SHUTDOWN", wait_for_reply=False)
    sys.exit()


def handle_request(*items, wait_for_reply=True):
    version = 1
    InfoStruct = struct.Struct("!IB")
    data = pickle.dumps(items, 3)

    try:
        with SocketManager(tuple(Address)) as sock:
            sock.sendall(InfoStruct.pack(len(data), version))
            sock.sendall(data)
            if not wait_for_reply:
                return

            info = sock.recv(InfoStruct.size)
            size, server_version = InfoStruct.unpack(info)
            assert server_version <= version, 'Incompatible server'
            result = bytearray()
            while True:
                data = sock.recv(4000)
                if not data:
                    break
                result.extend(data)
                if len(result) >= size:
                    break
        return pickle.loads(result)
    except socket.error as err:
        print("{0}: is the server running?".format(err))
        sys.exit(1)
    except AssertionError as err:
        print(err)
        sys.exit(1)


main()
