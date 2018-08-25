#Unity Scene Exporter Dock
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
import datetime
import pathlib

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

useBatchMode = True

fileExtension = ".png"
logExtension = ".txt"
xmlExtension = ".xml"

filepath = "C:/Users/seanf/Pictures/DigitalPainting/kritaScriptTesting/"
useFolders = True;
logFolder = "test/log/"
kritaFolder = "test/kritaDocuments/"
xmlFolder = "test/xml/"
exportFolder = "test/export/"

############
#
# Do Not Alter Below Variables!
#
############

logString = "Unity Scene Exporter Log [%s]\n\n" % (datetime.datetime.now().strftime("%m/%d/%Y"))
xmlString = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
xmlString += "<UnityScene>\n\t<" + unityScene + ">\n\t\t<LayerCollection>\n"
needToExit = False
layerKeyword = ""
doc = None

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

	tokens = layerName.split("_")
	name = tokens[1]

	
	xmlString += "\t\t\t<Layer>\n\t\t\t\t<Name>" + str(name) + "</Name>"
	xmlString += "\n\t\t\t\t<Filename>" + str(layerName) + "</Filename>"
	xmlString += "\n\t\t\t\t<Path>" + str(layerFilePath) + "</Path>"
	xmlString += "\n\t\t\t\t<Type>" + str(layerType) + "</Type>"
	xmlString += "\n\t\t\t\t<Position>\n\t\t\t\t\t<X>" + str(layerXPos) + "</X>"
	xmlString += "\n\t\t\t\t\t<Y>" + str(layerYPos) + "</Y>\n\t\t\t\t</Position>\n"
	xmlString += "\t\t\t</Layer>\n"
	

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

	xmlString += "\t</LayerCollection>\n\t</" + unityScene + ">\n</UnityScene>"
	
	if useFolders is True:
	
		xmlFilePath = filepath + xmlFolder
		
	else:
	
		xmlFilePath = filepath
	
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
	global layerKeyword

	nameToCheck = layerName.lower()
	foundWord = False
	layerKeyword = ""
	
	AddToLog("Checking " + nameToCheck)

	for word in keywords:
		
		AddToLog("Check Keyword: " + word)
		
		if nameToCheck.find(word + ":") != -1:
		
			AddToLog("Group has Keyword - '" + word + "'")
			
			#Assumption is that if there is a better word that fits
			#the Layer Keyword, it is longer than any other that would be found
			#Example: Foreground vs. Ground
			if len(word) > len(layerKeyword) and layerKeyword != "":
							
				AddToLog("Final Keyword Changed to: " + word)
				layerKeyword = word
				foundWord = True
				
			elif layerKeyword == "":
				
				AddToLog("Final Keyword Set to: " + word)
				layerKeyword = word
				foundWord = True
			
		
	if foundWord is True:
		
		AddToLog("Final Keyword Found: " + layerKeyword)
		return True
			
	else:
	
		AddToLog("Found No Keyword in Group! Cannot Export it!")
		return False
	
	
#########
#
# Merges and Exports Provided Layer
#
#########
def ExportLayer(layerToExport, layerType):

	global filepath
	global exportFolder
	global fileExtension
	global doc
	
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
		AddToLog("Merged " + str(mergeCount) + " Layer(s)")
		
	AddToLog("Confirming Successful Merge...")
	AddToLog("Getting Layer Size...")
		
	finalChild = children[0]
		
	size = finalChild.bounds()
	sizeW = size.width()
	sizeH = size.height()
	
	AddToLog("Size - W: " + str(sizeW) + " H: " + str(sizeH))
	AddToLog("Getting Position...")
		
	position = finalChild.position()
	posX = position.x()
	posY = position.y()
		
	AddToLog("Position - X: " + str(posX) + " Y: " + str(posY))
	AddToLog("Setting File Name...")
	
	fileName = finalChild.parentNode().name().replace(":", "_")
	fileName += "_exported%s" % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))
	
	AddToLog("Filename is: " + fileName)
	
	if useFolders is True:
	
		filePathToSave = filepath + exportFolder
		
	else:
	
		filePathToSave = filepath
		
	AddToLog("Saving " + fileName + " at: " + filePathToSave)
	fullPath = filePathToSave + fileName + fileExtension
	saved = finalChild.save(fullPath, sizeW, sizeH)
	
	if saved is False:
	
		AddToLog("Error! Saving Failed!")
		AddToLog("Layer Export Unsuccessful! Backing Out.")
		return False
		
	else:
	
		AddToLog("Save Successful...")
		AddToLog("Adding XML Data to XML File...")
		
		AddToXML(fileName, filePathToSave, layerKeyword, posX, posY)
		
		AddToLog("Add to XML Successful...")
		return True
		
#############################################################	


############
#
# Start Script
#
############	

AddToLog("Checking if Folders Exist...")

if useFolders is True:
	AddToLog("User Wishes to Use Folders...")
	AddToLog("Checking Log Folder...")
	pathlib.Path(filepath + logFolder).mkdir(parents=True, exist_ok=True)
	AddToLog("Checking XML Folder...")
	pathlib.Path(filepath + xmlFolder).mkdir(parents=True, exist_ok=True)
	AddToLog("Checking Export Folder...")
	pathlib.Path(filepath + exportFolder).mkdir(parents=True, exist_ok=True)
	AddToLog("Checking Document Folder...")
	pathlib.Path(filepath + kritaFolder).mkdir(parents=True, exist_ok=True)

else:
	AddToLog("User Wishes Not to Use Folders...")
	AddToLog("Checking Filepath...")
	pathlib.Path(filepath).mkdir(parents=True, exist_ok=True)

AddToLog("Checking Folders Complete...")
AddToLog("Attempting to Get the Active Document...")

doc = Krita.instance().activeDocument()

if doc is None:

	AddToLog("Error! Could Not Find Active Document! Backing Out.")
	SaveLogFile()
	
else:

	AddToLog("Found Active Document...")
	AddToLog("Setting Batch Mode for Document...")

	if useBatchMode is True:

		AddToLog("User Wishes to Use Batch Mode...")
		doc.setBatchmode(True)
		
	else:
	
		AddToLog("User Wishes Not to Use Batch Mode...")
		doc.setBatchmode(False)
		
	AddToLog("Batch Mode Set...")
	AddToLog("Checking Document Layers...")	
	layers = doc.topLevelNodes()
		
	if layers is None:
	
		AddToLog("Error! Found No Layers in Document! Backing Out.")
		SaveLogFile()
		
	else:
	
		AddToLog(("Found %d Layers...") % (len(layers)))
		AddToLog("Cloning Active Document: " + doc.name() + "...")
		cloned = doc.clone()
		
		if cloned is None:
		
			AddToLog("Error! Failed to Clone Active Document! Backing Out.")
			SaveLogFile()
			
		else:
		
			AddToLog("Clone Successful...")
			
			saveFilePath = ""
			
			if useFolders is True:
			
				saveFilePath = (filepath + kritaFolder + cloned.name() + "_" + "exported%s" + ".kra") % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))
				
			else:
			
				saveFilePath = (filepath + cloned.name() + "_" + "exported%s" + ".kra") % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))
			
			AddToLog("Saving Clone at " + saveFilePath + "...")
			
			saved = cloned.saveAs(saveFilePath)
			
			if saved is False:
			
				AddToLog("Error! Failed to Save Document! Backing Out.")
				SaveLogFile()
				
			else:
			
				AddToLog("Save Successful...")
				AddToLog("Opening and Setting Active Document at " + saveFilePath + "...")
				
				doc = Krita.instance().openDocument(saveFilePath)
				
				Krita.instance().setActiveDocument(doc)
				
				if doc is None:
				
					AddToLog("Error! Opening and Setting Active Document Failed! Backing Out.")
					SaveLogFile()
					
				else:
				
					AddToLog("Open and Set Active Document Successful...")
					AddToLog("Setting Batch Mode for Document...")

					if useBatchMode is True:

						AddToLog("User Wishes to Use Batch Mode...")
						doc.setBatchmode(True)
		
					else:
	
						AddToLog("User Wishes Not to Use Batch Mode...")
						doc.setBatchmode(False)
		
					AddToLog("Batch Mode Set...")
					AddToLog("Getting Top Layers...")
					
					allLayers = doc.topLevelNodes()
					
					if allLayers is None:
					
						AddToLog("Error! Could Not Find Layers! Backing Out.")
						SaveLogFile()
						
					else:
					
						for layer in allLayers:
							
							if layer.type() != "grouplayer" and needToExit is False:
								
								AddToLog("Found Top Layer...")
								AddToLog("Top Layer Type: " + layer.type())
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
						
							allLayers = doc.topLevelNodes()
						
							for layer in allLayers:
						
								if layer.type() != "grouplayer":
							
									AddToLog("Error! Failed to Remove Top Layers! Some Remain! Backing Out.")
									SaveLogFile()
									needToExit = True									
									break
									
							if needToExit is not True:
							
								AddToLog("Confirmed Layer Removal...")								
								AddToLog("Getting Remaining Groups...")
								
								groups = doc.topLevelNodes()
								
								if groups is None:
								
									AddToLog("Error! No Groups in Document! Backing Out.")
									SaveLogFile()
								
								else:
								
									AddToLog("Exporting Layers...")
								
									for g in groups:
									
										AddToLog("Checking Keyword For Group - '" + g.name() + "'")
										found = CheckKeyword(g.name())
										
										if found is True:
										
											exported = ExportLayer(g, layerKeyword)
											
											if exported is True:
											
												AddToLog("Layer Export Successful...")
												
											else:											
												
												SaveLogFile()
												needToExit = True
												break
												
									if needToExit is not True:
									
										AddToLog("Successfully Exported All Layers...")
										AddToLog("Saving XML File...")
										
										SaveXMLFile()
										
										AddToLog("Saving Log File...")
										
										SaveLogFile()