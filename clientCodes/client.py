import asyncio
import sys
import socketio
import os
import glob
from pathlib import Path
import logging
from cryptography.fernet import Fernet
import asyncio
import sys

BUFFER_SIZE = 4096  # send 4096 bytes each time step
SEPARATOR = "<SEPARATOR>"

# directory containing the mseed files
recordingLoc = ""
for item in "Desktop/ServerClientCode/data".split("/"):
    recordingLoc = os.path.join(recordingLoc, item)

# CODES
homeDir = str(Path.home())  # home directory
recordingLocPath = os.path.join(homeDir, f"{recordingLoc}")
all_mseeds = glob.glob(os.path.join(recordingLocPath, "*.mseed"))
# mseed = all_mseeds[3]
# print(all_mseeds)
filesSent = {}


with open('passcode.rf', 'rb') as f:
    passcode = f.readline()

sendFilesRegister = "list_of_sent_files.txt"


def write_finished_filename(filename):
    with open(sendFilesRegister, 'a') as f:
        f.write(f"{filename}\n")


if os.path.exists(sendFilesRegister):
    os.remove(sendFilesRegister)


def read_finished_filenames(sendFilesRegister):
    if os.path.exists(sendFilesRegister):
        with open(sendFilesRegister, 'r') as f:
            filesSent = [os.path.basename(line.rstrip())
                         for line in f]
    else:
        filesSent = []
    return filesSent


sio = socketio.Client()


def send_mseed_data():
    while True:
        try:
            all_mseeds = glob.glob(os.path.join(recordingLocPath, "*.mseed"))
            filesSent = set(read_finished_filenames(sendFilesRegister))
            for mseed in all_mseeds:
                # send only if not sent before
                if os.path.basename(mseed) not in filesSent:
                    # filesize = os.path.getsize(mseed)/(1024*1024)
                    filenameBase = ".".join(
                        os.path.basename(mseed).split(".")[:-1])
                    with open(mseed, "rb") as f:
                        counter = 0
                        while True:
                            # read the bytes from the file
                            bytes_read = f.read(BUFFER_SIZE)
                            if not bytes_read:
                                # file transmitting is done
                                break
                            # print(
                            #     f"sending file {filenameBase}_{counter}.mseedsplit")
                            returned_filename = sio.call(
                                'receive_mseed', {'filename': f"{filenameBase}{SEPARATOR}{counter}.mseedsplit", 'data_bytes': bytes_read})
                            counter += 1
                    write_finished_filename(
                        returned_filename)
                    print("returned filename: ", returned_filename,
                          os.path.basename(mseed))
                    sio.emit('merge_mseed', {
                        'filename': f"{filenameBase}{SEPARATOR}{counter-1}.mseedsplit"})
            sio.sleep(2)
        except KeyboardInterrupt:
            sys.exit()


@sio.event
def connect():
    print('connected')
    send_mseed_data()


@sio.event
def connect_error(e):
    print(e)


@sio.event
def disconnect():
    print('disconnected')


def main(username):
    sio.connect('http://localhost:8000',
                headers={'X-Username': username})
    sio.wait()


if __name__ == '__main__':
    clientName = "rfidget1"
    # main(sys.argv[1] if len(sys.argv) > 1 else None)
    main(clientName)
