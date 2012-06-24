from OutputStream import OutputStream
from CustomSerializerAdapter import CustomSerializerAdapter
from InputStream import InputStream

class AbstractSerializer:
    def __init__(self,ds,cs):
        self.ds = ds
        self.cs = CustomSerializerAdapter(cs)
        self.output = OutputStream()
        self.input = InputStream()
    def toByte(self,obj):
        self.output.flush()
        if object == None:
            return
        ts = self.ds if self.ds.isSuitable(obj) else self.cs
        self.output.writeByte(ts.getTypeId())
        ts.write(self.output,obj)
        return self.output.buf
    def toObject(self,data):
        self.input.setData(data)
        typeId = -1
        try:
            typeId = self.input.readByte()
            ts = self.ds if self.ds.getTypeId()==typeId else self.cs
            return ts.read(self.input)
        except Exception as e:
            print "serialization error"  , e
        self.input.flush()
    