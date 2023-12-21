import time
from lsFunctions import readRLS
import matplotlib.pyplot as plt

def get_frame(data, frame_number):
    """
    Extracts a specified frame from the 3D ndarray data.

    Parameters:
        data (ndarray): The 3D data array from which to extract the frame.
        frame_number (int): The index of the frame to extract.

    Returns:
        ndarray: The extracted 2D frame.
    """
    if frame_number >= data.shape[2] or frame_number < 0:
        raise ValueError("Invalid frame number. It should be between 0 and {}.".format(data.shape[2]-1))
    return data[:,:,frame_number]

def popup_frame(frame):
    """
    Pops up an interactive window displaying a 2D ndarray frame.

    Parameters:
        frame (ndarray): The 2D data frame to display.
    """
    plt.figure()
    plt.imshow(frame, cmap='gray')  # You can change the colormap if needed.
    plt.colorbar()
    plt.axis('off')  # to turn off axis numbers and ticks
    plt.show(block=True)  # block=True ensures the window stays open


def test_readRLS():
    path2numFive = "C:/Users/Alberto/OneDrive - Aarhus universitet/Skrivebord/github/data/dataFromNumberFive/20211213/baslerPulsatility/"
    nameFile = "20211213_4.rls"
    fileName = path2numFive + nameFile
    
    # Adjust the parameters as needed
    start_time_normal = time.time()
    data, sampling, timeStamps, sizeT = readRLS(fileName, 0, 200)
    print("Normal version: --- %s seconds ---" % (time.time() - start_time_normal))

    frame = get_frame(data, 1)
    popup_frame(frame)

    # Asserts or checks. For example:
    assert data is not None, "Data should not be None"
    assert len(timeStamps) == 200, "Expected 200 timestamps"

    print("All tests passed!")

if __name__ == "__main__":
    test_readRLS()
    
