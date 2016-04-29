# Noisy Cricket

A traffic generator made for the Dakota State University offensive security club, it takes an nmap's XML output as a its input.

The following is a listing of command line options

`-c` tells the program if it should attempt to connect to closed or filtered connections.

`-f <input file>` defines the name the input file currently the program takes the an nmap scan in an xml format (the `-oX` flag in nmap)

`-l <int>` defines how many links the HTTP spiders will follow

`-d <int>` is the maximum time -1 the the program will wait before making another request, the avrage delay is about half the delayFactor (set to 1024 be default)

`-D` tells the program to print debug mesages print debugging messages

`-r` tells the program to wait for instructions from a remote command and controll server.


SSH has not been implmented yet because I wrote this on a windows box and paramiko doesn't work on windows.  Will be implmented soon^tm
