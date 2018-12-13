squid-redirect
==============

A `json` configurable `squid`(3.5) `url_rewrite_program` written in `python3`.

Usecase: We wanted to transparently point our ios simulators at different content servers without modifying the ios application under test. Each test run on our ci-servers can transparently alias different endpoints.


Examples
--------

### 1.) Trial the `url_rewrite_program` flow in a terminal

```bash
    python3 squid-redirect.py --rewrite '{"www\.capitalfm\.com": "www.capitalfm.development.int.thisisglobal.com"}'
    0 http://www.capitalfm.com/_build/ -
    0 OK rewrite-url="http://www.capitalfm.development.int.thisisglobal.com/_build/"
```

### 2.) Startup an example `squid` server using our `url_rewrite_program`

```bash
    squid -N -f !./config.py
```

### 3.) Setup `osx` transparent `webproxy`.

Programs that respect `webproxy`:
* `chrome`
* `ios_simulator`

`webproxy` is not sufficient for system-level programs like:
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
