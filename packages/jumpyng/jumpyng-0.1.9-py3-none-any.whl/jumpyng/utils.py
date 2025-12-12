# jumping utilities
# Standard library imports
import fnmatch
import gc
import json
import os
import random
from pathlib import Path

# Third-party imports
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_pdf import PdfPages
from scipy import signal, stats
import sklearn
import sklearn.neighbors
from sklearn.linear_model import LinearRegression
from tqdm.notebook import tqdm

# Set matplotlib parameters
matplotlib.rcParams['pdf.fonttype'] = 42


# function to find files
def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files: 
            if fnmatch.fnmatch(name,pattern): 
                result.append(os.path.join(root,name))
    # if len(result)==1:
    #     result = result[0]
    return result

def findSingle(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files: 
            if fnmatch.fnmatch(name,pattern): 
                result.append(os.path.join(root,name))
    if len(result)==1:
        return result[0]
    return None

def findFileStrings(substrings, path):
    #this version takes a list of strings and will find any file with all the strings in it in any order
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if all(sub.lower() in name.lower() for sub in substrings):
                result.append(os.path.join(root, name))
    
    if len(result) == 1:
        return result[0]
    else:
        return result

def findSinglePartial(parts, experiment_path, suffix=None):
    """
    Walk experiment_path and return the first file whose basename:
      • endswith(suffix) if suffix is given
      • and contains every substring in parts.
    """
    for root, _, files in os.walk(experiment_path):
        for fn in files:
            if suffix and not fn.endswith(suffix):
                continue
            if all(str(p) in fn for p in parts):
                return os.path.join(root, fn)
    return None

def truncate_float(number, decimals):
    factor = 10 ** decimals
    return int(number * factor) / factor

def xy_axis(ax):
    
    ### Removes the top and right bounding axes that are plotted by default in matplotlib
    
    ### INPUTS
    ### ax: axis object (e.g. from fig,ax = plt.subplots(1,1))
    
    ### OUTPUTS
    ### ax: the same axis w/top and right lines removed
    
    # Hide the right and top spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Only show ticks on the left and bottom spines
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')

    return ax


# function to interpolate over nans and median/box filter for DLC traces with low likelihood points set to nan
def interpolateMovement(arr):
    arr = pd.Series(arr).interpolate().to_numpy()
    arr = pd.Series(arr).fillna(method='bfill').to_numpy()
    # arr = signal.medfilt(arr,kernel_size = 5)
    # box_size = 5
    # box = np.ones(box_size) / box_size
    # arr = np.convolve(arr, box, mode='same')
    return arr

# function to load dlc datapoints into a pandas array from an h5 file
def load_dlc_h5(dlc_file):
    df = pd.read_hdf(dlc_file)
    df.columns = [' '.join(col[:][1:3]).strip() for col in df.columns.values]
    return df

# function to load dlc datapoints into a pandas array from an h5 file the applying interpolateMovement to the data
def load_dlc_h5_filter(dlc_file,like_thresh,pix_per_cm):
    df = pd.read_hdf(dlc_file)
    df.columns = [' '.join(col[:][1:3]).strip() for col in df.columns.values]
    keys = df.keys()

    for key in keys:
        if (' x' in key) | (' y' in key):
            likelihood = df[key[:-1] + 'likelihood'].to_numpy()
            trace = df[key].copy()
            trace[likelihood<like_thresh] = np.nan
            trace = interpolateMovement(trace)
            trace = trace/pix_per_cm
            df[key] = trace

    return df

def dlc_to_groupdf(df, experiment_path, save_path):
    # loads in all dlc pts, puts into dlc_df, saves to file

    row = df.iloc[0]  # load first row to get column names
    dlc_file = findFileStrings(
        [row['date'], row['subject'], row['condition'], 
         'TOP_%sDLC' % str(int(row['trial_num']-1)), 'filtered.h5'], 
        experiment_path
    )
    print(f"Initial DLC file is: {dlc_file}")

    # handle both string and list outputs
    if isinstance(dlc_file, list):
        if len(dlc_file) == 0:
            raise FileNotFoundError("No matching DLC file found for the first row.")
        dlc_path = dlc_file[0]
    else:
        dlc_path = dlc_file

    pts = pd.read_hdf(dlc_path)
    pts.columns = [' '.join(col[:][1:3]).strip() for col in pts.columns.values]
    dlc_df = pd.DataFrame(index=np.arange(len(df)), columns=pts.keys())

    for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing rows"):
        dlc_file = findFileStrings(
            [row['date'], row['subject'] + '_', row['condition'], 
             'TOP_%sDLC' % str(int(row['trial_num']-1)), 'filtered.h5'], 
            experiment_path
        )
        print(f"File is: {dlc_file}")

        if isinstance(dlc_file, list):
            if len(dlc_file) == 0:
                print(f"No matching DLC file found for {row['subject']} trial {row['trial_num']}")
                continue
            dlc_path = dlc_file[0]
        else:
            dlc_path = dlc_file

        pts = pd.read_hdf(dlc_path)
        pts.columns = [' '.join(col[:][1:3]).strip() for col in pts.columns.values]

        for column in pts:
            dlc_df.loc[index, column] = pts[column].to_numpy()

    df = pd.concat([df, dlc_df], axis=1)
    df.to_hdf(os.path.join(save_path, 'dlc_df.h5'), key='df')

    return df


#function to find the closest item in a vector to a given item (e.g., know the time of a jump, find the DLC point closest to that)
def find_first(item, vec):
    return np.argmin(np.abs(vec-item))

def aborts_as_failures(og_df):
    df = og_df.copy()
    df = df.astype({'outcome': 'int32'})#,'Distance_Jumped':np.float64})
    df.loc[df['outcome'] == 2, 'outcome'] = 0
    
    return df

def remove_aborts(og_df):
    df = og_df.copy()
    # df = df.astype({'outcome': 'int32'})#,'Distance_Jumped':np.float64})
    df = df[df['outcome']!=2]
    df.reset_index(inplace=True,drop=True)

    return df

def get_vidname_from_row(row,vid_path):
    name = str(row['date']) + '_' + row['subject'] + '_' + row['condition'] + '_' + 'TOP' + '_' + str(row['trial_num']-1) + '.avi'
    print('looking for file %s ' % name)
    vid_name = find(name,vid_path)
    return vid_name

def get_dlcname_from_row(row,vid_path):
    name = str(row['date']) + '_' + row['subject'] + '_' + row['condition'] + '_' + 'TOP' + '_' + str(row['trial_num']-1) + 'DLC_resnet50_masters jumping dataNov14shuffle1_1000000_filtered.h5'
    print('looking for file %s ' % name)
    dlc_name = find(name,vid_path)
    return dlc_name

def get_vid_frame(vid_name,n_frame):
    vid = cv2.VideoCapture(vid_name)
    vid.set(cv2.CAP_PROP_POS_FRAMES, n_frame)
    ret, frame_1 = vid.read()
    return frame_1

def get_gerbil_vidname_from_row(row, vid_path):
    name = f"{row['date']}_{row['subject']}_{row['sex']}_jumping_probe_yao_TOP_{int(row['trial_num'])-1}.avi"
    print('looking for file %s ' % name)
    vid_name = findSingle(name,vid_path)
    return vid_name


def _detect_video_syntax(experiment_path):
    """
    Detect the syntax of the experiment TOP .avi files in the given folder.
    Returns a format string like
      "date_subject_sex_jumping_condition_TOP_{trial}.avi"
    or
      "date_subject_condition_TOP_{trial}.avi"
    """
    # find any .avi in the folder
    avis = find("*.avi", experiment_path)
    if not avis:
        raise FileNotFoundError(f"No .avi files found in {experiment_path}")
    sample = os.path.basename(avis[0])
    # split at the trial placeholder
    prefix, _, trial_ext = sample.partition("_TOP_")
    parts = prefix.split("_")
    if len(parts) >= 4 and parts[2] in ("M", "F") and parts[3] == "jumping":
        fields = ["{date}", "{subject}", "{sex}", "jumping", "{condition}"]
    else:
        fields = ["{date}", "{subject}", "{condition}"]
    return "_".join(fields) + "_TOP_{trial}.avi"


def get_unambiguous_vidname_from_row(row, experiment_path):
    """
    Build and return the TOP .avi filename for a given dataframe row,
    using the detected experiment syntax and a partial‐match search.
    """
    syntax = _detect_video_syntax(experiment_path)
    trial = int(row["trial_num"]) - 1
    vid_pattern = syntax.format(
        date=row["date"],
        subject=row["subject"],
        sex=row.get("sex", ""),
        condition=row["condition"],
        trial=trial
    )
    print(f"looking for file {vid_pattern}")
    # split off the extension and use parts for a partial match
    parts = vid_pattern.replace(".avi", "").split("_")
    return findSinglePartial(parts, experiment_path, suffix=f"TOP_{trial}.avi")

#function to load Bonsai timestamps
def load_Bonsai_TS(file_name):
    TS_read = pd.read_csv(file_name, header=None)
    ts = list(TS_read[0])
    return ts

def hms_to_seconds(t):
    h = int(t.split(':')[0])
    m = int(t.split(':')[1])
    s = float(t.split(':')[2])
    return 3600*h + 60*m + s

def calculate_firing_rates(spike_times, event_times, window=(-1, 1), bin_size=0.05):
    bins = np.arange(window[0], window[1] + bin_size, bin_size)
    bin_centers = bins[:-1] + bin_size / 2
    firing_rates = np.zeros((len(event_times), len(bin_centers)))
    
    for i, event_time in enumerate(event_times):
        relevant_spikes = np.array([spike for spike in spike_times if event_time + window[0] <= spike <= event_time + window[1]])
        relative_spikes = relevant_spikes - event_time
        counts, _ = np.histogram(relative_spikes, bins=bins)
        firing_rates[i] = counts / bin_size
    
    return bin_centers, firing_rates

def plot_spike_and_rate(spike_times, event_times_1, event_times_2, neuron_n, window=(-1, 1), bin_size=0.05, pp=[]):
    ### returns a figure that plots a raster plot and a peth for spiking around two types of events for each cell in a recording (jump vs. abort)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(3,6), sharex=True)

    # Spike Raster Plot event 1
    for i, event_time in enumerate(event_times_1):
        relevant_spikes = [spike for spike in spike_times if event_time + window[0] <= spike <= event_time + window[1]]
        ax1.vlines(x=[spike - event_time for spike in relevant_spikes], ymin=i + 0.8, ymax=i + 1.2, color='c')

    bin_centers, firing_rates = calculate_smoothed_firing_rates(spike_times, event_times_1, window, bin_size, sigma=0.05)
    mean_rates_1 = np.nanmean(firing_rates, axis=0)
    stderr = np.nanstd(firing_rates, axis=0, ddof=1) / np.sqrt(firing_rates.shape[0])

    ax3.plot(bin_centers, mean_rates_1, color='c', label='outcome')
    ax3.fill_between(bin_centers, mean_rates_1 - stderr, mean_rates_1 + stderr, color='c', alpha=0.25)
    
    # Spike Raster Plot event 2
    for i, event_time in enumerate(event_times_2):
        relevant_spikes = [spike for spike in spike_times if event_time + window[0] <= spike <= event_time + window[1]]
        ax2.vlines(x=[spike - event_time for spike in relevant_spikes], ymin=i + 0.8, ymax=i + 1.2, color='m')

    bin_centers, firing_rates = calculate_smoothed_firing_rates(spike_times, event_times_2, window, bin_size, sigma=0.05)
    mean_rates_2 = np.nanmean(firing_rates, axis=0)
    stderr = np.nanstd(firing_rates, axis=0, ddof=1) / np.sqrt(firing_rates.shape[0])

    ax3.plot(bin_centers, mean_rates_2, color='m', label='abort')
    ax3.fill_between(bin_centers, mean_rates_2 - stderr, mean_rates_2 + stderr, color='m', alpha=0.25)
    ax3.set_xlabel('Time from event (s)')
    ax3.set_ylabel('Firing rate (sp/s)')
    ax3.legend(loc=1,fontsize=6)
    # ax3.set_title('%s %s' % (type(mean_rates_1),type(mean_rates_2)))
    ax1.set_ylabel('outcome #')
    ax2.set_ylabel('abort #')
    ax1.set_xlim(window)
    ax2.set_xlim(window)
    ax3.set_xlim(window)
    ax1.spines[['right', 'top']].set_visible(False)
    ax2.spines[['right', 'top']].set_visible(False)
    ax3.spines[['right', 'top']].set_visible(False)
    ax1.get_xaxis().set_visible(False)
    ax2.get_xaxis().set_visible(False)
    
    # ax1.set_title('Spike Raster Plot')

    fig.suptitle('neuron %s' % neuron_n)
    plt.tight_layout()
    if pp:
        pp.savefig(fig)
        plt.close(fig)

    return mean_rates_1, mean_rates_2



def jump_peth(main_path,pdf_path):
    ### generate a PDF and a pandas df for average PSTH around time of jump/abort

    ### inputs
    ### path: local path to the top experiment folder

    ### outputs
    ### none, writes a PDF file with plots and a h5 file with dataframe
    path = main_path + '\jumping'
    ephys_file = find('*ephys.bin',path)[0]
    print('doing file %s' % ephys_file)
    
    nChansTotal = 128  #number of ADC channels

    filename = Path(path) / ephys_file

    # Get total number of samples
    file_size = filename.stat().st_size

    # Calculate total number of samples and chunks
    nSampsTotal = file_size // (nChansTotal * 2)  # Each int16 takes 2 bytes
    print('%d samples in the ephys data' % nSampsTotal)

    adc_file = find('*IMU.bin',path)[0]
    print(adc_file)
    nChansTotal = 8  #number of ADC channels

    filename = Path(path) / adc_file

    # Get total number of samples
    file_size = filename.stat().st_size

    print('Calculate total number of samples and chunks')
    nSampsTotal = file_size // (nChansTotal * 2)  # Each int16 takes 2 bytes
    print('%d samples in the adc board data' % nSampsTotal)

    pdf_name = os.path.join(path,adc_file[:-7] + 'jumping.pdf')
    pdf_name = os.path.split(pdf_name)[-1]
    pp = PdfPages(os.path.join(pdf_path,pdf_name))

    # Assuming 'pathList' and 'fileList' are already defined, similar to your Matlab setup
    subChans = np.array([0,1])
    chunkSize = 4000000
    fnum = 0
    filename = Path(path) / adc_file

    # Get total number of samples
    file_size = filename.stat().st_size

    # Calculate total number of samples and chunks
    nSampsTotal = file_size // (nChansTotal * 2)  # Each int16 takes 2 bytes
    nChunksTotal = np.ceil(nSampsTotal / chunkSize)

    print('Opening the camTTL file and read data')
    with open(filename, 'rb') as f:
        # Read the data as int16 directly into a numpy array
        dat = np.fromfile(f, dtype=np.int16).reshape((nChansTotal, -1),order='F') #order matters here! default, C, did not work

    # Sub-channel selection (adjusting for Python's 0-based indexing)
    dat = dat[subChans, :]

    # Convert to double
    dat = dat.astype(np.float64)
    dat = dat - np.median(dat,axis=1,keepdims=True)
    dat.shape

    print('finding TTL threshold crossings')
    # Define the threshold
    threshold = 5000

    # Find where data crosses the threshold
    above_threshold = dat > threshold

    # Shift the above_threshold array by one to align it for edge detection
    shifted_above_threshold = np.roll(above_threshold, 1, axis=1)

    # Find rising edge: True (1) in 'above_threshold' and False (0) in 'shifted_above_threshold'
    rising_edges = np.logical_and(above_threshold, np.logical_not(shifted_above_threshold))

    # Get indices of rising edges
    rising_edge_indices = [np.where(rising_edges[channel])[0] for channel in range(dat.shape[0])]

    # # Remove the first index if it is 0 because rolling could create a false positive at the start
    # if rising_edge_indices.size > 0 and rising_edge_indices[0] == 0:
    #     rising_edge_indices = rising_edge_indices[1:]

    # Print or process the rising edge indices
    for i, indices in enumerate(rising_edge_indices):
        print(f"Indices of rising edges for channel {i+1}: {indices}")

    ephys_camframe_inds = rising_edge_indices.copy()
    print('plotting first and last ten crossings from each channel')
    st_ind = rising_edge_indices[0][0]-1000
    max_ind = st_ind + 5000
    end_ind = rising_edge_indices[0][-10]-1000
    nchan = dat.shape[0]
    fig, axs = plt.subplots(2,nchan,figsize=(nchan*3,5))
    for i in range(nchan):
        ax = axs[0,i]
        ax.plot(dat[i,st_ind:max_ind],'k')
        ax.plot(rising_edge_indices[i][rising_edge_indices[i]<max_ind]-st_ind,dat[i,rising_edge_indices[i][rising_edge_indices[i]<max_ind]],'ro')
        ax.set_title('camera %d first ten frame pulses' % i)
        ax = axs[1,i]
        ax.plot(dat[i,end_ind:],'k')
        ax.plot(rising_edge_indices[i][rising_edge_indices[i]>end_ind]-end_ind,dat[i,rising_edge_indices[i][rising_edge_indices[i]>end_ind]],'ro')
        ax.set_title('camera %d last ten frame pulses' % i)
    plt.tight_layout()
    pp.savefig(fig)
    plt.close(fig)

    print('getting jump/abort information')
    jump_frames_file = find('*frame_nums.txt',path)[0]
    cam_jumpframe_inds = pd.DataFrame(json.load(open(jump_frames_file)))
    print(jump_frames_file)
    print()

    ephys_dt = 1/30000

    # get list of times of aborts/successes based on TTL pulses from camera, using manually identified frame numbers
    abort_frames = cam_jumpframe_inds[cam_jumpframe_inds['event_type']=='abort']['event_time_side'].to_list()
    abort_times = [ephys_camframe_inds[1][abort_frames[i]] * ephys_dt for i in range(len(abort_frames))]

    success_frames = cam_jumpframe_inds[cam_jumpframe_inds['event_type']=='outcome']['event_time_side'].to_list()
    success_times = [ephys_camframe_inds[1][success_frames[i]] * ephys_dt for i in range(len(success_frames))]

    print('there are %d abort and %d outcome trials' % (len(abort_times),len(success_times)))

    # rand_idxs = random.sample(range(0, len(abort_times)), len(success_times))
    # abort_times = np.array(abort_times)[np.sort(rand_idxs)].tolist()
    # abort_frames = np.array(abort_frames)[np.sort(rand_idxs)].tolist()

    ephys_top_times = ephys_camframe_inds[0]*ephys_dt
    ephys_side_times = ephys_camframe_inds[1]*ephys_dt

    default_cv2_offset = -0.0174733877925064
    # default_cv2_drift_rate = +1.00016678
    # default_cv2_drift_rate = +0.99983325
    default_cv2_drift_rate = 1 # the bug in cv2 seems to be gone???

    success_times = np.array(success_times)*default_cv2_drift_rate+default_cv2_offset
    abort_times = np.array(abort_times)*default_cv2_drift_rate+default_cv2_offset

    print('loading ephys data')
    phy_file = find('*ephys_merge.json',path)[0]
    phy_df = pd.read_json(phy_file)
    # phy_file = find('*grat_ephys.h5',main_path)[0]
    # phy_df = pd.read_hdf(phy_file,key='df')
    good_cells = np.where(phy_df['group']=='good')[0]
    phy_df = phy_df.iloc[good_cells]
    n_cells = len(phy_df)
    print('there are %d good cells' % n_cells)

    print('plotting rasters and peths to PDF')
    jump_peth, abort_peth = ([] for i in range(2)) #jump_peth_gaus, abort_peth_gaus

    for index,row in phy_df.iterrows():
        try:
            spike_times = row['spikeT']
            print('plotting cell %d...' % index)
            mean_rates_1, mean_rates_2 = plot_spike_and_rate(spike_times, success_times, abort_times, 'cell ' + str(index), window=(-3,3),bin_size=0.05,pp=pp)
            print('appending PETHs')
            jump_peth.append(mean_rates_1)
            abort_peth.append(mean_rates_2)
            # print('appending guassian PETHs')
            # jump_peth_gaus.append(calc_kde_PSTH(spike_times, success_times, bandwidth=10, resample_size=1,edgedrop=15, win=(-3000,3000)))
            # abort_peth_gaus.append(calc_kde_PSTH(spike_times, abort_times, bandwidth=10, resample_size=1,edgedrop=15, win=(-3000,3000)))
            print('finished analyzing cell %d' % index)
        except Exception as e:
            print(f'Error plotting cell {index}: {e}')
            pass
        finally:
            plt.close('all')  # Ensure all figures are closed
            gc.collect()  # Force garbage collection
    pp.close()

    phy_df['jump_peth'] = jump_peth
    phy_df['abort_peth'] = abort_peth
    # phy_df['jump_peth_gaus'] = jump_peth_gaus
    # phy_df['abort_peth_gaus'] = abort_peth_gaus

    print('saving peths to file')
    phy_df.to_hdf(os.path.join(path,adc_file[:-7] + 'jumping.h5'),key='df')

    print('finished!')


from scipy.ndimage import gaussian_filter1d
#made using ChatGPT 8/6/25
def calculate_smoothed_firing_rates(spike_times, event_times, window=(-1, 1), bin_size=0.05, sigma=0.05):
    bins = np.arange(window[0], window[1] + bin_size, bin_size)
    bin_centers = bins[:-1] + bin_size / 2
    firing_rates = np.zeros((len(event_times), len(bin_centers)))
    spike_times = np.array(spike_times)
    for i, event_time in enumerate(event_times):
        relevant_spikes = spike_times[(spike_times >= event_time + window[0]) & (spike_times <= event_time + window[1])]
        relative_spikes = relevant_spikes - event_time
        counts, _ = np.histogram(relative_spikes, bins=bins)
        firing_rates[i] = counts / bin_size

    # Smooth each trial with a Gaussian kernel
    smoothed_rates = gaussian_filter1d(firing_rates, sigma=sigma/bin_size, axis=1)

    return bin_centers, smoothed_rates

# correct and save out labels, save psths
from scipy.interpolate import CubicSpline
def get_grating_preferences(main_path,pdf_path):
    #find the ephys spike time data
    grat_path = main_path + '\gratings'
    grat_ephys_file = find('*ephys_merge.json',grat_path)[0]

    #load the ephys spike time data
    grat_phy_df = pd.read_json(grat_ephys_file)
    grat_phy_df = grat_phy_df[grat_phy_df['group']=='good']
    print('there are %d good neurons' % len(grat_phy_df))

    # load the gratings onset times
    grat_times = pd.read_csv(find('*frameTS.csv',grat_path)[0],header=None)

    # load the stimulus parameters (row for each individual stimulus presentation)
    grat_params = pd.read_csv(find('*stimRec.csv',grat_path)[0])
    # grat_params = grat_params.drop([0]) #delete the first row bc it's just the initialization
    grat_params.reset_index(inplace=True,drop=True) #reset the dataframe inde
    print('there are %d onset times and %d parameter entries' %(len(grat_times),len(grat_params)))

    # get the first ephys timestamp and convert into seconds
    ephys_ts = pd.read_csv(find('*Ephys_BonsaiBoardTS.csv',grat_path)[0],header=None)
    ephys_1st_ts = hms_to_seconds(ephys_ts.iloc[0].to_list()[0])

    # convert all the stimulus timestamps to seconds
    grat_ts = np.array([hms_to_seconds(t) for t in grat_times[0].to_numpy()])

    # align grating onset times and ephys timestamps by subtracting them
    aligned_stim_ts = grat_ts-ephys_1st_ts

    # find the indices where the stimulus started at least 0.5s after the ephys recording started
    stim_inds = np.where((aligned_stim_ts)>0.5)[0]

    # apply those indices to the stimulus times and parameter dataframe (ignore stimuli before ephys recording started)
    aligned_stim_ts = aligned_stim_ts[stim_inds]
    aligned_grat_params = grat_params.iloc[stim_inds]
    aligned_grat_params.reset_index(inplace=True,drop=True) #reset the dataframe inde

    # get the unique stimulus parameters
    angles = np.unique(aligned_grat_params['angle'])
    sfs = np.unique(aligned_grat_params['sf'])
    tfs = np.unique(aligned_grat_params['tf'])

    print('orientations: ', angles)
    print('spatial frequencies: ', sfs)
    print('temporal frequencies: ', tfs)
    sfs_deg = [0.04, 0.08, 0.16, 0.32]

    angle_inds = []
    sf_inds = []
    tf_inds = []

    for angle in angles:
        angle_inds.append(np.where(aligned_grat_params['angle']==angle)[0])   

    for sf in sfs:
        sf_inds.append(np.where(aligned_grat_params['sf']==sf)[0])   

    for tf in tfs:
        tf_inds.append(np.where(aligned_grat_params['tf']==tf)[0])

    angle_degrees = (angles*57.2958)%360
    sorted_angle_degrees_indices = np.argsort(angle_degrees)
    sorted_angle_degrees = np.sort(angle_degrees)

    default_ephys_offset = -0.0174733877925064
    default_ephys_drift_rate = +1.00016678

    window=(-0.25, 1.25)
    bin_size=0.05
    event_times_1 = aligned_stim_ts

    angle_tuning_values_list = []
    angle_tuning_values_list_smooth = []
    sf_tuning_values_list = []
    sf_tuning_values_list_smooth = []
    tf_tuning_values_list = []
    tf_tuning_values_list_smooth = []

    pref_oris, pref_sfs, pref_tfs, cell_class, peths = ([] for i in range(5))

    # index = grat_phy_df.index[0]
    # row = grat_phy_df.iloc[index]

    pdf_name = grat_ephys_file[:-16] + 'gratings.pdf'
    pdf_name = os.path.split(pdf_name)[-1]    
    with PdfPages(os.path.join(pdf_path,pdf_name)) as pdf:
        for cnt,(index, row) in enumerate(grat_phy_df.iterrows()):
            print('doing neuron %s (%d of %d)' % (index,cnt,len(grat_phy_df)))
            spike_times = row['spikeT']

            corrected_spike_times = default_ephys_offset + np.array(spike_times) * default_ephys_drift_rate
            base=np.arange(0,6)
            resp = np.arange(6,16)

            fig, axs = plt.subplots(2,4,figsize=(12,6))
            axs = axs.ravel()

            ax = axs[0]
            # Spike Raster Plot event 1
            for i, event_time in enumerate(event_times_1):
                relevant_spikes = [spike for spike in corrected_spike_times if event_time + window[0] <= spike <= event_time + window[1]]
                ax.vlines(x=[spike - event_time for spike in relevant_spikes], ymin=i + 0.8, ymax=i + 1.2, color='k')
            ax.set_xlabel('time (s)')
            ax.set_ylabel('stim #')

            angle_tuning_values=[]
            conds = angles
            cond_inds = angle_inds
            ax = axs[1]
            for i,cond in enumerate(conds):
                bin_centers, firing_rates = calculate_smoothed_firing_rates(corrected_spike_times, event_times_1[cond_inds[i]], window, bin_size)
                mean_rates = np.mean(firing_rates, axis=0)
                stderr = np.std(firing_rates, axis=0, ddof=1) / np.sqrt(firing_rates.shape[0])

                ax.plot(bin_centers, mean_rates, label='%d deg' % cond)
                ax.fill_between(bin_centers, mean_rates - stderr, mean_rates + stderr, alpha=0.5)

                before_onset_avg = np.mean(mean_rates[:10])
                max_rate_onset  = np.mean(mean_rates[resp])
                diff_firing_rate = max_rate_onset - before_onset_avg
                angle_tuning_values.append(diff_firing_rate)
            ax.legend(handlelength=0,labelcolor='linecolor',fontsize=6)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('firing rate (sp/s)')
            #angles_converted = np.array([i/57.2958 for i in angles])
            sorted_angle_tuning_values = [angle_tuning_values[i] for i in sorted_angle_degrees_indices]
            angle_tuning_values_list.append(sorted_angle_tuning_values)

            
            cs = CubicSpline(sorted_angle_degrees, sorted_angle_tuning_values)
            # Generate smooth curve data
            angles_smooth = np.linspace(sorted_angle_degrees.min(), sorted_angle_degrees.max(), 300)
            angle_tuning_values_smooth = cs(angles_smooth)
            angle_tuning_values_list_smooth.append(angle_tuning_values_smooth)

            conds = sfs
            cond_inds = sf_inds
            sf_tuning_values = []
            ax = axs[2]
            for i,cond in enumerate(conds):
                bin_centers, firing_rates = calculate_smoothed_firing_rates(corrected_spike_times, event_times_1[cond_inds[i]], window, bin_size)
                mean_rates = np.mean(firing_rates, axis=0)
                stderr = np.std(firing_rates, axis=0, ddof=1) / np.sqrt(firing_rates.shape[0])

                ax.plot(bin_centers, mean_rates, label='%0.2f cpd' % sfs_deg[i])
                ax.fill_between(bin_centers, mean_rates - stderr, mean_rates + stderr, alpha=0.5)

                before_onset_avg = np.mean(mean_rates[base])
                max_rate_onset  = np.mean(mean_rates[resp])
                diff_firing_rate = max_rate_onset - before_onset_avg
                sf_tuning_values.append(diff_firing_rate)
            ax.legend(handlelength=0,labelcolor='linecolor',fontsize=6)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('firing rate (sp/s)')
            sf_tuning_values_list.append(np.array(sf_tuning_values))
            cs = CubicSpline(sfs, sf_tuning_values)

            # Generate smooth curve data
            sfs_smooth = np.linspace(sfs.min(), sfs.max(), 300)
            sf_tuning_values_smooth = cs(sfs_smooth)
            sf_tuning_values_list_smooth.append(sf_tuning_values_smooth)

            conds = tfs
            cond_inds = tf_inds
            tf_tuning_values = []
            ax = axs[3]
            for i,cond in enumerate(conds):
                bin_centers, firing_rates = calculate_smoothed_firing_rates(corrected_spike_times, event_times_1[cond_inds[i]], window, bin_size)
                mean_rates = np.mean(firing_rates, axis=0)
                stderr = np.std(firing_rates, axis=0, ddof=1) / np.sqrt(firing_rates.shape[0])
                
                ax.plot(bin_centers, mean_rates, label='%d Hz' % cond)
                ax.fill_between(bin_centers, mean_rates - stderr, mean_rates + stderr, alpha=0.5)

                before_onset_avg = np.mean(mean_rates[base])
                max_rate_onset  = np.mean(mean_rates[resp])
                diff_firing_rate = max_rate_onset - before_onset_avg
                tf_tuning_values.append(diff_firing_rate)
            ax.legend(handlelength=0,labelcolor='linecolor',fontsize=6)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('firing rate (sp/s)')
            tf_tuning_values_list.append(np.array(tf_tuning_values))
            cs = CubicSpline(tfs, tf_tuning_values)

            # Generate smooth curve data
            tfs_smooth = np.linspace(tfs.min(), tfs.max(), 300)
            tf_tuning_values_smooth = cs(tfs_smooth)
            tf_tuning_values_list_smooth.append(tf_tuning_values_smooth)

            ax = axs[4]
            pref_tf = np.argmax(tf_tuning_values)
            pref_sf = np.argmax(sf_tuning_values)
            pref_ori = np.argmax(angle_tuning_values)
            if np.max(tf_tuning_values)>1:
                cell_class.append('responsive')
            elif np.max(tf_tuning_values)<0:
                cell_class.append('suppressed')
            else:
                cell_class.append('unresponsive')

            pref_ori_inds = np.intersect1d(tf_inds[pref_tf],sf_inds[pref_sf])
            conds = angles
            cond_inds = angle_inds
            angle_tuning_values_pref = []
            for i,cond in enumerate(conds):
                bin_centers, firing_rates = calculate_smoothed_firing_rates(corrected_spike_times, event_times_1[np.intersect1d(pref_ori_inds,cond_inds[i])], window, bin_size)
                mean_rates = np.mean(firing_rates, axis=0)
                if i==pref_ori:
                    peths.append(mean_rates)
                before_onset_avg = np.mean(mean_rates[base])
                max_rate_onset  = np.mean(mean_rates[resp])
                diff_firing_rate = max_rate_onset - before_onset_avg
                angle_tuning_values_pref.append(diff_firing_rate)
            ax.plot(sorted_angle_degrees, angle_tuning_values_pref,color='k')
            ax.set_xlabel('orientation (deg)')
            ax.set_ylabel('evoked sp/s')
            ax.set_title('ori for pref sf/tf vals')

            ax = axs[5]
            ax.plot(sorted_angle_degrees, angle_tuning_values,color='k')
            # ax.plot(angles_smooth,angle_tuning_values_smooth,color='k')
            ax.set_xlabel('orientation (deg)')
            ax.set_ylabel('evoked sp/s')

            ax = axs[6]
            ax.plot(sfs_deg, sf_tuning_values,color='k')
            # ax.plot(sfs_smooth/57.2958, sf_tuning_values_smooth,color='k')
            ax.set_xlabel('sf (cpd)')
            ax.set_ylabel('evoked sp/s')

            ax = axs[7]
            ax.plot(tfs, tf_tuning_values,color='k')
            # ax.plot(tfs_smooth, tf_tuning_values_smooth,color='k')
            ax.set_xlabel('tf (Hz)')
            ax.set_ylabel('evoked sp/s')

            for i in range(8):
                axs[i].spines[['right', 'top']].set_visible(False)
            plt.suptitle('neuron %d %s ori=%d, sf=%0.2f, tf=%d' % (index, cell_class[cnt], angles[pref_ori], sfs_deg[pref_sf],tfs[pref_tf]))
            plt.tight_layout()
            pdf.savefig(fig)
            plt.close(fig)

            pref_oris.append(angles[pref_ori])
            pref_sfs.append(sfs_deg[pref_sf])
            pref_tfs.append(tfs[pref_tf])
        
    grat_phy_df['pref_ori'] = pref_oris
    grat_phy_df['pref_sf'] = pref_sfs
    grat_phy_df['pref_tf'] = pref_tfs
    grat_phy_df['grat_peth'] = peths
    grat_phy_df['grat_class'] = cell_class

    grat_phy_df.to_hdf(os.path.join(grat_path,pdf_name[:-3] + 'h5'),key='df')

    print('finished plotting and saving grating data')


#this code from dylan's pipeline (line 1786 in FME/fmEphys/utils/ephys.py)
def calc_kde_PSTH(spikeT, eventT, bandwidth=10, resample_size=1,edgedrop=15, win=(-0.25,1.5)):
    """Calculate PSTH for a single unit.

    The Peri-Stimulus Time Histogram (PSTH) will be calculated using Kernel
    Density Estimation by sliding a gaussian along the spike times centered
    on the event time.

    Because the gaussian filter will create artifacts at the edges (i.e. the
    start and end of the time window), it's best to add extra time to the start
    and end and then drop that time from the PSTH, leaving the final PSTH with no
    artifacts at the start and end. The time (in msec) set with `edgedrop` pads
    the start and end with some time which is dropped from the final PSTH before
    the PSTH is returned.

    Parameters
    ----------
    spikeT : np.array
        Array of spike times in seconds and with the type float. Should be 1D and be
        the spike times for a single ephys unit.
    eventT : np.array
        Array of event times (e.g. presentation of stimulus or the time of a saccade)
        in seconds and with the type float.
    bandwidth : int
        Bandwidth of KDE filter in units of milliseconds.
    resample_size : int
        Size of binning when resampling spike rate, in units of milliseconds.
    edgedrop : int
        Time to pad at the start and end, and then dropped, to eliminate edge artifacts.
    win : int
        Window in time to use in positive and negative directions. For win=1000, the
        PSTH will start -1000 ms before the event and end +1000 ms after the event.

    Returns
    -------
    psth : np.array
        Peri-Stimulus Time Histogram

    """

    # Unit conversions
    bandwidth = bandwidth / 1000
    resample_size = resample_size / 1000
    # win = win / 1000
    edgedrop = edgedrop / 1000
    edgedrop_ind = int(edgedrop / resample_size)

    bins = np.arange(win[0]-edgedrop, win[1]+edgedrop+resample_size, resample_size)

    # Timestamps of spikes (`sps`) relative to `eventT`
    relative_spike_times = np.array(spikeT)[:, None] - np.array(eventT)  # Shape (len(spikeT), len(eventT))
    mask = (relative_spike_times >= (win[0] - edgedrop)) & (relative_spike_times <= (win[1] + edgedrop))
    sps = relative_spike_times[mask].flatten()
    sps = np.array(sps)

    if len(sps) < 10:
        n_bins = int(((win[1]-win[0]) * 1000 * 2) + 1)
        return np.zeros(int((win[1]-win[0])*1000 + 1))

    kernel = sklearn.neighbors.KernelDensity(kernel='gaussian',
                                                bandwidth=bandwidth).fit(sps[:, np.newaxis])
    density = kernel.score_samples(bins[:, np.newaxis])

    # Multiply by the # spikes to get spike count per point. Divide
    # by # events for rate/event.
    psth = np.exp(density) * (np.size(sps ) / np.size(eventT))

    # Drop padding at start & end to eliminate edge effects.
    psth = psth[edgedrop_ind:-edgedrop_ind]

    return psth



def get_grat_pref(path,pdf_path):
    #find the ephys spike time data
    grat_path = path + '\gratings'
    grat_ephys_file = find('*ephys_merge.json',grat_path)[0]

    #load the ephys spike time data
    grat_phy_df = pd.read_json(grat_ephys_file)
    grat_phy_df = grat_phy_df[grat_phy_df['group']=='good']
    print('there are %d good neurons' % len(grat_phy_df))

    # load the gratings onset times
    grat_times = pd.read_csv(find('*frameTS.csv',grat_path)[0],header=None)

    # load the stimulus parameters (row for each individual stimulus presentation)
    grat_params = pd.read_csv(find('*stimRec.csv',grat_path)[0])
    grat_params = grat_params.drop([0]) #delete the first row bc it's just the initialization
    grat_params.reset_index(inplace=True,drop=True) #reset the dataframe inde
    print('there are %d onset times and %d parameter entries' %(len(grat_times),len(grat_params)))

    # get the first ephys timestamp and convert into seconds
    ephys_ts = pd.read_csv(find('*Ephys_BonsaiBoardTS.csv',grat_path)[0],header=None)
    ephys_1st_ts = hms_to_seconds(ephys_ts.iloc[0].to_list()[0])

    # convert all the stimulus timestamps to seconds
    grat_ts = np.array([hms_to_seconds(t) for t in grat_times[0].to_numpy()])

    # align grating onset times and ephys timestamps by subtracting them
    aligned_stim_ts = grat_ts-ephys_1st_ts

    #drift correction
    #slope = 0.9998727130759026

    #aligned_stim_ts= aligned_stim_ts*slope

    # find the indices where the stimulus started at least 0.5s after the ephys recording started
    stim_inds = np.where((aligned_stim_ts)>0.5)[0]

    # apply those indices to the stimulus times and parameter dataframe (ignore stimuli before ephys recording started)
    aligned_stim_ts = aligned_stim_ts[stim_inds]
    aligned_grat_params = grat_params.iloc[stim_inds]
    aligned_grat_params.reset_index(inplace=True,drop=True) #reset the dataframe inde

    # get the unique stimulus parameters
    angles = np.unique(aligned_grat_params['angle'])
    sfs = np.unique(aligned_grat_params['sf'])
    tfs = np.unique(aligned_grat_params['tf'])

    # print('orientations: ', angles)
    # print('spatial frequencies: ', sfs)
    # print('temporal frequencies: ', tfs)

    angle_inds, sf_inds, tf_inds = ([] for i in range(3))

    for angle in angles:
        angle_inds.append(np.where(aligned_grat_params['angle']==angle))

    for sf in sfs:
        sf_inds.append(np.where(aligned_grat_params['sf']==sf))

    for tf in tfs:
        tf_inds.append(np.where(aligned_grat_params['tf']==tf))

    default_ephys_offset = -0.0174733877925064
    default_ephys_drift_rate = +1.00016678

    pref_tf, pref_sf, pref_ori, vis_resp = ([] for i in range(4))

    pdf_name = os.path.join(grat_path,grat_ephys_file[:-10] + 'gratings_analysis.pdf')
    pdf_name = os.path.split(pdf_name)[-1]
    pp = PdfPages(os.path.join(pdf_path,pdf_name))

    for index,row in grat_phy_df.iterrows():

        spike_times = row['spikeT']
        corrected_spike_times = default_ephys_offset + np.array(spike_times) * default_ephys_drift_rate
        
        ev_rate_tf, ev_rate_sf, ev_rate_ori = ([] for i in range(3))
        
        fig, axs = plt.subplots(1,3,figsize=(9,3))

        ax = axs[0]
        for t,tf in enumerate(tfs):
            peth = calc_kde_PSTH(corrected_spike_times, aligned_stim_ts[tf_inds[t]], bandwidth=10, resample_size=1,edgedrop=15, win=(-0.25,1.5))
            ax.plot(np.arange(-0.25,1.5+0.001,0.001),peth,label='%d hz' % tf)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('firing rate (sp/s)')
            ax.set_title('SF')
            baseline=np.arange(200)
            evoked=np.arange(250,1250)
            ev_rate_tf.append(np.max(peth[evoked])-np.mean(peth[baseline]))
        ax.legend(fontsize=4)

        ax = axs[1]
        ev_rate_sf = []
        for t,tf in enumerate(sfs):
            peth = calc_kde_PSTH(corrected_spike_times, aligned_stim_ts[sf_inds[t]], bandwidth=10, resample_size=1,edgedrop=15, win=(-0.25,1.5))
            ax.plot(np.arange(-0.25,1.5+0.001,0.001),peth,label='%d cpd' % tf)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('firing rate (sp/s)')
            ax.set_title('TF')
            baseline=np.arange(200)
            evoked=np.arange(250,1250)
            ev_rate_sf.append(np.max(peth[evoked])-np.mean(peth[baseline]))
        ax.legend(fontsize=4)

        ax = axs[2]
        ev_rate_ori = []
        for t,tf in enumerate(angles):
            peth = calc_kde_PSTH(corrected_spike_times, aligned_stim_ts[angle_inds[t]], bandwidth=10, resample_size=1,edgedrop=15, win=(-0.25,1.5))
            ax.plot(np.arange(-0.25,1.5+0.001,0.001),peth,label='%d deg' % tf)
            ax.set_xlabel('time (s)')
            ax.set_ylabel('firing rate (sp/s)')
            ax.set_title('orientation')
            baseline=np.arange(200)
            evoked=np.arange(250,1250)
            ev_rate_ori.append(np.max(peth[evoked])-np.mean(peth[baseline]))
        ax.legend(fontsize=4)
        
        pref_tf.append(tfs[np.argmax(ev_rate_tf)])
        pref_sf.append(sfs[np.argmax(ev_rate_sf)])
        pref_ori.append(angles[np.argmax(ev_rate_ori)])
        if np.max([np.max(ev_rate_tf),np.max(ev_rate_sf),np.max(ev_rate_ori)])>3:
            vis_resp.append(True)
        else:
            vis_resp.append(False)
        
        plt.suptitle('cell %d prefered: tf %d, sf %0.2f, ori %d deg, vis resp:%d' % (index,pref_tf[-1],pref_sf[-1],pref_ori[-1],vis_resp[-1]))
        fig.tight_layout()
        pp.savefig(fig)
        plt.close(fig)

    grat_phy_df['pref_tf'] = pref_tf
    grat_phy_df['pref_sf'] = pref_sf
    grat_phy_df['pref_ori'] = pref_ori
    grat_phy_df['vis_resp'] = vis_resp

    grat_phy_df.to_hdf(grat_ephys_file[:-10] + 'grat_ephys.h5',key='df')
    pp.close()


def plot_performance_platforms(axs,og_df,condition,aborts,plt_min,plt_max,color_scheme,ls_list):#,save_pdf,pp):
    
    ### Plot outcome versus distance for two conditions as a function of the platforms
    
    ### INPUTS
    ### df: the dataframe containing all of the data
    ### condition: the key from df that you want to split the data into (e.g. 'ocular')
    ### plot_params: a dictionary of parameters including a colormap 'cm' and colors 'cond_cols'
    ### save_pdf: whether option was selected to save pdf
    ### pp: the pdf object (only necessary if saving PDF)
    
    ### OUTPUTS
    ### fig, ax: the figure and axes objects
    if aborts:
        df = aborts_as_failures(og_df)
    else:
        df = remove_aborts(og_df)
    # df = aborts_as_failures(og_df)
    anis = np.unique(df['subject'])
    dists = np.unique(df['distance'])
    conds = np.unique(df[condition])
    
    # fig, axs = plt.subplots(1,len(conds),figsize=(5*len(conds),5))
    if len(conds)>1:
        axs = axs.ravel()
    else:
        ax = axs

    for c,cond in enumerate(conds):
        anova_df = pd.DataFrame(columns=['distance','platform','outcome'])
        if len(conds)>1:
            ax = axs[c]
        for pl in range(1,4):
            jumpcurve = df[(df['platform_DLC']==pl)&(df[condition]==cond)].groupby(['distance','subject']).mean()
            # jumpcurve.reset_index(inplace=True)
            mnplot = jumpcurve.groupby(['distance']).mean()
            semplot = jumpcurve.groupby(['distance']).std()/np.sqrt(len(anis))
            mnplot.reset_index(inplace=True)
            semplot.reset_index(inplace=True)
            ax.errorbar(mnplot['distance'],
                         mnplot['outcome'],
                         yerr=semplot['outcome'],color=color_scheme[c],ls=ls_list[pl-1],label='platform %d' % pl,linewidth=1)
            for d,dist in enumerate(dists):
                temp_df = pd.DataFrame(columns=['distance','platform_DLC','Distance_Jumped'])
                temp_df['distance']  = pd.Series(np.repeat(dist,len(anis)))
                temp_df['platform_DLC'] = pd.Series(np.repeat(pl,len(anis)))
                temp_df['outcome'] = pd.Series(jumpcurve.xs(dist)['outcome'].to_numpy())
                anova_df = pd.concat([anova_df,temp_df],axis=0)

        ax.set_xlabel('gap distance (cm)')
        ax.set_ylabel('outcome rate')
        ax.set_xlim(plt_min,plt_max)
        # ax.set_xticks([10,15,20,25])
        # ax.set_xticks(np.arange(plt_min,plt_max+plt_min,plt_min))
        ax.set_ylim(0,1.1)
        
        # ax.set_title(cond)
        ax.set_xticks(np.arange(10, 30, step=5))
        ax.set_yticks(np.arange(0, 1.5, step=0.5))
        ax = xy_axis(ax)

        # #print anova results
        model = ols('outcome ~ C(distance) + C(platform_DLC) + C(distance):C(platform_DLC)', data=anova_df).fit()
        print(cond)
        print(sm.stats.anova_lm(model, typ=2))
        print('')
    # if len(anis)==1:
    #     fig.suptitle(anis[0])
    # # fig.tight_layout()

    # if save_pdf:
    #     pp.savefig(fig)
    #     plt.close(fig)
    ax.legend(fontsize=8,loc=3)

    return ax#fig, ax


def plot_jumpdist_platforms(axs,og_df,condition,plt_min,plt_max,color_scheme,ls_list):#,save_pdf,pp):
    
    ### Plot outcome versus distance for two conditions as a function of the platforms
    
    ### INPUTS
    ### df: the dataframe containing all of the data
    ### condition: the key from df that you want to split the data into (e.g. 'ocular')
    ### plot_params: a dictionary of parameters including a colormap 'cm' and colors 'cond_cols'
    ### save_pdf: whether option was selected to save pdf
    ### pp: the pdf object (only necessary if saving PDF)
    
    ### OUTPUTS
    ### fig, ax: the figure and axes objects
    df = remove_aborts(og_df)
    anis = np.unique(df['subject'])
    dists = np.unique(df['distance'])
    conds = np.unique(df[condition])

    # fig, axs = plt.subplots(1,len(conds),figsize=(5*len(conds),5))
    if len(conds)>1:
        axs = axs.ravel()
    else:
        ax = axs
        
    for c,cond in enumerate(conds):
        anova_df = pd.DataFrame(columns=['distance','platform_DLC','Distance_Jumped'])
        if len(conds)>1:
            ax = axs[c]
        for pl in range(1,4):
            jumpcurve = df[(df['platform_DLC']==pl)&(df['outcome']==1)&(df[condition]==cond)].groupby(['distance','subject']).mean()
            # jumpcurve.reset_index(inplace=True)
            mnplot = jumpcurve.groupby(['distance']).mean()
            semplot = jumpcurve.groupby(['distance']).std()/np.sqrt(len(anis))
            mnplot.reset_index(inplace=True)
            semplot.reset_index(inplace=True)
            semplot[np.isnan(semplot)]=0
            xvals = np.unique(mnplot['distance'])
            ax.errorbar(xvals,
                         mnplot['Distance_Jumped'],
                         yerr=semplot['Distance_Jumped'],label='platform %d' % pl,color=color_scheme[c],ls=ls_list[pl-1],linewidth=1)
            for d,dist in enumerate(dists):
                temp_df = pd.DataFrame(columns=['distance','platform_DLC','Distance_Jumped'])
                temp_df['distance']  = pd.Series(np.repeat(dist,len(anis)))
                temp_df['platform_DLC'] = pd.Series(np.repeat(pl,len(anis)))
                temp_df['Distance_Jumped'] = pd.Series(jumpcurve.xs(dist)['Distance_Jumped'].to_numpy())
                anova_df = pd.concat([anova_df,temp_df],axis=0)
        ax.set_xlabel('gap distance (cm)')
        ax.set_ylabel('distance jumped (cm)')
        ax.set_xlim(plt_min,plt_max)
        ax.set_ylim(plt_min,plt_max)
        ax.set_xticks([10,15,20,25])
        ax.set_yticks([10,15,20,25])
        # ax.set_xticks(np.arange(plt_min,plt_max+plt_min,plt_min))
        # ax.set_yticks(np.arange(plt_min,plt_max+plt_min,plt_min))
        # ax1.set_title('both bi/monocular')
        # locs, labels = plt.xticks(fontsize=10)
        # plt.xticks(np.arange(8, 32, step=4))
        # for pl in range(3):
        ax.plot(xvals,xvals,'k:')
        # ax.set_title(cond)
        ax = xy_axis(ax)

        try:
            #print anova results
            model = ols('Distance_Jumped ~ C(distance) + C(platform_DLC) + C(distance):C(platform_DLC)', data=anova_df).fit()
            print(cond)
            print(sm.stats.anova_lm(model, typ=2))
            print('')
        except:
            print('could not do anova bc nans')

    # if len(anis)==1:
    #     fig.suptitle(anis[0])
    # fig.tight_layout()

    # if save_pdf:
    #     pp.savefig(fig)
    #     plt.close(fig)
    ax.legend(fontsize=8,loc=4)  

    return axs#fig, axs


def plot_variable_vs_distance(ax,df,variable,condition,x_min,x_max,y_min,y_max,color_scheme,save_pdf,pp,suptitle=''):
    
    ### Plot outcome versus distance for two conditions
    
    ### INPUTS
    ### df: the dataframe containing all of the data
    ### condition: the key from df that you want to split the data into (e.g. 'ocular')
    ### plot_params: a dictionary of parameters including a colormap 'cm' and colors 'cond_cols'
    ### save_pdf: whether option was selected to save pdf
    ### pp: the pdf object (only necessary if saving PDF)
    
    ### OUTPUTS
    ### fig, ax: the figure and axes objects
    anis = np.unique(df['subject'])
    dists = np.unique(df['distance'])
    conds = np.unique(df[condition])
    # suc_lab = ['failure','outcome']

    # fig, axs = plt.subplots(1,len(conds),figsize=(2*len(conds),2))
    # axs = axs.ravel()
    # y_max=[]
    for c,cond in enumerate(conds):
        # stats_array = np.empty((len(anis),len(dists),2))
        # stats_array[:] = np.nan
        # anova_df = pd.DataFrame(columns=['distance','outcome',variable])

        # for suc in range(2):
        # jumpcurve = df[(df['outcome']==suc)&(df[condition]==cond)].groupby(['distance','subject']).mean()
        jumpcurve = df[(df[condition]==cond)].groupby(['distance','subject']).mean()
        # jumpcurve.reset_index(inplace=True)
        mnplot = jumpcurve.groupby(['distance']).mean()
        semplot = jumpcurve.groupby(['distance']).std()/np.sqrt(len(anis))
        mnplot.reset_index(inplace=True)
        semplot.reset_index(inplace=True)
        semplot[np.isnan(semplot)]=0
        xvals = np.unique(mnplot['distance'])
        # ax = axs[c]
        ax.errorbar(xvals,
                        mnplot[variable],
                        yerr=semplot[variable],label=cond,color=color_scheme[c],linewidth=1,zorder=c)
        jumpcurve.reset_index(inplace=True)            
        for ani in anis:
            ax.plot(jumpcurve[jumpcurve['subject']==ani]['distance'],jumpcurve[jumpcurve['subject']==ani][variable],'-',color=color_scheme[c],linewidth=0.25,alpha=0.5)
        ax.set_xlabel('gap distance (cm)')
        ax.set_ylabel(variable)
        ax.axis([x_min,x_max,y_min,y_max])
        ax.set_xticks(np.arange(10,30,5))
        # ax.set_ylim(plt_min,plt_max)
        # ax.set_yticks(np.arange(plt_min,plt_max+plt_max/4,plt_max/4))
        # y_max.append(np.ceil(np.max(mnplot[variable])))
        # ax.set_title(cond)
        # ax1.set_title('both bi/monocular')
        # locs, labels = plt.xticks(fontsize=10)
        # plt.xticks(np.arange(8, 32, step=4))
        # for pl in range(3):
        # ax.plot(xvals,xvals,'k:')
        ax = xy_axis(ax)

        #     for d,dist in enumerate(dists):
        #         try:
        #             stats_array[:,d,suc] = jumpcurve.xs(dist)[variable]
        #             temp_df = pd.DataFrame(columns=['distance','outcome',variable])
        #             temp_df['distance']  = pd.Series(np.repeat(dist,len(anis)))
        #             temp_df['outcome'] = pd.Series(np.repeat(suc,len(anis)))
        #             temp_df[variable] = pd.Series(jumpcurve.xs(dist)[variable].to_numpy())
        #             anova_df = pd.concat([anova_df,temp_df],axis=0)
        #         except:
        #             stats_array[:,d,suc] = np.repeat(np.nan,len(anis))
        #             temp_df = pd.DataFrame(columns=['distance','outcome',variable])
        #             temp_df['distance']  = pd.Series(np.repeat(dist,len(anis)))
        #             temp_df['outcome'] = pd.Series(np.repeat(suc,len(anis)))
        #             temp_df[variable] = pd.Series(np.repeat(np.nan,len(anis)))
        #             anova_df = pd.concat([anova_df,temp_df],axis=0)

        # #print anova results
        # try:
        #     model = ols('%s ~ C(distance) + C(condition) + C(distance):C(condition)' % variable, data=anova_df).fit()
        #     print(cond)
        #     print(sm.stats.anova_lm(model, typ=2))
        #     print('')
        # except:
        #     print('could not do anova due to nans')

        # for d,dist in enumerate(dists):
        #     fail = stats_array[:,d,0]
        #     suc = stats_array[:,d,1]
        #     fail = fail[~np.isnan(fail)]
        #     suc = suc[~np.isnan(suc)]
        #     s, p = stats.ttest_ind(fail,suc)
        #     print('distance %d, p=%0.3f' % (dist,p))
        # print('alpha=%0.3f' % (0.05/len(dists)))


    # if len(anis)==1:
    #     fig.suptitle(anis[0])
    # ax.legend(fontsize=10)
    # fig.tight_layout()
    # y_max = np.max(y_max)
    # y_min = 0
    # for c in range(len(conds)):
    #     axs[c].set_ylim(plt_min,plt_max)
    #     axs[c].set_yticks(np.arange(plt_min,plt_max+plt_max/4,plt_max/4))
        # axs[c].set_ylim(y_min,y_max)
        # axs[c].set_yticks(np.arange(y_min,y_max+y_max/4,y_max/4))

    # fig.suptitle(suptitle)
    # if save_pdf:
    #     pp.savefig(fig)
    #     plt.close(fig)
        
    return ax#fig, ax


def plot_variable_vs_distance_manipulation(axs,df,variable,condition,manipulation,x_min,x_max,y_min,y_max,color_scheme,save_pdf,pp,suptitle=''):
    
    ### Plot outcome versus distance for two conditions
    
    ### INPUTS
    ### df: the dataframe containing all of the data
    ### condition: the key from df that you want to split the data into (e.g. 'ocular')
    ### plot_params: a dictionary of parameters including a colormap 'cm' and colors 'cond_cols'
    ### save_pdf: whether option was selected to save pdf
    ### pp: the pdf object (only necessary if saving PDF)
    
    ### OUTPUTS
    ### fig, ax: the figure and axes objects
    anis = np.unique(df['subject'])
    dists = np.unique(df['distance'])
    conds = np.unique(df[condition])
    mans = np.unique(df[manipulation])

    axs = axs.ravel()
    # y_max=[]
    for c,cond in enumerate(conds):
        # stats_array = np.empty((len(anis),len(dists),2))
        # stats_array[:] = np.nan
        # anova_df = pd.DataFrame(columns=['distance','outcome',variable])
        ax = axs[c]
        for m,man in enumerate(mans):
            jumpcurve = df[(df[manipulation]==man)&(df[condition]==cond)].groupby(['distance','subject']).mean()
            # jumpcurve.reset_index(inplace=True)
            mnplot = jumpcurve.groupby(['distance']).mean()
            semplot = jumpcurve.groupby(['distance']).std()/np.sqrt(len(anis))
            mnplot.reset_index(inplace=True)
            semplot.reset_index(inplace=True)
            semplot[np.isnan(semplot)]=0
            xvals = np.unique(mnplot['distance'])
            
            ax.errorbar(xvals,
                         mnplot[variable],
                         yerr=semplot[variable],label='%s %s' % (manipulation,man),color=color_scheme[m],linewidth=1,zorder=c)
            jumpcurve.reset_index(inplace=True)            
            for ani in anis:
                ax.plot(jumpcurve[jumpcurve['subject']==ani]['distance'],jumpcurve[jumpcurve['subject']==ani][variable],':',color=color_scheme[m],linewidth=0.25,alpha=0.5)
        ax.set_xlabel('gap distance (cm)')
        ax.set_ylabel(variable)
        ax.set_xlim(x_min,x_max)
        ax.set_xticks(np.arange(10,30,5))
        ax.set_ylim(y_min,y_max)
        # ax.set_yticks(np.arange(plt_min,plt_max+plt_max/4,plt_max/4))
        # y_max.append(np.ceil(np.max(mnplot[variable])))
        # ax.set_title(cond)
        # ax1.set_title('both bi/monocular')
        # locs, labels = plt.xticks(fontsize=10)
        # plt.xticks(np.arange(8, 32, step=4))
        # for pl in range(3):
        # ax.plot(xvals,xvals,'k:')
        ax = xy_axis(ax)

        #     for d,dist in enumerate(dists):
        #         try:
        #             stats_array[:,d,suc] = jumpcurve.xs(dist)[variable]
        #             temp_df = pd.DataFrame(columns=['distance','outcome',variable])
        #             temp_df['distance']  = pd.Series(np.repeat(dist,len(anis)))
        #             temp_df['outcome'] = pd.Series(np.repeat(suc,len(anis)))
        #             temp_df[variable] = pd.Series(jumpcurve.xs(dist)[variable].to_numpy())
        #             anova_df = pd.concat([anova_df,temp_df],axis=0)
        #         except:
        #             stats_array[:,d,suc] = np.repeat(np.nan,len(anis))
        #             temp_df = pd.DataFrame(columns=['distance','outcome',variable])
        #             temp_df['distance']  = pd.Series(np.repeat(dist,len(anis)))
        #             temp_df['outcome'] = pd.Series(np.repeat(suc,len(anis)))
        #             temp_df[variable] = pd.Series(np.repeat(np.nan,len(anis)))
        #             anova_df = pd.concat([anova_df,temp_df],axis=0)

        # #print anova results
        # try:
        #     model = ols('%s ~ C(distance) + C(condition) + C(distance):C(condition)' % variable, data=anova_df).fit()
        #     print(cond)
        #     print(sm.stats.anova_lm(model, typ=2))
        #     print('')
        # except:
        #     print('could not do anova due to nans')

        # for d,dist in enumerate(dists):
        #     fail = stats_array[:,d,0]
        #     suc = stats_array[:,d,1]
        #     fail = fail[~np.isnan(fail)]
        #     suc = suc[~np.isnan(suc)]
        #     s, p = stats.ttest_ind(fail,suc)
        #     print('distance %d, p=%0.3f' % (dist,p))
        # print('alpha=%0.3f' % (0.05/len(dists)))


    # if len(anis)==1:
    #     fig.suptitle(anis[0])
    # ax.legend(fontsize=8)
    # fig.tight_layout()
    
    # y_max = np.max(y_max)
    # y_min = 0
    # for c in range(len(conds)):
    #     axs[c].set_ylim(plt_min,plt_max)
    #     axs[c].set_yticks(np.arange(plt_min,plt_max+plt_max/4,plt_max/4))
    #     # axs[c].set_ylim(y_min,y_max)
    #     # axs[c].set_yticks(np.arange(y_min,y_max+y_max/4,y_max/4))

    # fig.suptitle(suptitle)
    # if save_pdf:
    #     pp.savefig(fig)
    #     plt.close(fig)
        
    return axs#fig, ax


def plot_variable_vs_distance_manipulation(axs,df,variable,condition,manipulation,aborts,plt_min,plt_max,color_scheme,ylabel):#,save_pdf,pp,suptitle):
    ### Calculate and plot the jumping distance error given movement cluster k_clust at each distance

    ### INPUTS
    ### df: the dataframe with all of the data
    ### condition: the key from df that you want to split the data into (e.g. 'ocular')
    ### manipulation: e.g. laser, outcome etc.
    ### save_pdf: whether option was selected to save pdf
    ### pp: the pdf object (only necessary if saving PDF)

    ### OUTPUTS
    ### fig, ax: the figure and axes objects

    anis = np.unique(df['subject'])
    dists = np.unique(df['distance'])
    conds = np.unique(df[condition])

    # fig, axs = plt.subplots(1,len(conds),figsize=(len(conds)*5,5))
    # axs = axs.ravel()

    if aborts:
        temp_df = aborts_as_failures(df)
    else:
        temp_df = remove_aborts(df)

    for c,cond in enumerate(conds):
        ax = axs[c]
        for m,man in enumerate(np.unique(df[manipulation])):
            mn = temp_df[(df[manipulation]==man)&(df[condition]==cond)].groupby(['distance','subject']).mean(numeric_only=True)
            mnplot = mn.groupby(['distance']).mean(numeric_only=True)#apply(lambda x: np.mean(x))
            mnplot.reset_index(inplace=True)
            semplot = mn.groupby(['distance']).std(numeric_only=True)/np.sqrt(len(anis))#apply(lambda x: np.std(x)/np.sqrt(len(anis)))
            semplot.reset_index(inplace=True)
            try:
                ax.errorbar(mnplot['distance'],
                            mnplot[variable],
                            yerr=semplot[variable],
                            label=manipulation + ' %s' % man,
                            color=color_scheme[m],marker='o',linewidth=1,zorder=c) # this only works for manipulation having two types...
            except:
                pass
            mn.reset_index(inplace=True)
            for ani in anis:
                ax.plot(mn[mn['subject']==ani]['distance'],mn[mn['subject']==ani][variable],'-',color=color_scheme[m],linewidth=0.25,alpha=0.5)
        ax.set_xlabel('gap distance (cm)')
        ax.set_ylabel(ylabel)
        ax.set_title(cond)
        # ax.set_title(('%s ' +  manipulation) % cond)
        ax.set_xlim(plt_min,plt_max)
        # ax.set_ylim(0,1.1)
        # ax.legend(fontsize=10)
        # ax.set_xticks(np.arange(10,30,5))
        #         plt.yticks(np.arange(0, 1.5, step=0.5))
        ax = xy_axis(ax)

    # fig.suptitle(suptitle)

    # plt.tight_layout()

    # if save_pdf:
    #     pp.savefig(fig)
    #     plt.close(fig)

    return axs#fig, ax



def plot_jumpdist_manipulation(axs,df,condition,manipulation,plt_min,plt_max,color_scheme):
    ### Calculate and plot the jumping distance error given movement cluster k_clust at each distance

    ### INPUTS
    ### df: the dataframe with all of the data
    ### condition: the key from df that you want to split the data into (e.g. 'ocular')
    ### manipulation: e.g. laser, outcome etc.
    ### save_pdf: whether option was selected to save pdf
    ### pp: the pdf object (only necessary if saving PDF)

    ### OUTPUTS
    ### fig, ax: the figure and axes objects

    anis = np.unique(df['subject'])
    dists = np.unique(df['distance'])
    conds = np.unique(df[condition])

    # fig, axs = plt.subplots(1,len(conds),figsize=(len(conds)*3,3))
    axs = axs.ravel()

    temp_df = remove_aborts(df)
    for c,cond in enumerate(conds):
        ax = axs[c]
        ax.plot([plt_min,plt_max],[plt_min,plt_max],':',color=[0.5,0.5,0.5])
        for m,man in enumerate(np.unique(df[manipulation])):
            mn = temp_df[(df[manipulation]==man)&(df[condition]==cond)].groupby(['subject','distance']).mean(numeric_only=True)
            mnplot = mn.groupby(['distance']).mean(numeric_only=True)
            mnplot.reset_index(inplace=True)
            semplot = mn.groupby(['distance']).std(numeric_only=True)/np.sqrt(len(anis))
            semplot.reset_index(inplace=True)

            try:
                ax.errorbar(mnplot['distance'],
                            mnplot['Distance_Jumped'],
                            yerr=semplot['Distance_Jumped'],
                            label=manipulation + ' %s' % man,
                            color=color_scheme[m],linewidth=1,zorder=c) # this only works for manipulation having two types...
            except:
                pass
            mn.reset_index(inplace=True)
            for ani in anis:
                ax.plot(mn[mn['subject']==ani]['distance'],mn[mn['subject']==ani]['Distance_Jumped'],'-',color=color_scheme[m],linewidth=0.25,alpha=0.5)
        ax.set_xlabel('gap distance (cm)')
        ax.set_ylabel('distance jumped (cm)')
        ax.set_title(cond)
        # ax.set_title(('%s ' +  manipulation) % cond)
        # ax.set_xlim(plt_min,plt_max)
        # ax.set_ylim(plt_min,plt_max)
        # ax.legend(fontsize=10)
        # plt.xticks(np.arange(10, 30, step=5))
        # plt.yticks(np.arange(10, 30, step=5))
        ax = xy_axis(ax)

    # fig.suptitle(suptitle)

    # plt.tight_layout()

    # if save_pdf:
    #     pp.savefig(fig)
    #     plt.close(fig)

    return axs

def create_short_video_clip_avi(vidFilePath, startTimeSeconds, vidLengthSeconds):
    #split the vidfile into the path name and video name
    base_dir, vidname = os.path.split(vidFilePath)

    # #change the working directory to where the video lives
    # os.chdir(base_dir)

    #"open" the video
    vid = cv2.VideoCapture(vidFilePath)

    #get the width, height, framerate and total number of frames for the video
    frame_width = int(vid.get(3))
    frame_height = int(vid.get(4))
    fps = vid.get(cv2.CAP_PROP_FPS)
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

    #create a new video file to output the clip
    out = cv2.VideoWriter(os.path.join(base_dir,vidname[:-4]+ '_clip.avi'),cv2.VideoWriter_fourcc('M','J','P','G'), fps,(frame_width,frame_height))

    #calculate the frames we need to grab to make the clip
    start_frame = int(fps*startTimeSeconds)
    end_frame = start_frame + int(fps*vidLengthSeconds)  

    #iterate over those frames and write them to the new video file
    for frame in range(start_frame, end_frame):
        vid.set(cv2.CAP_PROP_POS_FRAMES, frame)
        ret1, frame_1 = vid.read()
        out.write(frame_1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                
    out.release()
    vid.release()
    cv2.destroyAllWindows()

def delete_analyzed_video_dlc_files(experiment_path, experiment_syntax='*DLC_resnet50_Gerbil_RIS_correctionSep30shuffle1_1000000*'):
    # substring = '*DLC_resnet50_Gerbil_RIS_correctionSep30shuffle1_1000000*' # <--- change this to the files you want to delete
    files = find(experiment_syntax, experiment_path)
    # Loop through files and delete those that contain the substring
    for filename in files:
        os.remove(filename)
        print(f"Deleted: {filename}")

