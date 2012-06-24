from TypeSerializer import TypeSerializer
import time
SERIALIZER_TYPE_OBJECT = 0;
SERIALIZER_TYPE_BYTE_ARRAY = 1;
SERIALIZER_TYPE_INTEGER = 2;
SERIALIZER_TYPE_LONG = 3;
SERIALIZER_TYPE_CLASS = 4;
SERIALIZER_TYPE_STRING = 5;
SERIALIZER_TYPE_DATE = 6;
SERIALIZER_TYPE_BIG_INTEGER = 7;
SERIALIZER_TYPE_EXTERNALIZABLE = 8;
SERIALIZER_TYPE_BOOLEAN = 9;
#SERIALIZER_PRIORITY_OBJECT = Integer.MAX_VALUE;
SERIALIZER_PRIORITY_BYTE_ARRAY = 100;
SERIALIZER_PRIORITY_INTEGER = 300;
SERIALIZER_PRIORITY_BOOLEAN = 200;# changed from 300 because of bool is subclass of int
SERIALIZER_PRIORITY_LONG = 200;
SERIALIZER_PRIORITY_CLASS = 500;
SERIALIZER_PRIORITY_STRING = 400;
SERIALIZER_PRIORITY_DATE = 500;
SERIALIZER_PRIORITY_BIG_INTEGER = 600;
SERIALIZER_PRIORITY_EXTERNALIZABLE = 50;
class DefaultSerializer:
    def __init__(self):
        self.serializers = []
        self.addSerializer(IntegerSerializer())
        self.addSerializer(StringSerializer())
        self.addSerializer(LongSerializer())
        self.addSerializer(BooleanSerializer())
        self.typeSerializer = {}
        self.serializers = sorted(self.serializers)
        for ts in self.serializers:
            self.typeSerializer[ts.getTypeId()] = ts           
    def addSerializer(self, serializer):
        self.serializers.append(serializer)
    def write(self, output, obj):
        typeId = -1
        for ts in self.serializers:
            if ts.isSuitable(obj):
                self.typeSerializer[ts.getTypeId()] = ts
                typeId = ts.getTypeId()
                break
        if typeId == -1:
            raise AttributeError("There is no suitable serializer")
        output.writeByte(typeId)
        self.typeSerializer[typeId].write(output, obj)
        
    def read(self, inputStream):
        typeId = inputStream.readByte()
        if typeId == -1:
            raise AttributeError("There is no suitable serializer")
        return self.typeSerializer[typeId].read(inputStream)
        
class StringSerializer(TypeSerializer):
    def priority(self):
        return SERIALIZER_PRIORITY_STRING
    def isSuitable(self, obj):
        return isinstance(obj, basestring)
    def getTypeId(self):
        return SERIALIZER_TYPE_STRING
    def read(self,inputStream):
        print "read ss"
        #return readed string
        pass
    def write(self, output, obj):
        print "serializing with ss"
        output.writeUTF(obj)
class IntegerSerializer(TypeSerializer):
    def priority(self):
        return SERIALIZER_PRIORITY_INTEGER
    def isSuitable(self, obj):
        return isinstance(obj, int)
    def getTypeId(self):
        return SERIALIZER_TYPE_INTEGER
    def read(self,inputStream):
        data = inputStream.readInt()
        return data
    def write(self, output, obj):
        print "serializing with is"
        output.writeInt(obj)
class LongSerializer(TypeSerializer):
    def priority(self):
        return SERIALIZER_PRIORITY_LONG
    def isSuitable(self, obj):
        return isinstance(obj, long)
    def getTypeId(self):
        return SERIALIZER_TYPE_LONG
    def read(self,inputStream):
        print "read ls"
        #return readed integer
        pass
    def write(self, output, obj):
        print "serializing with long serializer"
        output.writeLong(obj)
class BooleanSerializer(TypeSerializer):
    def priority(self):
        return SERIALIZER_PRIORITY_BOOLEAN
    def isSuitable(self, obj):
        return isinstance(obj, bool)
    def getTypeId(self):
        return SERIALIZER_TYPE_BOOLEAN
    def read(self):
        print "read is"
        #return readed integer
        pass
    def write(self, output, obj):
        print "serializing with boolean serializer"
        output.writeBoolean(obj)
class DateSerializer(TypeSerializer):
    def priority(self):
        return SERIALIZER_PRIORITY_DATE
    def isSuitable(self, obj):
        return isinstance(obj, time)
    def getTypeId(self):
        return SERIALIZER_TYPE_DATE
    def read(self):
        #return readed integer
        pass
    def write(self, output, obj):
        print "serializing with boolean serializer"
        output.writeLong(long((obj.time() * 1000))) # time in milis
                
        