##
# This file is part of the carambot-usherpa project.
#
# Copyright (C) 2012 Stefan Wendler <sw@kaltpost.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##

'''
This file is part of the pyscmpd project.
'''

import logging
import sys 
import argparse
import os

USER_WORK_DIR	=	("%s/.pyscmpd" 		% os.getenv("HOME"))
DEF_PID_FILE	=	("%s/pyscmpd.pid" 	% USER_WORK_DIR)
DEF_CONF_FILE	=	("%s/pyscmpd.conf" 	% USER_WORK_DIR)
DEF_LOG_FILE	= 	("%s/pyscmpd.log" 	% USER_WORK_DIR)

def prepare():

	if not os.path.exists(USER_WORK_DIR):
		print("Note: pyscmpd working dir created: %s" % USER_WORK_DIR)
		os.makedirs(USER_WORK_DIR)

	if not os.path.exists(DEF_CONF_FILE):
		print("Note: pyscmpd default config created: %s" % DEF_CONF_FILE)

		f = open(DEF_CONF_FILE, 'w')
		f.write(";; pyscmpd autogenerated default config\n\n")
		f.write("\n[server]\n")
		f.write("port=9900\n")
		f.write("\n[logging]\n")
		f.write("level=info\n")
		f.write("file=%s\n" % DEF_LOG_FILE) 
		f.write("\n[favorites]\n")
		f.write("gethoswing : maddecent, barelylegit\n")
		f.write("electrosoul: griz\n")
		f.close()

try:

	parser = argparse.ArgumentParser(description='Python Soundcloud Music Player Daemon "pyscmpd"')

	parser.add_argument('command', metavar='COMMAD', type=str, 
		help='Command to operate the daemon: start, stop, restart')

	parser.add_argument('--foreground', dest="foreground", action='store_true', default=False, 
		help='Run in foreground, do not fork')

	parser.add_argument('--pid', dest="pidfile", metavar='FILE', default=DEF_PID_FILE, 
		type=str, help='PID file to use')

	parser.add_argument('--conf', dest="conffile", metavar='FILE', default=DEF_CONF_FILE, 
		type=str, help='Configuration file to use')

	args = parser.parse_args()

	if not args.command in ['start', 'stop', 'restart']:
		sys.stderr.write("Unknown command [%s]\n" % args.command)
 		sys.exit(1)
		
	prepare()

	from pyscmpd.daemon import PyScMpd 

	pyscmpd = PyScMpd(args.pidfile)
	pyscmpd.readConfig(args.conffile, args.foreground)

	if args.command == "start":
		logging.info("Starting daemon")

		if args.foreground:
			pyscmpd.run()
		else:
			pyscmpd.start()	

	elif args.command == "stop":
		logging.info("Stopping daemon")
		pyscmpd.stop()	

	elif args.command == "restart":
		logging.info("Restarting daemon")
		pyscmpd.restart()	

except KeyboardInterrupt:
	pass

except Exception as e:

	logging.error("Exception occurred: %s" % `e`)