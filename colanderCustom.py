from colander import SchemaType, Invalid, null
import ipaddress
from loguru import logger


class IpaddressColander(SchemaType):
    def serialize(self, node, appstruct):
        if appstruct is null:
            return null
        try:
            ipaddrObj=ipaddress.ip_address(appstruct)                        
        except:
            raise Invalid(node, '%r is not a valid IP Address string' % appstruct)        
        return appstruct 
    
    @logger.catch
    def deserialize(self, node, cstruct):
        if cstruct is null:
            return null
        try:
            ipaddrObj=ipaddress.ip_address(cstruct)                        
        except:
            raise Invalid(node, '%r is not a valid IP Address string' % cstruct)     
        value = cstruct.lower()        
        return cstruct