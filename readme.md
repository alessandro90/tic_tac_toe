Very simple tic tac toe game. The goal was just to use python sockets to connect two devices in the same network.

If you want to run two instances on the same machine (localhost) just launch two times the script with

`python tic_tac_toe.py`

To connect to different machines launch the server with

`python tic_tac_toe.py 0.0.0.0`

for example, and the script on the client with

`python tic_tac_toe.py <server IP address>`

The IP address can be found with `ipconfig` on Windows or `ifconfig` on Linux.