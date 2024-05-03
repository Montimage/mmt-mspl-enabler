__author__ = "Gustavo Jodar Soares"
__copyright__ = "Copyright 2023, CERBERUS"
__credits__ = ["Antonio Skarmeta", "Alejandro Molina Zarca","Gustavo jodar Soares","Huu-Nghia Nguyen" "Juan Francisco Martínez Gil", "Emilio García de la Calera Molina"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Gustavo Jodar Soares"
__email__ = "gustavo.jodar@um.es"
__status__ = "Development"

import xml.etree.ElementTree as ET
import sys

MMT_PROBE_CONF_PATH = "mmt-probe.conf"

#Class that reads the .xml file from the MSPL and gets the relavant data for mmt-security
class Mspl:
 
    def parsepacketfilter(self, config_rule, namespace=None):
        if namespace == None:
            namespace = 'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd'
        rules = []
        #packetfiltercondition   
        packet_filter_condition = config_rule.find(".//{%s}packetFilterCondition" % namespace)
        if packet_filter_condition is not None:
            src_address = packet_filter_condition.find(".//{%s}SourceAddress" % namespace)
            dst_address = packet_filter_condition.find(".//{%s}DestinationAddress" % namespace)
            dst_port = packet_filter_condition.find(".//{%s}DestinationPort" % namespace)
            protocol_type = packet_filter_condition.find(".//{%s}ProtocolType" % namespace)
            payload = packet_filter_condition.find(".//{%s}Payload" % namespace)
            size = packet_filter_condition.find(".//{%s}Size" % namespace)
            direction = packet_filter_condition.find(".//{%s}direction" % namespace)

        rule_content_aux = {"src_address": src_address.text if src_address is not None else None,
                        "dst_address": dst_address.text if dst_address is not None else None,
                        "dst_port": dst_port.text if dst_port is not None else None,
                        "protocol_type": protocol_type.text if protocol_type is not None else None,
                        "payload": payload.text if payload is not None else None,
                        "size": size.text if size is not None else None,
                        "direction": direction.text if direction is not None else None
                        }
        rule_content = {}
        for key in rule_content_aux:
            if(rule_content_aux[key] != None):
                rule_content[key] = rule_content_aux[key] 
        return rule_content
    
    def is_monitoring(self, configurationRule, namespace=None):
        if namespace == None:
            namespace = 'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd'
        
        action_type = configurationRule.find(".//{%s}monitoringActionType" % namespace)
        return action_type != None

    # return the configuration from the mspl source
    def getConfig(self, mspl_source):
        
        rules = []
        namespace = 'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd'
        mspl_source_object = ET.fromstring(mspl_source)
        
        for config_rule in mspl_source_object.findall(".//{%s}configurationRule" % namespace):
            # it has to generate a rule here
            if self.is_monitoring(config_rule, namespace):
                action_type = config_rule.find(".//{%s}monitoringActionType" % namespace)
                description = config_rule.find(".//{%s}Description" % namespace)
                name = config_rule.find(".//{%s}Name" % namespace)        
                monitoring_configuration_condition = config_rule.find(".//{%s}monitoringConfigurationCondition" % namespace)
                
                if monitoring_configuration_condition is not None:
                    
                    rules_monitoring = self.parsepacketfilter(config_rule, namespace)
                    if len(rules_monitoring) > 0:
                        rules.append({"packetFilterCondition":rules_monitoring})
        
                for rule in rules:
                    if(action_type != None):
                        rule["configuration"] = action_type.text
                    if(description != None):
                        rule["description"] = description.text
                    if(name != None):
                        rule["name"] = name.text
        return rules

#Adapts mmt-probe.conf to include a new rule
class ConfigAdapter:

    def modify_config_file(self, file_path, config_changes):
        with open(MMT_PROBE_CONF_PATH, 'r') as f:
            lines = f.readlines()

        for key in config_changes.keys():
            for i in range(0, len(lines)):
                if key in lines[i]:
                    #Modify the value
                    lines[i] = f"    {key}    = {config_changes[key]}\n"
                    print("Aplying change -> ", lines[i])
                    break
            
        with open("new-mmt--probe.conf", 'w') as f:
            f.writelines(lines)



if __name__ == "__main__":
    xml_file = sys.argv[1] 
    
    print("Reading mspl file...")
    
    xml_source = open(xml_file).read()

    msplHelper = Mspl()

    rules = msplHelper.getConfig(xml_source)

    configAdapter = ConfigAdapter()

    # Example usage:
    config_changes = {
        'rules-mask': "\"114\"",
    }

    configAdapter.modify_config_file('mmt-probe.conf', config_changes)
