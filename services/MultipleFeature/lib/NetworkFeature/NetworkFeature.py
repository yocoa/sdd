#!/usr/env/bin python
# encoding: utf-8

import re
import sys
import time

import dns.query
import numpy
from whois import NICClient as WhoisClient

def get_feature(string):
    cleaned_string = string.strip('.')
    return _NetworkFeature(cleaned_string).get_feature()

class _NetworkFeature(object):
    nameserver = '223.5.5.5'
    whoishost = 'whois.cymru.com'
    feature = {}
    whois_cache = None

    def __init__(self, string):
        self.client = WhoisClient()
        self.resp_cache = self._make_response(string)

        funcs = (
            self._ttl_mean,
            self._a,
            self._a_seg,
            self._a_as,
            self._ns,
            self._ns_as,
            self._ns_ttl_mean,
            self._reg_date,
            self._org,
        )
        if not string:
            return [-1 for i in range(len(funcs))]
        for f in funcs:
            f()

    def get_feature(self):
        return self.feature

    def _make_response(self, string):
        domain = dns.name.from_text(string)
        request = dns.message.make_query(domain, dns.rdatatype.ANY)
        response = dns.query.udp(request, self.nameserver)
        return response

    def _reset_nameserver(self, nameserver):
        self.nameserver = nameserver

    def _ttl_mean(self):
        self.feature['_ttl_mean'] = numpy.mean(
            [int(i.to_text().split(' ')[1]) for i in self.resp_cache.answer if 'IN A' in i.to_text()])

    def _a(self):
        for i in self.resp_cache.answer:
            if 'IN A' in i.to_text():
                self.feature['_a'] = i.to_text().split(' ')[-1]
                return
        self.feature['_a'] = ''

    def _a_seg(self):
        query = '-v %s' % self.feature['_a']
        whois_text = self.client.whois(query, self.whoishost, self.client.WHOIS_QUICK, False, 20)
        if not whois_text.strip() or 'Error' in whois_text:
            self.feature['_a_seg'] = ''
            return
        self.whois_cache = whois_text
        self.feature['_a_seg'] = self.whois_cache.split('\n')[1].split('|')[2].strip()

    def _a_as(self):
        if self.whois_cache:
            self.feature['_a_as'] = self.whois_cache.split('\n')[1].split('|')[0].strip()
            return
        self.feature['_a_as'] = ''
        

    def _ns(self):
        for i in self.resp_cache.answer:
            if 'IN NS' in i.to_text():
                self.feature['_ns'] = i.to_text().split(' ')[-1]
                return
        self.feature['_ns'] = ''

    def _ns_as(self):
        for i in self.resp_cache.answer:
            if 'IN NS' in i.to_text():
                string = i.to_text().split(' ')[-1] 
                temp_resp = self._make_response(string)
                for j in temp_resp.answer:
                    if 'IN A' in j.to_text():
                        ip = j.to_text().split(' ')[-1]
                        query = '-v %s' % ip
                        whois_text = self.client.whois(query, self.whoishost, self.client.WHOIS_QUICK, False, 20)
                        if not whois_text.strip() or 'Error' in whois_text:
                            continue
                        self.feature['_ns_as'] = whois_text.split('\n')[1].split('|')[0].strip()
                        return
        self.feature['_ns_as'] = ''

    def _ns_ttl_mean(self):
        if self.whois_cache:
            self.feature['_ns_ttl_mean'] = numpy.mean(
                [int(i.to_text().split(' ')[1]) for i in self.resp_cache.answer if 'IN NS' in i.to_text()])
            return
        self.feature['_ns_ttl_mean'] = ''

    def _reg_date(self):
        if self.whois_cache:
            self.feature['_reg_date'] = self.whois_cache.split('\n')[1].split('|')[5].strip()
            return
        self.feature['_reg_date'] = ''

    def _org(self):
        if self.whois_cache:
            self.feature['_org'] = self.whois_cache.split('\n')[1].split('|')[3].strip()
            return
        self.feature['_org'] = ''

