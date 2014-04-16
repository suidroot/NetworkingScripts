#!/usr/bin/env python## This Script polls and returns the current routing table#from vendors.snmp import querysnmpdataimport sysimport stringimport argparseimport csvdef initArgs():	parser = argparse.ArgumentParser()	parser.add_argument('-i', '--ip_address', help='i.e. -i "192.168.31.21"')	parser.add_argument('-c', '--community', help='Enter SNMP Community')	parser.add_argument('-f', '--file', help='Load Host list from File')	parser.add_argument('-b', '--csv', help='CSV Format', action='store_true')	parser.add_argument('-o', '--output', help='Output to file')	arg = parser.parse_args()	# Gather host information from File or Commandline	if arg.file:		hosts = {}		with open(arg.file, "r") as host_list:			for line in host_list:				(device, community) = string.split(line,':')				if device[0] == "#":					pass				else:					hosts[device] = community.rstrip()	else:		# set ip address to make calls on		if arg.ip_address:			device = arg.ip_address		else:			sys.exit("You should specify a Host")			#device = '10.5.6.254'		if arg.ip_address:			community = arg.community		else:			sys.exit("You should specify a community")			#community = 'poopie'				hosts = { device : community }	# Parse other options		if arg.csv:		format = 'csv'	else:		format = 'text'	if arg.output:		outputfile = arg.output	else:		outputfile = ""			return hosts, format, outputfile# This function retrieves the available interface datadef collectroutingtable(device, community):	oids = '1.3.6.1.2.1.4.24.4.1.'		walkreturn = querysnmpdata.snmpwalkoid(device, community, oids)			# oid example 1.3.6.1.2.1.4.24.4.1.24.4.1.1.10.5.6.0.255.255.255.0.0.0.0.0.0	indextable = {}		for currentrow in walkreturn:		for indexoid, val in currentrow:			replaced = string.replace(indexoid.prettyPrint(), oids, '')			value = val.prettyPrint()					(oidnumber, routeindex) = string.split(replaced,'.', 1)			oidnumber = int(oidnumber)			if routeindex in indextable:				indextable[routeindex][oidnumber] = value			else:				indextable[routeindex] = {}				indextable[routeindex][oidnumber] = value	return indextabledef printroutingtable (routingtable):	for routeid in sorted(routingtable):		#print "{0}".format(routeid),		for oid in sorted(routingtable[routeid]):			print "{0}".format(routingtable[routeid][oid]),		print "\n",if __name__ == "__main__":##### Start Main Section ######	hosts, format, outputfile = initArgs()		for i in hosts:		device = str(i)		community = str(hosts[i])				if format == 'Text':			print "Gathering SNMP Data for, %s using the community %s" % (device, community)		hostname = querysnmpdata.hostinfo(device, community)		routetable = collectroutingtable(device, community)		printroutingtable = printroutingtable(routetable)