import numpy as np
import struct
import warnings

def readRLS(fileName, *args):

    # Check if the fileName ends with .rls, add .rls otherwise
    if not fileName.endswith('.rls'):
        fileName += '.rls'

    # Initializing default values for optional parameters
    framesToSkip = 0
    framesToRead = None
    ROI = None
    dataSize = 1  # 1 is default for 'uint8'

    # Checking that inputs are in the correct format
    for iVar, arg in enumerate(args, start=1):
        if iVar < 3:
            rounded_arg = round(arg)
        if iVar == 1 and framesToSkip != rounded_arg:
            framesToSkip = rounded_arg
            warnings.warn('Rounding number of frames to nearest integer')
        elif iVar == 2 and framesToRead != rounded_arg and arg:
            framesToRead = rounded_arg
            warnings.warn('Rounding number of frames to nearest integer')
        elif iVar == 3:
            ROI = arg
            if np.shape(ROI) != (2, 2):
                raise ValueError(
                    'ROI format is incorrect, please check the matrix dimensions are:\n'
                    '[firstRow, lastRow;\n firstColumn, lastColumn]'
                )

    # Read the meta data
    with open(fileName, 'rb') as file:
        file.seek(0*1024)
        sizeX, sizeY, sizeT, sampling = struct.unpack('<QQQQ', file.read(32))
        version = file.read(4).decode()

        if version == 'Ver.':
            nVer = struct.unpack('<Q', file.read(8))[0]
            if nVer > 1:
                dataSize, = struct.unpack('<Q', file.read(8))
        print(dataSize)
        # Set default values based on meta data
        if ROI is None:
            ROI = [[1, sizeX], [1, sizeY]]
        if framesToRead is None:
            framesToRead = sizeT

        # Determine data type
        dt_lookup = {1: 'uint8', 2: 'uint16'}
        dataType = dt_lookup.get(dataSize)
        if dataType is None:
            raise ValueError('Unidentified data type')

        # Pre-allocate memory for arrays
        timeStamps = np.zeros(framesToRead, dtype=np.int64)
        data_shape = (ROI[0][1] - ROI[0][0] + 1, ROI[1][1] - ROI[1][0] + 1, framesToRead)

        data = np.zeros(data_shape, dtype=dataType)

        # Move to the first timeStamp/frame location
        firstByte = 30*1024 + sizeX*sizeY*np.uint64(framesToSkip)*dataSize + 8*np.uint64(framesToSkip)
        file.seek(int(firstByte))

        # Define dtype and itemsize
        dtype = np.dtype(dataType)
        itemsize = dtype.itemsize

        # Read data
        for t in range(framesToRead):
            timeStamps[t], = struct.unpack('<Q', file.read(8))
            frame_data = np.frombuffer(file.read(sizeY*sizeX*itemsize), dtype=dtype)
            frame = frame_data.reshape(sizeX, sizeY, order='C')
            data[:, :, t] = frame[ROI[0][0]-1:ROI[0][1], ROI[1][0]-1:ROI[1][1]]
        

    return data, sampling, timeStamps, sizeT
