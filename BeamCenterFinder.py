#BeamCenterFinder is a script based on the article "Beam focal spot position: The forgotten linac QA parameter. An EPID-based phantomless method for routine Stereotactic linac QA" 
#by Jacek M. Chojnowski et al. DOI: 10.1002/acm2.12147. The idea is to find the actual position of the beam focal spot using different distances from target to X, Y jaws and MLC.

#After running the script choose a folder with 4 dicom images and press analyze. There is no need to specially name the files or anything else, at least for Varian Truebeam platform machines. 
#Files are distinguished automatically by the jaws position, as their X coordinate will be larger for MLC plan than for a jaws-only plan.

#Copyright (c) 2021 Alexey Popodko

from pydicom import read_file
import os
import numpy as np
import scipy.ndimage
import scipy.interpolate
from cv2 import resize, INTER_CUBIC

def findcenter(PathDicom, Depi, Djaw, Dmlc, ResF):
    
    lstFilesDCM = []  # create an empty list
    for dirName, subdirList, fileList in os.walk(PathDicom):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                lstFilesDCM.append(os.path.join(dirName+'/'+filename))
    
    if lstFilesDCM == []:
        return('There are no DICOM files')
    
    # Get ref file
    RefDs = read_file(lstFilesDCM[0])            

    # Load dimensions based on the number of rows, columns, and number of portal images (along the Z axis)
    ConstPixelDims = (int(RefDs.Rows), int(RefDs.Columns), len(lstFilesDCM))

    # Load pixel size (in mm)
    PixelSize = (float(RefDs.ImagePlanePixelSpacing[0]), float(RefDs.ImagePlanePixelSpacing[1]))
    
    # The BeamCenter array [X and Y coordinates, Number of taken images]
    ArrayBeamCenters = np.empty((0, 3))
 
     # Define alpha coefficient
    a = np.zeros(2)
 
    # Loop through all the DICOM files and find in DICOM array beam centers
    for filenameDCM in lstFilesDCM:
        # read the file
        ds = read_file(filenameDCM)
        
        JawXPos = round(abs(ds.ExposureSequence[0].BeamLimitingDeviceSequence[0].LeafJawPositions[0]), 1)
        
        # Apply 3x3 median filter to the image
        MedianFltrIMG = scipy.ndimage.median_filter(ds.pixel_array, 3)
        
        # Scale filtered image to values between 0 and 1 where min pixel value is assigned to 0 and max value to 1
        MinFltrIMG = np.amin(MedianFltrIMG)
        MaxMFltrIMG = np.amax(MedianFltrIMG)
        NormIMG = (MedianFltrIMG - MinFltrIMG)/(MaxMFltrIMG - MinFltrIMG).astype(np.float32)
        
        # Resize the image with bicybic interpolation by a factor of ResF
        BinFltrIMG = resize(NormIMG, dsize = (ConstPixelDims[0]*ResF, ConstPixelDims[1]*ResF), interpolation=INTER_CUBIC) > 0.5
        
        # Find beam center and convert its X and Y values to int with rounding them
        BeamCenter = np.rint(np.asarray(scipy.ndimage.measurements.center_of_mass(BinFltrIMG)))
        ArrayBeamCenters = np.r_[ArrayBeamCenters, [np.append(BeamCenter, JawXPos)]]
    
    # Calculate result beam center shift at portal imager level and convert it to mm
    JawFieldPos = np.amin(ArrayBeamCenters[:,2])
    JawBeamCenter = ArrayBeamCenters[ArrayBeamCenters[:, 2] <= JawFieldPos].mean(axis = 0)[0:2]
    MLCBeamCenter = ArrayBeamCenters[ArrayBeamCenters[:, 2] > JawFieldPos].mean(axis = 0)[0:2]
    ResultShiftPortal = (JawBeamCenter - MLCBeamCenter) * PixelSize / ResF
        
    # Convert the shit to focal spot level in mm with an alpha factor for [X, Y] jaws
    a[0] = 1 / ((Depi - Djaw[0])/Djaw[0] - (Depi - Dmlc)/Dmlc)
    a[1] = 1 / ((Depi - Djaw[1])/Djaw[1] - (Depi - Dmlc)/Dmlc)    
    ResultFSpotShift = ResultShiftPortal * a
    
    print(np.flip(ResultFSpotShift))
    return np.flip(ResultFSpotShift)

if __name__ == '__main__':
    # Distance from the X‐ray target to the EPID
    Depi = 100.0 #For Truebeam
    # Distance from the X‐ray target to the jaws
    Djaw = [40.6, 31.9] #For Truebeam
    # Distance from the X‐ray target to the MLC
    Dmlc = 49.0 #For Truebeam
    # Image resize factor for bicubic interpolation
    ResF = 10 #Default
    findcenter('/Users/Admin/FolderName', Depi, Djaw, Dmlc, ResF)