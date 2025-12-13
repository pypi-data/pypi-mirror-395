Access libraries and data definitions for the Buttler project.
For more information ask Oliver Birkholz.

## Versions
### 0.4.0
- Adding vhost Support
### 0.4.3
- Adding sending automatic heartbeats in publisher-function
### 0.4.4
- update sending automatic heartbeats
- handling error
### 0.5.0
- adding group-types
### 0.5.2
- adding signalOptionType and groupOptionType with forwardingMQTT
### 0.5.5
- Solving problems on publishing data without connecting dest
### 0.5.5
- Solving Problems with createConsumer with same topic an different routing_keys

### 0.6.0
- add new signal  types f.ex. system_state or set_temperature.heater

### 0.7.0
- change signal Description and add ext. !!! No backwards compatibility! if Using Schmema for parsing

### 0.7.1
- Bugifx in Signal().__init__(.. ext was missing)
### 0.7.2
- create SignalDirection()
- add convertFrom to SignalOptionType
- add different consumptionSignals to SignalType
### 0.7.3
- add buildingHardware to signalOptionType and groupOptionType
- add agent_building to groupOptionType
### 0.7.4 
- add SignalType co2
- add SignalType consumption*Current
### 0.7.5
- add SignalOptionType SignalOptionType.buildingHardware.energy
### 0.8.0 
- add analytics to GroupOptionType
- create GroupOptionType_labels
### 0.8.1
- bugfix in GroupOptionType_labels
### 0.8.2
- add GroupOptionType_labels to __init__
### 0.8.3
- bugfix in GroupOptionType.agent.building
### 0.8.4
- bugfix automatic destory of connection on BasicBrokerThreadingConnection on class destroy
### 0.8.5
- add heating_sub_system to signal and group
### 0.9.0
- add some internal functions to pikaButler for mor stability
- better loghandling in pikaBulter with the gobale Vars': 
-- logInfoMessages = False
-- logInfoConnection = True
### 0.9.5
- add flow and return values to signal
### 0.9.6
- add storage temperature
### 0.9.7
- add freeze protection temperature
### 0.9.8
- add durable Option to create Consumer
### 0.10.0 buggy
- disable BasicPikaConnection -> Veraltet
- add checkConnectionConsumer to BasicBrokerThreadingConnection
- Überarbeitung stop() der Consumer

### 0.10.1
- fixing some bugs
### 0.10.2
- fixing some bugs
### 0.10.4/5
- add heatcurve eco
### 0.10.6
- add vdd and battery to Signal

### 0.10.9
- add new Signals Descriptions based on CORE-178

### 0.11.0
- add types for the energy-manager

### 0.11.1
- add labelList to SingalCollection

### 0.11.2
- erweiterung SignalType

### 0.11.3
- Anpassung em.unit -> Label und name vertauscht

### 0.11.4
- Anpassung Fehler in Leerzeichen in data_type

### 0.11.5
- Anpassung labels nach Namenskonvention

### 0.11.6
- add lowBattery
### 0.11.7
- add eM: get_period_range
### 0.11.8
- add labels to SignalType
### 0.11.9
- Anpassungen einiger Labels in SignalType
### 0.11.11
- Füge neue SignalType ..Reference Verbrauch hinzu

### 0.11.12
- add SiganlType consumptionRef_.$$$current

### 0.11.13
- add 'w' week to get_period_range in energymanager

### 0.12.0
- Erstellung aller exchanges und que's immer mit der eigenschaft durable. Übergabeparameter für durable bleiben vorhanden sind aber nicht mehr verknüpft
