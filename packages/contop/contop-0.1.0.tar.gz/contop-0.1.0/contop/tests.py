
import numpy as np

from .optimisation import optimiseRandom



def testingRandomness( TS, numPatterns: int = 100, embDim: int = 4 ):

    """
    Test assessing the random nature of a time series, or a set thereof. The time series composing the input are randomly shuffled, for then assessing the distance between the original version and the shuffled one. If the distance is not null, we can conclude that the underlying time series are not random.

    Parameters
    ----------
    TS : numpy.ndarray, or list
        Input time series, as a NumPy array, or list of multiple time series, to be analysed.
    numPatterns : int
        Number of random COPs that are tested. Optional, default: 100.
    embDim : int
        Embedding dimension, i.e. size of each COP. Optional, default: 4

    Returns
    -------
    numpy.ndarray
        COP resulting the the maximum difference between the two time series.
    float
        Best (i.e. smallest) p-value of the comparison. Results below a significance threshold (e.g. 0.01) indicate that the time series (or sets thereof) are different from their random counterparts, using the previously obtained COP; and therefore that are not random.
    float
        Statistic of the test, corresponding to the optimal p-value (as reported above); indicates the distance between the time series (or sets thereof), and their random counterpart.

    Raises
    ------
    ValueError
        None.
    """


    if type( TS ) == np.ndarray:

        TS_Null = np.random.permutation( TS )

    
    bestPattern, bestPValue, bestStatistic = \
        optimiseRandom( TS, \
                        TS_Null, \
                        numPatterns = numPatterns, \
                        embDim = embDim )

    return bestPattern, bestPValue, bestStatistic
