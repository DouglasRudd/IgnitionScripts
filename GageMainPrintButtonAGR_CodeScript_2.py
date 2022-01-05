def runAction(self, event):
	"""
	This event is fired when the 'action' of the component occurs.

	Arguments:
		self: A reference to the component that is invoking this function.
		event: An empty event object.
	"""
	
	try:
		
		
		GageID = "NA" # declare so the handler knows what it is

		Total = self.parent.parent.getChild("Tote Completion").custom.TotalPartCount
		GageID = self.view.params.machine
		
		STN_1_Count = self.parent.parent.getChild("Tote Completion").custom.AGR_St_1
		STN_2_Count = self.parent.parent.getChild("Tote Completion").custom.AGR_St_2
		STN_3_Count = self.parent.parent.getChild("Tote Completion").custom.AGR_St_3
		STN_4_Count = self.parent.parent.getChild("Tote Completion").custom.AGR_St_4
		STN_5_Count = self.parent.parent.getChild("Tote Completion").custom.AGR_St_5
		STN_6_Count = self.parent.parent.getChild("Tote Completion").custom.AGR_St_6
		
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
		
		startParams = {
					  'Mach_Total_Start':Total,
					  'GageID':GageID,
					  'Start_STN_1':STN_1_Count,
					  'Start_STN_2':STN_2_Count,
					  'Start_STN_3':STN_3_Count,
					  'Start_STN_4':STN_4_Count,
					  'Start_STN_5':STN_5_Count,
					  'Start_STN_6':STN_6_Count
					  }
		if AGR_Counts.blackToteIsFull == True:
			system.db.runNamedQuery("Gages", "AGR_Counts/stop_AGR_black_tote", stopParams)
			system.db.runNamedQuery("Gages", "AGR_Counts/start_AGR_black_tote", startParams)
		
		
		system.perspective.print(GageID)

		if AGR_Counts.redToteIsFull == True:
			system.db.runNamedQuery("Gages", "AGR_Counts/stop_AGR_red_tote", stopParams)
			system.db.runNamedQuery("Gages", "AGR_Counts/start_AGR_red_tote", startParams)
		
	except Exception as e:
		Debug.LogMessage(GageID, getattr(e, 'message', repr(e)), "Gage - Main print button's code XM3WSEZ5W8")
#		pass
	finally:
		AGR_Counts.blackToteIsFull = False
		AGR_Counts.redToteIsFull = False