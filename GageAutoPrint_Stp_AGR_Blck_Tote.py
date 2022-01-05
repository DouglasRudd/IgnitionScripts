
# In addition to printing the Gage Tote-Tags, this script also (stops) or (flags) the AGR record in 
# the database as (complete) by providing the End Count values/data

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
                     'msgSource':'GageAutoPrint_Stp_AGR_Blck_Tote.GetGageFromPath OBOV88'}
			   
		system.db.runNamedQuery("Gages", "Debug/LogMsg", errParams)


try:

	if (initialChange == 1):  # 1 means this script may have been 'saved'  and that saving it generated the change event 
		quit()
	
	batchCount = int(newValue.getValue())
	GageID = GetGageFromPath(str(event.tagPath))
	 
	pathGageID = '[default]' + GageID + '/' + GageID   
	pathToTag = pathGageID + '/Gage/Count/Batch Target'  # [default]G11/G11/Gage/Count/Batch Target
	batchMax = int(system.tag.readBlocking([pathToTag])[0].value) # element [0] is the max value, full batch, full tote
	

	
	if batchCount != batchMax:
		quit()
	
	heatNum = system.tag.readBlocking([pathGageID + '/Database/WIP Details/Heat'])[0].value
	wipNum = system.tag.readBlocking([pathGageID + '/Scanner/Active Wip'])[0].value

	shortPartNum = system.tag.readBlocking([pathGageID + '/Gage/Running Part Number'])[0].value # returns 'G22-881'
	
	if (shortPartNum is None): shortPartNum = '000-000'  # sometimes shortPartNum is None?? (Why??), when this happens we need to set the part number to a value that will, at least, 
	                                                     # let it be written to the database instead of error ==> This is for the error ('NoneType' object has no attribute 'find')
	                                                     
	shortPartNum = shortPartNum[shortPartNum.find('-') + 1 : len(shortPartNum)] # gets the chars after the '-'
	longPartNum = system.db.runNamedQuery("Gages", "Printing/getLongPartNum", {'partNum':shortPartNum})
	
	user =  system.tag.readBlocking([pathGageID + '/Scanner/User'])[0].value
	skid_ID = system.tag.readBlocking([pathGageID + '/Skid/skid id'])[0].value
	hydroMachine = system.db.runNamedQuery("Gages", "Printing/getAsset", {'skidID':skid_ID}) 
	barCode = system.tag.readBlocking([pathGageID + '/Skid/skid name'])[0].value 
	
	seqNum = system.db.runNamedQuery("Printing/getToteTagsPrintedCount", {"p_skidID":skid_ID})
	seqNum += 1
	
	printerName = GageID
	
	# logDebugMsg(GageID, batchCount, longPartNum)
	

	rptParams = {'heat':heatNum,
				 'wip':wipNum,
				 'part':longPartNum,
				 'q':batchCount,
				 'user':user,
				 'Autogage':GageID,
				 'h':hydroMachine,   # param 'h' = hydromat = asset
				 'lp':barCode,
				 'seq':seqNum,
				 'shortLeft':'~',
				 'shortRight':'~'}
	
	system.report.executeAndDistribute(path = 'Tote Tag',
                                       project = 'Gages',
                                       action = 'print',
                                       parameters = rptParams,
                                       actionSettings = {"primaryPrinterName":printerName,"copies":1,"useAutoLandscape":'true','pageOrientation':"landscape"})

	system.db.runNamedQuery('Gages', 'Skid/addTote', {'wip':wipNum,
                                                      'skid':skid_ID,
                                                      't_stamp':system.date.now(),
                                                      'use':user,
                                                      'part_count':batchCount,
                                                      'tote_short':'N'})

# ==========================================================================================================
# =========Stop reject count record for (Black Tote)========================================================

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
	
	
	stopParams = {
				'MachTotalStop':Total,
				'GageID':GageID,
				'StopSTN_1':STN_1_Count,
				'StopSTN_2':STN_2_Count,
				'StopSTN_3':STN_3_Count,
				'StopSTN_4':STN_4_Count,
				'StopSTN_5':STN_5_Count,
				'StopSTN_6':STN_6_Count
				}
	
	# logDebugMsg('whiskey', 'a', 'a')
	system.db.runNamedQuery("Gages", "AGR_Counts/stop_AGR_black_tote", stopParams)
	# logDebugMsg('whiskey', 'b', 'b')

# =========Stop reject count record for (Black Tote)========================================================
# ==========================================================================================================
                                                      

except Exception as e:

	eParams = {'msgID':GageID + ', ' + heatNum,
             'message':getattr(e, 'message', repr(e)),
           'msgSource':'GageAutoPrint_Stp_AGR_Blck_Tote... S47AX59'}
           
	system.db.runNamedQuery("Gages", "Debug/LogMsg", eParams)