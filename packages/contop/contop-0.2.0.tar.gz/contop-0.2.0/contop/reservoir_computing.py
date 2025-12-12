
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from scipy.stats import binomtest
import numpy as np

from .core import normWindow, transformTS





def ExtractAllFeatures( TS_f, TS_r, patternSize = 3, numElements = 10 ):

    Features = []
    Class = []


    patterns = []
    for k in range( numElements ):
        ptn = np.random.uniform( 0.0, 1.0, ( patternSize ) )
        ptn = normWindow( ptn )
        patterns.append( ptn )


    for k in range( np.size( TS_f ) - patternSize ):
        Features.append( [] )
        Class.append( 0 )
        Features.append( [] )
        Class.append( 1 )

    for ptn in patterns:

        newTS_f = transformTS( TS_f, ptn )
        newTS_r = transformTS( TS_r, ptn )
        for k in range( np.size( TS_f ) - patternSize ):
            Features[ 2*k ].append( newTS_f[ k ] )
            Features[ 2*k + 1 ].append( newTS_r[ k ] )


    Features = np.array( Features )
    Class = np.array( Class )

    return patterns, Features, Class




def testingReservoirComputing( TS, TS_null, numPatterns: int = 100, embDim: int = 4, maxFeatures: int = 10 ):


    """
    Test assessing whether a time series, or set thereof, is the result of the same dynamical process as the one that generated a reference time series - which constitute the null hypothesis of the test. This assessment is done through a reservoir computing approach, in which multiple COPs are tested, and the results are used to train a Random Forest classification model.

    Parameters
    ----------
    TS : numpy.ndarray, or list
        Input time series, as a NumPy array, or list of multiple time series, to be analysed.
    TS_null : numpy.ndarray, or list
        Time series, or set thereof, used as null hypothesis for the test.
    numPatterns : int
        Number of random COPs that are tested. Optional, default: 100.
    embDim : int
        Embedding dimension, i.e. size of each COP. Optional, default: 4.
    maxFeatures : int
        Maximum number of features (i.e. of values obtained through COPs) that can be used at the same time in the Random Forest model. Optional, default: 10.

    Returns
    -------
    numpy.ndarray
        Set of COPs used to calculate the test.
    float
        p-value of the comparison. Results below a significance threshold (e.g. 0.01) indicate that the time series (or sets thereof) are different from those constituting the null model.
    float
        Statistic of the test, indicating how different are the time series. This distance corresponds to the accuracy of the classification performed by the Random Forest model, and is therefore defined between zero and one.

    Raises
    ------
    ValueError
        None.
    """

    patterns, Features, Class = ExtractAllFeatures( np.copy( TS ), TS_null, \
                                          embDim, \
                                          numPatterns )

    reorder = np.random.permutation( np.size( Class ) )
    Features = Features[ reorder, : ]
    Class = Class[ reorder ]

    clf = RandomForestClassifier( n_estimators = 1000, \
                                  max_depth = 2, max_features = maxFeatures, min_samples_split = 10 )

    kf = KFold( n_splits = 10, shuffle = True )
    scores = cross_val_score( clf, Features, Class, cv = kf )
    finalScore = np.mean( scores )

    numTrials = int( np.size( Features, 0 ) * 5 )
    numSuccesses = int( numTrials * finalScore )

    result = binomtest( numSuccesses, numTrials, \
                        p = 0.5, alternative = 'greater' )

    pV = result.pvalue
    stat = finalScore
    
    return patterns, pV, stat

