#!/usr/bin/python
class mainClass:
	# Description: Python Script Used for Obtaining Performance Data from Multiple Units in Multiple Servers
	# Modified and written by Duc Nguyen
	# Date Start: 04/01/2016
	# Updated: 10/10/2016 by Erick Valle
		#Modified unitVersions Func
	# Updated: 10/26/217 by Erick Valle
		#Added runResetReport() and updated runEvery()
	#Main class
	#11/29/17 Modified to run in  Windows. By Erick Valle 

	#class MyPlace():
		#Function - Scheduler checker - (runEvery)
	import socket
	
	# runEveryDebugMode=False
	# Generating Host Name
	# import socket
	host = socket.gethostname()
	#host_lower = host.lower()
	#Windows
	host_lower = host.split('-')[0]
	
	# Working Path
	logPath = '/Users/' + host_lower + '/winlogs'
	projectPath = '/Users/' + host_lower + '/winlogs/myplace'
	# extractPath = projectPath + '/new_system_files'
	# activeSystemFilesPath = projectPath + '/main'
	# archivedSystemFilesPath = projectPath + '/temp'

	# Log Path
	performanceDataPath = projectPath + '/performance_data'
	mcp200PerformanceDataPath = performanceDataPath + '/MCP200'
	mcp110PerformanceDataPath = performanceDataPath + '/MCP110'
	mcp50PerformanceDataPath = performanceDataPath + '/MCP50'
	ivgPerformanceDataPath = performanceDataPath + '/IVG'

	# Url
	myplaceUrl = "http://myplace.qtdev.x10.mx"
	myplaceApiUrl = "http://myplace.qtdev.x10.mx/api"

	# initUrl = "http://amadar.x10.mx/myplace/api/init/latest/"
	mainUrl = "http://myplace.qtdev.x10.mx/api/main/latest"

	# List
	# - Winlogs
	list_unit_MCP200_server = []
	list_unit_MCP110_server = []
	list_unit_MCP50_server 	= []
	list_unit_IVG_server 	= []

	# - Winlogs: SW Logs
	list_unit_MCP200_SW = []
	list_unit_MCP110_SW = []
	list_unit_MCP50_SW  = []
	list_unit_IVG_SW 	= []

	# - Winlogs: HW Logs
	list_unit_MCP200_HW = []
	list_unit_MCP110_HW = []
	list_unit_MCP50_HW  = []
	list_unit_IVG_HW 	= []

	# - API
	list_unit_MCP200_api = []
	list_unit_MCP110_api = []
	list_unit_MCP50_api	 = []
	list_unit_IVG_api 	 = []

	# Dict
	dict_unit_by_id_SW = {'105':list_unit_MCP200_SW,'106':list_unit_MCP110_SW,'107':list_unit_MCP50_SW,'108':list_unit_IVG_SW}
	dict_unit_by_id_HW = {'105':list_unit_MCP200_HW,'106':list_unit_MCP110_HW,'107':list_unit_MCP50_HW,'108':list_unit_IVG_HW}

	# Input
	# inputTestUnits = ['105427792','106045306','107005433', '108001068']
	# inputUnit = '108001068'



	host=socket.gethostname()
	# hostpath="/Users/%s/winlogs/" % host
	hostpath = '/Users/' + host.lower() + '/winlogs/'
	mainpath = hostpath + 'myplace/main/' 
	perfFileName = 'unitPerformanceDetails.py'

	def runEvery(self, minuteCheck):
		import datetime
		runEveryDebugMode=False
		currentMinute=int(datetime.datetime.now().strftime('%M'))
		currentHour=int(datetime.datetime.now().strftime('%H'))
		if (runEveryDebugMode):
			print "current hour: %s" % currentHour
			print "current minute: %s" % currentMinute
		#	print minuteCheck	
		if minuteCheck<60:
			if (runEveryDebugMode):
				print "Greater than 60!"
			main = currentMinute%minuteCheck
			# print main	
		elif minuteCheck>60:
			if (runEveryDebugMode):
				print "Smaller than 60!"
			main =((currentHour*60)+currentMinute)%minuteCheck
			print main
		else:
			if (runEveryDebugMode):
				print "Invalid input - check input in an integer!"
			return False

		if main==0:
			if (runEveryDebugMode):
				print "retuning TRUE!"
			return True
		else:
			if (runEveryDebugMode):
				print "returning FALSE!"
			return False


	def checkCpuMemRequest(self):
		import datetime
		import time
		import sys
		import os
		import shutil
		import json
		#import MySQLdb
		import subprocess
		import urllib
		import urllib2
		import Queue
		import requests
		# Generate a list of units which have CPU_MEM_REQUEST_ENABLE = TRUE   #TESTWIN
		url = self.mainUrl + '/' + 'check_cpu_mem_request?server=%s' % (self.host_lower)
		print url
		response = json.load(urllib2.urlopen(url))	
		print 'response:  %s'  % (response)
		# response = checkCpuMemRequestUrlRequestResponse
		return response
		
				
	def generatePath(self, path):
		import datetime
		import time
		import os
		import sys
		import errno

		print "A new path is being verified and generated. Please wait.."
		
		try:
			if not os.path.exists(path):
				print "Path %s does not exist. Generating a new path.." % (path)
				os.makedirs(path)
				print "Path %s was created successfully.\n"
				
			else:
				print "Path %s exists.\n" % (path)
		except OSError as exc:  # Python >2.5
			if exc.errno == errno.EEXIST and os.path.isdir(directory):
				print "The path %s already exists.. Removing and recreating folder..." % (path)

			else:
				print "Error! Could not create this path %s!\n" % (path)
				raise			
				
	def writePerformanceDataToTxtFile(self, unit, samples):
		import datetime
		import time
		import sys
		import os
		import shutil
		import json
		#import MySQLdb
		import subprocess
		import urllib
		import urllib2
		import Queue

		mcp200DebugMode = unit.startswith('105')
		mcp110DebugMode = unit.startswith('106')
		mcp50DebugMode 	= unit.startswith('107')
		ivgDebugMode 	= unit.startswith('108')
		
		uaSWType = self.logPath + '/' + unit + 'SW'
		
		line = str(int(samples) * 100)
		
		print "Performance data is being generated and saved into a .txt file for unit % s. Please wait.." % (unit)
		
		try:
			if (mcp200DebugMode): 
				# print "\tMCP200. UA = %s" % (unit)
				
				self.generatePath(self.mcp200PerformanceDataPath)
				outputTxtFile = self.mcp200PerformanceDataPath + '/' + 'PerformanceData' + '_' + unit + '.txt'
				
				command = 'tail -' + line + ' ' + uaSWType + ' | grep -a "Total CPU" | tail -' + str(samples) + ' | awk \'{print ' + unit + ',$1,$2,$6,$5}\' > ' + outputTxtFile
				subprocess.call(command, shell=True)
				
				return self.mcp200PerformanceDataPath
			else:
				print "Not MCP200."
		
			if (mcp110DebugMode): 
				# print "\tMCP110. UA = %s" % (unit)
					
				self.generatePath(self.mcp110PerformanceDataPath)
				outputTxtFile = self.mcp110PerformanceDataPath + '/' + 'PerformanceData' + '_' + unit + '.txt'

				command = 'tail -' + line + ' ' + uaSWType + ' | grep -a "Total CPU" | tail -' + str(samples) + ' | awk \'{print ' + unit + ',$1,$2,$6,$5}\' > ' + outputTxtFile
				subprocess.call(command, shell=True)
				
				return self.mcp110PerformanceDataPath
			else:
				print "Not MCP110."
				

			if (mcp50DebugMode):
				# print "\tMCP50. UA = %s" % (unit)

				self.generatePath(self.mcp50PerformanceDataPath)
				outputTxtFile = self.mcp50PerformanceDataPath + '/' + 'PerformanceData' + '_' + unit + '.txt'
				
				command = 'tail -' + line + ' ' + uaSWType + ' | grep -a "Heap.*CPU" | tail -' + str(samples) + ' | awk \'{print ' + unit + ',$1,$2,$7,$8}\' > ' + outputTxtFile
				subprocess.call(command, shell=True)
				
				return self.mcp50PerformanceDataPath
			else:
				print "Not MCP50."	
		
			if (ivgDebugMode): 
				# print "\tIVG. UA = %s" % (unit)
				
				self.generatePath(self.ivgPerformanceDataPath)
				outputTxtFile = self.ivgPerformanceDataPath + '/' + 'PerformanceData' + '_' + unit + '.txt'
				#DEBUG
				print "DEBUG:  "+ outputTxtFile
				# command = 'tail -10000 ~/winlogs/108001068SW | grep -a "Heap.*CPU" | tail -100 | awk {\'print ' + unit + ',$3,$4,$9,$10\'} > ' + outputTxtFile
				
				command = 'tail -' + line + ' ' + uaSWType + ' | grep -a "Heap.*CPU" | tail -' + str(samples) + ' | awk \'{print ' + unit + ',$3,$4,$9,$10}\' > ' + outputTxtFile
				#command = 'tail --version'
				print "DEBUG: " +command
				subprocess.call(command, shell=True)
					
				return self.ivgPerformanceDataPath
			else:
				print "Not IVG.\n"
				
			print "Successfully writing performance data of unit %s into .txt file.\n" %(unit)
			
		except:
			print "Failed to write performance data into .txt file for unit %s.\n" % (unit)
			raise

	def converTxtFileToJsonFile(self, unit, path):		
		import datetime
		import time
		import sys
		import os
		import shutil
		import json
		import subprocess
		import os
		import json
		
		# Variables - Date/Time
		now = datetime.datetime.now()
		currentYear = now.year
		
		print "Starting to Convert the txt File into a json File. Please wait.."
		
		try:
			txtFileName = path + '/' + 'PerformanceData' + '_' + unit + '.txt'
			jsonFileName = path + '/' + 'PerformanceData' + '_' + unit + '.json'
			
			txtFile = open(txtFileName, 'r')
			jsonFile = open(jsonFileName, 'w')

			list_txt = []
			list_json = []
			
			list_payload = []
			payload = {}
			dict_performance = {'Server':self.host,'Payload':list_payload} 
			
			for line in txtFile.readlines():
				line = str(line)
				line = line.split(' ')
				list_txt.append(line)
			
			for row in list_txt:
				ua 	 = row[0]
				date = row[1].replace('/', '-')
				time = row[2]
				mem  = row[3].replace('Mem=','').replace('Mem:','').replace('%','')
				cpu  = row[4].replace('CPU=','').replace('CPU:','').replace('%\r\n','')
				
				full_date = str(currentYear) + '-' + date
				timestamp = full_date + ' ' + time
				
				payload['UA'] = ua
				payload['Timestamp'] = timestamp
				payload['CPU'] = cpu
				payload['Memory'] = mem
			
				list_payload.append(payload.copy())
			
			dict_performance = {'Server':self.host,'Payload':list_payload} 		
				
			list_json.append(dict_performance)

			# jsonFile.write(json.dumps(list_json))
			
			jsonFile.write(json.dumps(list_json, sort_keys=True, indent=4))
			
			print "Successfully converting from .csv file into .json file.\n"
		except:
			print "Failed to convert from .csv file into .json file.\n"
			raise

	def consumeCpuMemRequest(self, host_name, unit):
		import datetime
		import time
		import sys
		import os
		import shutil
		import json
		#import MySQLdb
		import subprocess
		import urllib
		import urllib2
		import Queue
		import requests			
		
		# http://amadar.x10.mx/myplace/api/main/latest/consume_cpu_mem_request?server=qtserver&ua=105349780
		
		print "Starting to update LAST_CPU_MEM_SYNC.."
		
		try:
			consumeUnitPerformanceRequestUrl = self.mainUrl + '/' + 'consume_cpu_mem_request?server=%s&ua=%s' % (host_name, unit)
			cconsumeUnitPerformanceRequestResponse = urllib2.urlopen(consumeUnitPerformanceRequestUrl).read()
			
			print "Unit: %s. Reponse: %s" % (unit, cconsumeUnitPerformanceRequestResponse)
		except:
			print "Failed to update LAST_CPU_MEM_SYNC\n"
			raise

	def insertCpuMemPayload(self, unit, path):
		import datetime
		import time
		import sys
		import os
		import shutil
		import json
		
		import subprocess
		import urllib
		import urllib2
		import Queue
		import requests	
		
		# http://amadar.x10.mx/myplace/api/main/latest/insert_unit_perf_data?server=test&json=123	
		
		jsonFileName = path + '/' + 'PerformanceData' + '_' + unit + '.json'
		jsonData = json.load(open(jsonFileName, 'r'))
		
		print "Starting to insert CPU/Memory Payload to the Database.."
		
		try:
			insertUnitPerformanceDataUrl = self.mainUrl + '/' + 'insert_unit_perf_data'
		
			url = insertUnitPerformanceDataUrl		
			payload = jsonData
			response = requests.post(url, data=json.dumps(payload))
			
			# print response.text		
			print "Successfully inserted CPU/Memory Payload to the Database..\n"
		except:
			print "Failed to insert CPU/Memory Payload to the Database..\n"
			raise
		
	def unitPerformance(self):
		import datetime
		import time
		import sys
		import os
		import shutil
		import json
		import subprocess
		import urllib
		import urllib2
		import Queue
		import requests
		# http://amadar.x10.mx/myplace/api/main/latest/json_parse_test
		# http://amadar.x10.mx/myplace/api/main/latest/check_cpu_mem_request?server=qtserver --> generate a list of unit
		response = self.checkCpuMemRequest()
		try:
			for item in response:
				unit = item['UA']
				samples = item['SAMPLES']
				
				# print "Unit: %s. Samples: %s" % (unit, samples)
				
				print "Starting to update Performance Data to the Database for Server: %s - Unit: %s" % (self.host_lower, unit)
				
				filePath = self.writePerformanceDataToTxtFile(unit, samples)
				#print filePath #DEBUG Changed filePath
				#filePathTest='/Users/Qualitest/winlogs/myplace/performance_data/IVG/'
				self.converTxtFileToJsonFile(unit, filePath)
				self.insertCpuMemPayload(unit, filePath)
				self.consumeCpuMemRequest(self.host_lower, unit)
				
				print "Successfully updated Performance Data to the Database..\n"
		except:
			print "Failed to update Performance Data to the Database..\n"
			raise
		

			
	def validateLogs():
		import datetime
		#import MySQLdb
		import datetime
		import os
		import time
		import socket
		import subprocess
		import Queue
		validateLogsDebugMode=False
		print(socket.gethostname())
		tailq = Queue.Queue(maxsize=10) # buffer at most 100 lines


		threshold=60
		host=socket.gethostname()
		hostpath="/Users/%s/winlogs/" % host
		if (validateLogsDebugMode):
			print "host: ", host
			print "hostpath: ", hostpath

		db = MySQLdb.connect(host='amadar.x10.mx' , user='amadarxm_server', passwd='Qualitest1234!', db='amadarxm_myplace')
		cursor = db.cursor()
		query = ("SELECT units.UA, units_servers.NAME, units.SW_LOG_MONITORED, units.HW_LOG_MONITORED FROM units, units_servers WHERE units.QT_SERVER = units_servers.ID AND units_servers.NAME = %s", host)
		cursor.execute(*query)

		#cursor.close()
		for (UA, QT_SERVER, SW_LOG_MONITORED, HW_LOG_MONITORED) in cursor:
			if (validateLogsDebugMode):
				print "\n"
				print(UA, QT_SERVER, SW_LOG_MONITORED, HW_LOG_MONITORED)
			###################
			#Validating SW log#
			###################
			if (SW_LOG_MONITORED=='YES'): #Check if SW should be monitored
				if (os.path.isfile("%s%sSW"%(hostpath,UA))): #Check if SW file exists in winlogs folder
					#print "SW File exists... Verifying file..."
					dt=os.path.getmtime(("%s%sSW"%(hostpath,UA)))
					currentTime = time.time()
					delta = currentTime-dt
					swStatus=""
					if (validateLogsDebugMode):
						print "Delta: ", delta
					if (currentTime - dt > threshold):
						p = subprocess.Popen(["tail", "-600", ("%s%sSW"%(hostpath,UA))], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						stderr, stdout = p.communicate()
						if (validateLogsDebugMode):
							print "Checking if unit is sleeping..."
						#print "\nstdout = ", stdout
						#print "\nstderr = ", stderr

						#print "stdout: ",stdout
						# for line in stderr:
							# print line
							# #print "\n",line
							# #print "\n*"
							# if ("SLEEP" in line):
								# swStatus = "SLEEP"
								# #break
						if ("SLEEP" in stderr):
							swStatus = "SLEEP"
						if (swStatus==""):
							if (validateLogsDebugMode):
								print "INVALID log file - updating db..."
							#INVALID - Update SW log status on DB
							swStatus='INVALID'
					else:
						#print 'VALID'
						#VALID - Update SW log status on DB
						swStatus='VALID'
					if (validateLogsDebugMode):
						print (datetime.datetime.fromtimestamp(dt))
				else:
					#print "SW file is missing!"
					#ERROR - Update SW log status on DB
					swStatus='ERROR'
			else:
				swStatus='NA'
			###################
			#Validating HW log#
			###################
			if (HW_LOG_MONITORED=='YES'): #Check if SW should be monitored
				if (os.path.isfile("%s%sHW"%(hostpath,UA))): #Check if HW file exists in winlogs folder
					#print "HW File exists... Verifying file..."
					dt=os.path.getmtime(("%s%sHW"%(hostpath,UA)))
					currentTime = time.time()
					delta = currentTime-dt
					if (validateLogsDebugMode):
						print "Delta: ", delta			
					if (currentTime - dt > threshold):
						p = subprocess.Popen(["tail", "-600", ("%s%sHW"%(hostpath,UA))], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
						stderr, stdout = p.communicate()			
						#print "HW Status: INVALID"
						hwStatus='INVALID'
						#INVALID - Update HW log status on DB
						
						if ("SLEEP" in stderr):
							hwStatus = "SLEEP"
						if (hwStatus==""):
							if (validateLogsDebugMode):
								print "INVALID log file - updating db..."
							#INVALID - Update HW log status on DB
							hwStatus='INVALID'				
							
					else:
						#print "HW VALID"
						hwStatus='VALID'
						#VALID - Update HW log status on DB
					if (validateLogsDebugMode):
						print (datetime.datetime.fromtimestamp(dt))
				else:
					#print "HW file is missing!"
					hwStatus='ERROR'
					#ERROR - Update SW log status on DB
			else:
				hwStatus='NA'
			if (validateLogsDebugMode):
				print "Results for %s: SW-%s HW-%s"%(UA, swStatus, hwStatus)
				print "Updating DB with results for %s..."%(UA)
			cursor2 = db.cursor()
			query=("UPDATE units SET SW_STATUS=%s, HW_STATUS=%s WHERE UA=%s",(swStatus,hwStatus,UA))
			cursor2.execute(*query)
			db.commit()
			cursor2.close()

		cursor.close()
		db.close()

	def keepAlive(self):
		import datetime
		#import MySQLdb
		import datetime
		import os
		import time
		import socket
		import subprocess
		import Queue
		import urllib2
		keepAliveDebugMode=True
		#host=socket.gethostname()
		#host = "qtserver"
		if(keepAliveDebugMode):
			print "Starting keepalive for %s..." % self.host_lower
		#db = MySQLdb.connect(host='amadar.x10.mx' , user='amadarxm_server', passwd='Qualitest1234!', db='amadarxm_myplace')
		#cursor = db.cursor()
		#query = ("UPDATE units_servers SET LAST_KEEP_ALIVE=now() WHERE NAME=%s", host)
		# query = ("UPDATE units_servers SET UPDATING=True WHERE NAME=%s", (host))
		#cursor.execute(*query)
		#db.commit()
		#cursor.close()
		#db.close()
		url = "http://myplace.qtdev.x10.mx/api/keepalive?server=%s"% self.host_lower
		response = urllib2.urlopen(url).read()
		print response;

	def sendLogs(self):
		import datetime
		import os
		from datetime import date, timedelta
		import time
		import socket
		import subprocess
		import Queue
		import urllib2
		import json
		import smtplib
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEBase import MIMEBase
		from email import Encoders
		import gzip
		import shutil
		import subprocess
		
		sendLogsDebugMode=True
		noResults=True
		#host=socket.gethostname()
		host=self.host_lower
		if(sendLogsDebugMode):
			print "Verifying if there are any logs to be sent from %s..." % host
		with open("mainClassLog.txt", "a") as myfile:
			myfile.write("\nVerifying if there are any logs to be sent from %s..." % host)
		url = "http://myplace.qtdev.x10.mx/api/log_delivery_date?server=%s"% host
		response = json.load(urllib2.urlopen(url))
			#response = urllib2.urlopen(url).read()
		print response;
		
		
		for units in response:
			noResults=False
			#print response[0].items()
			#print response[0]["UA"]
			unit=units["UA"]
			startDate= units["START_DATE"]
			endDate= units["END_DATE"]
			logYear='17'
			ivgMode = unit.startswith('108')
			
			print unit;
			if (startDate=="" or endDate==""):
				SUBJECTSW = "SW logs for %s"% unit
				SUBJECTHW = "HW logs for %s"% unit
			else:
				SUBJECTSW = "SW logs for %s from %s to %s"% (unit,startDate,endDate)
				SUBJECTHW = "HW logs for %s from %s to %s"% (unit,startDate,endDate)
			print SUBJECTSW
			with open("mainClassLog.txt", "a") as myfile:
						myfile.write("SW logs for %s"% unit)
			
			msg = MIMEMultipart()
			msg['Subject'] = SUBJECTSW 
			msg['From'] = "Truck"
			msg['To'] = units["EMAIL"]
			#msg['To'] = 'assafam@qualitestgroup.com'
			
			hwMsg = MIMEMultipart()
			hwMsg['Subject'] = SUBJECTHW
			hwMsg['From'] = "Truck"
			hwMsg['To'] = units["EMAIL"]
			#hwMsg['To'] = 'assafam@qualitestgroup.com'

			part = MIMEBase('application', "octet-stream")
			hwPart = MIMEBase('application', "octet-stream")		
			
			if (startDate=="" or endDate==""):
				#script = "./Users/" + self.host_lower + "/winlogs/myplace/main/create_temp.sh"
				#print(os.path.isdir("/Users/" + self.host_lower + "/winlogs/myplace/main/"))
				
				#subprocess.check_call(["sh",script, unit, "SW"], shell=True)
				try:
					
					subprocess.check_call(["sh","/Users/" + self.host_lower + "/winlogs/myplace/main/create_temp.sh", unit, "SW"])
					print "Created temp SW file..."
					swTempFile=True
				except:
					print "Failed to create a SW temp file... Will not be sending SW log"
					swTempFile=False
				try:
					subprocess.check_call(["sh","/Users/" + self.host_lower + "/winlogs/myplace/main/create_temp.sh", unit, "HW"])
					print "Created temp HW file..."
					hwTempFile=True
				except:
					print "Failed to create a HW temp file... Will not be sending HW log"
					hwTempFile=False
			#output = process.communicate()[0]
			
			else:
				print "NOTHING"
					
					
					
			
			file = "/Users/" + self.host_lower + "/winlogs/temp_" + unit + "SW.txt"
			hwFile = "/Users/" + self.host_lower + "/winlogs/temp_" + unit + "HW.txt"
			
			#Renaming Files
			fileTime = time.strftime("%H%M%S")
			fileDate = date.today().strftime("%m%d%Y")
			newFileSw = "/Users/" + self.host_lower + "/winlogs/" + unit+"SW_Pulled_" + fileDate + "_" + fileTime+ "_PST.txt"
			newFileHw = "/Users/" + self.host_lower + "/winlogs/" + unit+"HW_Pulled_" + fileDate + "_" + fileTime+ "_PST.txt"
			
			print newFileSw
			print newFileHw
			
			os.rename(hwFile, newFileHw)	
			
			if swTempFile:
				#Compressing log file
				os.rename(file, newFileSw)
				print "Compressing SW log file..."
				with open(newFileSw, 'rb') as f_in, gzip.open(newFileSw+'.gz', 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)
				compressedFile = newFileSw + '.gz'
				part.set_payload(open(compressedFile, "rb").read())
				Encoders.encode_base64(part)
				part.add_header('Content-Disposition', 'attachment; filename="%sSW.gz"'%unit)
				msg.attach(part)
			if hwTempFile:	
				#Compressing log file
				os.rename(hwFile, newFileHw)
				print "Compressing HW log file..."
				with open(newFileHw, 'rb') as hwf_in, gzip.open(newFileHw+'.gz', 'wb') as hwf_out:
								shutil.copyfileobj(hwf_in, hwf_out)
				compressedHWFile = newFileHw + '.gz'
				hwPart.set_payload(open(compressedHWFile, "rb").read())
				Encoders.encode_base64(hwPart)
				hwPart.add_header('Content-Disposition', 'attachment; filename="%sHW.gz"'%unit)
				hwMsg.attach(hwPart)
				
			#server = smtplib.SMTP("127.0.0.1:1025")
			server = smtplib.SMTP("smtp.gmail.com:587")
			#server.sendmail(host, "assafam@qualitestgroup.com", msg.as_string())
			server.starttls()
			#server.ehlo()
			#server.login('qualitestx', 'Qualitest123!')
			server.login('qualitestx', 'Qualitest1!')
			if swTempFile:
				print "Sending SW log..."
				server.sendmail(host, units["EMAIL"], msg.as_string())
			if hwTempFile:
				print "Sending HW log..."
				server.sendmail(host, units["EMAIL"], hwMsg.as_string())
			
		if(sendLogsDebugMode):
			if(noResults):
				print "No logs needs to be sent."
				with open("mainClassLog.txt", "a") as myfile:
					myfile.write("\nNo logs needs to be sent.")

	def unitsVersions(self):
		import datetime
		import datetime
		import os
		import time
		import socket
		import subprocess
		import Queue
		import urllib2
		import urllib
		import json
		import smtplib
		from email.MIMEMultipart import MIMEMultipart
		from email.MIMEBase import MIMEBase
		from email import Encoders
		import gzip
		import shutil
		import subprocess
		unitsVersionsDebugMode=True
		#host=socket.gethostname()
		#host2=socket.gethostname().lower()
		host=self.host_lower #<---------------------------HOST------------------------------------
		if(unitsVersionsDebugMode):
				print "Starting unitsVersions for %s..." % host
		#db = MySQLdb.connect(host='amadar.x10.mx' , user='amadarxm_server', passwd='Qualitest1234!', db='amadarxm_myplace')
		#cursor = db.cursor()
		#query = ("UPDATE units_servers SET LAST_KEEP_ALIVE=now() WHERE NAME=%s", host)
		# query = ("UPDATE units_servers SET UPDATING=True WHERE NAME=%s", (host))
		#cursor.execute(*query)
		#db.commit()
		#cursor.close()
		#db.close()
		url = "http://myplace.qtdev.x10.mx/api/units_versions?server=%s"% host
		
		response = json.load(urllib2.urlopen(url))
		#response = urllib2.urlopen(url).read()
		#print response;


		for units in response:
			noResults=False
			unit=units["UA"]
			print unit
			
			try:
				result = subprocess.check_output(["sh","/Users/"+ self.host_lower +"/winlogs/myplace/main/get_unit_version_details.sh", "all", unit])
				all=result.split(',')[:-1]
				print all
				app = urllib.quote_plus(all[0])
				os = urllib.quote_plus(all[1])
				papi = urllib.quote_plus(all[2])
				viop = urllib.quote_plus(all[3])
				
				foundVersions = True
				print "updating version for %s"% unit
				
			except:
				####To be implemented later
				foundVersions = False
				print "Failed getting UA version..."	
			
			if (foundVersions):
				versionUpdateUrl = "http://myplace.qtdev.x10.mx/api/main/latest/update_unit_version?ua=%s&app=%s&os=%s&papi=%s&viop=%s"% (unit, app, os, papi, viop)
				response = urllib2.urlopen(versionUpdateUrl).read()
				
				print response
			else:
				print "Saving last known version..."
	
	def runResetReport(self):
		import os
		import os.path
		import socket
		import subprocess
		import Queue
		import shutil
		import sys
		import getpass
		import urllib2
		import json
 

		host=getpass.getuser()
		resetReportFile = self.projectPath + '/' + 'main/' + 'resetReport.py'
		url = self.myplaceUrl + "/api/get_reset_report?server=%s"% host
		response = json.load(urllib2.urlopen(url))
		
		print response
		for items in response:
			getReport= items["GET_REPORT"]
			print getReport

			if (getReport=="1"):
		
				try:
					print "Running reset report..."
					execfile(resetReportFile)
					
				except:
					print "Could not run resetReport.py"
					raise	
	

	def __init__(self):
		##### MAIN #####		
		# running keepalive every minute
		if self.runEvery(1):
			#with open("mainClassLog.txt", "a") as myfile:
			#	myfile.write("\nRunning keepAlive")
			self.keepAlive()
			
		# Checking if any logs need to be sent
		if self.runEvery(1):
		#	with open("mainClassLog.txt", "a") as myfile:
		#		myfile.write("\nRunning sendLogs")
			self.sendLogs()
		
		# updating mobile versions every 30 minutes
		if self.runEvery(1):
		#	with open("mainClassLog.txt", "a") as myfile:
		#		myfile.write("\nRunning unitsVersions")
			self.unitsVersions()
		
		if self.runEvery(1):
		#	with open("mainClassLog.txt", "a") as myfile:
		#		myfile.write("\nRunning unitPerformanceDetails")
			self.unitPerformance()
			print "Entering per"
		#	# execfile(mainpath + perfFileName)
		#if self.runEvery(1):
		#	with open("mainClassLog.txt", "a") as myfile:
		#		myfile.write("\nRunning Reset Report")
		#	self.runResetReport()

if __name__ == "__main__":
	mainClass()
	# mainClass()
	# a.main()
	# self.main()
