# Noisy Cricket

A traffic generator made for the Dakota State University offensive security club, it takes an nmap's XML output as a its input.

The following is a listing of command line options

`-c` tells the program if it should attempt to connect to closed or filtered connections.

`-f <input file>` defines the name the input file currently the program takes the an nmap scan in an xml format (the `-oX` flag in nmap)

`-d <int>` is the maximum time -1 the the program will wait before making another request, the avrage delay is about half the delayFactor (set to 1024 be default)

`-D` tells the program to print debug mesages print debugging messages