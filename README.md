# DSUOffSecClubTrafficGenerator

A traffic generator made for the Dakota State University offensive security club

`attemptClosedAndFilteredConnections` tells the program if it should attempt to connect to closed or filtered connections.

`inputFile` defines the name the input file currently the program takes the an nmap scan in an xml format (the `-oX` flag in nmap)

`maxLinksFollowed` defines how many links the HTTP spiders will follow

`delayFactor` is the maximum time -1 the the program will wait before making another request, the avrage delay is about half the delayFactor (set to 1024 be default)

`debug` tells the program to print debug mesages print debugging messages


SSH has not been implmented yet because I wrote this on a windows box and paramiko doesn't work on windows.  Will be implmented soontm
