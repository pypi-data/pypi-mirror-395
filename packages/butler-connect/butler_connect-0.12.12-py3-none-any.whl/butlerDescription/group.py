class GroupType():
    unDef   = 'undef'
    groupClimate     = 'group_climate'
    groupAnalytics   = 'group_analytics'
    
class GroupOptionType():
    unDef = 'undef'
    forwardingMQTT = 'forwarding_mqtt'
    class buildingHardware():
        unDef = 'undef'
        heating = 'building_hardware_heating'
        heating_sub_system = 'building_hardware_heating_sub_system'
        cooling = 'building_hardware_cooling'
        ventilation = 'building_hardware_ventilation'
        lighting = 'building_hardware_lighting'
        energy = 'building_hardware_energy'
    
    class agent():
        building = 'agent_building'
    class analytics():
        occupancy = 'analytics_occupancy'
        
class GroupOptionType_info():   
    labels = {
        GroupOptionType.unDef : "undef",    
        GroupOptionType.forwardingMQTT : "forwarding mqtt",
        
        GroupOptionType.buildingHardware.heating : "heating",
        GroupOptionType.buildingHardware.heating_sub_system : "heating sub system",
        GroupOptionType.buildingHardware.cooling : "cooling",
        GroupOptionType.buildingHardware.ventilation : "ventilation",
        GroupOptionType.buildingHardware.lighting : "lighting",
        GroupOptionType.buildingHardware : "building hardware",

        GroupOptionType.agent.building : "building agent",
        
        GroupOptionType.analytics.occupancy : "group occupancy",
    }