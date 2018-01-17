#!/usr/bin/env python3
## -*- coding: utf-8 -*-

import logging
import sys
import re
import json
from collections import namedtuple, ChainMap

SquidRequest = namedtuple('SquidRequest', ('channel_id', 'url', 'extras'))  # "%>a/%>A %un %>rm myip=%la myport=%lp"

log = logging.getLogger(__name__)

VERSION = '0.0'


# Utils ------------------------------------------------------------------------

def _postmortem(func, *args, **kwargs):
    import traceback
    import pdb
    import sys
    try:
        return func(*args, **kwargs)
    except Exception:
        type, value, tb = sys.exc_info()
        traceback.print_exc()
        pdb.post_mortem(tb)


def load_data(*sources):
    def _open_source(source):
        assert source
        if isinstance(source, dict):
            return source
        if isinstance(source, str) and source.startswith('{') and source.endswith('}'):
            return json.loads(source)
        if os.path.exists(source):
            return json.load(source)

    return dict(ChainMap(*map(_open_source, sources)))


# Squid Request Processing ----------------------------------------------------

def process_squid_request(request_line, rewrite_rules={}, redirect_rules={}, **args):
    """
    >>> rules = {
    ...     'rewrite_rules': {
    ...         'www.site.com': 'www.test.com',
    ...         '/my/path': '/my/test_path',
    ...     },
    ...     'redirect_rules': {
    ...         'www.notreal.com': 'www.real.com',
    ...     }
    ... }
    >>> process_squid_request('0 http://www.google.com/ extras', **rules)
    '0 OK'
    >>> process_squid_request('1 http://www.site.com/my/path.json?test=yes extras', **rules)
    '1 OK rewrite-url=http://www.test.com/my/path.json?test=yes'
    >>> process_squid_request('2 http://www.notreal.com/data?test=yes extras', **rules)
    '2 OK status=301 url=http://www.real.com/data?test=yes'
    """
    def _replace_url(url, rules, template):
        for regex, replacement in rules.items():
            if re.search(regex, url):
                return template.format(url=re.sub(regex, replacement, url))

    def _lookup_response(url):
        return next(filter(None, (
            _replace_url(url, rewrite_rules, 'rewrite-url={url}'),
            _replace_url(url, redirect_rules, 'status=301 url={url}'),
            ' ',
        )))

    request = SquidRequest(*request_line.split(' '))
    return f'{request.channel_id} OK {_lookup_response(request.url)}'.strip()


def process_input_output_handlers(input_handle=sys.stdin, output_handle=sys.stdout, **args):
    for request_line in input_handle.readline():
        output_handle.write(process_squid_request(request_line, **args))
        output_handle.flush()


# Commandline -----------------------------------------------------------------

def get_args():
    import argparse
    parser = argparse.ArgumentParser(
        description=f'''{__file__} {VERSION}
        
        Example Useage:
            python3 {__file__} TODO
        
        Tests:
            pytest --doctest-modules {__file__}
        
        ''',
        epilog=''''''
    )

    parser.add_argument('--rewrite', nargs='+', help='')
    parser.add_argument('--redirect', nargs='+', help='')

    parser.add_argument('-v', '--verbose', action='store_true', help='', default=False)
    parser.add_argument('--postmortem', action='store_true', help='Automatically drop into pdb shell on exception. Used for debuging')
    parser.add_argument('--version', action='version', version=VERSION)

    args = vars(parser.parse_args())
    return args


if __name__ == "__main__":
    args = get_args()
    logging.basicConfig(level=logging.DEBUG if args['verbose'] else logging.INFO)

    def main(**args):
        process_input_output_handlers(
            **{
                f'{arg}_rules': load_data(*args.get(arg))
                for arg in ('rewrite', 'redirect')
            },
            **args,
        )

    if args.get('postmortem'):
        _postmortem(main, **args)
    else:
        main(**args)
