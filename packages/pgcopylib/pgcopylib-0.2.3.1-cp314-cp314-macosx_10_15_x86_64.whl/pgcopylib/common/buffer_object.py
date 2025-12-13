from io import BytesIO


class BufferObject(BytesIO):
    """BytesIO which always reads the requested number of bytes."""

    def read(self, size: int = -1) -> bytes:
        """Custom reader method."""

        if size <= 0:
            return super().read(size)

        data = b""

        while len(data) < size:
            chunk = super().read(size - len(data))

            if not chunk:
                break

            data += chunk

        return data
