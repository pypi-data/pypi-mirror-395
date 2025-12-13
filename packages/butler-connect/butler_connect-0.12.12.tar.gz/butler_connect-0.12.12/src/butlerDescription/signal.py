   
from marshmallow import Schema, fields,post_load
from datetime import datetime

class SignalType():
    unDef = 'undef'
    temperature = 'temperature'
    class temperature_():
        heater = 'temperature_heater'
        outside = 'temperature_outside'
        flow = 'temperature_flow'
        returnFlow = 'temperature_return_flow'
        storage = 'temperature_storage'
        freezProtection = 'temperature_freez_protection'
        outsideTemperature = 'temperature_outside'    
        room = 'temperature_room'
        chiller = 'temperature_chiller'
        chillerFlow = 'temperature_chiller_flow'
        chillerReturnFlow = 'temperature_chiller_return_flow'
        chillerStorage = 'temperature_chiller_storage'
        
        
    setTemperature = 'set_temperature'
    class setTemperature_():
        heater = 'set_temperature_heater'
        class heater_():
            comfort = 'set_temperature_heater_comfort'
            boost = 'set_temperature_heater_boost'
            setback = 'set_temperature_heater_setback'
        cooler = 'set_temperature_cooler'
        flow = 'set_temperature_flow'
        returnFlow = 'set_temperature_return_flow'
        storage = 'set_temperature_storage'
        room = 'set_temperature_room'
        roomBoost = 'set_temperature_room_boost'
        conditioning = 'set_temperature_conditioning'
    humidity = 'humidity'
    windowIsOpen = 'window_is_open'
    presence = 'presence'
    motion = 'motion'
    presence_merged = 'presence_merged'
    illumination = 'illumination'
    co2 = 'co2'
    pressure = 'pressure'
    tvoc = 'tvoc'
    o3 = 'o3'
    pm10 = 'pm10'
    pm2_5 = 'pm2_5'
    open = 'open'
    close = 'close'
    actuatorValue = 'actuator_value'
    systemState = 'system_state'
    vdd = 'vdd'
    battery = 'battery'
    lowBattery = 'low_battery'
    class systemState_():
        heater = 'system_state_heater'
        heaterMode = 'system_state_heater_mode'
        tapWater = 'system_state_tap_water'
        tapWaterMode = 'system_state_tap_water_mode'
        cooler = 'system_state_cooler'
        ventilation = 'system_state_ventilation'
        conditioning = 'system_state_conditioning'
        boost = 'system_state_boost'
        pump = 'system_state_pump'
        
    consumption = 'consumption'
    class consumption_():
        gas = 'consumption_gas'
        gasRel = 'consumption_gas_rel'
        gasCurrent = 'consumption_gas_current'
        power = 'consumption_power'
        powerRel = 'consumption_power_rel'
        powerCurrent = 'consumption_power_current'
        water = 'consumption_water'
        waterRel = 'consumption_water_rel'
        waterCurrent = 'consumption_water_current'
        heat = 'consumption_heat'
        heatRel = 'consumption_heat_rel'
        heatCurrent = 'consumption_heat_current'
        cool = 'consumption_cool'
        coolRel = 'consumption_cool_rel'
        coolCurrent = 'consumption_cool_current'   
    consumptionRef = 'consumption_reference'
    class consumptionRef_():
        gas = 'consumption_gas_ref' 
        gasCurrent = 'consumption_gas_ref_current'
        power = 'consumption_power_ref'
        powerCurrent = 'consumption_power_ref_current'
        water = 'consumption_water_ref'
        waterCurrent = 'consumption_water_ref_current'
        heat = 'consumption_heat_ref'
        heatCurrent = 'consumption_heat_ref_current'
        cool = 'consumption_cool_ref' 
        coolCurrent = 'consumption_cool_ref_current'

    class curve_():
        outsideTemperature = 'curve_outside_temperature'
        flowTemperature = 'curve_flow_temperature'
        flowTemperatureEco = 'curve_flow_temperature_eco'
        returnFlowTemperature = 'curve_return_flow_temperature'
        gradient = 'curve_heating_gradient'    
        intercept = 'curve_heating_intercept'    # entspricht dem Offset
        gradientCooling = 'curve_cooling_gradient'
        interceptCooling = 'curve_cooling_intercept'    # entspricht dem Offset
   
    valve = 'valve'
    class valve_():
        flow = 'valve_flow'
        returnFlow = 'valve_return_flow'
        heating = 'valve_heating'
        cooling = 'valve_cooling'
        tap = 'valve_tap'
        ventilation  = 'valve_ventilation'
        conditionoing = 'valve_conditioning'
    pump = 'pump'
    class pump_():
        heating = 'pump_heating'
        cooling = 'pump_cooling'
        tap = 'pump_tap'
        ventilation = 'pump_ventilation'
        conditionoing = 'pump_conditioning'
        input = 'pump_in'
        output = 'pump_out'
        circulation = 'pump_circulation'
    fan = 'fan'
    class fan_():
        ventilation = 'fan_ventilation'
        conditioning = 'fan_conditioning'
        
        
    
    
    flowTemperature = 'flow_temperature'
    returnFlowTemperature = 'return_flow_temperature'
    storageTemperature = 'storage_temperature'
    freezProtectionTemperature = 'freez_protection_temperature'
    outsideTemperature = 'outside_temperature'
    
    # Mapping von Konstanten zu lesbaren Labels
    _label_map = {
        unDef: "Undefiniert",
        temperature: "Temperatur",
        temperature_.outside: "Außentemperatur",
        temperature_.flow: "Vorlauftemperatur",
        temperature_.returnFlow: "Rücklauftemperatur",
        temperature_.storage: "Speichertemperatur",
        temperature_.freezProtection: "Frostschutztemperatur",
        temperature_.room: "Raumtemperatur",
        temperature_.chiller: "Wärmetauscher Temperatur",
        temperature_.chillerFlow: "Wärmetauscher Vorlauftemperatur",
        temperature_.chillerReturnFlow: "Wärmetauscher Rücklauftemperatur",
        temperature_.chillerStorage: "Wärmetauscher Speichertemperatur",
        setTemperature: "Solltemperatur",
        setTemperature_.heater: "Heizung Solltemperatur",
        setTemperature_.heater_.comfort: "Heizung Komforttemperatur",
        setTemperature_.heater_.setback: "Heizung Absenktemperatur",
        setTemperature_.cooler: "Kühlung Solltemperatur",
        setTemperature_.flow: "Vorlauf Solltemperatur",
        setTemperature_.returnFlow: "Rücklauf Solltemperatur",
        setTemperature_.storage: "Speicher Solltemperatur",
        setTemperature_.room: "Raum Solltemperatur",
        setTemperature_.conditioning: "Klimatisierung Solltemperatur ",
        humidity: "Luftfeuchtigkeit",
        windowIsOpen: "Fenster offen",
        presence: "Anwesenheit",
        motion: "Bewegung",
        presence_merged: "Anwesenheit (gemergt)",
        illumination: "Beleuchtungsstärke",
        co2: "CO2",
        pressure: "Druck",
        tvoc: "TVOC",
        o3: "Ozon",
        pm10: "PM10",
        pm2_5: "PM2.5",
        open: "Öffnen",
        close: "Schließen",
        actuatorValue: "Aktorwert",
        systemState: "Systemzustand",
        vdd: "Spannungsversorgung",
        battery: "Batterie",
        lowBattery: "Schwache Batterie",
        systemState_.heater: "Heizungsstatus",
        systemState_.heaterMode: "Heizmodus",
        systemState_.tapWater: "Warmwasserstatus",
        systemState_.tapWaterMode: "Warmwassermodus",
        systemState_.cooler: "Kühlerstatus",
        systemState_.ventilation: "Lüftungsstatus",
        systemState_.conditioning: "Klimaanlage",
        consumption: "Verbrauch",
        consumptionRef: "Verbrauch Referenz",
        consumption_.gas: "Gasverbrauch Zählerstand",
        consumption_.gasRel: "Gasverbrauch relative ",
        consumption_.gasCurrent: "Gasverbrauch aktuell",
        consumptionRef_.gas: "Gasverbrauch Referenz Zählerstand",
        consumptionRef_.gasCurrent: "Gasverbrauch Referenz aktuell",
        consumption_.power: "Stromverbrauch Zählerstand",
        consumption_.powerRel: "Stromverbrauch relevative",
        consumption_.powerCurrent: "Stromverbrauch aktuell",
        consumptionRef_.power: "Stromverbrauch Referenz Zählerstand",
        consumptionRef_.powerCurrent: "Stromverbrauch Referenz aktuell",
        consumption_.water: "Wasserverbrauch Zählerstand",
        consumption_.waterRel: "Wasserverbrauch relativ",
        consumption_.waterCurrent: "Wasserverbrauch aktuell",
        consumptionRef_.water: "Warmwasserverbrauch Referenz Zählerstand",
        consumptionRef_.waterCurrent: "Warmwasserverbrauch Referenz aktuell",
        consumption_.heat: "Wärmeverbrauch Zählerstand",
        consumption_.heatRel: "Wärmeverbrauch relativ",
        consumption_.heatCurrent: "Wärmeverbrauch aktuell",
        consumptionRef_.heat: "Wärmeverbrauch Referenz Zählerstand",
        consumptionRef_.heatCurrent: "Wärmeverbrauch Referenz aktuell",
        consumption_.cool: "Kühlverbrauch Zählerstand",
        consumption_.coolRel: "Kühlverbrauch relativ",
        consumption_.coolCurrent: "Kühlverbrauch aktuell",
        consumptionRef_.cool: "Kühlverbrauch Referenz Zählerstand",
        consumptionRef_.coolCurrent: "Kühlverbrauch Referenz aktuell",
        curve_.outsideTemperature: "Kurve Außentemperatur",
        curve_.flowTemperature: "Kurve Fließtemperatur",
        curve_.flowTemperatureEco: "Kurve Fließtemperatur (Eco)",
        curve_.returnFlowTemperature: "Kurve Rücklauftemperatur",
        valve: "Ventil",
        valve_.flow: "Ventil Fluss",
        valve_.returnFlow: "Ventil Rückfluss",
        valve_.heating: "Ventil Heizung",
        valve_.cooling: "Ventil Kühlung",
        valve_.tap: "Ventil Wasserhahn",
        valve_.ventilation: "Ventil Lüftung",
        valve_.conditionoing: "Ventil Klimatisierung",
        pump: "Pumpe",
        pump_.heating: "Heizung Pumpe",
        pump_.cooling: "Kühlung Pumpe",
        pump_.tap: "Wasserhahn Pumpe",
        pump_.ventilation: "Lüftung Pumpe",
        pump_.conditionoing: "Klimatisierung Pumpe",
        pump_.input: "Eingang Pumpe",
        pump_.output: "Ausgang Pumpe",
        pump_.circulation: "Zirkulation Pumpe",
        fan: "Lüfter",
        fan_.ventilation: "Lüftung Lüfter",
        fan_.conditioning: "Klimatisierung Lüfter",
    }
    
    @classmethod
    def get_label(cls, signal_type):
        """Gibt das lesbare Label für einen gegebenen Signaltyp zurück."""
        return cls._label_map.get(signal_type, "Unbekannt")
    
    @classmethod
    def get_label_list(cls, key_name="name", key_label="label"):
        """
        Gibt eine Liste von Dictionaries mit den gewählten Key-Namen zurück.
        Standardmäßig werden die Keys 'name' und 'label' verwendet.
        """
        return [
            {key_name: key, key_label: label}
            for key, label in cls._label_map.items()
        ]

class SignalOptionType():
    unDef = 'undef'
    forwardingMQTT = 'forwarding_mqtt'
    convertFrom    = 'convert_from'
    class buildingHardware():
        unDef = 'undef'
        heating = 'building_hardware_heating'
        heating_sub_system = 'building_hardware_heating_sub_system'
        cooling = 'building_hardware_cooling'
        ventilation = 'building_hardware_ventilation'
        lighting = 'building_hardware_lighting'
        energy = 'building_hardware_energy'
    
class SignalDirection():
    input = 'input'
    output = 'output'

def singnalDirection2Flags(direction):
    isInput = False
    isOutput = False
    if direction == SignalDirection.input:
        isInput = True
    elif direction == SignalDirection.output:
        isOutput = True
    return isInput,isOutput
    
class Signal():
    def __init__(self, type, component=None, group=None, ioDevice=None, ioSignal=None, parameter=None, timestamp=None, value=None, valueStr=None, ext=None):
        self.timestamp  = timestamp if timestamp is not None else datetime.now()
        self.component  = int(component) if component is not None else 0
        self.group      = int(group) if group is not None else 0
        self.ioDevice   = ioDevice if ioDevice is not None else ""
        self.ioSignal   = ioSignal if ioSignal is not None else ""
        self.type       = type if type is not None else self.ioSignal  
        self.value      = float(value) if value is not None else 0.0
        self.valueStr   = str(valueStr) if valueStr is not None else ""
        self.ext        = dict(ext) if ext is not None else {}     
    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)
    def __str__(self) -> str:
        return f'component={self.component}, group={self.group}, ioDevice={self.ioDevice}, ioSignal={self.ioSignal}, type={self.type}, value={self.value}, valueStr={self.valueStr}, timestamp={self.timestamp}, ext={self.ext}'        

class SignalSchmea(Schema):
    timestamp   = fields.DateTime(required=True)
    component   = fields.Int()
    group       = fields.Int()
    ioDevice    = fields.Str()
    ioSignal    = fields.Str()
    type        = fields.Str()
    value       = fields.Float()
    valueStr    = fields.Str()
    ext         = fields.Dict()
    
    @post_load
    def make_control(self, data, **kwargs):
        return Signal(**data)