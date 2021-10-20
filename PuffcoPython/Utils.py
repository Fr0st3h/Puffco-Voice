import struct

class Utils():
    def parseFloat(data):
        stuct = struct.unpack('f', data)
        remove = ['(', ',', ')']
        for chars in remove:
            stuct = str(stuct).replace(chars, "")
        return float(stuct)

    def parseInt(data):
        stuct = struct.unpack('i', data)
        remove = ['(', ',', ')']
        for chars in remove:
            stuct = str(stuct).replace(chars, "")
        return int(stuct)

    def packInt(data):
        return struct.pack("<i", data)

    def packFloat(data):
        return struct.pack("<f", data)