import dns.zone
import dns.resolver 

domain_name = 'funinc.org' # --- CHANGE THIS
dns_server = 'ns1.rimuhosting.com'

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
    

