import socket

class ByteKVClient:
    def __init__(self, host="127.0.0.1", port=6379):
        self.host = host
        self.port = port

    def _build_resp(self, *args):
        res = f"*{len(args)}\r\n"
        for arg in args:
            res += f"${len(str(arg))}\r\n{arg}\r\n"
        return res.encode()

    def _send_command(self, *args):
        with socket.create_connection((self.host, self.port)) as s:
            s.sendall(self._build_resp(*args))
            return self._parse_response(s)

    def _parse_response(self, sock):
        def readline():
            line = b""
            while not line.endswith(b"\r\n"):
                chunk = sock.recv(1)
                if not chunk:
                    break
                line += chunk
            return line.decode().strip()

        line = readline()
        if not line:
            return None

        prefix, payload = line[0], line[1:]

        if prefix == "+":
            return payload
        elif prefix == "-":
            raise Exception(payload)
        elif prefix == ":":
            return int(payload)
        elif prefix == "$":
            n = int(payload)
            if n == -1:
                return None
            data = sock.recv(n)
            sock.recv(2)  # skip \r\n
            return data.decode()
        else:
            return line

    # Basic KV operations
    def set(self, key, value, ttl=None):
        args = ["SET", key, value]
        if ttl is not None:
            args.append(str(ttl))
        return self._send_command(*args)

    def get(self, key):
        return self._send_command("GET", key)

    def delete(self, key):
        return self._send_command("DEL", key)

    def ping(self):
        return self._send_command("PING")

    # TTL commands
    def expire(self, key, seconds):
        """Set TTL for a key, returns 1 if successful, 0 otherwise."""
        return self._send_command("EXPIRE", key, str(seconds))

    def ttl(self, key):
        """Returns TTL in seconds: -2 if key missing, -1 if no expiration."""
        return self._send_command("TTL", key)

    # Optional publish
    def publish(self, channel, message):
        """Publish a message to a channel, returns number of subscribers."""
        return self._send_command("PUBLISH", channel, message)
