#### import the simple module from the paraview
from paraview.simple import *
import glob
import os
Path='/path/to/folder/'

'''
For Reddit:
In this script I had a problem where I wanted to extract x and y dimension slices from my dataset and
save them into a separate csv.

This code is crap and you can probably get paraview to print out code for you to compensate for my
bad coding BUT paraview will not print out the 'Resetsession' function which is important for HPC work!

What Resetsession does is it clears the RAM of your dataset. If you decide to just delete it instead,
some residual data will still remain in your RAM and eventually you will get RAM issues.

Make sure you use Resetsession!, it took me two weeks to find that simple five line code which was hidden
in the paraview mailing list.
'''


def file_extractor(filename,location,res)
    #Location For slice 1
    x1=3.6*(Resolution-1)
    y1=0.5*(Resolution-1)
    z1=0.5*(Resolution-1)
    #location for slice 2
    x2=3.6*(Resolution-1)
    y2=0.5*(Resolution-1)
    z2=0.5*(Resolution-1)
    #Iteration n
    n=0.045*Resolution
    # create a new 'XML Image Data Reader'
    volume000 = XMLImageDataReader(FileName=[filename])

    # create a new 'Slice'
    slice1 = Slice(Input=volume000)
    slice1.SliceType = 'Plane'
    slice1.SliceOffsetValues = [0.0]
    # init the 'Plane' selected for 'SliceType'
    slice1.SliceType.Origin = [x1, y1, z1]

    # Properties modified on slice1.SliceType
    slice1.SliceType.Normal = [0.0, 0.0, 1.0]


    for i in range(-2,3):
        # create a new 'Slice' name
        slice2 = Slice(Input=slice1)
        slice2.SliceType = 'Plane'
        slice2.SliceOffsetValues = [0.0]


        #CHANGE HERE
        # init the 'Plane' selected for 'SliceType'
        slice2.SliceType.Origin = [x2, y2+i*n, z2]

        # Properties modified on slice2.SliceType
        slice2.SliceType.Normal = [0.0, 1.0, 0.0]
        ff = str(filename)
        num=str(i)
        # save data
        SaveData(Path + '/data/dataRow' + ff + num  + '.csv', proxy=slice2, UseScientificNotation=1,
            WriteAllTimeSteps=1)
        # save data
        #### saving camera placements for all active views



    for j in range(-2,7):
        # create a new 'Slice' name
        slice3 = Slice(Input=slice1)
        slice3.SliceType = 'Plane'
        slice3.SliceOffsetValues = [0.0]


        #CHANGE HERE
        # init the 'Plane' selected for 'SliceType'
        slice3.SliceType.Origin = [Resolution*10*j*0.01+Resolution*0.36, y2, z2]

        # Properties modified on slice2.SliceType
        slice3.SliceType.Normal = [1.0, 0.0, 0.0]
        ff = str(filename)
        num=str(j)
        # save data
        SaveData(Path + '/data/Horizontal' + ff + num  + '.csv', proxy=slice3, UseScientificNotation=1,
            WriteAllTimeSteps=1)
        # save data
        #### saving camera placements for all active views
        Resetsession()

def Resetsession():
    pxm = servermanager.ProxyManager()
    pxm.UnRegisterProxies()
    del pxm
    disconnect()
    connect()

Resolution=100
os.chdir(Path)


for filename in glob.glob("*.vti"):
    file_extractor(filename,Path,Resolution)
    print(filename,"analysis complete")
