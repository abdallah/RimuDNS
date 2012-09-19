import dns.zone
import dns.resolver 
import dns.name
from dns.rdataclass import *
from dns.rdatatype import *
import dns.rdtypes.ANY
import dns.rdtypes.IN


dns_server = 'ns1.rimuhosting.com'

class Zone:
    def __init__(self, domain_name):
        self.domain_name = dns.name.Name(domain_name)
        self.zone = dns.zone.Zone(self.domain_name)
        self.possible_subdomains = ['@', 
                                    'www', 'www1', 'www2', 
                                    'ftp', 
                                    'webmail', 'mail', 'mail1', 'mail2' 'smtp', 'imap', 'pop', 
                                    'ns1', 'ns2', 'ns3', 'ns4']
        self.dns_server = 'ns1.rimuhosting.com'
        self.debug = False
        
    def from_axfr(self, dns_server):
        try:
            self.zone = dns.zone.from_xfr(dns.query.xfr(dns_server, domain_name))
            return True
        except Exception, e:
            if self.debug: print e
            return False

    def from_file(self, file):
        try:
            self.zone = dns.zone.from_file(file, self.zone.origin)
            return True
        except Exception, e:
            if self.debug: print e
            return False
        
    def from_text(self, text):
        try:
            self.zone = dns.zone.from_text(text, self.zone.origin)
            return True
        except Exception, e:
            if self.debug: print e
            return False
        
    def from_guessing(self):
        if not self._guess_soa(): 
            raise Exception('Unable to guess SOA!')
        if not self._guess_ns():
            if self.debug: print 'Unable to guess NS records'
        if not self._guess_mx():
            if self.debug: print 'Unable to guess MX records'
        if not self._guess_a():
            if self.debug: print 'Unable to guess A records'
        if not self._guess_cname():
            if self.debug: print 'Unable to guess CNAME records'
        if not self._guess_txt():
            if self.debug: print 'Unable to guess TXT records'
        
        if self.debug: print self.zone.items()
        return True
            
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
        
    def _get_txt(self):
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
        self.zone.to_file(file, sorted, relativize)

def guess_zone(domain_name):
    try:
        soa_answer = dns.resolver.query(domain_name, 'SOA')
        soa_rr = soa_answer.rrset[0]
        ns_answer = dns.resolver.query(domain_name, 'NS')
        mx_answer = dns.resolver.query(domain_name, 'MX')
        a_answer = dns.resolver.query(domain_name, 'A')
        txt_answer = dns.resolver.query(domain_name, 'TXT')
    except Exception, e:
        print e
        txt_answer = ''
        
    zone_text  = '\n; SOA Record\n'
    zone_text += '$ORIGIN %s.\n' % domain_name
    zone_text += '$TTL 1h\n'
    zone_text += '%s. IN SOA %s %s (\n' % (domain_name, soa_rr.mname.to_text(), soa_rr.rname.to_text())
    zone_text += '  %s ; serial number of this zone file\n' % soa_rr.serial
    zone_text += '  %s ; slave refresh\n' % soa_rr.refresh
    zone_text += '  %s ; slave retry time in case of a problem\n' % soa_rr.retry
    zone_text += '  %s ; slave expiration time\n' % soa_rr.expire
    zone_text += '  %s ; maximum caching time in case of failed lookups\n' % soa_rr.minimum
    zone_text += ')\n'
    zone_text += '\n; NS Records\n'
    zone_text += ns_answer.rrset.to_text() + '\n'
    zone_text += '\n; MX Records\n'
    zone_text += mx_answer.rrset.to_text() + '\n'
    zone_text += '\n; A Records\n'
    zone_text += a_answer.rrset.to_text()  + '\n'
    if txt_answer:
        zone_text += txt_answer.rrset.to_text()  + '\n'

    zone_text += '\n; Guessed Records\n'
    possible_cnames = ['@', 'www', 'www1', 'www2', 'ftp', 'webmail', 'mail', 'mail1', 'mail2' 'smtp', 'imap', 'pop', 'ns1', 'ns2', 'ns3', 'ns4']
    for cn in possible_cnames:
        try: 
            a_answer = dns.resolver.query('%s.%s.' % (cn, domain_name), 'A')
            zone_text += a_answer.rrset.to_text()  + '\n'
        except:
            pass
        try:
            cn_answer = dns.resolver.query('%s.%s.' % (cn, domain_name), 'CNAME')
            zone_text += cn_answer.rrset.to_text()  + '\n'
        except:
            pass
    print zone_text

    try:
        zone = dns.zone.from_text(zone_text)
        return zone
    except Exception, e:
        print e
        return False
        
def axfr_zone(domain_name, dns_server):
    try:
        zone = dns.zone.from_xfr(dns.query.xfr(dns_server, domain_name))
        return zone
    except Exception, e:
        print e
        return False
       
#zone = axfr_zone(domain_name, dns_server)
#if not zone: 
zone = guess_zone(domain_name)
    
zone.to_file('/tmp/%s.db' % domain_name)
    

