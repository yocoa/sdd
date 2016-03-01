#!/usr/env/bin python
# encoding: utf-8

import re
import sys
import time

import dns.query
import numpy

def get_feature(string):
    cleaned_string = string.strip('.')
    return _NetworkFeature(cleaned_string).get_feature()

class _NetworkFeature(object):
    nameserver = '223.5.5.5'
    host = 'origin.asn.cymru.com'
    feature = {}

    def __init__(self, domain):
        self.domain = domain
        self.cache_a = self._make_a_response(domain)
        self.cache_ns = self._make_ns_response(domain)
        for i in self.cache_a.answer:
            ip = i.to_text().split(' ')[-1]
            self.cache_as = self._make_as_response(ip)

    def get_feature(self):
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
        if not self.domain:
            return [-1 for i in range(len(funcs))]
        for f in funcs:
            f()
        return self.feature

    def _make_a_response(self, domain):
        d = dns.name.from_text(domain)
        req = dns.message.make_query(d, dns.rdatatype.A)
        resp = dns.query.udp(req, self.nameserver)
        return resp

    def _make_ns_response(self, domain):
        d = dns.name.from_text(domain)
        req = dns.message.make_query(d, dns.rdatatype.NS)
        resp = dns.query.udp(req, self.nameserver)
        return resp

    def _make_as_response(self, ip):
        d = dns.name.from_text('%s.%s' % (ip, self.host))
        req = dns.message.make_query(d, dns.rdatatype.TXT)
        resp = dns.query.udp(req, self.nameserver)
        return resp

    def _reset_nameserver(self, nameserver):
        self.nameserver = nameserver

    def _ttl_mean(self):
        self.feature['_ttl_mean'] = numpy.mean(
            [int(i.to_text().split(' ')[1]) for i in self.cache_a.answer])
        return self.feature['_ttl_mean']

    def _a(self):
        for i in self.cache_a.answer:
            self.feature['_a'] = i.to_text().split(' ')[-1]
            return self.feature['_a']
        self.feature['_a'] = -1
        return self.feature['_a']

    def _a_seg(self):
        for i in self.cache_as.answer:
            self.feature['_a_seg'] = i.to_text().split('"')[1].split('|')[1].strip()
            return self.feature['_a_seg']
        self.feature['_a_seg'] = -1
        return self.feature['_a_seg']

    def _a_as(self):
        for i in self.cache_as.answer:
            self.feature['_a_as'] = i.to_text().split('"')[1].split('|')[0].strip()
            return self.feature['_a_as']
        self.feature['_a_as'] = -1
        return self.feature['_a_as']
        

    def _ns(self):
        for i in self.cache_ns.answer:
            self.feature['_ns'] = i.to_text().split(' ')[-1]
            return self.feature['_ns']
        self.feature['_ns'] = -1
        return self.feature['_ns']

    def _ns_as(self):
        for i in self.cache_ns.answer:
            domain = i.to_text().split(' ')[-1] 
            temp1 = self._make_a_response(domain)
            for j in temp1.answer:
                ip = j.to_text().split(' ')[-1]
                temp2 = self._make_as_response(ip)
                for k in temp2.answer:
                    self.feature['_ns_as'] = k.to_text().split('"')[1].split('|')[0].strip()
                    return self.feature['_ns_as']
        self.feature['_ns_as'] = -1
        return self.feature['_ns_as']

    def _ns_ttl_mean(self):
        self.feature['_ns_ttl_mean'] = numpy.mean(
            [int(i.to_text().split(' ')[1]) for i in self.cache_ns.answer])
        return self.feature['_ns_ttl_mean']

    def _reg_date(self):
        for i in self.cache_as.answer:
            self.feature['_reg_date'] = i.to_text().split('"')[1].split('|')[4].strip()
            return self.feature['_reg_date']
        self.feature['_reg_date'] = -1
        return self.feature['_reg_date']

    def _org(self):
        for i in self.cache_as.answer:
            self.feature['_org'] = i.to_text().split('"')[1].split('|')[2].strip()
            return self.feature['_org']
        self.feature['_org'] = -1
        return self.feature['_org']
