# send-mseed-files-to-remote-server-socketio

This repository contains client and server scripts that enable the transfer and merging of mseed files using the Socket.IO library in Python. The client script sends mseed files to the server, which merges the files into a single file.

## Client side script
The client.py script is a Python script that uses the Socket.IO library to send mseed data files from the client to the server. It sends files to the server that are located in a specific directory on the client machine.

The client script uses asyncio for concurrency and also relies on the glob and os libraries for directory and file management. It also uses the cryptography library for encryption.

### Dependencies
- Python 3.x
- Socket.IO client library
- asyncio
- glob
- os
- logging
- cryptography.fernet

### Run
The client.py script can be run from the command line using the following command:
```
python client.py
```

## Server side script
The `app.py` script is the server-side script that receives mseed files sent by the client and merges them into a single file. The server uses the Socket.IO library to handle communication with the client.

The script uses the os, glob, eventlet, and socketio libraries. It also uses the cryptography library for encryption.

The app.py script requires a passcode.rf and key.rf files to be present in the same directory. The passcode.rf file contains the passcode used to encrypt and decrypt messages between the client and server. The key.rf file contains the encryption key used to encrypt and decrypt the passcode.

The app.py script can be run from the command line using the following command:
```
python app.py
```
