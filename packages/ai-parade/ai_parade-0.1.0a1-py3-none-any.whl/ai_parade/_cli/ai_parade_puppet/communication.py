import asyncio
import pickle
import socket
import struct
from typing import Any


class ConnectionClosed(Exception):
	"""Exception raised when the connection is closed"""

	def __init__(self, message: str):
		super().__init__(message)
		self.message = message


def send(socket: socket.socket, data: Any):
	pickled_data = pickle.dumps(data, 4)
	data_len = struct.pack(">L", len(pickled_data))
	socket.sendall(data_len + pickled_data)


async def send_async(writer: asyncio.StreamWriter, data: Any):
	pickled_data = pickle.dumps(data, 4)
	data_len = struct.pack(">L", len(pickled_data))
	writer.write(data_len + pickled_data)
	await writer.drain()


BUFF_SIZE = 4096  # 4 KiB


def receive(socket: socket.socket):
	return asyncio.run(receive_async(socket))


async def receive_async(reader: asyncio.StreamReader | socket.socket):
	raw_len = (
		await reader.read(4)
		if isinstance(reader, asyncio.StreamReader)
		else reader.recv(4)
	)
	if len(raw_len) != 4:
		if raw_len == b"":
			raise ConnectionClosed("Empty data received")
		else:
			raise RuntimeError(f"Wrong data received {raw_len} (expected data length)")
	data_len = struct.unpack(">L", raw_len)[0]

	fragments = []
	data_read = 0
	fragment = b""
	while data_read < data_len:
		fragment = (
			await reader.read(BUFF_SIZE)
			if isinstance(reader, asyncio.StreamReader)
			else reader.recv(BUFF_SIZE)
		)
		if len(fragment) == 0:
			raise ConnectionClosed("Empty data received")
		fragments.append(fragment)
		data_read += len(fragment)
	assert len(fragment) < BUFF_SIZE

	return pickle.loads(b"".join(fragments))
