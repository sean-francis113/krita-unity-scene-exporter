# Unity Scene Exporter For Krita
-------------------------------------------------

**Summary**

This script accesses the active document in Krita and makes sure that the document has layers in it. Once it sees that there is an active document and that it has layers, it will duplicate the document, rename it and save it to a specified location (set by the filepath, useFolders and documentFolder variables). Once it has successfully saved the document, it will then open and set active the cloned document. From there, it takes all of the top layers (the layers not inside of groups) and removes them completely. Then it goes through the rest of the layers (checking to see if there are any more layers), and merges the children of each group. After merging, it will export/save the merged layer to a specified location (set by the filepath, useFolders and exportFolder variables) with the specified extension (set by the fileExtension variable). After exporting the layer, it will then add information about the layer to an XML String. Once all of the layers have been exported properly, it will save the XML String into a XML File and the Log String into a Log File (its extension set by the logExtension variable).

-------------------------------------------------

**Notes**

*General*

Both the Standalone Script and Extension have been tested on Krita 4.1.1.

*Standalone Script*

Most of the global variables can be altered as needed by the user. Alterable variables are under the section labeled "Alter These Variables as Needed." These include the file extensions, file paths, and whether you wish to use a folder system or not.

The global variables that SHOULD NOT be altered are under the "Do Not Alter Below Variables!" section.

In order to use the Standalone Script:

1. Open Krita
2. Open the Scripter under 'Tools' -> 'Scripter'
3. Open the script by clicking 'File' -> 'Open'
4. Inside of the script, change the global variables as needed.
5. Run the script by hitting the 'Play' button

*Extension*

In order to use the extension:

1. Open Krita
2. Under 'Settings' -> 'Manage Resources...' click on 'Open Resource Folder'
3. This will open up a folder.
4. Find the 'pykrita' folder.
5. Paste/Insert the 'unity_scene_exporter' folder and 'unity_scene_exporter.desktop' file into the 'pykrita' folder.
6. Close and Reopen Krita.
7. Now, whenever you wish to use the Extension, click on 'Tools' -> 'Unity Scene Exporter'
8. This will open the UI Dialogue that you can then use to export the Unity Scene

Copyright: Sean Francis 2019
