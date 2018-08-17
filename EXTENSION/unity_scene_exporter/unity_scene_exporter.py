#Unity Scene Exporter Dock

#Confirms There Are Layers in an Open Document.
#Takes Layers from Krita Based on Keywords.
#Removes Top Layers (Layers Outside Groups)
#Exports Keyworded Layers.
#Saves XML and Log files to be Used in an Unity Importer.

#Created By: Sean Francis

#BBD's Krita Script Starter Feb 2018

#############################################################

##########
#
# Using Statements
#
##########

import sys, os, datetime, pathlib
from PyQt5.QtWidgets import *
from krita import *
from PyQt5.QtCore import QStandardPaths, QSettings
import PyQt5.uic as uic

#############################################################

EXTENSION_ID = 'pykrita_unity_scene_exporter'
MENU_ENTRY = 'Unity Scene Exporter'
UI_FILE = "UnitySceneExporterUI.ui"

##########
#
# Gets and Loads the UI file
#
##########

def load_ui(ui_file):
	abs_path = os.path.dirname(os.path.realpath(__file__))
	ui_file = os.path.join(abs_path, UI_FILE)
	return uic.loadUi(ui_file)

class UnitySceneExporter(Extension):

	##########
	#
	# Global Variables
	#
	##########

	unityScene = ""
	keywords = {""}
	useBatchMode = False
	fileExtension = ""
	logExtension = ""
	xmlExtension = ""
	filepath = ""
	useFolders = True
	logFolder = ""
	kritaFolder = ""
	xmlFolder = ""
	exportFolder = ""
	logString = ""
	xmlString = ""
	needToExit = False
	layerKeyword  = ""
	doc = None

	##########
	#
	# Function Definitions
	#
	##########

	#########
	#
	# Adds a Time Stamp to stringToAdd
	# and Adds Created String to Log String
	#
	#########
	def AddToLog(self, stringToAdd):

		timeStamp = "[%s]: " % (datetime.datetime.now().strftime("%H:%M:%S"))
		string = timeStamp + stringToAdd + "\n"
		self.logString += string
		self.ui.logOutput.setPlainText(self.logString)

	##########
	#
	# Sets the unityScene variable
	# based on UI setting
	#
	##########

	def SetUnitySceneName(self):

		self.unityScene = self.ui.unitySceneLineEdit.text()
		tokenOutput = self.unityScene.split(" ")
		self.unityScene = ""
		i = 0
		for token in tokenOutput:
			i += 1
			self.unityScene += token
			if i != (len(tokenOutput)):
				self.unityScene += "_"
		self.AddToLog("Unity Scene Name is: " + self.unityScene)

	##########
	#
	# Sets the filepath variable
	# based on UI setting
	#
	##########

	def SetFilePath(self):
		self.filepath = self.ui.filepathLineEdit.text()
		if self.filepath[len(self.filepath) - 1] != "/" or self.filepath[len(self.filepath - 1)] != "\\":
			self.filepath += "/"

		self.AddToLog("Filepath is: " + self.filepath)

	##########
	#
	# Sets the useFolders variable
	# based on UI setting
	#
	##########

	def SetUseFolders(self):
		self.useFolders = self.ui.useFoldersCheckBox.isChecked()
		self.AddToLog("Use Folders is " + str(self.useFolders))

	##########
	#
	# Sets the useBatchMode variable
	# based on UI setting
	# Currently Does Not Work!
	#
	##########

	#def SetBatchMode(self):
		#self.useBatchMode = self.ui.useBatchModeCheckBox.isChecked()
		#self.AddToLog("Batch Mode is " + str(self.useBatchMode))

	##########
	#
	# Sets the folder variables
	# based on UI setting
	#
	##########

	def SetSubFolders(self):
		
		self.logFolder = self.ui.logFolderLineEdit.text()
		if self.logFolder[len(self.logFolder) - 1] != "/" or self.logFolder[len(self.logFolder - 1)] != "\\":
			self.logFolder = self.ui.logFolderLineEdit.text() + "/"
		else:
			self.logFolder = self.ui.logFolderLineEdit.text()
		self.AddToLog("Log Folder is: " + self.logFolder)
		
		self.xmlFolder = self.ui.xmlFolderLineEdit.text()
		if self.xmlFolder[len(self.xmlFolder) - 1] != "/" or self.xmlFolder[len(self.xmlFolder - 1)] != "\\":
			self.xmlFolder = self.ui.xmlFolderLineEdit.text() + "/"
		else:
			self.xmlFolder = self.ui.xmlFolderLineEdit.text()
		self.AddToLog("XML Folder is: " + self.xmlFolder)
		
		self.kritaFolder = self.ui.docFolderLineEdit.text()
		if self.kritaFolder[len(self.kritaFolder) - 1] != "/" or self.kritaFolder[len(self.kritaFolder - 1)] != "\\":
			self.kritaFolder = self.ui.docFolderLineEdit.text() + "/"
		else:
			self.kritaFolder = self.ui.docFolderLineEdit.text()
		self.AddToLog("Krita Document Folder is: " + self.kritaFolder)
		
		self.exportFolder = self.ui.exportFolderLineEdit.text()
		if self.exportFolder[len(self.exportFolder) - 1] != "/" or self.exportFolder[len(self.exportFolder - 1)] != "\\":
			self.exportFolder = self.ui.exportFolderLineEdit.text() + "/"
		else:
			self.exportFolder = self.ui.exportFolderLineEdit.text()
		self.AddToLog("Export Folder is: " + self.exportFolder)

	##########
	#
	# Sets the Keywords Based on
	# UI settings
	#
	##########

	def SetKeywords(self):
		self.keywords = self.ui.keywordsTextEdit.toPlainText().split(", ")
		i = 0
		for word in self.keywords:
			i += 1
			self.AddToLog("Keyword " + str(i) + " is " + word)

	##########
	#
	# Sets File Extensions Based on
	# UI settings
	#
	##########

	def SetExtensions(self):
		self.fileExtension = self.ui.exportExtensionLineEdit.text()
		if self.fileExtension[0] != ".":
			self.fileExtension = "." + self.ui.exportExtensionLineEdit.text()
		self.AddToLog("Export Image Extension is: " + self.fileExtension)

		self.xmlExtension = self.ui.xmlExtensionLineEdit.text()
		if self.xmlExtension[0] != ".":
			self.xmlExtension = "." + self.ui.xmlExtensionLineEdit.text()
		self.AddToLog("XML Extension is: " + self.xmlExtension)

		self.logExtension = self.ui.logExtensionLineEdit.text()
		if self.logExtension[0] != ".":
			self.logExtension = "." + self.ui.logExtensionLineEdit.text()
		self.AddToLog("Log Extension is: " + self.logExtension)

	#########
	#
	# Adds Layer Information to XML String
	#
	#########
	def AddToXML(self, layerName, layerFilePath, layerType, layerXPos, layerYPos):

		tokens = layerName.split("_")
		name = tokens[1]

		self.xmlString += "\t\t<Layer>\n\t\t\t<Name>" + str(name) + "</Name>"
		self.xmlString += "\n\t\t\t<Filename>" + str(layerName) + "</Filename>"
		self.xmlString += "\n\t\t\t<Path>" + str(layerFilePath) + "</Path>"
		self.xmlString += "\n\t\t\t<Type>" + str(layerType) + "</Type>"
		self.xmlString += "\n\t\t\t<Position>\n\t\t\t\t<X>" + str(layerXPos) + "</X>"
		self.xmlString += "\n\t\t\t\t<Y>" + str(layerYPos) + "</Y>\n\t\t\t</Position>\n"
		self.xmlString += "\t\t</Layer>\n"

	##########
	#
	# Creates Log File Name and Saves
	# The Log File Based On Save Settings
	#
	##########
	def SaveLogFile(self):

		savePath = ""
		logFile = None

		if self.useFolders is True:

			savePath = (self.filepath + self.logFolder + "log_%s" + self.logExtension) % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))
			logFile = open(savePath, "w+")
			logFile.write(self.logString)
			logFile.close()

		else:

			savePath = (self.filepath + "log_%s" + self.logExtension) % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))
			logFile= open(self.filepath + "log_" + self.logExtension, "w+")
			logFile.write(self.logString)
			logFile.close()

	#########
	#
	# Closes XML String and Saves String
	# to XML File
	#
	#########
	def SaveXMLFile(self):

		xmlFilePath = ""
		xmlFile = None

		self.xmlString += "\t</LayerCollection>\n</" + self.unityScene + ">"

		if self.useFolders is True:

			xmlFilePath = self.filepath + self.xmlFolder

		else:

			xmlFilePath = self.filepath

		xmlFile = open((xmlFilePath + "xml_%s" + self.xmlExtension) % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S")), "w+")
		xmlFile.write(self.xmlString)
		xmlFile.close()

	#########
	#
	# Checks That the Group Layer Contains
	# the Keyword With a Colon
	#
	#########
	def CheckKeyword(self, layerName):

		nameToCheck = layerName.lower()
		foundWord = False
		self.layerKeyword = ""

		self.AddToLog("Checking " + nameToCheck)

		for word in self.keywords:

			self.AddToLog("Check Keyword: " + word)

			if nameToCheck.find(word + ":") != -1:

				self.AddToLog("Group has Keyword - '" + word + "'")

				#Assumption is that if there is a better word that fits
				#the Layer Keyword, it is longer than any other that would be found
				#Example: Foreground vs. Ground
				if len(word) > len(self.layerKeyword) and self.layerKeyword != "":

					self.AddToLog("Final Keyword Changed to: " + word)
					self.layerKeyword = word
					foundWord = True

				elif self.layerKeyword == "":

					self.AddToLog("Final Keyword Set to: " + word)
					self.layerKeyword = word
					foundWord = True


		if foundWord is True:

			self.AddToLog("Final Keyword Found: " + self.layerKeyword)
			return True

		else:

			self.AddToLog("Found No Keyword in Group! Cannot Export it!")
			return False

	#########
	#
	# Merges and Exports Provided Layer
	#
	#########
	def ExportLayer(self, layerToExport, layerType):

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
			self.AddToLog("Merged " + str(mergeCount) + " Layer(s)")

		self.AddToLog("Confirming Successful Merge...")
		self.AddToLog("Getting Layer Size...")

		finalChild = children[0]

		size = finalChild.bounds()
		sizeW = size.width()
		sizeH = size.height()

		self.AddToLog("Size - W: " + str(sizeW) + " H: " + str(sizeH))
		self.AddToLog("Getting Position...")

		position = finalChild.position()
		posX = position.x()
		posY = position.y()

		self.AddToLog("Position - X: " + str(posX) + " Y: " + str(posY))
		self.AddToLog("Setting File Name...")

		fileName = finalChild.parentNode().name().replace(":", "_")
		fileName += "_exported%s" % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))

		self.AddToLog("Filename is: " + fileName)

		if self.useFolders is True:

			filePathToSave = self.filepath + self.exportFolder

		else:

			filePathToSave = self.filepath

		self.AddToLog("Saving " + fileName + " at: " + filePathToSave)
		fullPath = filePathToSave + fileName + self.fileExtension
		saved = finalChild.save(fullPath, sizeW, sizeH)

		if saved is False:

			self.AddToLog("Error! Saving Failed!")
			self.AddToLog("Layer Export Unsuccessful! Backing Out.")
			return False

		else:

			self.AddToLog("Save Successful...")
			self.AddToLog("Adding XML Data to XML File...")

			self.AddToXML(fileName, filePathToSave, self.layerKeyword, posX, posY)

			self.AddToLog("Add to XML Successful...")
			return True

	########
	#
	# Main Function of the Plugin
	# Called By Hitting Dock Button
	#
	########
	def StartSceneExport(self):

		self.logString = "Unity Scene Exporter Log [%s]\n\n" % (datetime.datetime.now().strftime("%m/%d/%Y"))

		self.AddToLog("Setting Data...")
		self.SetUnitySceneName()
		self.SetFilePath()
		self.SetUseFolders()
		if self.useFolders is True:
			self.SetSubFolders()
		self.SetKeywords()
		self.SetExtensions()
		#self.SetBatchMode()
		self.AddToLog("Data Set...")

		self.xmlString = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
		self.xmlString += "<" + self.unityScene + " xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\nxmlns:xsd=\"http://www.w3.org/2001/XMLSchema\">\n\t<LayerCollection>\n"

		#self.AddToLog("Checking if Folders Exist...")

		if self.useFolders is True:

			self.AddToLog("User Wishes to Use Folders...")

			self.AddToLog("Checking Log Folder...")
			pathlib.Path(self.filepath + self.logFolder).mkdir(parents=True, exist_ok=True)
			self.AddToLog("Full Log Filepath: " + (self.filepath + self.logFolder))

			self.AddToLog("Checking XML Folder...")
			pathlib.Path(self.filepath + self.xmlFolder).mkdir(parents=True, exist_ok=True)
			self.AddToLog("Full XML Filepath: " + (self.filepath + self.xmlFolder))

			self.AddToLog("Checking Export Folder...")
			pathlib.Path(self.filepath + self.exportFolder).mkdir(parents=True, exist_ok=True)
			self.AddToLog("Full Export Filepath: " + (self.filepath + self.exportFolder))

			self.AddToLog("Checking Document Folder...")
			pathlib.Path(self.filepath + self.kritaFolder).mkdir(parents=True, exist_ok=True)
			self.AddToLog("Full Log Filepath: " + (self.filepath + self.kritaFolder))

		else:

			self.AddToLog("User Wishes Not to Use Folders...")

			self.AddToLog("Checking Filepath...")
			pathlib.Path(self.filepath).mkdir(parents=True, exist_ok=True)

		self.AddToLog("Checking Folders Complete...")
		self.AddToLog("Attempting to Get the Active Document...")

		self.doc = Krita.instance().activeDocument()

		if self.doc is None:

			self.AddToLog("Error! Could Not Find Active Document! Backing Out.")
			self.SaveLogFile()

		else:

			self.AddToLog("Found Active Document...")
			#self.AddToLog("Setting Batch Mode for Document...")

			#if self.useBatchMode is True:

				#self.AddToLog("User Wishes to Use Batch Mode...")
				#self.doc.setBatchmode(True)

			#else:

				#self.AddToLog("User Wishes Not to Use Batch Mode...")
				#self.doc.setBatchmode(False)

			#self.AddToLog("Batch Mode Set...")
			self.AddToLog("Checking Document Layers...")
			layers = self.doc.topLevelNodes()

			if layers is None:

				self.AddToLog("Error! Found No Layers in Document! Backing Out.")
				self.SaveLogFile()

			else:

				self.AddToLog(("Found %d Layers...") % (len(layers)))
				self.AddToLog("Cloning Active Document: " + self.doc.name() + "...")
				cloned = self.doc.clone()

				if cloned is None:

					self.AddToLog("Error! Failed to Clone Active Document! Backing Out.")
					self.SaveLogFile()

				else:

					self.AddToLog("Clone Successful...")

					saveFilePath = ""

					if self.useFolders is True:

						saveFilePath = (self.filepath + self.kritaFolder + cloned.name() + "_" + "exported%s" + ".kra") % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))

					else:

						saveFilePath = (self.filepath + cloned.name() + "_" + "exported%s" + ".kra") % (datetime.datetime.now().strftime("%m%d%Y_%H%M%S"))

					self.AddToLog("Saving Clone at " + saveFilePath + "...")

					saved = cloned.saveAs(saveFilePath)

					if saved is False:

						self.AddToLog("Error! Failed to Save Document! Backing Out.")
						self.SaveLogFile()

					else:

						self.AddToLog("Save Successful...")
						self.AddToLog("Opening and Setting Active Document at " + saveFilePath + "...")

						self.doc = Krita.instance().openDocument(saveFilePath)

						Krita.instance().setActiveDocument(self.doc)

						if self.doc is None:

							self.AddToLog("Error! Opening and Setting Active Document Failed! Backing Out.")
							self.SaveLogFile()

						else:

							self.AddToLog("Open and Set Active Document Successful...")
							#self.AddToLog("Setting Batch Mode for Document...")

							#if self.useBatchMode is True:

								#self.AddToLog("User Wishes to Use Batch Mode...")
								#self.doc.setBatchmode(True)

							#else:

								#self.AddToLog("User Wishes Not to Use Batch Mode...")
								#self.doc.setBatchmode(False)

							#self.AddToLog("Batch Mode Set...")
							self.AddToLog("Getting Top Layers...")

							allLayers = self.doc.topLevelNodes()

							if allLayers is None:

								self.AddToLog("Error! Could Not Find Layers! Backing Out.")
								self.SaveLogFile()

							else:

								for layer in allLayers:

									if layer.type() != "grouplayer" and self.needToExit is False:

										self.AddToLog("Found Top Layer...")
										self.AddToLog("Top Layer Type: " + layer.type())
										self.AddToLog("Removing Layer...")

										removed = layer.remove()

										if removed is False:

											self.AddToLog("Error! Failed to Remove Layer! Backing Out.")
											self.SaveLogFile()
											self.needToExit = True
											break

										else:

											self.AddToLog("Removed Layer...")
											self.needToExit = False

								if self.needToExit is not True:

									self.AddToLog("Confirming Layer Removal...")

									allLayers = self.doc.topLevelNodes()

									for layer in allLayers:

										if layer.type() != "grouplayer":

											self.AddToLog("Error! Failed to Remove Top Layers! Some Remain! Backing Out.")
											self.SaveLogFile()
											self.needToExit = True
											break

									if self.needToExit is not True:

										self.AddToLog("Confirmed Layer Removal...")
										self.AddToLog("Getting Remaining Groups...")

										groups = self.doc.topLevelNodes()

										if groups is None:

											self.AddToLog("Error! No Groups in Document! Backing Out.")
											self.SaveLogFile()

										else:

											self.AddToLog("Exporting Layers...")

											for g in groups:

												self.AddToLog("Checking Keyword For Group - '" + g.name() + "'")
												found = self.CheckKeyword(g.name())

												if found is True:

													exported = self.ExportLayer(g, self.layerKeyword)

													if exported is True:

														self.AddToLog("Layer Export Successful...")

													else:

														self.SaveLogFile()
														self.needToExit = True
														break

											if self.needToExit is not True:

												self.AddToLog("Successfully Exported All Layers...")
												self.AddToLog("Saving XML File...")

												self.SaveXMLFile()

												self.AddToLog("Saving Log File...")

												self.SaveLogFile()

	def __init__(self, parent):
		#Always initialise the superclass, This is necessary to create the underlying C++ object
		super().__init__(parent)

	def setup(self):
		self.script_abs_path =  os.path.dirname(os.path.realpath(__file__))
		self.ui_file = os.path.join(self.script_abs_path,  UI_FILE)
		self.ui = load_ui(self.ui_file)

		self.ui.cancelButton.clicked.connect(self.cancel)
		self.ui.exportSceneButton.clicked.connect(self.StartSceneExport)

	def createActions(self, window):
		action = window.createAction(EXTENSION_ID, MENU_ENTRY, "tools/exporters")
		# parameter 1 =  the name that Krita uses to identify the action
		# parameter 2 = the text to be added to the menu entry for this script
		# parameter 3 = location of menu entry
		action.triggered.connect(self.action_triggered)

	def action_triggered(self):
		self.ui.show()
		self.ui.activateWindow()

	def cancel(self):
		self.ui.close()



# And add the extension to Krita's list of extensions:
app=Krita.instance()
extension=UnitySceneExporter(parent=app) #instantiate your class
app.addExtension(extension)
