squid-redirect
==============

Configurable squid url redirector (python3)


Examples
--------

```
    url_rewrite_children 3 startup=0 idle=1 concurrency=10
    url_rewrite_program /home/jenkins/tools/squid-redirect.py --rewrite '{"www.site.com": "www.replacement.com"}'
```

```bash
    SQUID_CONF=/home/jenkins/squid.conf
    cp /usr/local/etc/squid.conf ${SQUID_CONF}
    echo "url_rewrite_program $(pwd)/squid-redirect.py --rewrite $(pwd)/myrules.json" >> ${SQUID_CONF}
    squid -k stop
    squid -f ${SQUID_CONF}
    #squid -k stop
```

Reference
---------

http://www.squid-cache.org/Doc/config/url_rewrite_children/
http://www.squid-cache.org/Doc/config/url_rewrite_extras/
https://www.mindchasers.com/dev/app-squid-redirect
https://gofedora.com/how-to-write-custom-redirector-rewritor-plugin-squid-python/
https://github.com/krllmnkv/rewrite-squid
