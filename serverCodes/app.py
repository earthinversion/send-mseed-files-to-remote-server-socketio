import random
import socketio
import eventlet
from cryptography.fernet import Fernet
import os
import glob


SEPARATOR = "<SEPARATOR>"

with open('passcode.rf', 'rb') as f:
    line = f.readline()

with open('key.rf', 'rb') as f:
    key = f.read()
# print(key)

fernet = Fernet(key)  # build the passcode reader
serverpasscode = fernet.decrypt(line).decode()  # passcode read


sio = socketio.Server()
app = socketio.WSGIApp(sio)
client_count = 0
a_count = 0
b_count = 0


@sio.event
def connect(sid, environ):
    global client_count
    global a_count
    global b_count

    username = environ.get('HTTP_X_USERNAME')
    if not username:
        return False
    print('username:', username)

    with sio.session(sid) as session:
        session['username'] = username
    # sio.emit('user_joined', username)

    client_count += 1
    print(sid, 'connected')
    # sio.start_background_task(task, sid)


@sio.event
def disconnect(sid):
    global client_count
    global a_count
    global b_count
    client_count -= 1
    print(sid, 'disconnected')


@sio.event
def receive_mseed(sid, data):
    # print(data)
    filename = data['filename']
    filename_to_return = filename.split(SEPARATOR)[0] + ".mseed"
    with sio.session(sid) as session:
        username = session['username']
        os.makedirs(username, exist_ok=True)
        new_filename = username+SEPARATOR+filename

    # print(f"Receiving file {filename}")
    with open(os.path.join(username, filename), "wb") as f:
        # write to the file the bytes we just received
        f.write(data['data_bytes'])
    return filename_to_return


def merge_task(filename, username):
    # to read all splits: taiwan_2017-03-10_IU.TATO.00.BHZ<SEPARATOR>962.mseedsplit
    # rfidget1/taiwan_2017-03-01_TW.KMNB..BHZ<SEPARATOR>0.mseedsplit
    # rfidget1/taiwan_2017-03-10_IU.TATO.00.BHZ<SEPARATOR>0.mseedsplit
    fileprefix = filename.split(SEPARATOR)[0]
    fileprefix = os.path.join(username, fileprefix)
    filesuffix = filename.split(SEPARATOR)[1].split(".")[0]
    filetowrite = fileprefix+".mseed"
    if os.path.exists(filetowrite):
        os.remove(filetowrite)
    with open(filetowrite, "ab") as fileobjtowrite:
        for i in range(int(filesuffix)+1):
            splitFile = fileprefix+SEPARATOR+str(i)+".mseedsplit"
            with open(splitFile, 'rb') as fileobjtoread:
                fileobjtowrite.write(fileobjtoread.read())
            os.remove(splitFile)


@sio.event
def merge_mseed(sid, data):
    with sio.session(sid) as session:
        username = session['username']
    if os.path.exists(os.path.join(username, data['filename'])):
        print(f"Merging {data['filename']}")
        sio.start_background_task(merge_task, data['filename'], username)
    else:
        print(f"File {data['filename']} not exists")


if __name__ == '__main__':
    SERVER_HOST = ''
    SERVER_PORT = 8000
    eventlet.wsgi.server(eventlet.listen(
        (SERVER_HOST, SERVER_PORT)), app)  # websocket

    # or
    # gunicorn -k eventlet -w 1 --reload app:app
