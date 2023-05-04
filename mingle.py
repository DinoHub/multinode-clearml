import ipaddress
import colander
import json
from colanderCustom import IpaddressColander
from loguru import logger
import multicast_expert
import socket
import click

# logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")
multicastaddr='239.1.2.3'

class Mingledata(colander.MappingSchema):
    sessionName=colander.SchemaNode(colander.String())
    sourceIP=colander.SchemaNode(IpaddressColander())

class Mingle:
    def __init__(self, isRank0=False, sessionId=None, setup=False):      
        srcipaddress=self.getMyIP()  
        json_dict = {
        'sessionName': sessionId,
        'sourceIP': srcipaddress,        
         }
        api_json_request_simulated = json.dumps(json_dict)
        dict_deserialized = json.loads(api_json_request_simulated)
        self.MingleData=Mingledata()
        self.deserialisedMingleData=self.MingleData.deserialize(dict_deserialized)
        logger.info("Loaded Session ID: {0}\tLoaded Source IP: {1}".format(self.deserialisedMingleData['sessionName'], self.deserialisedMingleData['sourceIP']))
        if (setup):
            self.setup(self.deserialisedMingleData['sourceIP'], self.deserialisedMingleData['sessionName'], isRank0)

    def getMyIP(self):
            interfaces=multicast_expert.get_interface_ips(include_ipv4=True, include_ipv6=False)            
            self.interfaceip=interfaces[-1]
            logger.info(interfaces)
            return self.interfaceip

        
    def setup(self,srcipaddress=None, sessionId=None, isRank0=False):
        
        if (isRank0):
            logger.info("Setting up as Rank 0, sending out multicast about myself")    
            self.serialisedMingleData=json.dumps(self.MingleData.serialize(self.deserialisedMingleData)).encode('utf-8')
            logger.info("Sending out following json to multicast:{0} via {1} --> {2}".format(multicastaddr, self.interfaceip, self.serialisedMingleData))

            with multicast_expert.McastTxSocket(socket.AF_INET, mcast_ips=[multicastaddr], iface_ip=self.interfaceip) as mcast_tx_sock:
                mcast_tx_sock.sendto(self.serialisedMingleData, (multicastaddr, 12345))
        else:
            logger.info("Setting up as Rank N, waiting to receive multicast from RANK 0")    
            with multicast_expert.McastRxSocket(socket.AF_INET, mcast_ips=[multicastaddr], port=12345, iface_ip=self.interfaceip) as mcast_rx_sock:
                bytes, src_address = mcast_rx_sock.recvfrom()
                logger.info("Received from Rank0 from {0}! Info as follows: {1}".format(src_address, bytes))                
        
@click.command()
@click.option('--sessionid', required=True, help='A string that all your RANKs use to tell each other they are in same DDP session')
@click.option('--rank0/--rankN', required=True, help='Indicate if this is for Rank 0 or Rank N')
def runme(sessionid,rank0):
    mingle=Mingle(isRank0=rank0, sessionId=sessionid, setup=True)


if __name__ == "__main__":
    runme()
    


