	def printEnabled(recCount):
		
		return ((recCount > 0) == True) and (userIsAdmin() == True)

	def userIsAdmin():

		if (self.session.props.auth.authenticated == False):
			return False
	
		userRoles = str(self.session.props.auth.user.roles)
		userRoles = userRoles.upper()
	#		system.perspective.print(userRoles)
		return ((userRoles.find('Administrator'.upper()) > -1) or
				(userRoles.find('HR'.upper()) > -1) or
				(userRoles.find('Leader'.upper()) > -1) or
				(userRoles.find('Supervisor'.upper()) > -1))	
			# system.perspective.print('start: userIsAdmin')
		
		count = 0
		chkName = ''
	try:
	
	
		skidID = strFuncs.strRightNumChrs(self.view.params.skidname, 9)
		results = system.db.runNamedQuery("Printing/getToteReprintData", {"p_skidID":skidID})
	
		ToteReprint.labelCount = int(system.db.runNamedQuery("Printing/getToteTagsPrintedCount", {"p_skidID":skidID}))
	
		fld = ToteReprint.ReprintFields
		ToteReprint.qryResults = results
		ToteReprint.shortMark = ':Short'

#    ==========================================	
#    ==========================================

		count = 1
		while count <= 10:
			chkName = 'chk' + str(count)
			
			self.getChild(chkName).props.enabled = False
			self.getChild(chkName).props.style.opacity = .4
			self.getChild(chkName).props.text = 'No Data'
			
			count += 1

#    ==========================================	
#    ==========================================
	

		rec = 0	
		while rec < results.getRowCount():
	
			chkName = 'chk' + str(rec + 1)
			
			self.getChild(chkName).props.text = results.getValueAt(rec, fld.dateTime)
			self.getChild(chkName).props.enabled = True
			self.getChild(chkName).props.style.opacity = 1			 
			
			rec +=1
   
#    ==========================================
#    ==========================================   
   

		if results.getRowCount() > 0:

			self.getChild("ReportViewer").props.params.heat = results.getValueAt(0, fld.heat)
			self.getChild("ReportViewer").props.params.wip = results.getValueAt(0, fld.wip_ID)
			self.getChild("ReportViewer").props.params.part = results.getValueAt(0, fld.partRev)
			self.getChild("ReportViewer").props.params.q = results.getValueAt(0, fld.tote_part_count)
			self.getChild("ReportViewer").props.params.user = results.getValueAt(0, fld.userID)
			self.getChild("ReportViewer").props.params.Autogage = results.getValueAt(0, fld.gageName)
			self.getChild("ReportViewer").props.params.h = results.getValueAt(0, fld.asset)
			self.getChild("ReportViewer").props.params.lp = results.getValueAt(0, fld.barCode)
		
			
			if results.getValueAt(0, fld.short_tote) == 'Y':
				self.getChild("ReportViewer").props.params.shortLeft = ToteReprint.shortMark
				self.getChild("ReportViewer").props.params.shortRight = ToteReprint.shortMark
				
			else:
				self.getChild("ReportViewer").props.params.shortLeft = ''
				self.getChild("ReportViewer").props.params.shortRight = '.'
							
			self.getChild("ReportViewer").props.params.seq = ToteReprint.labelCount

		#	system.perspective.print('calling printEnabled')
		
		self.getChild("btnPrint").props.enabled = printEnabled(results.getRowCount())

#    ==========================================
#    ========================================== 
		
		count = 1
		while count <= 10:
			chkName = 'chk' + str(count)
			self.getChild(chkName).props.selected = False
			count += 1
		self.getChild("chk1").props.selected = True		
				
		
	except Exception as e:
		Debug.LogMessage('skidLook', getattr(e, 'message', repr(e)), 'Gages.Page/Embedded/Pops.skidLook F6BSAB')
		
	finally:
		pass