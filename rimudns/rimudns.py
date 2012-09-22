# See https://rimuhosting.com/dns/dyndns.jsp for more information
#  or https://zonomi.com/app/dns/dyndns.jsp
# Tests
#
# from rimudns import RimuDNS
#
# api_key = 'GETYOURAPIKEYFROMTHECONTROLPANEL'
# dns = DNS(api_key)
#
# dns.change_ip('192.168.59.133', '192.168.59.132')
# if dns.set_record('aa1.example.com', '94.162.59.133'): 
#     print 'updated: %s records' % dns.record_count
#
# dns.list_zones()
#
# dns.create_zone('test.example.com') # should work the first time
# dns.create_zone('test.example.com') # should fail with 500 error
#
# dns.delete_zone('test.example.com') # should work the first time
# dns.delete_zone('test.example.com') # should fail with 500 error
#
# dns.list_records('example.com')
# dns.list_records('example.com', all_records=True)
#
# dns.create_zone('test.example.com') # should work the first time
# dns.set_record('test.example.com', '127.0.0.1')
# dns.set_record('mail.test.example.com', 'test.example.com', 'CNAME')
#
# updates_list = [
#            {
#                'action': 'SET', # or 'DELETE',
#                'host': 'foo.test.example.com,bar.test.deeb.com', # or ['foo.com', 'bar.com],
#                'value': '192.168.1.1',
#                'type': 'A' # or 'MX' or 'CNAME' or 'TXT', optional default A, 
#                #'prio': for MX records, number default 0,
#                #'ttl': number, optional default 3600,
#            },
#            { 
#                'action': 'DELETE',
#                'host': ['foo.test.example.com', 'bar.test.example.com'],
#                'value': '192.168.1.1',
#                'type': 'CNAME', # or 'TXT', optional default A, 
#                #'prio': for MX records, number default 0,
#                #'ttl': number, optional default 3600,
#            },      
#        ]
# dns.multiple_actions(updates_list)
# dns.delete_zone('test.example.com') # should work the first time

import urllib2
from lxml import objectify
from zonehandle import ZoneHandle
import consts

class RimuDNS:
    
    def __init__(self, apikey):
        self.apikey = apikey
        self.debug = False
        self.base_url = 'https://rimuhosting.com' 
        
    def use_rimuhosting(self):
        self.base_url = consts.rimu_base_url
        
    def use_zonomi(self):
        self.base_url = consts.zonomi_base_url
        
    def change_ip(self, old_ip, new_ip):
        '''Change an IP across all your zones.
        https://rimuhosting.com/dns/ipchange.jsp?old_ip=0.0.0.0&new_ip=0.0.0.0&api_key=apikeyvaluehere
        
        '''
        url = '%s/dns/ipchange.jsp?old_ip=%s&new_ip=%s&api_key=%s' % (self.base_url, old_ip, new_ip, self.apikey)
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                self.record_count = root.record_count
                return self.record_count
        except Exception, e:
            if self.debug: print e.read()
            raise e
        
    
    def list_zones(self):
        '''Return a list of zones on your account
        https://rimuhosting.com/dns/dyndns.jsp?action=QUERYZONES&api_key=apikeyvaluehere 
        
        '''
        zones = []
        url = '%s/dns/dyndns.jsp?action=QUERYZONES&api_key=%s' % (self.base_url, self.apikey)
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                for zone in root.actions.action.iterchildren():
                    zoneinfo = {}
                    for item in zone.items():
                        zoneinfo[item[0]]= item[1]
                    zones.append(zoneinfo) 
        except Exception, e:
            if self.debug: print e.read()
            raise e
        return zones
        
    def create_zone(self, zone_name):
        '''Setup a new DNS zone
        https://rimuhosting.com/dns/addzone.jsp?name=example.com&api_key=apikeyvaluehere

        '''
        url = '%s/dns/addzone.jsp?name=%s&api_key=%s' % (self.base_url, zone_name, self.apikey)
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                return zone_name
        except urllib2.HTTPError, e:
            raise e
            
    def delete_zone(self, zone_name):
        '''Delete a DNS zone.
        https://rimuhosting.com/dns/dyndns.jsp?action=DELETEZONE&name=example.com&api_key=apikeyvaluehere

        '''
        url = '%s/dns/dyndns.jsp?action=DELETEZONE&name=%s&api_key=%s' % (self.base_url, zone_name, self.apikey)
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                return zone_name
        except Exception, e:
            raise e
            
    def convert_to_slave(self, zone_name, master_ip): 
        '''Convert a zone to a slave zone with the specified master name server IP address.
         https://rimuhosting.com/dns/converttosecondary.jsp?name=example.com&master=0.0.0.0&api_key=apikeyvaluehere

        '''
        url = '%s/dns/converttosecondary.jsp?name=%s&master=%s&api_key=%s' % (self.base_url, zone_name, master_ip, self.apikey)
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                return zone_name
        except urllib2.HTTPError, e:
            raise e
            
    def convert_to_regular(self, zone_name): 
        '''Convert a zone from a slave zone back to a 'regular' zone.
         https://rimuhosting.com/dns/converttomaster.jsp?name=example.com&api_key=apikeyvaluehere

        '''
        url = '%s/dns/converttosecondary.jsp?name=%s&master=%s&api_key=%s' % (self.base_url, zone_name, self.apikey)
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                return zone_name
        except urllib2.HTTPError, e:
            raise e
            
    def list_records(self, zone_name, all_records=False):
        '''Retrieve a list of records with the specified name.
        https://rimuhosting.com/dns/dyndns.jsp?action=QUERY&name=example.com&api_key=apikeyvaluehere

        '''
        if all_records: zone_name = '**.%s' % zone_name
        url = '%s/dns/dyndns.jsp?action=QUERY&name=%s&api_key=%s' % (self.base_url, zone_name, self.apikey)
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            records = {}
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                for record in root.actions.action.iterchildren():
                    record_type = record.attrib['type']
                    if not records.has_key(record_type): records[record_type] = []
                    records[record_type].append(record.attrib)
                return records
        except Exception, e:
            raise e
            

            
    def set_record(self, host, value, record_type='A', prio=None, ttl=None):
        '''Set an IP Address (A) record
        https://rimuhosting.com/dns/dyndns.jsp?action=SET&name=example.com&value=10.0.0.1&type=A&api_key=apikeyvaluehere

        '''
        url = '%s/dns/dyndns.jsp?api_key=%s&action=SET' % (self.base_url, self.apikey)
        url += '&name=%s' % host
        url += '&value=%s' % value
        url += '&type=%s' % record_type
        if prio and record_type=='MX': 
            url += '&prio=%s' % prio
        if ttl: 
            url += '&ttl=%s' % ttl
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                self.result_counts = root.result_counts.attrib
                return self.result_counts
        except Exception, e:
            if self.debug: print e.read()
            raise e

    def delete_record(self, host, value, record_type='A'):
        '''Delete an IP Address (A) record
        https://rimuhosting.com/dns/dyndns.jsp?action=DELETE&name=example.com&type=A&api_key=apikeyvaluehere

        '''
        url = '%s/dns/dyndns.jsp?api_key=%s&action=DELETE' % (self.base_url, self.apikey) 
        url += '&name=%s' % host
        url += '&value=%s' % value
        url += '&type=%s' % record_type
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                self.result_counts = root.result_counts.attrib
                return self.result_counts
        except Exception, e:
            if self.debug: print e.read()
            raise e
            
            
           
    def multiple_actions(self, updates_list):
        '''Multiple actions: set two records to the same IP and delete the bar.example.com IP Address (A) record. 
        https://rimuhosting.com/dns/dyndns.jsp?action[1]=SET&name[1]=example.com,bar.example.com&value[1]=10.0.0.1&action[2]=DELETE&host[2]=bar.example.com&api_key=apikeyvaluehere
        
        updates_list = [
            {
                'action': 'SET' or 'DELETE',
                'host': 'foo.com,bar.com' or ['foo.com', 'bar.com],
                'value': '192.168.1.1',
                'type': 'A' or 'MX' or 'CNAME' or 'TXT', optional default A, 
                'prio': for MX records, number default 0,
                'ttl': number, optional default 3600,
            }        
        ]
        
        '''
        url = '%s/dns/dyndns.jsp?api_key=%s' % (self.base_url, self.apikey)
        for index, update in enumerate(updates_list):
            for key,val in update.iteritems():
                if key=='host' and isinstance(val, list):
                    val = ','.join([str(i) for i in val])
                url_part = '&%s[%s]=%s' % (key, index, val)
                if self.debug: print url_part
                url += url_part
            if self.debug: print url 
        req = urllib2.Request(url, headers={'User-Agent': consts.user_agent})
        try:
            response = urllib2.urlopen(req).read()
            if self.debug: print response
            root = objectify.fromstring(response)
            if str(root.is_ok).startswith('OK'):
                self.result_counts = root.result_counts.attrib
                return self.result_counts
        except urllib2.HTTPError, e:
            if self.debug: "Error: %s" % e.read()
            raise e
        
    def to_file(self, zone_name, file, records_dict=None):
        '''Export zone to file
        
        '''
        try:
            if not records_dict:
                records_dict = self.list_records(zone_name, True)
            if records_dict:
                zh = ZoneHandle(zone_name)
                zh.from_records_dict(records_dict)
                zh.to_file(file)
        except Exception, e:
            if self.debug: print e
            raise e
            
    def import_zone(self, zone_name, method, param=None, dryrun=False):
        '''Import zone 
        methods are AXFR, FILE, TEXT, DICT and GUESS
        
        '''
        zh = ZoneHandle(zone_name)
        try:
            if method==ZoneHandle.IMPORT_AXFR:
                zh.from_axfr(param)
            elif method==ZoneHandle.IMPORT_FILE: 
                zh.from_file(param)
            elif method==ZoneHandle.IMPORT_TEXT:
                zh.from_text(param)
            elif method==ZoneHandle.IMPORT_DICT:
                zh.from_records_dict(param)
            elif method==ZoneHandle.IMPORT_GUESS:
                zh.from_guessing()
                
        except Exception, e:
                if self.debug: print e
                raise e
            
        records_dict = zh.to_records_dict()
        if not dryrun:
            created = self.create_zone(zone_name)
            for record_type, records in records:
                if record_type=='SOA': continue
                for record in records:
                    try:
                        self.set_record(record['name'], record['content'], record_type, record['prio'], record['ttl'])
                    except Exception, e:
                        if self.debug: print e
                        raise e
                    
        return records_dict
            
            
            
            
