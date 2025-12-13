

class ControlMsgType():
    newSignal = 'newSignal'
    
from marshmallow import Schema, fields,post_load
from datetime import datetime

class Control():
    def __init__(self,type,component=0,group=0,ioDevice="",ioSignal="",parameter={},timestamp=datetime.now()):
        self.timestamp  = timestamp
        self.component  = int(component)
        self.group      = int(group)
        self.ioDevice   = ioDevice
        self.ioSignal   = ioSignal
        self.type       = type
        self.parameter  = parameter
        
    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)
        

class ControlSchmea(Schema):
    timestamp = fields.DateTime(required=True,metadata={'Beschreibung':"Timestamp of the data in sec as datetime",'example':datetime.now()})
    component = fields.Int(metadata={'Beschreibung':"Id of the component",'example':1})
    group = fields.Int(metadata={'Beschreibung':"Id of the group",'example':1})
    ioDevice = fields.Str(metadata={'Beschreibung':"ioDevice address as string",'example':"Thermostat Raum 1"})
    ioSignal = fields.Str(metadata={'Beschreibung':"ioSignal address as string",'example':"TEMPERATURE"})
    type = fields.Str(metadata={'Beschreibung':"Type of the control action. By controlMsgTypes.",'example':ControlMsgType.newSignal})
    parameter = fields.Dict(metadata={'Beschreibung':"Addional Parameter. Will be stored ind the Database as json."})
    
    @post_load
    def make_control(self, data, **kwargs):
        return Control(**data)