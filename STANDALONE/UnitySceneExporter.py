#Unity Scene Exporter
#Confirms There Are Layers in an Open Document.
#Takes Layers from Krita Based on Keywords.
#Removes Top Layers (Layers Outside Groups)
#Exports Keyworded Layers.
#Saves XML and Log files to be Used in an Unity Importer.

#Created By: Sean Francis

#############################################################

##########
#
# Using Statements
#
##########

from krita import *
import time
import datetime

#############################################################

##########
#
# Global Variables
#
##########

##########
#
# Alter These Variables as Needed
#
##########

unityScene = "UnityTestScene"
keywords = {"foreground", "backgroundscenery", "ground", "platform"}

fileExtension = ".png"
logExtension = ".txt"
xmlExtension = ".xml"

filepath = "C:/Users/seanf/Pictures/Digital Painting/kritaScriptTesting/"
useFolders = True;
logFolder = "log/"
kritaFolder = "kritaDocument/"
xmlFolder = "xml/"
exportedFolder = "export/"

############
#
# Do Not Alter Below Variables!
#
############

logString = "Unity Scene Exporter Log [%s]\n\n" % (datetime.datetime.now().strftime("%m/%d/%Y"))
xmlString = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
xmlString += "<" + unityScene + " xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\nxmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\n\t<LayerCollection>\n"
needToExit = False
layerKeyword = ""

#############################################################

#########
#
# Function Definitions
#
#########


#########
#
# Adds a Time Stamp to stringToAdd
# and Adds Created String to Log String
#
#########
def AddToLog(stringToAdd):

	global logString

	timeStamp = "[%s]: " % (datetime.datetime.now().strftime("%H:%M:%S"))
	string = timeStamp + stringToAdd + "\n"
	logString += string

	
#########
#
# Adds Layer Information to XML String
#
#########
def AddToXML(layerName, layerFilePath, layerType, layerXPos, layerYPos):

	global xmlString

	xmlString += "\t\t<Layer>\n\t\t\t<Name>" + layerName + "</Name>"
	xmlString += "\n\t\t\t<Path>" + layerFilePath + "</Path>"
	xmlString += "\n\t\t\t<Type>" + layerType + "</Type>"
	xmlString += "\n\t\t\t<Position>\n\t\t\t\t<X>" + layerXPos + "</X>"
	xmlString += "\n\t\t\t\t<Y>" + layerYPos + "</Y>\n\t\t\t</Position>\n"
	xmlString += "\t\t</Layer>\n"
	

##########
#
# Creates Log File Name and Saves
# The Log File Based On Save Settings
#
##########
def SaveLogFile():

	global logString
	global filepath
	global logFolder
	global logExtension
	global useFolders

	savePath = ""
	logFile = None
	
	if useFolders is True:
	
		savePath = (filepath + logFolder + "log_%s" + logExtension) % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))
		logFile = open(savePath, "w+")
		logFile.write(logString)
		logFile.close()
		
	else:
	
		savePath = (filepath + "log_%s" + logExtension) % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))
		logFile= open(filepath + "log_" + logExtension, "w+")
		logFile.write(logString)
		logFile.close()	
		
		
#########
#
# Closes XML String and Saves String
# to XML File
#
#########	
def SaveXMLFile():

	global xmlString
	global filepath
	global xmlFolder
	global xmlExtension
	global useFolders

	xmlFilePath = ""
	xmlFile = None

	xmlString += "\t</LayerCollection>\n</" + unityScene + ">"
	
	if useFolders is True:
	
		xmlFilePath = filePath + xmlFolder
		
	else:
	
		xmlFilePath = filePath
	
	xmlFile = open((xmlFilePath + "xml_%s" + xmlExtension) % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S")), "w+")
	xmlFile.write(xmlString)
	xmlFile.close()
	
	
#########
#
# Checks That the Group Layer Contains 
# the Keyword With a Colon
#
#########
def CheckKeyword(layerName):

	global keywords

	nameToCheck = layerName.lower()

	for word in keywords:
		
		if layerName.find(word + ":") != -1:
		
			AddToLog("Group has Keyword - '" + word + "'")
			return True
			
	AddToLog("Found No Keyword in Group! Cannot Export it!")
	return False
	
	
#########
#
# Merges and Exports Provided Layer
#
#########
def ExportLayer(layerToExport, layerType):

	global filepath
	global exportedFolder
	global fileExtension
	
	finalChild = None
	children = layerToExport.childNodes()
	childCount = len(children)
	mergeCount = 0	
	fileName = ""
	filePathToSave = ""
	fullPath = ""
	
	#While We Still Have Children To Merge
	while(mergeCount < childCount - 1):
		
		finalChild = children[0].mergeDown()
		mergeCount += 1
		AddToLog("Merged " + mergeCount + " Layer(s)")
		
	AddToLog("Confirming Successful Merge...")
	
	parent = finalChild.parentNode()
	
	children = parent.childNodes()
	
	if len(children) != 1:
		
		AddToLog("Error! Unsuccessful Merge!")
		AddToLog("Layer Export Unsuccessful! Backing Out.")
		return False
	
	else:
		
		AddToLog("Merge Successful...")
		AddToLog("Getting Layer Size...")
		
		size = finalChild.bounds()
		sizeW = size.width()
		sizeH = size.height()
		
		AddToLog("Size - W: " + sizeW + " H: " + sizeH)
		AddToLog("Getting Position...")
		
		position = finalChild.position()
		posX = position.x()
		posY = position.y()
		
		AddToLog("Position - X: " + posX + " Y: " + posY)
		AddToLog("Setting File Name...")
		
		fileName = finalChild.parentNode().name().replace(":", "_")
		fileName += "_exported%s" % (time.strftime("%Y%m%d_%H%M%S", time.gmtime()))
		
		AddToLog("Filename is: " + fileName)
		
		if useFolders is True:
		
			filePathToSave = filePath + exportedFolder
			
		else:
		
			filePathToSave = filePath
		
		
		AddToLog("Saving " + fileName + " at: " + filePathToSave)
		fullPath = filePathToSave + fileName + fileExtension
		saved = finalChild.save(fullPath, sizeW, sizeH)
		
		if saved is False:
		
			AddToLog("Error! Saving Failed!")
			AddToLog("Layer Export Unsuccessful! Backing Out.")
			SaveLogFile()
			return False
			
		else:
		
			AddToLog("Save Successful...")
			AddToLog("Adding XML Data to XML File...")
			
			AddToXML(fileName, filePathToSave, layerKeyword, posX, posY)
			
			AddToLog("Add to XML Successful...")
			AddToLog("Layer Export Successful...")
			return True
	
	
#############################################################	


############
#
# Start Script
#
############

AddToLog("Attempting to Get the Active Document...")

doc = Krita.instance().activeDocument()

if doc is None:

	AddToLog("Error! Could Not Find Active Document! Backing Out.")
	SaveLogFile()
	
else:

	AddToLog("Found Active Document...")
	AddToLog("Checking Document Layers...")	
	layers = doc.topLevelNodes()
		
	if layers is None:
	
		AddToLog("Error! Found No Layers in Document! Backing Out.")
		SaveLogFile()
		
	else:
	
		AddToLog("Found Layers...")
		AddToLog("Cloning Active Document...")
		cloned = doc.clone()
		
		if cloned is None:
		
			AddToLog("Error! Failed Cloning Active Document! Backing Out.")
			SaveLogFile()
			
		else:
		
			AddToLog("Clone Successful...")
			AddToLog("Saving Clone...")
			
			if useFolders is True:
			
				saveFilePath = filepath + kritaFolder + cloned.name() + "_" + "exported" + ".kra"
				
			else:
			
				saveFilePath = filepath + docToSave.name() + "_" + "exported" + ".kra"
			
			saved = cloned.saveAs(saveFilePath)
			
			if saved is False:
			
				AddToLog("Error! Failed to Save Document! Backing Out.")
				SaveLogFile()
				
			else:
			
				AddToLog("Save Successful...")
				AddToLog("Opening and Setting Active New Document...")
				
				doc = Krita.instance().setActiveDocument(Krita.instance().openDocument(saveFilePath))
				
				if doc is None:
				
					AddToLog("Error! Opening and Setting Active Document Failed! Backing Out.")
					SaveLogFile()
					
				else:
				
					AddToLog("Open and Set Active Document Successful...")
					AddToLog("Getting Top Layers...")
					
					allLayers = Krita.instance().topLevelNodes()
					
					if allLayers is None:
					
						AddToLog("Error! Could Not Find Layers! Backing Out.")
						SaveLogFile()
						
					else:
					
						for layer in allLayers:
							
							if layer.type() is not "grouplayer" and needToExit is False:
								
								AddToLog("Found Top Layer...")
								AddToLog("Removing Layer...")
								
								removed = layer.remove()
								
								if removed is False:
									
									AddToLog("Error! Failed to Remove Layer! Backing Out.")
									SaveLogFile()
									needToExit = True
									break
									
								else:
									
									AddToLog("Removed Layer...")
									
						if needToExit is not True:
													
							AddToLog("Confirming Layer Removal...")
						
							allLayers = Krita.instance().topLevelNodes()
						
							for layer in allLayers:
						
								if layer.type() is not "grouplayer":
							
									AddToLog("Error! Failed to Remove Top Layers! Some Remain! Backing Out.")
									SaveLogFile()
									needToExit = True									
									break
									
							if needToExit is not True:
							
								AddToLog("Confirmed Layer Removal...")								
								AddToLog("Getting Remaining Groups...")
								
								groups = Krita.instance().topLevelNodes()
								
								if groups is None:
								
									AddToLog("Error! No Groups in Document! Backing Out.")
									SaveLogFile()
								
								else:
								
									AddToLog("Exporting Layers...")
								
									for g in groups:
									
										AddToLog("Checking Keyword For Group - '" + g.name() + "'")
										found = CheckKeyword(g.name())
										
										if found is True:
										
											exported = ExportLayer(g)
											
											if exported is True:
											
												AddToLog("Layer Export Successful...")
												
											else:											
												
												SaveLogFile()
												needToExit = True
												
									if needToExit is not True:
									
										AddToLog("Successfully Exported All Layers...")
										AddToLog("Saving XML File...")
										
										SaveXMLFile()
										
										AddToLog("Saving Log File...")
										
										SaveLogFile()