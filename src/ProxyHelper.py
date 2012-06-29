from AbstractSerializer import AbstractSerializer
from DataSerializer import DataSerializer
from DefaultSerializer import DefaultSerializer
import types

class ProxyHelper:
    def __init__(self, connection):
        self.__connection = connection
        self.__newline = '\r\n'
        self.__serializer = AbstractSerializer(DataSerializer(), DefaultSerializer())
    def check(self, obj):
        if obj == None:
            raise ValueError("Object cannot be null")
    def doOp(self, command, flag=0, argsCount=0, binary=None, *c_args):
        command_str = command + ' ' + str(flag) + ' ' + ' '.join(c_args) + ' #' + str(argsCount) + self.__newline
        if argsCount != 0 and binary != None:
            size = ""
            data = bytearray()
            if isinstance(binary, (types.ListType, types.TupleType)):
                for item in binary:
                    byte = self.__serializer.toByte(item)
                    size += str(len(byte)) + " " 
                    data.extend(byte)
            elif isinstance(binary, types.DictionaryType):
                for k in binary.keys():
                    key = list(self.__serializer.toByte(k))
                    value = list(self.__serializer.toByte(binary[k]))
                    size += str(len(key)) + " " + str(len(value)) + " "
                    data.extend(key)
                    data.extend(value)
            else:
                byte = self.__serializer.toByte(binary)
                size += str(len(byte)) + " "
                data.extend(byte)
            command_str += size + self.__newline
            command_str += data
        return self.__connection.sendCommand(command_str)