RimuDNS
=======

[RimuHosting](http://rimuhosting.com) Python DNS tools

Documentation for the API can be found [here](https://rimuhosting.com/dns/dyndns.jsp) 
and [here](https://zonomi.com/app/dns/dyndns.jsp) for RimuHosting and Zonomi respectively.

The RimuDNS class is a wrapper around the REST API calls.

Installation
------------
    easy_install rimudns
or 

    pip install rimudns

Usage
-----

The API key can be generated and replaced in the RimuHosting control panel 
from https://rimuhosting.com/cp/apikeys.jsp

Get started::

    #!/usr/bin/env python
    from rimudns import RimuDNS
    api_key = 'GETYOURAPIKEYFROMTHECONTROLPANEL'
    dns = RimuDNS(api_key)
    dns.use_rimuhosting()

List all domains::
	
    for domain in dns.list_zones():
        print domain['name']

Create a new domain::

    dns.create_zone('example.com')

Delete a domain::

    dns.delete_zone('example.com')

* IMPORT_AXFR = 1
* IMPORT_FILE = 2
* IMPORT_TEXT = 3
* IMPORT_DICT = 4
* IMPORT_GUESS = 5

Import a domain from a BIND zone file or string::

    from rimudns import ZoneHandle
    dns.import_zone('example.com', ZoneHandle.IMPORT_FILE, '/tmp/example.com.zone')

Export a domain to file::
    
    dnsdns.to_file('/tmp/example.com.zone')

Delete a domain::

    dns.delete_zone('example.com')

List all records for a domain::

    records = dns.list_records('example.com')
    for record_type in records:
        print 'Type: ', record_type
        for record in records[record_type]
            print 'name: %s -> %s' % (record['name'], record['content')

Add/Update a record::

    dns.set_record('example.com', '127.0.0.1', record_type='A', ttl=600)

Delete a record::

    dns.delete_record('example.com', '127.0.0.1', 'A')

Change an IP across all zones::

    old_ip = '127.0.0.1'
    new_ip = '127.0.0.2'
    dns.change_ip(old_ip, new_ip)

Convert a zone to slave/back to regular::

    dns.convert_to_regular('example.com')
    dns.convert_to_slave('example.com')

Web Interface
=============

You can always use the RimuHosting/Zonomi tools to edit your DNS zones
Try: https://rimuhosting.com/dns/

