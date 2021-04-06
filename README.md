BeamCenterFinder is a script based on the article "Beam focal spot position: The forgotten linac QA parameter. An EPID-based phantomless method for routine Stereotactic linac QA" by Jacek M. Chojnowski et al. DOI: 10.1002/acm2.12147. The idea is to find the actual position of the beam focal spot using different distances from target of X, Y jaws and MLC.
 
These distances were taken from the paper. Also, to obtain the values of distances to MLC and jaws you could go to beam configuration in your eclipse system. Open beam parameters and there you might find the values of distance of top and bottom surfaces from target so you can find the distance of middle of the jaw from target.



All the measurements could be performed in Service Dosimetry mode for beam alignment. To do that go to the XI tab, MV, Dosimetry. For MLC images you need to create a plan in Eclipse and export it to the folder on your dcf server. 



On Truebeam platform machine to obtain DICOM images from portal imager you need to go to XI tab in Service mode. On the second screen choose 4 filmed images for each session with SHIFT and export them to flash drive or any other way you like. You can put any filename, but choose the DICOM file format before exporting.



There are 2 files with script, one is for image processing and other is just a GUI. Also there is an exe file for those who don't want to install the python or have any other reason. Libraries dependencies: numpy, scipy, cv2, pydicom, tkinter.

After running the script choose a folder with 4 dicom images and press analyze. There is no need to specially name the files or anything else, at least for Varian Truebeam platform machines. Files are distinguished automatically by the jaws position, as their X coordinate will be larger for MLC plan than for a jaws-only plan. Resize factor for bicubic interpolation should be taken carefully because of the memory overflow.

Copyright (c) 2021- Alexey Popodko

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
