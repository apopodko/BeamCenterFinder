BeamCenterFinder is a script based on the article "Beam focal spot position: The forgotten linac QA parameter. An EPID-based phantomless method for routine Stereotactic linac QA" by Jacek M. Chojnowski et al. DOI: 10.1002/acm2.12147. The idea is to find the actual position of the beam focal spot using different distances from target of X, Y jaws and MLC.
 
These distances were taken from the paper. Also, to obtain the values of distances to MLC and jaws you could go to beam configuration in your eclipse system. Open beam parameters and there you might find the values of distance of top and bottom surfaces from target so you can find the distance of middle of the jaw from target.

![Open beam parameters](https://user-images.githubusercontent.com/81773641/113697626-1e48ef80-96dc-11eb-96f4-4b852811c071.PNG)

All the measurements could be performed in Service Dosimetry mode for beam alignment. To do that go to the XI tab, MV, Dosimetry. For MLC images you need to create a plan in Eclipse and export it to the folder on your dcf server. 

![XI Tab](https://user-images.githubusercontent.com/81773641/113697667-2f91fc00-96dc-11eb-9a5e-cb6513034e7d.png)

On Truebeam platform machine to obtain DICOM images from portal imager you need to go to XI tab in Service mode. On the second screen choose 4 filmed images for each session with SHIFT and export them to flash drive or any other way you like. You can put any filename, but choose the DICOM file format before exporting.

![Service mode export images](https://user-images.githubusercontent.com/81773641/113697689-34ef4680-96dc-11eb-99d9-321353683f81.png)

There are 2 files with script, one is for image processing and other is just a GUI. Also there is an exe file for those who don't want to install the python or have any other reason. Libraries dependencies: numpy, scipy, cv2, pydicom, tkinter.

After running the script choose a folder with 4 dicom images and press analyze. There is no need to specially name the files or anything else, at least for Varian Truebeam platform machines. Files are distinguished automatically by the jaws position, as their X coordinate will be larger for MLC plan than for a jaws-only plan. Resize factor for bicubic interpolation should be taken carefully because of the memory overflow.

<meta name="google-site-verification" content="qI6xJQcvhL-RTbhEOwlpai4jJIu0shVAf6rZU56H7u8" />
