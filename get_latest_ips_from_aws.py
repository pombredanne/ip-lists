#! /usr/bin/env python

# Standard libraries
import datetime
import json
import os
import urllib

# 3rd party libraries

# Project libraries

def create_xml_for_list(service, region, values):
	"""
	"""
	return """
		<IPList id="">
			<TBUID></TBUID>
			<Name>{} {}</Name>
			<Description>Public IPs as of {}.

AWS maintained list is available at https://ip-ranges.amazonaws.com/ip-ranges.json</Description>
			<Items>{}</Items>
		</IPList>""".format(
	service,
	region,
	datetime.datetime.now().strftime("%d-%b-%Y"),
	','.join(values).strip(',')
	)

def write_xml_for_import(list_name, list_xml):
	"""
	"""
	xml = """<?xml version="1.0" encoding="utf-8"?>
<Export type="IPList" date="{}" version="">
	<IPLists>
	{}	
	</IPLists>
</Export>""".format(
	datetime.datetime.now().strftime("%B %-d, %Y %H:%M"),
	"\n".join(list_xml)
	)

	output_path = os.path.join(os.getcwd(), 'lists')
	if not os.path.exists(output_path): 
		try:
			os.mkdir(output_path)
		except Exception, err:
			print "Could not create the 'lists' subfolder. Writing output to current folder"
			output_path = os.getcwd()

	timestamp = datetime.datetime.now().strftime("%Y-%b-%d").lower()

	fn = os.path.join(output_path, '{}-{}.xml'.format(timestamp, list_name))
	wrote_file = False
	try:
		with open(fn, 'w') as fh:
			fh.write(xml)
			wrote_file = True
	except Exception, err:
		print "Could not write the list XML to [{}]. Echoing to stdin instead".format(fn)
		print "------------------------------"
		print list_xml

	return (wrote_file, fn)

def main():
	"""
	Get the latest list of IP address from AWS and convert them to 
	a format for import to Deep Security
	"""
	ip_range_url = "https://ip-ranges.amazonaws.com/ip-ranges.json"

	ips = None
	try:
		uh = urllib.urlopen(ip_range_url)
		if uh: ips = json.load(uh)
		uh.close()
	except Exception, err:
		print "Threw exception:\n\t{}".format(err)
		print "Could not download the IP .json document, unable to general from lists for import"

	lists = {}
	if ips:
		for prefix in ips['prefixes']:
			if not lists.has_key(prefix['service']):
				lists[prefix['service']] = { 'all': [] }
			
			if not lists[prefix['service']].has_key(prefix['region']):
				lists[prefix['service']][prefix['region']] = []

			lists[prefix['service']][prefix['region']].append(prefix['ip_prefix'])
			lists[prefix['service']]['all'].append(prefix['ip_prefix'])

	lists_xml = []
	lists_key = []
	for service, data in lists.items():
		for region, values in data.items():
			if region == 'GLOBAL': continue

			lists_xml.append(create_xml_for_list(service, region, values))
			lists_key.append('{}-{}-public-ips'.format(service.lower(), region.lower()))

	print "Writing XML files for import..."
	result, fn = write_xml_for_import('all-aws-public-ips', lists_xml)
	if result: print fn
	for i, list_xml in enumerate(lists_xml):
		result, fn = write_xml_for_import(lists_key[i], lists_xml)
		if result: print fn
		

if __name__ == '__main__': main()