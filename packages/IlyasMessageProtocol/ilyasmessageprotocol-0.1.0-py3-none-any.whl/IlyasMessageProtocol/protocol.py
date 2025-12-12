import socket
import json
import os
from typing import List, Any

# size[10];type[3]{PIC,AUD,TXT,FIL,JSN,ERR};filename[20]:

HEADER_SIZE = 36


def send(socket_: socket.socket, data: bytes, type_: str, filename: str = '') -> None:
    size = str(len(data))
    size = (10 - len(size)) * '0' + size
    filename = (20 - len(filename)) * '0' + filename
    local_header = f'{size};{type_};{filename}:'
    socket_.sendall(local_header.encode())
    socket_.sendall(data)


def _get_data(socket_: socket.socket, amount_data: int):
    saved_amount_data = amount_data
    return_data = b''
    while amount_data != 0:
        data = socket_.recv(amount_data)
        amount_data = amount_data - len(data)
        if data != b'':
            return_data += data
        else:
            raise ConnectionError(f'Receive: {len(return_data)}; Expect: {saved_amount_data}')
    return return_data


def receive(socket_: socket.socket) -> list[str | int] | list[str] | list[str | Any]:
    header = _get_data(socket_, HEADER_SIZE).decode()[:-1]
    header_elements = header.split(';')
    size = int(header_elements[0])
    type_ = header_elements[1]
    filename = header_elements[2]
    while filename[0] == '0':
        filename = filename[1:]

    data = _get_data(socket_, size)

    if type_ == 'ERR':
        return [type_, int(data.decode())]

    elif type_ == 'TXT':
        return [type_, data.decode()]

    elif type_ == 'JSN':
        return [type_, json.loads(data.decode())]

    elif type_ in ['FIL', 'AUD', 'PIC']:
        os.makedirs('../../received_files', exist_ok=True)
        file = open(f'received_files/{filename}', 'wb')
        file.write(data)
        file.close()
        return [type_, f'received_files/{filename}']

    else:
        raise TypeError(f'Unknown type: {type_}')
