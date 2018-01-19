squid-redirect
==============

A `json` configurable `squid`(3.5) `url_rewrite_program` written in `python3`.

Usecase: We wanted to transparently point our ios simulators at different content servers without modifying the ios application under test.

Each test run on our ci-servers can transparently alias different endpoints.


Examples
--------

### 1.) Trial the `url_rewrite_program` flow in a terminal

```bash
    python3 squid-redirect.py --rewrite '{"www\.capitalfm\.com": "www.capitalfm.development.int.thisisglobal.com"}'
    0 http://www.capitalfm.com/_build/ -
    0 OK rewrite-url="http://www.capitalfm.development.int.thisisglobal.com/_build/"
```

### 2.) Edit your `squid.conf` to include the `url_rewrite_program`

```

    url_rewrite_children 3 startup=0 idle=1 concurrency=1
    url_rewrite_extras ""
    url_rewrite_program /usr/local/bin/python3 /PATH/TO/squid-redirect.py --rewrite '{"www\.capitalfm\.com": "www.capitalfm.development.int.thisisglobal.com"}'
```

### 3.) Startup an example `squid` server

```bash
    cat <<EOF > rules.json
    {
        "www\\\\.capitalfm\\\\.com": "www.capitalfm.development.int.thisisglobal.com"
    }
    EOF

    SQUID_CONF_SOURCE=/usr/local/etc/squid.conf
    SQUID_CONF=./squid.conf
    cp ${SQUID_CONF_SOURCE} ${SQUID_CONF}

    cat <<EOF >> ${SQUID_CONF}

    url_rewrite_children 3 startup=0 idle=1 concurrency=1
    url_rewrite_extras ""
    url_rewrite_program /usr/local/bin/python3 $(pwd)/squid-redirect.py --rewrite $(pwd)/rules.json
    EOF

    squid -N -f ${SQUID_CONF}
```

### 4.) Setup `osx` transparent `webproxy`.

Programs that respect `webproxy`:
* `chrome`
* `ios_simulator`

but not system level programs like:
* `firefox`
* `curl`

```bash
    NETWORK_DEVICE="Wi-Fi"
    PROXY_HOST="localhost"
    PROXY_PORT="3128"
    networksetup -setwebproxy ${NETWORK_DEVICE} ${PROXY_HOST} ${PROXY_PORT}
    networksetup -setsecurewebproxy ${NETWORK_DEVICE} ${PROXY_HOST} ${PROXY_PORT}

    networksetup -setwebproxy ${NETWORK_DEVICE} "" ""
    networksetup -setsecurewebproxy ${NETWORK_DEVICE} "" ""
    networksetup -setwebproxystate ${NETWORK_DEVICE} off
    networksetup -setsecurewebproxystate ${NETWORK_DEVICE} off
```


References
----------

### Squid Documentation

* https://wiki.squid-cache.org/Features/Redirectors
* http://www.squid-cache.org/Doc/config/url_rewrite_program/
* http://www.squid-cache.org/Doc/config/url_rewrite_children/
* http://www.squid-cache.org/Doc/config/url_rewrite_extras/

### Alternate Example Implementations of `url_rewrite_program`

* https://www.mindchasers.com/dev/app-squid-redirect
* https://gofedora.com/how-to-write-custom-redirector-rewritor-plugin-squid-python/
* https://github.com/krllmnkv/rewrite-squid
