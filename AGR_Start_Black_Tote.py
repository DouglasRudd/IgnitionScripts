
def logDebugMsg(msgID, message, msgSource):
		
	params = {'msgID':msgID,
			  'message':message,
			  'msgSource':msgSource}
	import system
	system.db.runNamedQuery('Gages', 'Debug/LogMsg', params)

def GetGageFromPath(path):
	# passed value like  [default]G11/G11/Gage/Count/Batch Good Count
	# returns 'G11'
	try:
		pth = path.replace('[default]', '')
		pathAry = pth.split('/')
		return pathAry[0]
	
	except Exception as e:
		errParams = {'msgID':'GetGageFromPath',
	                 'message':getattr(e, 'message', repr(e)),
                     'msgSource':'AGR_Start_Black_Tote.GetGageFromPath O3WLTR'}
			   
		system.db.runNamedQuery("Gages", "Debug/LogMsg", errParams)



try:

#	quit()
	debugGage = 'GXX'

	batchCount = int(newValue.getValue())
	GageID = GetGageFromPath(str(event.tagPath))
	pathGageID = '[default]' + GageID + '/' + GageID
	
	if (initialChange == 1):  # 1 means this script may have been 'saved'  and that saving it generated the change event 
		quit()
#		pass

#	pathToTag = pathGageID + '/Gage/Count/Batch Target'  # [default]G11/G11/Gage/Count/Batch Target

	if (GageID != debugGage):
		if batchCount != 0:  # batchCount has to trigger off of the count being 0 if we want to get accurate (total counts) in the database.  
			quit()           # Triggering batchCount off of the count being 1 gives us a more accurate 'timestamp' of when the black-tote actually started but it causes all of the total counts to be off by 1         
	
#	logDebugMsg('Juliett', GageID, batchCount)

	Total = system.tag.readBlocking([pathGageID + '/Station Data/ST1/ST 1 Total Bad Parts'])[0].value
	STN_1_Count = system.tag.readBlocking([pathGageID + '/Station Data/ST1/ST 1 Total Rejects'])[0].value
	STN_2_Count = system.tag.readBlocking([pathGageID + '/Station Data/ST2/ST 2 Total Bad Parts'])[0].value
	STN_3_Count = system.tag.readBlocking([pathGageID + '/Station Data/ST3/ST 3 Total Bad Parts'])[0].value
	STN_4_Count = system.tag.readBlocking([pathGageID + '/Station Data/ST4/ST 4 Total Bad Parts'])[0].value
	STN_5_Count = system.tag.readBlocking([pathGageID + '/Station Data/ST5/ST 5 Total Bad Parts'])[0].value
	STN_6_Count = system.tag.readBlocking([pathGageID + '/Station Data/ST6/ST 6 Total Bad Parts'])[0].value
	

	if (Total is None): Total = '0'
	if (STN_1_Count is None): STN_1_Count = '0'
	if (STN_2_Count is None): STN_2_Count = '0'			
	if (STN_3_Count is None): STN_3_Count = '0'
	if (STN_4_Count is None): STN_4_Count = '0'
	if (STN_5_Count is None): STN_5_Count = '0'
	if (STN_6_Count is None): STN_6_Count = '0'
	

	SkidNum = system.tag.readBlocking([pathGageID + '/Skid/skid id'])[0].value
	hydroMachine = system.db.runNamedQuery("Gages", "Printing/getAsset", {'skidID':SkidNum})
	heatNum = system.tag.readBlocking([pathGageID + '/Skid/Skid Heat'])[0].value
	wipID = system.tag.readBlocking([pathGageID + '/Scanner/Active Wip'])[0].value
	PartNumber = system.tag.readBlocking([pathGageID + '/Gage/Running Part Number'])[0].value
	PartNumber = strFuncs.strRightDelim(PartNumber, '-')
	empID = system.tag.readBlocking([pathGageID + '/Scanner/User'])[0].value

#	logDebugMsg('whiskey', SkidNum, 'eeee')

	startParams = {
				  'Mach_Total_Start':Total,
				  'GageID':GageID,
				  'Start_STN_1':STN_1_Count,
				  'Start_STN_2':STN_2_Count,
				  'Start_STN_3':STN_3_Count,
				  'Start_STN_4':STN_4_Count,
				  'Start_STN_5':STN_5_Count,
				  'Start_STN_6':STN_6_Count,
				  'Hydro':hydroMachine,
				  'WIP_Num':wipID,
				  'HeatNum':heatNum,
				  'PartNum':PartNumber,
				  'Skid_ID':SkidNum,
				  'EmpID':empID
				  }

#	if (GageID == debugGage):
#			logDebugMsg('bluebonnet', debugGage + ', Total', Total)
#			logDebugMsg('bluebonnet', debugGage + ', STN_1_Count', STN_1_Count)
#			logDebugMsg('bluebonnet', debugGage + ', STN_2_Count', STN_2_Count)
#			logDebugMsg('bluebonnet', debugGage + ', STN_3_Count', STN_3_Count)
#			logDebugMsg('bluebonnet', debugGage + ', STN_4_Count', STN_4_Count)
#			logDebugMsg('bluebonnet', debugGage + ', STN_5_Count', STN_5_Count)
#			logDebugMsg('bluebonnet', debugGage + ', STN_6_Count', STN_6_Count)
#			logDebugMsg('bluebonnet', debugGage + ', hydroMachine', hydroMachine)
#			logDebugMsg('bluebonnet', debugGage + ', wipID', wipID)
#			logDebugMsg('bluebonnet', debugGage + ', heatNum', heatNum)
#			logDebugMsg('bluebonnet', debugGage + ', PartNumber', PartNumber)
#			logDebugMsg('bluebonnet', debugGage + ', SkidNum', SkidNum)
#			logDebugMsg('bluebonnet', debugGage + ', empID', empID)



#	logDebugMsg('Juliett1', GageID, wipID)
	system.db.runNamedQuery("Gages", "AGR_Counts/start_AGR_black_tote", startParams)
#	logDebugMsg('Juliett2', GageID, wipID)

	if (GageID == debugGage):
		logDebugMsg('bluebonnet', GageID, 'Echo')


except Exception as e:

	eParams = {'msgID':GageID + ', ' + heatNum,
             'message':getattr(e, 'message', repr(e)),
           'msgSource':'Gateway AGR_Start_Black_Tote... S9N2CB'}
           
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)