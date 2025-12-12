from typing import List, Literal

import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, MaxAbsScaler, RobustScaler,
    QuantileTransformer, PowerTransformer, Normalizer, 
    KBinsDiscretizer, Binarizer, PolynomialFeatures, SplineTransformer
)
from scipy import signal
from scipy.fft import fft, rfft
from scipy.stats import skew, kurtosis
from pydantic import BaseModel

class DataItem(BaseModel):
    data: List[float]
    label: str

class DataSettings(BaseModel):
    input_axes: List[str]
    """List of input data axis names, e.g., ['x', 'y', 'z'] for accelerometer data"""
    output_class: List[str]
    """List of output classification labels, e.g., ['class1', 'class2']"""
    use_data_dot: int
    """Number of data points to use for model training"""
    time_interval: int
    """Global timing parameter - sampling interval in milliseconds"""

class FlattenSettings(BaseModel):
    enabled: bool
    SimpleImputer: bool
    strategy: Literal["mean", "median", "most_frequent", "constant"] = "constant"
    fill_value: float = 0.0
    StandardScaler: bool
    MinMaxScaler: bool
    MaxAbsScaler: bool
    RobustScaler: bool
    QuantileTransformer: bool
    n_quantiles: int = 100
    PowerTransformer: bool
    Normalizer: bool
    norm: Literal['l1', 'l2', 'max'] = 'l2'
    KBinsDiscretizer: bool
    n_bins: int = 5
    encode: Literal['onehot', 'onehot-dense', 'ordinal'] = 'ordinal'
    Binarizer: bool
    threshold: float = 0.0
    PolynomialFeatures: bool
    degree: Literal[2, 3] = 2
    SplineTransformer: bool
    n_knots: int = 5
    average: bool
    min: bool
    max: bool
    std: bool
    rms: bool
    skew: bool
    kurtosis: bool
    slope: bool
    var: bool
    mean: bool
    median: bool
    ptp: bool

class AnalysisSettings(BaseModel):
    enabled: bool
    stft: bool
    fs: float
    nperseg: int
    noverlap: int
    nfft: int
    fft: bool
    n: int
    rfft: bool

class FilterSettings(BaseModel):
    enabled: bool
    btype: Literal['low', 'high']
    Wn: float
    N: int
    fs: float

class PreprocessSettings(BaseModel):
    Flatten: FlattenSettings
    Analysis: AnalysisSettings
    Filter: FilterSettings
# ================ PREPROCESSING IMPLEMENTATION FUNCTIONS ================

def normalize_axis_length(data: np.ndarray, target_len: int, flatten_cfg: FlattenSettings) -> np.ndarray:
    """
    Normalize the length of input data to match the target length.
    
    This function ensures that the input data array has exactly the specified
    target length by either truncating or padding the data as needed.
    
    Args:
        data (np.ndarray): Input data array to normalize
        target_len (int): Target length for the output array
        flatten_cfg (FlattenSettings): Configuration settings containing padding options
        
    Returns:
        np.ndarray: Array with length equal to target_len
        
    Note:
        - If data is longer than target_len, it will be truncated
        - If data is shorter than target_len, it will be padded with fill_value
        - Fill value is determined by flatten_cfg settings
    """
    if len(data) > target_len:
        return data[:target_len]
    elif len(data) < target_len:
        fill = flatten_cfg.fill_value if flatten_cfg.SimpleImputer else 0.0
        return np.pad(data, (0, target_len - len(data)), constant_values=fill)
    return data

def apply_filter_to_axis(data: np.ndarray, fcfg: FilterSettings) -> np.ndarray:
    """
    Apply Butterworth digital filter to input signal data.
    
    This function applies a low-pass or high-pass Butterworth filter to the input
    signal using the specified filter configuration parameters.
    
    Args:
        data (np.ndarray): Input signal data to be filtered
        fcfg (FilterSettings): Filter configuration containing filter parameters
                              including cutoff frequency, filter order, and type
        
    Returns:
        np.ndarray: Filtered signal data with the same shape as input
        
    Note:
        - Uses second-order sections (SOS) format for numerical stability
        - Cutoff frequency is normalized against Nyquist frequency
        - Supports both low-pass and high-pass filtering
    """
    nyquist = fcfg.fs / 2
    if 0 < fcfg.Wn < nyquist:
        cutoff = fcfg.Wn / nyquist
    else:
        cutoff = fcfg.Wn  

    sos = signal.butter(fcfg.N, cutoff, btype=fcfg.btype, fs=fcfg.fs, output='sos')
    return signal.sosfilt(sos, data)

def apply_analysis_to_axis(data: np.ndarray, acfg: AnalysisSettings, target_length: int) -> np.ndarray:
    """
    Apply frequency domain analysis transformations to signal data.
    
    This function performs various frequency domain analyses including Short-Time
    Fourier Transform (STFT), Fast Fourier Transform (FFT), or Real FFT based
    on the analysis configuration settings.
    
    Args:
        data (np.ndarray): Input time-domain signal data
        acfg (AnalysisSettings): Analysis configuration specifying which transform to apply
        target_length (int): Expected length of input data for validation
        
    Returns:
        np.ndarray: Transformed data in frequency domain or original data if no analysis
        
    Raises:
        ValueError: If analysis parameters are invalid relative to target_length
        
    Note:
        - STFT returns flattened magnitude spectrogram
        - FFT returns magnitude spectrum
        - RFFT returns magnitude of real-valued FFT with fixed size of 32
        - Validates parameter constraints before processing
    """

    if acfg.stft:
        if acfg.nperseg > target_length:
            raise ValueError(f"STFT nperseg ({acfg.nperseg}) cannot be greater than target_length ({target_length})")
        if acfg.noverlap >= acfg.nperseg:
            raise ValueError(f"STFT noverlap ({acfg.noverlap}) must be less than nperseg ({acfg.nperseg})")
        if acfg.nfft < acfg.nperseg:
            raise ValueError(f"STFT nfft ({acfg.nfft}) must be >= nperseg ({acfg.nperseg})")

        _, _, Zxx = signal.stft(data, fs=acfg.fs,
                                nperseg=acfg.nperseg,
                                noverlap=acfg.noverlap,
                                nfft=acfg.nfft)
        return np.abs(Zxx).flatten()

    elif acfg.fft:
        if acfg.n > target_length:
            raise ValueError(f"FFT n ({acfg.n}) cannot be greater than target_length ({target_length})")
        return np.abs(fft(data, n=acfg.n))

    elif acfg.rfft:

        return np.abs(rfft(data,32))

    return data

def apply_flatten_to_axis(data: np.ndarray, fcfg: FlattenSettings) -> np.ndarray:
    """
    Apply comprehensive data preprocessing and feature extraction to signal data.
    
    This function applies a pipeline of data preprocessing steps including imputation,
    scaling, normalization, discretization, feature transformation, and statistical
    feature extraction based on the provided configuration settings.
    
    Args:
        data (np.ndarray): Input signal data to be processed
        fcfg (FlattenSettings): Configuration settings specifying which preprocessing
                               steps to apply and their parameters
        
    Returns:
        np.ndarray: Processed feature vector, either transformed raw data or
                   statistical features depending on configuration
        
    Note:
        - Applies preprocessing steps in a specific order for optimal results
        - Only one scaler is applied even if multiple are enabled (priority order)
        - Statistical features are computed if any stat option is enabled
        - Returns flattened array suitable for machine learning models
    """
    x = data.reshape(1, -1)

    if fcfg.SimpleImputer:
        x = SimpleImputer(strategy=fcfg.strategy, fill_value=fcfg.fill_value).fit_transform(x)
    
    scaler_applied = False
    if not scaler_applied and fcfg.StandardScaler:
        x = StandardScaler().fit_transform(x)
        scaler_applied = True
    if not scaler_applied and fcfg.MinMaxScaler:
        x = MinMaxScaler().fit_transform(x)
        scaler_applied = True
    if not scaler_applied and fcfg.MaxAbsScaler:
        x = MaxAbsScaler().fit_transform(x)
        scaler_applied = True
    if not scaler_applied and fcfg.RobustScaler:
        x = RobustScaler().fit_transform(x)
        scaler_applied = True

    if fcfg.QuantileTransformer:
        x = QuantileTransformer(n_quantiles=fcfg.n_quantiles).fit_transform(x)
    if fcfg.PowerTransformer:
        x = PowerTransformer().fit_transform(x)
    if fcfg.Normalizer:
        x = Normalizer(norm=fcfg.norm).fit_transform(x)
    if fcfg.KBinsDiscretizer:
        x = KBinsDiscretizer(n_bins=fcfg.n_bins, encode=fcfg.encode).fit_transform(x)
    if fcfg.Binarizer:
        x = Binarizer(threshold=fcfg.threshold).fit_transform(x)
    if fcfg.PolynomialFeatures:
        x = PolynomialFeatures(degree=fcfg.degree).fit_transform(x)
    if fcfg.SplineTransformer:
        x = SplineTransformer(degree=fcfg.degree, n_knots=fcfg.n_knots).fit_transform(x)

    x = x.flatten()

    stats_enabled = any([
        fcfg.average, fcfg.min, fcfg.max, fcfg.std, fcfg.rms,
        fcfg.skew, fcfg.kurtosis, fcfg.slope, fcfg.var,
        fcfg.mean, fcfg.median, fcfg.ptp
    ])

    if stats_enabled:
        feats = []
        if fcfg.average or fcfg.mean: feats.append(np.mean(x))
        if fcfg.min: feats.append(np.min(x))
        if fcfg.max: feats.append(np.max(x))
        if fcfg.std: feats.append(np.std(x))
        if fcfg.rms: feats.append(np.sqrt(np.mean(np.square(x))))
        if fcfg.skew: feats.append(skew(x))
        if fcfg.kurtosis: feats.append(kurtosis(x))
        if fcfg.slope:
            xi = np.arange(len(x))
            feats.append(np.polyfit(xi, x, 1)[0])
        if fcfg.var: feats.append(np.var(x))
        if fcfg.median: feats.append(np.median(x))
        if fcfg.ptp: feats.append(np.ptp(x))
        return np.array(feats)

    return x


def preprocess(data_list: List[DataItem], 
               data_settings: DataSettings, 
               preprocess_settings: PreprocessSettings) -> List[DataItem]:
    """
    Apply comprehensive preprocessing pipeline to multi-axis sensor data.
    
    This is the main preprocessing function that applies a complete data processing
    pipeline including filtering, frequency analysis, and feature extraction to
    multi-dimensional sensor data (e.g., accelerometer, gyroscope data with x,y,z axes).
    
    Args:
        data_list (List[DataItem]): List of data items containing raw sensor data
                                   and corresponding labels
        data_settings (DataSettings): Configuration for data structure including
                                     input axes, output classes, and data dimensions
        preprocess_settings (PreprocessSettings): Complete preprocessing configuration
                                                  including filter, analysis, and flatten settings
        
    Returns:
        List[DataItem]: List of processed data items with transformed features
                       maintaining original labels
        
    Processing Pipeline:
        1. Normalize raw data length to match expected dimensions
        2. Reshape data to separate individual axes (x, y, z, etc.)
        3. For each axis independently:
           - Normalize axis data length
           - Apply filtering (if enabled)
           - Apply frequency analysis (if enabled)  
           - Apply feature extraction/flattening (if enabled)
        4. Combine processed axes into final feature vector
        
    Note:
        - Maintains data order and labels throughout processing
        - Each axis is processed independently then recombined
        - Final output is flattened for machine learning compatibility
    """
    processed_data = []
    num_axes = len(data_settings.input_axes)
    target_length = data_settings.use_data_dot
    
    for idx, item in enumerate(data_list):
        raw = np.array(item.data, dtype=np.float32)
        
        expected_len = target_length * num_axes
        raw = normalize_axis_length(raw, expected_len, preprocess_settings.Flatten)


        reshaped = raw.reshape(-1, num_axes).T  

        transformed_axes = []
        for axis_data in reshaped:

            axis_data = normalize_axis_length(axis_data, target_length, preprocess_settings.Flatten)

            if preprocess_settings.Filter.enabled:
                axis_data = apply_filter_to_axis(axis_data, preprocess_settings.Filter)


            if preprocess_settings.Analysis.enabled:
                axis_data = apply_analysis_to_axis(axis_data, preprocess_settings.Analysis, target_length)


            if preprocess_settings.Flatten.enabled:
                axis_data = apply_flatten_to_axis(axis_data, preprocess_settings.Flatten)


            transformed_axes.append(axis_data)


        final = np.stack(transformed_axes, axis=1).reshape(-1)
        processed_data.append(DataItem(data=final.tolist(), label=item.label))

    return processed_data