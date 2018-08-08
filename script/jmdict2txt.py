#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import xml.etree.ElementTree as et

jmdict_fname = "JMdict_e"
output_fname = "je-jmdict.txt"

wf = open(output_fname, 'wt')
tree = et.parse(jmdict_fname)
jmdict = tree.getroot()
entries = jmdict.findall('entry')
for entry in entries:
    keys = list()
    k_ele = entry.find('k_ele')
    if k_ele is not None:
        keys.extend([keb.text for keb in k_ele.findall('keb')])
    r_ele = entry.find('r_ele')
    if r_ele is not None:
        keys.extend([reb.text for reb in r_ele.findall('reb')])
    sense = entry.find('sense')
    values = [gloss.text for gloss in sense.findall('gloss')]
    value = ', '.join(values)
    for key in keys:
        wf.write("%s\t%s\n" % (key, value))
wf.close()
