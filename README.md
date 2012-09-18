RimuDNS
=======

RimuHosting Python DNS tools

https://rimuhosting.com/dns/dyndns.jsp

https://zonomi.com/app/dns/dyndns.jsp

The RimuDNS class is a wrapper around the REST API calls. 

    from rimudns import RimuDNS

    api_key = 'GETYOURAPIKEYFROMTHECONTROLPANEL'
    dns = DNS(api_key)

    dns.change_ip('192.168.59.133', '192.168.59.132')
    if dns.set_record('aa1.example.com', '94.162.59.133'): 
        print 'updated: %s records' % dns.record_count

    dns.list_zones()

    dns.create_zone('test.example.com') # should work the first time
    dns.create_zone('test.example.com') # should fail with 500 error

    dns.delete_zone('test.example.com') # should work the first time
    dns.delete_zone('test.example.com') # should fail with 500 error

    dns.list_records('example.com')
    dns.list_records('example.com', all_records=True)

    dns.create_zone('test.example.com') # should work the first time
    dns.set_record('test.example.com', '127.0.0.1')
    dns.set_record('mail.test.example.com', 'test.example.com', 'CNAME')

    updates_list = [
                {
                    'action': 'SET', # or 'DELETE',
                    'host': 'foo.test.example.com,bar.test.deeb.com', # or ['foo.com', 'bar.com],
                    'value': '192.168.1.1',
                    'type': 'A' # or 'MX' or 'CNAME' or 'TXT', optional default A, 
                    #'prio': for MX records, number default 0,
                    #'ttl': number, optional default 3600,
                },
                { 
                    'action': 'DELETE',
                    'host': ['foo.test.example.com', 'bar.test.example.com'],
                    'value': '192.168.1.1',
                    'type': 'CNAME', # or 'TXT', optional default A, 
                    #'prio': for MX records, number default 0,
                    #'ttl': number, optional default 3600,
                },      
            ]
    dns.multiple_actions(updates_list)
    dns.delete_zone('test.example.com') # should work the first time