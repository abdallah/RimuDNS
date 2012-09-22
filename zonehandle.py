import dns.zone
import dns.resolver 
import dns.name
from dns.rdataclass import *
from dns.rdatatype import *
import dns.rdtypes.ANY
import dns.rdtypes.ANY.CNAME
import dns.rdtypes.ANY.SOA
import dns.rdtypes.ANY.TXT
import dns.rdtypes.ANY.NS
import dns.rdtypes.ANY.MX
import dns.rdtypes.IN.A
import dns.rdtypes.IN
import re

class ZoneHandle:
    IMPORT_AXFR = 1
    IMPORT_FILE = 2
    IMPORT_TEXT = 3
    IMPORT_DICT = 4
    IMPORT_GUESS = 5
    
    def __init__(self, domain_name):
        self.dns_name = dns.name.Name((domain_name,))
        self.domain_name = domain_name
        self.zone = dns.zone.Zone(self.dns_name)
        self.possible_subdomains = ['www', 'www1', 'www2', 
                                    'ftp', 
                                    'webmail', 'mail', 'mail1', 'mail2' 'smtp', 'imap', 'pop', 
                                    'ns1', 'ns2', 'ns3', 'ns4']
        self.dns_server = 'ns1.rimuhosting.com'
        self.debug = False
        
    def from_axfr(self, dns_server):
        try:
            self.zone = dns.zone.from_xfr(dns.query.xfr(dns_server, self.domain_name))
            return self.zone
        except Exception, e:
            if self.debug: print e
            raise e

    def from_file(self, file):
        try:
            self.zone = dns.zone.from_file(file, self.domain_name)
            return self.zone
        except Exception, e:
            if self.debug: print e
            raise e
        
    def from_text(self, text):
        try:
            self.zone = dns.zone.from_text(text, self.domain_name)
            return self.zone
        except Exception, e:
            if self.debug: print e
            raise e
    
    def from_records_dict(self, records_dict):
        try:
            zone_text = ''
            for rtype in records_dict.keys():
                records = records_dict[rtype]
                if rtype=='SOA' and len(records)>0: 
                    soa_rec = records[0]
                    mname, rname, serial, refresh, retry, expire, minimum = soa_rec['content'].split(' ')
                    if self.domain_name!=soa_rec['name']:
                        if self.debug: print 'Domain name does not match'
                        return False
                    zone_text += '\n; SOA Record\n'
                    zone_text += '$ORIGIN %s.\n' % self.domain_name
                    zone_text += '$TTL 1h\n'
                    zone_text += '%s. IN SOA %s %s (\n' % (self.domain_name, mname, rname)
                    zone_text += '  %s ; serial number of this zone file\n' % serial
                    zone_text += '  %s ; slave refresh\n' % refresh
                    zone_text += '  %s ; slave retry time in case of a problem\n' % retry
                    zone_text += '  %s ; slave expiration time\n' % expire
                    zone_text += '  %s ; maximum caching time in case of failed lookups\n' % minimum
                    zone_text += ')\n'
                if rtype=='A' and len(records)>0:
                    for record in records:
                        ttl = re.findall('\d+', record['ttl'])[0]
                        zone_text += '%s  %s  IN  A %s\n' % (record['name'], ttl, record['content'])
                if rtype=='MX' and len(records)>0:
                    for record in records:
                        ttl = re.findall('\d+', record['ttl'])[0]
                        if record['name']==self.domain_name:
                            record['name'] = '@'
                        zone_text += '%s  %s  IN  MX  %s  %s\n' % (record['name'], ttl, record['prio'], record['content'])
                if rtype=='NS' and len(records)>0:
                    for record in records:
                        ttl = re.findall('\d+', record['ttl'])[0]
                        zone_text += '@  %s  IN  NS %s\n' % (ttl, record['content'])
                if rtype=='TXT' and len(records)>0:
                    for record in records:
                        ttl = re.findall('\d+', record['ttl'])[0]
                        zone_text += '%s  %s  IN  TXT "%s"\n' % (record['name'], ttl, record['content'])
                if rtype=='CNAME' and len(records)>0:
                    for record in records:
                        ttl = re.findall('\d+', record['ttl'])[0]
                        if record['content']==self.domain_name:
                            record['content'] = '@'
                        zone_text += '%s  %s  IN  CNAME  %s\n' % (record['name'], ttl, record['content'])
                
            print zone_text
            self.zone = dns.zone.from_text(zone_text)
            return self.zone

        except Exception, e:
            print e
            if self.debug: print e
            raise e
        
    def to_records_dict(self):
        records_dict = { 'SOA': [], 'A': [], 'MX': [], 'NS': [], 'TXT': [], 'CNAME': [] }
        try:
            zone = self.zone
            for name, node in zone.nodes.items():
                prio = 0
                if self.debug: print 'name: ', name
                rdatasets = node.rdatasets
                for rdataset in rdatasets:
                    if self.debug:
                        print "--- BEGIN RDATASET ---"
                        print "rdataset string representation:", rdataset
                        print "rdataset rdclass:", rdataset.rdclass
                        print "rdataset rdtype:", rdataset.rdtype
                        print "rdataset ttl:", rdataset.ttl
                        print "rdataset has following rdata:"
                    for rdata in rdataset:
                        if rdataset.rdtype == SOA:
                            if self.debug: print 'SOA, getting info ...'
                            rdtype = 'SOA'
                            content = ' '.join((
                                                str(rdata.mname), str(rdata.rname), 
                                                str(rdata.serial), 
                                                str(rdata.refresh), 
                                                str(rdata.retry), 
                                                str(rdata.expire), 
                                                str(rdata.minimum)
                                                ))
                            if self.debug: print 'SOA, contents: ', content
                        if rdataset.rdtype == A:
                            rdtype = 'A'
                            content = rdata.address
                        if rdataset.rdtype == MX:
                            rdtype = 'MX'
                            content = str(rdata.exchange)
                            prio = rdata.preference
                        if rdataset.rdtype == NS:
                            rdtype = 'NS'
                            content = str(rdata.target)
                        if rdataset.rdtype == TXT:
                            rdtype = 'TXT'
                            content = rdata.strings
                        if rdataset.rdtype == CNAME:
                            rdtype = 'CNAME'
                            content = str(rdata.target)
                            
                        record = {'content': content,  'type': rdtype, 'name': str(name), 'prio': prio, 'ttl': rdataset.ttl}
                        records_dict[rdtype].append(record)
                
            return records_dict
        except Exception, e:
            if self.debug: print e
            raise e

    def from_guessing(self):
        if not self._guess_soa(): 
            raise Exception('Unable to guess SOA!')
        if not self._guess_ns():
            if self.debug: raise Exception( 'Unable to guess NS records')
        if not self._guess_mx():
            if self.debug: raise Exception('Unable to guess MX records')
        if not self._guess_a():
            if self.debug: raise Exception('Unable to guess A records')
        if not self._guess_cname():
            if self.debug: raise Exception('Unable to guess CNAME records')
        if not self._guess_txt():
            if self.debug: raise Exception('Unable to guess TXT records')
        
        if self.debug: print self.zone.items()
        return self.zone
            
    def _guess_soa(self):
        try:
            soa_answer = dns.resolver.query(self.domain_name, 'SOA')
            soa_rr = soa_answer.rrset[0]
            rd_set = self.zone.find_rdataset(self.domain_name, rdtype=SOA , create=True)
            rdata = dns.rdtypes.ANY.SOA.SOA(soa_rr.rdclass, 
                                            soa_rr.rdtype,
                                            soa_rr.mname, 
                                            soa_rr.rname, 
                                            soa_rr.serial, 
                                            soa_rr.refresh, 
                                            soa_rr.retry,
                                            soa_rr.expire, 
                                            soa_rr.minimum)
            rd_set.add(rdata)
            return True
        except Exception, e:
            if self.debug: print e
            return False

    def _guess_ns(self):
        try: 
            ns_answer = dns.resolver.query(self.domain_name, 'NS')
            for ns_record in ns_answer.rrset:
                rd_set = self.zone.find_rdataset(self.domain_name, rdtype=NS, create=True)
                rdata = dns.rdtypes.ANY.NS.NS(IN, NS, ns_record.target)
                rd_set.add(rdata)
            return True
        except Exception, e:
            if self.debug: print e
            return False

    def _guess_mx(self):
        try: 
            mx_answer = dns.resolver.query(self.domain_name, 'MX')
            for mx_record in mx_answer.rrset:
                rd_set = self.zone.find_rdataset(self.domain_name, rdtype=MX, create=True)
                rdata = dns.rdtypes.ANY.MX.MX(IN, MX, mx_record.preference, mx_record.exchange)
                rd_set.add(rdata)
            return True
        except Exception, e:
            if self.debug: print e
            return False

    def _guess_a(self):
        try: 
            a_answer = dns.resolver.query(self.domain_name, 'A')
            for a_record in a_answer.rrset:
                rd_set = self.zone.find_rdataset(self.domain_name, rdtype=A, create=True)
                rdata = dns.rdtypes.IN.A.A(IN, A, address=a_record.address)
                rd_set.add(rdata)
            for subdomain in self.possible_subdomains:
                try: 
                    a_answer = dns.resolver.query('%s.%s.' % (subdomain, self.domain_name), 'A')
                    for a_record in a_answer.rrset:
                        rd_set = self.zone.find_rdataset(self.domain_name, rdtype=A, create=True)
                        rdata = dns.rdtypes.IN.A.A(IN, A, address=a_record.address)
                        rd_set.add(rdata)
                except:
                    pass
            return True
        except Exception, e:
            if self.debug: print e
            return False
        
    def _guess_cname(self):
        try: 
            for subdomain in self.possible_subdomains:
                try: 
                    cname_answer = dns.resolver.query('%s.%s.' % (subdomain, self.domain_name), 'CNAME')
                    for cname_record in cname_answer.rrset:
                        rd_set = self.zone.find_rdataset(self.domain_name, rdtype=CNAME, create=True)
                        rdata = dns.rdtypes.ANY.CNAME.CNAME(IN, CNAME, target=cname_record.target)
                        rd_set.add(rdata)
                except:
                    pass
            return True
        except Exception, e:
            if self.debug: print e
            return False
        
    def _guess_txt(self):
        try: 
            txt_answer = dns.resolver.query(self.domain_name, 'TXT')
            for txt_record in txt_answer.rrset:
                rd_set = self.zone.find_rdataset(self.domain_name, rdtype=TXT, create=True)
                rdata = dns.rdtypes.ANY.TXT.TXT(IN, TXT, txt_record.strings)
                rd_set.add(rdata)
            return True
        except Exception, e:
            if self.debug: print e
            return False

    def to_file(self, file, sorted=True, relativize=True):
        try:
            self.zone.to_file(file, sorted, relativize)
            return True 
        except Exception, e:
            raise e