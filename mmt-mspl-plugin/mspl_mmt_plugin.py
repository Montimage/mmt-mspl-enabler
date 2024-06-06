__author__ = "Gustavo Jodar Soares"
__copyright__ = "Copyright 2023, CERBERUS"
__credits__ = ["Antonio Skarmeta", "Alejandro Molina Zarca","Gustavo jodar Soares","Huu-Nghia Nguyen", "Juan Francisco Martínez Gil", "Emilio García de la Calera Molina"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Gustavo Jodar Soares"
__email__ = "gustavo.jodar@um.es"
__status__ = "Development"

import xml.etree.ElementTree as ET
import sys

MMT_PROBE_CONF_PATH = "mmt-confs/"
NEW_RULE_NUMBER = "114"

#Class that reads the .xml file from the MSPL and gets the relavant data for mmt-security
class Mspl:
    def parsepacketfilter(self, config_rule, namespace=None):
        if namespace is None:
            namespace = 'http://modeliosoft/xsddesigner/a22bd60b-ee3d-425c-8618-beb6a854051a/ITResource.xsd'
        
        rules = []
        # packetfiltercondition
        packet_filter_condition = config_rule.find(".//{%s}packetFilterCondition" % namespace)
        if packet_filter_condition is not None:
            src_address = packet_filter_condition.find(".//{%s}SourceAddress" % namespace)
            dst_address = packet_filter_condition.find(".//{%s}DestinationAddress" % namespace)
            dst_port = packet_filter_condition.find(".//{%s}DestinationPort" % namespace)
            protocol_type = packet_filter_condition.find(".//{%s}ProtocolType" % namespace)
            packet_size = packet_filter_condition.find(".//{%s}packetSize" % namespace)
            size_operator = packet_size.find(".//{%s}operator" % namespace) if packet_size is not None else None
            size_bytes = packet_size.find(".//{%s}bytes" % namespace) if packet_size is not None else None
            direction = packet_filter_condition.find(".//{%s}direction" % namespace)
            icmp_condition = packet_filter_condition.find(".//{%s}ICMPCondition" % namespace)
            tcp_condition = packet_filter_condition.find(".//{%s}TCPCondition" % namespace)
            syn_flag = None
            if tcp_condition is not None:
                syn_flag = tcp_condition.find(".//{%s}SYNFlag" % namespace)

        rule_content_aux = {
            "src_address": src_address.text if src_address is not None else None,
            "dst_address": dst_address.text if dst_address is not None else None,
            "dst_port": dst_port.text if dst_port is not None else None,
            "protocol_type": protocol_type.text if protocol_type is not None else None,
            "size_operator": size_operator.text if size_operator is not None else None,
            "size_bytes": size_bytes.text if size_bytes is not None else None,
            "direction": direction.text if direction is not None else None,
            "syn_flag": syn_flag.text if syn_flag is not None else None,
            "icmp_type": icmp_condition.find(".//{%s}Type" % namespace).text if icmp_condition is not None else None
        }
        
        rule_content = {key: value for key, value in rule_content_aux.items() if value is not None}
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
        with open(MMT_PROBE_CONF_PATH + "mmt-probe.conf", 'r') as f:
            lines = f.readlines()

        for key in config_changes.keys():
            for i in range(0, len(lines)):
                if key in lines[i]:
                    #Modify the value
                    lines[i] = f"    {key}    = {config_changes[key]}\n"
                    break
            
        with open(MMT_PROBE_CONF_PATH + "new-mmt--probe.conf", 'w') as f:
            f.writelines(lines)
        print("  -> New mmt-probe.conf file created...")

class RuleMaker:
    def create_rule(self, rules):
        for i, rule in enumerate(rules):
            packet_filter_condition = rule["packetFilterCondition"]
            
            # Handling Ping of Death
            if packet_filter_condition["protocol_type"] == '1' and packet_filter_condition.get("size_operator") == 'greater':
                size = packet_filter_condition["size_bytes"]
                changes = ["2", f"((ip.src != ip.dst) && (meta.packet_len > {size}))"]
                
                # Loading rule
                rule_source_object = ET.parse("rules/51.ping_of_death.xml")
                root = rule_source_object.getroot()
                property_element = root.find(".//property")
                property_element.set("description", "Ping of death attack - size > " + size)

                # Finding the event element with the specified ID
                event_element = property_element.find(f"./event[@event_id='{changes[0]}']")

                # Changing size of packet to alert
                event_element.set("boolean_expression", changes[1])

                # Write the modified XML as a new rule
                rule_source_object.write("rules/new_rule.xml")
            
            # Handling TCP SYN Scan
            #about nmap snyc 
            elif packet_filter_condition["protocol_type"].lower() == 'tcp' and packet_filter_condition.get("syn_flag", "").lower() == 'true':
                # Loading rule
                rule_source_object = ET.parse("rules/40.TCP_SYN_scan.xml")
                # Write the modified XML as a new rule
                rule_source_object.write("rules/new_rule.xml")

            
if __name__ == "__main__":
    xml_file = sys.argv[1] 
    
    print("  -> Reading mspl file...")
    xml_source = open(xml_file).read()

    msplHelper = Mspl()
    configAdapter = ConfigAdapter()
    ruleMaker = RuleMaker()

    rules = msplHelper.getConfig(xml_source)

    print(f"  -> Obtained info: {rules}")
    ruleMaker.create_rule(rules)

    # Example usage:
    config_changes = {
        'rules-mask': f"\"(1:{NEW_RULE_NUMBER})\""
    }   

    configAdapter.modify_config_file('mmt-probe.conf', config_changes)
