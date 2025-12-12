# Standard library imports
import datetime
import logging
import os
import random
import re
import shutil
import subprocess

# Third-party imports
import numpy as np
import pandas as pd
import ray
from PIL import Image
from scipy.ndimage import gaussian_filter1d, median_filter
from scipy.optimize import curve_fit
from sklearn.cluster import KMeans

# Matplotlib setup
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
mpl.rcParams['figure.max_open_warning'] = 0

# Local imports
import jumpyng.utils as ju

def _setup_logger():
    user = os.getlogin()
    log_dir = f"C:/Users/{user}/jumpyng/logs/"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"{log_dir}jumping_algorithm_{timestamp}.log"
    logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    return logger


## TODO: documentation for docstrings needs to be fixed, argumentations aren't working properly
## TODO: add a function to auto find syntax for an experiment folder, e.g. "2023-10-01_subject1_condition1_TOP_0_filtered.h5"
## TODO: use openCV CUDA for video 
def _interpolateMovement(data) -> np.ndarray:
    """
    Interpolates NaN values in a 1D numpy array using linear interpolation. Overrides jumping_utils interpolateMovement function.
    
    Args:
    data -- 1D numpy array with NaN values to be interpolated.

    Returns:
    data -- 1D numpy array with NaN values replaced by interpolated values.

    """
    nans = np.isnan(data)
    if np.all(nans):
        return data
    x = np.arange(len(data))
    data[nans] = np.interp(x[nans], x[~nans], data[~nans])
    return data

def _normalize_date(val) -> str:
    """Convert m/d/YYYY or mm/dd/YYYY → YYYY-MM-DD, else leave untouched."""
    s = str(val)
    m = re.match(r'^(?P<m>\d{1,2})/(?P<d>\d{1,2})/(?P<y>\d{4})$', s)
    if m:
        return f"{int(m.group('y')):04d}-{int(m.group('m')):02d}-{int(m.group('d')):02d}"
    return s

def rename_subjects(path_to_folder, old_prefix, new_prefix) -> None:
    """Renames files in a folder by replacing the old prefix with the new prefix.
    - Useful for renaming video files or other data files, if you are encountering issues with a date format, etc.

    Args:
    path_to_folder -- Path to the folder containing the files to be renamed.
    old_prefix -- The prefix to be replaced in the filenames.
    new_prefix -- The new prefix to replace the old prefix in the filenames.

    Returns:
    None -- The function renames the files in place and prints the changes made.

    """
    for filename in os.listdir(path_to_folder):
        if filename.startswith(old_prefix):
            new_name = filename.replace(old_prefix, new_prefix, 1)
            os.rename(os.path.join(path_to_folder, filename), os.path.join(path_to_folder, new_name))
            print(f'Renamed: {filename} → {new_name}')

def rename_columns(df: pd.DataFrame, map:dict, suffixes:list) -> pd.DataFrame:
    col_map = {
        f'{old}{sfx}': f'{new}{sfx}'
        for old, new in map.items()
        for sfx in suffixes
    }

    df = df.rename(columns=col_map)
    
    return df

def sample_and_copy_videos(experiment_path, destination_path, prefix, n=10, extensions=('.mp4', '.avi', '.mov')):
    """
    Randomly samples n videos containing a specific prefix from the experiment folder
    and copies them to the destination folder.

    Args:
        experiment_path (str): Root path of the dataset to crawl.
        destination_path (str): Path where sampled videos will be copied.
        prefix (str): Keyword that must be in the filename.
        n (int): Number of videos to randomly sample.
        extensions (tuple): Allowed video file extensions.
    """
    # Ensure destination directory exists
    os.makedirs(destination_path, exist_ok=True)

    # Collect eligible video files
    eligible_videos = []
    for root, dirs, files in os.walk(experiment_path):
        for file in files:
            if prefix in file and file.lower().endswith(extensions):
                eligible_videos.append(os.path.join(root, file))

    if not eligible_videos:
        print("No videos found matching the criteria.")
        return

    # Randomly sample videos
    sampled_videos = random.sample(eligible_videos, min(n, len(eligible_videos)))

    # Copy sampled videos
    for video_path in sampled_videos:
        shutil.copy(video_path, destination_path)

    print(f"Copied {len(sampled_videos)} videos to {destination_path}")


def extract_audio_tags(path: str) -> None:
    folder, fname = os.path.split(path)
    name, ext   = os.path.splitext(fname)
    backup = os.path.join(folder, f"{name}.old")

    os.replace(path, backup)
    df = pd.read_csv(backup, dtype=str)
    tags = df['audio_file'].str.extract(r'(4Hz|12Hz)', expand=False).to_numpy()

    if len(tags) == 0:
        print(f"No audio tags found in {path}.")
        return
    
    # Replace audio_file column with just the tags
    df['audio_file'] = tags
    
    # Save the modified dataframe back to the original path
    df.to_csv(path, index=False)
    print(f"Updated audio tags in {path}.")


def adjust_audio_csv(path: str) -> None:
    folder, fname = os.path.split(path)
    name, ext   = os.path.splitext(fname)

    backup = os.path.join(folder, f"{name}.old")
    os.replace(path, backup)

    df = pd.read_csv(backup, dtype=str)

    tags = df['audio_file'].str.extract(r'(4Hz|12Hz)', expand=False).to_numpy()

    real_inds = np.arange(0, len(tags), 2)
    half_rows = len(df) // 2
    for i in real_inds:
        m = i // 2
        if m < half_rows:
            df.loc[m, 'audio_file'] = tags[i]

    to_drop = []
    for r in range(half_rows, len(df)):
        p = int(df.loc[r, 'platform'])
        if p == 1:
            df.loc[r, 'audio_file'] = '12Hz'
        elif p == 5:
            df.loc[r, 'audio_file'] = '4Hz'
        elif p == 3:
            to_drop.append(r)

    if to_drop:
        df = df.drop(index=to_drop).reset_index(drop=True)

    corrected = os.path.join(folder, f"{name}{ext}")
    df.to_csv(corrected, index=False)

    print(f"Backed up original → {backup}")
    print(f"Saved corrected file → {corrected}")

def side_top_interchange_vid_files(path_to_folder, subjects=None):
    """
    Interchanges all side↔top video files in all subfolders of path_to_folder.
    If `subjects` is given (list of folder names), only those subfolders are touched.
    """

    def ci_replace(s, old, new):
        return re.sub(old, new, s, flags=re.IGNORECASE)

    for dirpath, dirnames, filenames in os.walk(path_to_folder):
        subject = os.path.basename(dirpath)
        if subjects and subject not in subjects:
            continue

        # Build dictionaries to match files by index
        side_videos = {}
        top_videos = {}

        for filename in filenames:
            side_match = re.search(r"_SIDE_(\d+)", filename, flags=re.IGNORECASE)
            if side_match:
                idx = side_match.group(1)
                side_videos[idx] = filename
                continue

            top_match = re.search(r"_TOP_(\d+)", filename, flags=re.IGNORECASE)
            if top_match:
                idx = top_match.group(1)
                top_videos[idx] = filename

        common_indices = set(side_videos.keys()) & set(top_videos.keys())

        if not common_indices:
            print(f"No matching side/top video pairs found in '{dirpath}'")
            continue

        for idx in sorted(common_indices):
            side_vid = side_videos[idx]
            top_vid = top_videos[idx]

            new_side_name = ci_replace(side_vid, r"_SIDE_", "_TOP_")
            new_top_name = ci_replace(top_vid, r"_TOP_", "_SIDE_")

            src_side = os.path.join(dirpath, side_vid)
            src_top = os.path.join(dirpath, top_vid)
            tgt_side = os.path.join(dirpath, new_side_name)
            tgt_top = os.path.join(dirpath, new_top_name)

            # If the swap is already done, skip
            if side_vid == new_side_name and top_vid == new_top_name:
                print(f"Skipping index {idx} in '{dirpath}': files already correctly named")
                continue

            # Atomic swap
            tmp = src_side + ".swap"
            os.rename(src_side, tmp)
            os.rename(src_top, tgt_top)
            os.rename(tmp, tgt_side)

            print(f"Swapped in {dirpath}: {side_vid} → {new_side_name}, {top_vid} → {new_top_name}")

@ray.remote(num_cpus=2)
def calculate_decision_end_algorithm(row,
                            features,
                            likelihood_threshold=0.9,
                            sigma=2,
                            k=3,
                            baseline_window=100,
                            slack=2,
                            logic=True,
                            debug=False,
                            use_largest_peak=True,
                            median_filter_size=3,
                            gaussian_peak_threshold=0.1,  # Threshold for peak width (percentage of max height)
                            fit_window_size=20,           # Window around peak for Gaussian fitting
                            ):
    """
    Calculate the decision and end frames for a given row of data using Gaussian fitting.

    Args:
    row -- A pandas Series containing the data for a single trial.
    features -- A list of keypoint features to analyze.
    likelihood_threshold -- Threshold for keypoint confidence to consider valid data.
    sigma -- Standard deviation for Gaussian filter applied to velocity.
    k -- Multiplier for baseline standard deviation to set spike threshold.
    baseline_window -- Number of frames to use for calculating the baseline.
    slack -- Number of frames to extend the detected spikes.
    logic -- If True, use advanced logic to determine the decision and end frames.
    debug -- If True, print debug information.
    use_largest_peak -- If True, use the largest velocity peak for decision and end frames.
    median_filter_size -- Size of the median filter to apply before Gaussian filtering.
    gaussian_peak_threshold -- Threshold for determining peak width (as percentage of max height).
    fit_window_size -- Window size around peak for Gaussian fitting.

    Returns:
    starts -- List of start frames for detected jumps. (decision frames)
    ends -- List of end frames for detected jumps. (end frames)
    agg_pos -- Aggregated position data after processing.
    diff_pos -- Absolute difference of the aggregated position data. (velocity)
    thresh -- Threshold used for spike detection.
    smooth_diff -- Smoothed difference of the aggregated position data (smoothed velocity).
    y_fit -- Gaussian fitted curve (None if fitting fails).
    """
    
    def get_clean_trace(kp):
        x = np.atleast_1d(row[f"{kp} x"])
        y = np.atleast_1d(row[f"{kp} y"])
        lik = np.atleast_1d(row[f"{kp} likelihood"])
        pos = np.hypot(x, y)
        pos[lik < likelihood_threshold] = np.nan
        return _interpolateMovement(pos)

    def detect_spikes(signal, thresh):
        spikes = []
        in_spike = False
        for i, v in enumerate(signal):
            if not in_spike and v > thresh:
                start = i
                in_spike = True
            elif in_spike and v < thresh:
                spikes.append((start, i))
                in_spike = False
        if in_spike:
            spikes.append((start, len(signal)-1))
        return spikes
    
    def gaussian_func(x, a, b, c, d):
        # a: amplitude, b: mean, c: standard deviation, d: offset
        return a * np.exp(-(x - b)**2 / (2 * c**2)) + d
    
    # Initialize y_fit as None
    y_fit = None
    
    # Get clean position traces and compute velocity
    all_traces = np.stack([get_clean_trace(kp) for kp in features])
    agg_pos = np.nanmedian(all_traces, axis=0)
    
    # Apply median filter before Gaussian filter
    if median_filter_size > 1:
        agg_pos = median_filter(agg_pos, size=median_filter_size)
    
    diff_pos = np.abs(np.diff(agg_pos))
    smooth_diff = gaussian_filter1d(diff_pos, sigma)
    
    # Calculate baseline and threshold
    baseline = smooth_diff[:baseline_window]
    thresh = baseline.mean() + k*baseline.std()
    
    # Initial spike detection using threshold
    raw_spikes = detect_spikes(smooth_diff, thresh)
    
    if not raw_spikes:
        return [], [], agg_pos, diff_pos, thresh, smooth_diff, y_fit
    
    # Find the largest peak
    peak_indices = [(s, e) for s, e in raw_spikes if s != e and e > s and e <= len(smooth_diff) and s > 0]

    peak_values = [np.max(smooth_diff[s:e]) for s, e in peak_indices]
    
    if not peak_values:
        return [], [], agg_pos, diff_pos, thresh, smooth_diff, y_fit
    
    # Get the largest peak
    largest_peak_idx = np.argmax(peak_values)
    peak_start, peak_end = peak_indices[largest_peak_idx]
    peak_max_idx = peak_start + np.argmax(smooth_diff[peak_start:peak_end])
    peak_height = smooth_diff[peak_max_idx]
    
    # Define window around peak for Gaussian fitting
    fit_start = max(0, peak_max_idx - fit_window_size)
    fit_end = min(len(smooth_diff), peak_max_idx + fit_window_size)
    
    # Prepare data for fitting
    x_data = np.arange(fit_start, fit_end)
    y_data = smooth_diff[fit_start:fit_end]
    
    try:
        # Initial parameter guesses: [amplitude, mean, std_dev, offset]
        p0 = [
            peak_height - baseline.mean(),  # amplitude
            peak_max_idx,                   # mean (peak position)
            (peak_end - peak_start) / 4,    # standard deviation (width)
            baseline.mean()                 # vertical offset
        ]
        
        # Fit Gaussian to the peak
        popt, _ = curve_fit(gaussian_func, x_data, y_data, p0=p0)
        a, b, c, d = popt

        # Create full Gaussian fit curve for the entire data range
        x_full = np.arange(len(smooth_diff))
        y_fit = gaussian_func(x_full, *popt)
        
        # Calculate start and end based on the fitted Gaussian
        # Find points where curve falls to gaussian_peak_threshold of peak height
        delta = np.sqrt(-2 * c**2 * np.log(gaussian_peak_threshold))
        gaussian_start = max(0, int(b - delta))
        gaussian_end = min(len(smooth_diff) - 1, int(b + delta))
        
        if debug:
            print(f"Gaussian fit parameters: a={a:.2f}, b={b:.2f}, c={c:.2f}, d={d:.2f}")
            print(f"Peak width at {gaussian_peak_threshold*100}% max: {delta:.2f} frames")
            print(f"Fitted start/end: {gaussian_start}, {gaussian_end}")

        return [gaussian_start], [gaussian_end], agg_pos, diff_pos, thresh, smooth_diff, y_fit
    
    except Exception as e:
        if debug:
            print(f"Gaussian fitting failed: {e}")
        
        # Fall back to the original method if fitting fails
        accel = np.diff(smooth_diff)
        
        if logic and use_largest_peak:
            return [peak_start], [peak_end], agg_pos, diff_pos, thresh, smooth_diff, y_fit
        else:
            # Use all detected spikes
            starts, ends = zip(*raw_spikes) if raw_spikes else ([], [])
            return list(starts), list(ends), agg_pos, diff_pos, thresh, smooth_diff, y_fit

    


@ray.remote(num_cpus=2)
def _get_dlc_data(params, experiment_path, dlc_suffix, camera, debug=False, logger=None):
    """
    Try to load the filtered HDF for one successful trial;
    on failure, return None so we can skip it later.
    -- This function is used to load the DLC data for a specific trial.

    Args:
    date -- Date of the trial in 'YYYY-MM-DD' format.
    subject -- Subject identifier (e.g., 'subject1').
    condition -- Condition of the trial (e.g., 'condition1').
    trial_num -- Trial number (1-indexed).
    experiment_path -- Path to the experiment data.
    dlc_suffix -- Suffix for the DLC files (e.g., '_filtered').

    Returns:
    pts -- A dictionary of numpy arrays containing the keypoint data for the specified trial.
    -- If the trial data cannot be loaded, it returns None and prints a warning.

    """
    try:
        params['date'] = _normalize_date(params['date'])
        parts = [
            params['date'],
            params['subject'],
            f"{camera}_{params['trial']}DLC"
        ]
        if params.get('sex'):       parts.append(params['sex'])
        if params.get('condition'): parts.append(params['condition'])

        suffix = dlc_suffix + ".h5"
        if debug:
            logger.debug(f"Looking for DLC data with parts: {parts} and suffix: {suffix}")
        h5path = ju.findSinglePartial(parts, experiment_path, suffix=suffix)
        if debug:
            logger.debug(f"Located DLC file at: {h5path}")
        if not h5path:
            if debug:
                logger.debug(f"[Warning] no file for {parts} + suffix={suffix}")
            print(f"[Warning] no file for {parts} + suffix={suffix}")
            return None

        df = pd.read_hdf(h5path)
        cols = [" ".join(c[1:3]).strip() for c in df.columns.values]
        df.columns = cols
        return {c: df[c].to_numpy() for c in cols}
        # # build the h5 filename and locate it
        # fname = f"{date}_{subject}_{condition}_TOP_{trial_num-1}{dlc_suffix}.h5"
        # h5_path = ju.findSingle(fname, experiment_path)

        # pts = pd.read_hdf(h5_path)
        # # rename multi-index cols → "bodypart x"/"bodypart y"
        # pts.columns = [' '.join(col[1:3]).strip() for col in pts.columns.values]
        # # return a dict of numpy arrays
        # return {col: pts[col].to_numpy() for col in pts.columns}
    except Exception as e:
        # warning printed in Ray’s worker log
        print(f"[Warning] skipping trial {params['date']}-{params['subject']}-{params['condition']}-{params['trial']}: {e}")
        # print(f"[Warning] skipping trial {date}-{subject}-{condition}-{trial_num-1}: {e}")
        return None
    
@ray.remote(num_cpus=2)
def _getSize(path):
    """
    Get the dimensions of a video file using ffprobe. **Must have ffprobe installed to PATH for this to work.**
    -- This function is used to get the width and height of a video file.

    Args:
    path -- Path to the video file.

    Returns:
    width -- Width of the video.
    height -- Height of the video.

    """
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'csv=p=0',
        path
    ]
    try:
        output = subprocess.check_output(cmd).decode().strip()
        width, height = map(int, output.split(','))
        return width, height
    except subprocess.CalledProcessError:
        print(f"Failed to get dimensions for {path}")
        return None, None

def _detect_experiment_syntax(experiment_path, dlc_suffix, camera):
    """
    Detect the syntax of the experiment files based on the provided path and DLC suffix.
    -- This function will look for a sample file in the experiment path and return the syntax used in the filenames.

    Args:
    experiment_path -- Path to the experiment data.
    dlc_suffix -- Suffix for the DLC files (e.g., '_filtered').

    Returns:
    syntax -- A string representing the detected syntax of the experiment files.

    """
    h5s = ju.find(f"*{dlc_suffix}.h5", experiment_path)
    if not h5s:
        raise FileNotFoundError(f"No HDF files with suffix '{dlc_suffix}' in {experiment_path}")
    sample = os.path.basename(h5s[0])
    prefix, _, _ = sample.partition(f"_{camera}_")
    parts = prefix.split("_")
    if len(parts) >= 4 and parts[2] in ("M","F") and parts[3] == "jumping":
        fields = ["{date}", "{subject}", "{sex}", "jumping", "{condition}"]
    else:
        fields = ["{date}", "{subject}", "{condition}"]
    return "_".join(fields) + f"_{camera}_{{trial}}" + dlc_suffix + ".h5"

def create_ray_dataframe(
    experiment_path,
    dlc_suffix,
    camera='TOP',
    gerbilDF=None,
    save_path=None,
    debug=False
):
    """
    Build a final_df of successful trials + DLC data.
    If gerbilDF (a DataFrame) is provided, we skip CSV loading.
    Otherwise we glob *TrialData.csv, pick outcome==1, and build success_df.
    """
    
    # 1) start Ray
    if debug:
        ctx = ray.init(
            include_dashboard=True,
            num_cpus=24,
            num_gpus=1,
            _memory=100 * 1024 * 1024 * 1024,
            object_store_memory=50 * 1024 * 1024 * 1024,
            dashboard_host="127.0.0.1",
            dashboard_port=8854,
            ignore_reinit_error=True,
        )
        logger = _setup_logger()
        logger.debug("→ Dashboard running at %s", ctx.dashboard_url)
        print("→ Dashboard running at", ctx.dashboard_url)

    else:
        ctx = ray.init(
            include_dashboard=False,
            ignore_reinit_error=True,
            num_cpus=24,
            num_gpus=1,
            _memory=100 * 1024 * 1024 * 1024,
            object_store_memory=50 * 1024 * 1024 * 1024,
        )
        logger = None
    # 2) infer DLC filename template
    syntax = _detect_experiment_syntax(experiment_path, dlc_suffix, camera)
    if debug:
        logger.debug("→ Detected experiment syntax: %s", syntax)

    # 3) build success_df
    if gerbilDF is not None:
        success_df = gerbilDF.reset_index(drop=True)
    else:
        csvs = ju.find("*TrialData.csv", experiment_path)
        print(f"→ Found {len(csvs)} CSVs")
        if debug:
            logger.debug("→ Found %d CSVs", len(csvs))
            logger.debug("→ Loading CSVs from: %s", csvs)
        grp = pd.concat((pd.read_csv(f) for f in csvs), ignore_index=True)
        grp.dropna(subset=["trial_num"], inplace=True)
        grp["trial_num"] = grp["trial_num"].astype(int)
        success_df = grp.reset_index(drop=True)
        success_df['date'] = success_df['date'].apply(_normalize_date)

    if success_df.empty:
        print("No successful trials.")
        ray.shutdown()
        return success_df

    # 4) load DLC data in parallel
    futures, row_idxs = [], []
    for i, row in success_df.iterrows():
        params = {
            "date":    row["date"],
            "subject": row["subject"],
            "trial":   int(row["trial_num"]) - 1,
        }
        if "{sex}" in syntax:
            params["sex"] = row.get("sex")
        if "{condition}" in syntax:
            params["condition"] = row.get("condition")
        futures.append(
            _get_dlc_data.remote(params, experiment_path, dlc_suffix, camera, debug, logger)
        )
        row_idxs.append(i)

    results = ray.get(futures)
    if debug:
        logger.debug("→ Loaded DLC data for %d trials", len(results))
    good = [(i, r) for i, r in zip(row_idxs, results) if r is not None]
    if not good:
        print("No DLC data loaded.")
        ray.shutdown()
        return success_df

    # 5) assemble DataFrame
    good_idxs, dicts = zip(*good)
    dlc_df   = pd.DataFrame(dicts)
    sub_df   = success_df.loc[list(good_idxs)].reset_index(drop=True)
    final_df = pd.concat([sub_df, dlc_df], axis=1)

    # 6) get video sizes via findSinglePartial on *.avi
    size_futs = []
    for _, row in final_df.iterrows():
        parts = [
            row["date"],
            row["subject"],
            f"{camera}_{int(row['trial_num'])-1}"
        ]
        vid_path = ju.findSinglePartial(parts, experiment_path, suffix=".avi")
        if not vid_path:
            raise FileNotFoundError(f"No .avi for parts {parts}")
        size_futs.append(_getSize.remote(vid_path))

    widths, heights = zip(*ray.get(size_futs))
    final_df["vid_width"], final_df["vid_height"] = widths, heights

    # 7) save & shutdown
    if save_path:
        final_df.to_hdf(save_path, "df", mode="w")
        if debug:
            logger.debug("→ Saved final DataFrame to %s", save_path)
        print(f"→ Saved final DataFrame to {save_path}")
    ray.shutdown()
    return final_df



def propogate_jumping_end_frames(df, subhyperfeatures, likelihood_threshold=0.6, sigma=2, k=3, baseline_window=200, logic=True, use_largest_peak=True, debug=False):
    """
    Propogate the jumping start and end frames to the dataframe and return it.
    -- Ensure you are feeding in successful trials only.
    -- Toggle logic and use_largest_peak to use the largest peak or the widest start-end pair.
    -- If you are having issues with the algorithm, feel free to tinker with the liklihood threshold, sigma, k, and baseline_window.
    
    Args:
    df -- DataFrame containing the trial data.
    subhyperfeatures -- List of subhyperfeatures to transform.
    likelihood_threshold -- Threshold for keypoint confidence to consider valid data (default: 0.6).
    sigma -- Standard deviation for Gaussian smoothing (default: 2).
    k -- Kernel size for Gaussian smoothing (default: 3).
    baseline_window -- Window size for baseline calculation (default: 200).
    logic -- If True, use advanced logic to determine the decision and end frames (default: True).
    use_largest_peak -- If True, use the largest velocity peak for decision and end frames (default: True).
    debug -- If True, start a Ray dashboard (default: False).

    Returns:
    df -- DataFrame with the algorithmic decision and end frames added.
    -- The DataFrame will have two new columns: 'Algorithm_Decision' and 'Algorithm_End', which contain the algorithmic decision and end frames, respectively.
    
    """
    df = df.reset_index(drop=True)

    if debug:
        ctx = ray.init(
            include_dashboard=True,
            num_cpus=24,
            num_gpus=1,
            _memory=100 * 1024 * 1024 * 1024,
            object_store_memory=50 * 1024 * 1024 * 1024,
            dashboard_host="127.0.0.1",
            dashboard_port=8854,
            ignore_reinit_error=True,
        )
        print("→ Dashboard running at", ctx.dashboard_url)

    else:
        ctx = ray.init(
            include_dashboard=False,
            ignore_reinit_error=True,
            num_cpus=24,
            num_gpus=1,
            _memory=100 * 1024 * 1024 * 1024,
            object_store_memory=50 * 1024 * 1024 * 1024,
        )


    calculate_frames = [calculate_decision_end_algorithm.remote(row, subhyperfeatures, likelihood_threshold, sigma, k, baseline_window, logic=logic, use_largest_peak=use_largest_peak) for idx, row in df.iterrows()]
    calculate_frames_results = ray.get(calculate_frames)

    pjd_list = []
    pen_list = []
    for js, je, *_ in calculate_frames_results:
        pjd_list.append(js[-1] if js else np.nan)
        pen_list.append(je[-1] if je else np.nan)
    
    df['Algorithm_Decision'] = pjd_list
    df['Algorithm_End']      = pen_list

    ray.shutdown()
    
    ## TODO: potentially take these lines out, and still figure out if it works
    mask = (df['outcome'] == 0) | (df['outcome'] == 2)
    df.loc[mask, ['Algorithm_Decision', 'Algorithm_End']] = np.nan

    df.reset_index(drop=True, inplace=True)
    return df

def _compute_distance_jumped(row, ppcm, feature='center-tail'):
    """
    Helper function to calculate the distance jumped based on the algorithmic decision and end frames.

    Args:
    row -- A pandas Series containing the data for a single trial.
    ppcm -- Pixels per centimeter, used to convert pixel distances to centimeters.
    feature -- The keypoint feature to use for calculating the distance jumped (default: 'nose').

    Returns:
    distance -- The distance jumped in centimeters, or None if the algorithmic decision or end frames are not available.

    """
    if pd.notna(row['Algorithm_Decision']) and pd.notna(row['Algorithm_End']):
        s = int(row['Algorithm_Decision'])
        e = int(row['Algorithm_End'])
        x = np.atleast_1d(row[f"{feature} x"])
        y = np.atleast_1d(row[f"{feature} y"])
        if 0 <= s < x.shape[0] and 0 <= e < x.shape[0]:
            dx = x[e] - x[s]
            dy = y[e] - y[s]
            return np.hypot(dx, dy) / ppcm
    return None

def _compute_landing_position(row, likelihood_threshold, ppcm, rightward, feature='nose'):
    """
    Helper function to calculate the landing position based on the algorithmic end frame.

    Args:
    row -- A pandas Series containing the data for a single trial.
    likelihood_threshold -- Threshold for keypoint confidence to consider valid data.
    ppcm -- Pixels per centimeter, used to convert pixel distances to centimeters.
    rightward -- If True, the jump from the takeoff platform is oriented rightward, otherwise leftward.
    feature -- The keypoint feature to use for calculating the landing position (default: 'nose').

    Returns:
    platform -- The landing position in centimeters, or None if the algorithmic end frame is not available or the landing position is not valid.

    """
    if pd.notna(row['Algorithm_End']):            
        e = int(row['Algorithm_End'])
        if rightward:
            landingTop = np.atleast_1d(row["landingTL x"])
            landingBottom = np.atleast_1d(row["landingBL x"])
            landingTopLikelihood = np.atleast_1d(row["landingTL likelihood"])
            landingBottomLiklihood = np.atleast_1d(row["landingBL likelihood"])
            landingTop = np.where(landingTopLikelihood < likelihood_threshold, np.nan, landingTop)
            landingBottom = np.where(landingBottomLiklihood < likelihood_threshold, np.nan, landingBottom)
        else:
            landingTop = np.atleast_1d(row["landingTR x"])
            landingBottom = np.atleast_1d(row["landingBR x"])
            landingTopLikelihood = np.atleast_1d(row["landingTR likelihood"])
            landingBottomLiklihood = np.atleast_1d(row["landingBR likelihood"])
            landingTop = np.where(landingTopLikelihood < likelihood_threshold, np.nan, landingTop)
            landingBottom = np.where(landingBottomLiklihood < likelihood_threshold, np.nan, landingBottom)

        all_pf = np.concatenate([landingTop, landingBottom])
        if all_pf.size and not np.all(np.isnan(all_pf)):
            platform = np.nanmean(all_pf)
            arr = np.atleast_1d(row[f"{feature} x"])
            if 0 <= e < arr.shape[0] and not np.isnan(arr[e]):
                return abs(platform - arr[e]) / ppcm
    return None

def _compute_actual_gap_distance(row, likelihood_threshold, ppcm, rightward):
    """
    Helper function to calculate the actual gap distance based on the takeoff and landing positions.

    Args:
    row -- A pandas Series containing the data for a single trial.
    likelihood_threshold -- Threshold for keypoint confidence to consider valid data.
    ppcm -- Pixels per centimeter, used to convert pixel distances to centimeters.
    rightward -- If True, the jump from the takeoff platform is oriented rightward, otherwise leftward.

    Returns:
    distance -- The actual gap distance in centimeters, or None if the takeoff or landing positions are not valid.

    """
    if rightward:
        takeoffTop = np.atleast_1d(row["takeoffTR x"])
        takeoffBottom = np.atleast_1d(row["takeoffBR x"])
        landingTop = np.atleast_1d(row["landingTL x"])
        landingBottom = np.atleast_1d(row["landingBL x"])
        takeoffTop[row['takeoffTR likelihood'] < likelihood_threshold] = np.nan
        takeoffBottom[row['takeoffBR likelihood'] < likelihood_threshold] = np.nan
        landingTop[row['landingTL likelihood'] < likelihood_threshold] = np.nan
        landingBottom[row['landingBL likelihood'] < likelihood_threshold] = np.nan
    else:
        takeoffTop = np.atleast_1d(row["takeoffTL x"])
        takeoffBottom = np.atleast_1d(row["takeoffBL x"])
        landingTop = np.atleast_1d(row["landingTR x"])
        landingBottom = np.atleast_1d(row["landingBR x"])
        takeoffTop[row['takeoffTL likelihood'] < likelihood_threshold] = np.nan
        takeoffBottom[row['takeoffBL likelihood'] < likelihood_threshold] = np.nan
        landingTop[row['landingTR likelihood'] < likelihood_threshold] = np.nan
        landingBottom[row['landingBR likelihood'] < likelihood_threshold] = np.nan

    tp = np.nanmean(np.array([takeoffTop, takeoffBottom]))
    lp = np.nanmean(np.array([landingTop, landingBottom]))
    if not np.isnan(tp) and not np.isnan(lp):
        return abs(lp - tp) / ppcm
    return None

def _compute_ppcm_direction_platform_size(row, likelihood_threshold, takeoffWidthInches=5.0):
    """
    Helper function to calculate the platform size based on the takeoff positions.
    -- This function computes the platform size using the Euclidean distance between the top and bottom takeoff points.

    Arguments:
    - row -- A pandas Series containing the data for a single trial.
    - likelihood_threshold -- Threshold for keypoint confidence to consider valid data.
    - takeoffWidthInches -- Width of the takeoff platform in inches (default: 3.0).

    Returns:

    - ppcm: Pixels per centimeter, used to convert pixel distances to centimeters.
    - rightward -- If True, the jump from the takeoff platform is oriented rightward, otherwise leftward.
    - platform_size -- The landing platform size in centimeters, or None if the landing positions are not valid.

    """
    widthCM = takeoffWidthInches * 2.54
    takeoffTL = np.atleast_1d(row["takeoffTL y"])
    takeoffBL = np.atleast_1d(row["takeoffBL y"])
    takeoffTR = np.atleast_1d(row["takeoffTR y"])
    takeoffBR = np.atleast_1d(row["takeoffBR y"])

    takeoffTL_lik = np.atleast_1d(row["takeoffTL likelihood"])
    takeoffBL_lik = np.atleast_1d(row["takeoffBL likelihood"])
    takeoffTR_lik = np.atleast_1d(row["takeoffTR likelihood"])
    takeoffBR_lik = np.atleast_1d(row["takeoffBR likelihood"])

    maskTakeoffTL = takeoffTL_lik < likelihood_threshold
    maskTakeoffBL = takeoffBL_lik < likelihood_threshold
    maskTakeoffTR = takeoffTR_lik < likelihood_threshold
    maskTakeoffBR = takeoffBR_lik < likelihood_threshold

    takeoffTL[maskTakeoffTL] = np.nan
    takeoffBL[maskTakeoffBL] = np.nan
    takeoffTR[maskTakeoffTR] = np.nan
    takeoffBR[maskTakeoffBR] = np.nan

    landingTL = np.atleast_1d(row["landingTL y"])
    landingBL = np.atleast_1d(row["landingBL y"])
    landingTR = np.atleast_1d(row["landingTR y"])
    landingBR = np.atleast_1d(row["landingBR y"])
    landingTL_lik = np.atleast_1d(row["landingTL likelihood"])
    landingBL_lik = np.atleast_1d(row["landingBL likelihood"])
    landingTR_lik = np.atleast_1d(row["landingTR likelihood"])
    landingBR_lik = np.atleast_1d(row["landingBR likelihood"])

    maskLandingTL = landingTL_lik < likelihood_threshold
    maskLandingBL = landingBL_lik < likelihood_threshold
    maskLandingTR = landingTR_lik < likelihood_threshold
    maskLandingBR = landingBR_lik < likelihood_threshold

    landingTL[maskLandingTL] = np.nan
    landingBL[maskLandingBL] = np.nan
    landingTR[maskLandingTR] = np.nan
    landingBR[maskLandingBR] = np.nan

    takeoffTLx = np.atleast_1d(row["takeoffTL x"])
    takeoffBLx = np.atleast_1d(row["takeoffBL x"])
    takeoffTRx = np.atleast_1d(row["takeoffTR x"])
    takeoffBRx = np.atleast_1d(row["takeoffBR x"])

    takeoffTLx_lik = np.atleast_1d(row["takeoffTL likelihood"])
    takeoffBLx_lik = np.atleast_1d(row["takeoffBL likelihood"])
    takeoffTRx_lik = np.atleast_1d(row["takeoffTR likelihood"])
    takeoffBRx_lik = np.atleast_1d(row["takeoffBR likelihood"])

    maskTakeoffTLx = takeoffTLx_lik < likelihood_threshold
    maskTakeoffBLx = takeoffBLx_lik < likelihood_threshold
    maskTakeoffTRx = takeoffTRx_lik < likelihood_threshold
    maskTakeoffBRx = takeoffBRx_lik < likelihood_threshold

    takeoffTLx[maskTakeoffTLx] = np.nan
    takeoffBLx[maskTakeoffBLx] = np.nan
    takeoffTRx[maskTakeoffTRx] = np.nan
    takeoffBRx[maskTakeoffBRx] = np.nan

    landingTLx = np.atleast_1d(row["landingTL x"])
    landingBLx = np.atleast_1d(row["landingBL x"])
    landingTRx = np.atleast_1d(row["landingTR x"])
    landingBRx = np.atleast_1d(row["landingBR x"])

    landingTLx_lik = np.atleast_1d(row["landingTL likelihood"])
    landingBLx_lik = np.atleast_1d(row["landingBL likelihood"])
    landingTRx_lik = np.atleast_1d(row["landingTR likelihood"])
    landingBRx_lik = np.atleast_1d(row["landingBR likelihood"])

    maskLandingTLx = landingTLx_lik < likelihood_threshold
    maskLandingBLx = landingBLx_lik < likelihood_threshold
    maskLandingTRx = landingTRx_lik < likelihood_threshold
    maskLandingBRx = landingBRx_lik < likelihood_threshold

    landingTLx[maskLandingTLx] = np.nan
    landingBLx[maskLandingBLx] = np.nan
    landingTRx[maskLandingTRx] = np.nan
    landingBRx[maskLandingBRx] = np.nan

    # Find direction of jump based on difference between x positions of takeoff and landing:
    rightward = False

    if np.nanmean([takeoffTLx, takeoffBLx, takeoffBRx, takeoffTRx]) < np.nanmean([landingTRx, landingBRx, landingTLx, landingBLx]):
        rightward = True

    # Calculate the ppcm:
    if rightward:
        takeoffDiff = np.nanmean(takeoffTR) - np.nanmean(takeoffBR)
    else:
        takeoffDiff = np.nanmean(takeoffTL) - np.nanmean(takeoffBL)

    ppcm = np.abs(takeoffDiff) / widthCM

    # Calculate the platform size:
    if rightward:
        platform_size = np.round(np.abs(np.nanmean(landingTL) - np.nanmean(landingBL)) / ppcm, 2)
    else:
        platform_size = np.round(np.abs(np.nanmean(landingTR) - np.nanmean(landingBR)) / ppcm, 2)
    
    return platform_size, ppcm, rightward
       

def calculate_trial_start(input_df, liklihood_threshold=.9, featureLOS = 'side_eyeR', featuresetBoard = ['clipboardBL', 'clipboardBM', 'clipboardBR'] ):
    df = input_df.reset_index(drop=True)
    df = df.copy()
    for col in ['Algorithm_Start']:
        if col not in df.columns:
            df[col] = np.nan
    
    for idx, row in df.iterrows():
        if pd.notna(row['Algorithm_Decision']):
            s = int(row['Algorithm_Decision'])
            # use the clipboard data to check and see if all of the points cross the eye np nanmean line of sight (horizontal line)
            # Get feature positions and filter by likelihood
            y_vals = np.atleast_1d(row[f"{featureLOS} y"])
            lik = np.atleast_1d(row[f"{featureLOS} likelihood"])
            mask = lik < liklihood_threshold
            y_vals[mask] = np.nan

            clipboard_y = [row[f"{y} y"] for y in featuresetBoard if f"{y} y" in row]

            # Calculate mean y position (horizontal line of sight)
            mean_y = np.nanmean(y_vals)

            if not np.isnan(mean_y):
                # Find frames where clipboard's three points crosses the mean line
                crossing_frames = []
                for feature in featuresetBoard:
                    feature_crossing_frames = {}
                    for feature in featuresetBoard:
                        board_y = np.atleast_1d(row[f"{feature} y"])
                        board_lik = np.atleast_1d(row[f"{feature} likelihood"])
                        
                        # Filter by likelihood threshold
                        mask = board_lik < liklihood_threshold
                        board_y[mask] = np.nan
                        
                        # Find the first frame where the board point is above the eye line (y < mean_y)
                        for frame_idx in range(min(s, len(board_y))):
                            if not np.isnan(board_y[frame_idx]) and board_y[frame_idx] < mean_y:
                                feature_crossing_frames[feature] = frame_idx
                                break

                    # If all features have crossed, find the frame where the last one crossed
                    if len(feature_crossing_frames) == len(featuresetBoard):
                        last_crossing_frame = max(feature_crossing_frames.values())
                        crossing_frames.append(last_crossing_frame)
                if crossing_frames:
                    df.at[idx, 'Algorithm_Start'] = crossing_frames[0]
    return df

def calculate_jump_metrics(df, likelihood_threshold=.9, takeoffWidthInches=5.0, feature='nose', ppcmOverride=0.0):
    """
    Calculate the distance jumped based on the algorithmic decision and end frames.

    Arguments:
    df -- DataFrame containing the trial data.
    likelihood_threshold -- Threshold for keypoint confidence to consider valid data (default: 0.9).
    secondary_threshold -- Secondary threshold for platform size calculation (default: 0.4).
    ppcm1 -- Pixels per centimeter for the first video resolution (default: 14.37). If not using multiple video resolutions, set ppcm1 == ppcm2.
    ppcm2 -- Pixels per centimeter for the second video resolution (default: 27.6). If not using multiple video resolutions, set ppcm1 == ppcm2.

    Returns:
    df -- DataFrame with the calculated metrics added.
    -- The DataFrame will have four new columns: 'Distance_Jumped', 'Landing_Position', 'Actual_Gap_Dist', and 'Platform_Size', which contain the calculated metrics.

    """
    df = df.reset_index(drop=True)
    for col in ['Distance_Jumped', 'Landing_Position', 'Actual_Gap_Dist', 'Platform_Size']:
        if col not in df.columns:
            df[col] = np.nan

    widths = df['vid_width'].unique()
    heights = df['vid_height'].unique()
    
    for idx, row in df.iterrows():
        # if row['vid_width'] == widths[0] and row['vid_height'] == heights[0]:
        #     ppcm = ppcm1
        # elif row['vid_width'] == widths[1] and row['vid_height'] == heights[1]:
        #     ppcm = ppcm2
        # else:
        #     print(f"Warning: Unknown video dimensions for row {idx}. Using default ppcm.")
        #     ppcm = ppcm2

        if row['outcome'] != 1:
            ## Abort / Failed Trial Platform Size Calculation
            try:
                val, ppcm, rightward = _compute_ppcm_direction_platform_size(row, likelihood_threshold, takeoffWidthInches=takeoffWidthInches)
                if val is not None:
                    df.at[idx, 'Platform_Size'] = val
                if rightward is not None:
                    df.at[idx, 'rightward'] = rightward
                    
                if ppcmOverride > 0.0:
                    df.at[idx, 'ppcm'] = ppcmOverride
                elif ppcm is not None:
                    df.at[idx, 'ppcm'] = ppcm
            except Exception as e:
                print(f"Oops — error computing Platform_Size at row {idx}: {e}")
            try:
                val = _compute_actual_gap_distance(row, likelihood_threshold, ppcm, rightward)
                if val is not None:
                    df.at[idx, 'Actual_Gap_Dist'] = val
            except Exception as e:
                print(f"Oops — error computing Actual_Gap_Dist at row {idx}: {e}")
        else:
            # Platform Size
            try:
                val, ppcm, rightward = _compute_ppcm_direction_platform_size(row, likelihood_threshold, takeoffWidthInches=takeoffWidthInches)
                if val is not None:
                    df.at[idx, 'Platform_Size'] = val
                if rightward is not None:
                    df.at[idx, 'rightward'] = rightward
                    
                if ppcmOverride > 0.0:
                    df.at[idx, 'ppcm'] = ppcmOverride
                elif ppcm is not None:
                    df.at[idx, 'ppcm'] = ppcm
            except Exception as e:
                print(f"Oops — error computing Platform_Size at row {idx}: {e}")

            ## Distance Jumped
            try:
                val = _compute_distance_jumped(row, ppcm, feature=feature)
                if val is not None:
                    df.at[idx, 'Distance_Jumped'] = val
            except Exception as e:
                print(f"Oops — error computing Distance_Jumped at row {idx}: {e}")

            # Landing Position
            try:
                val = _compute_landing_position(row, likelihood_threshold, ppcm, rightward, feature)
                if val is not None:
                    df.at[idx, 'Landing_Position'] = val
            except Exception as e:
                print(f"Oops — error computing Landing_Position at row {idx}: {e}")

            # Actual Gap Distance
            try:
                val = _compute_actual_gap_distance(row, likelihood_threshold, ppcm, rightward)
                if val is not None:
                    df.at[idx, 'Actual_Gap_Dist'] = val
            except Exception as e:
                print(f"Oops — error computing Actual_Gap_Dist at row {idx}: {e}")

    return df


def propogate_actual_gap_classes(df, rightward, distanceCount=7, labels=None, likelihood_threshold=0.9):
    """
    Cluster the measured gaps into the labels + distanceCount's above
    using KMeans, and add a 'Actual_Gap_Class' column to the dataframe.
    
    Args:
    df -- DataFrame containing the trial data.
    rightward -- If True, the jump from the takeoff platform is oriented rightward, otherwise leftward.
    distanceCount -- Number of distance categories to create (default: 3).
    labels -- List of labels for the distance categories (default: None, which means it will use ['Short', 'Medium', 'Long']).
    likelihood_threshold -- Threshold for keypoint confidence to consider valid data (default: 0.9).

    Returns:
    df -- DataFrame with the 'Actual_Gap_Class' column added.
    -- The DataFrame will have a new column 'Actual_Gap_Class' which contains the category of the distance jumped (Short, Medium, Long).
    """
    safecopy = df.copy()
    
    def _compute_actual_gap_distance_filtered(row, likelihood_threshold, rightward):
        if rightward:
            takeoffTop = np.atleast_1d(row["takeoffTR x"])
            takeoffBottom = np.atleast_1d(row["takeoffBR x"])
            landingTop = np.atleast_1d(row["landingTL x"])
            landingBottom = np.atleast_1d(row["landingBL x"])
            
            takeoffTopLik = np.atleast_1d(row["takeoffTR likelihood"])
            takeoffBottomLik = np.atleast_1d(row["takeoffBR likelihood"])
            landingTopLik = np.atleast_1d(row["landingTL likelihood"])
            landingBottomLik = np.atleast_1d(row["landingBL likelihood"])
        else:
            takeoffTop = np.atleast_1d(row["takeoffTL x"])
            takeoffBottom = np.atleast_1d(row["takeoffBL x"])
            landingTop = np.atleast_1d(row["landingTR x"])
            landingBottom = np.atleast_1d(row["landingBR x"])
            
            takeoffTopLik = np.atleast_1d(row["takeoffTL likelihood"])
            takeoffBottomLik = np.atleast_1d(row["takeoffBL likelihood"])
            landingTopLik = np.atleast_1d(row["landingTR likelihood"])
            landingBottomLik = np.atleast_1d(row["landingBR likelihood"])
        
        # Filter out low-likelihood values
        takeoffTop[takeoffTopLik < likelihood_threshold] = np.nan
        takeoffBottom[takeoffBottomLik < likelihood_threshold] = np.nan
        landingTop[landingTopLik < likelihood_threshold] = np.nan
        landingBottom[landingBottomLik < likelihood_threshold] = np.nan
        
        # Calculate means ignoring NaN values
        tp = np.nanmean(np.array([takeoffTop, takeoffBottom]))
        lp = np.nanmean(np.array([landingTop, landingBottom]))
        
        # Calculate distance if both points are valid
        if not np.isnan(tp) and not np.isnan(lp):
            return abs(lp - tp)
        return np.nan
    
    # Calculate filtered gap distances
    for idx, row in safecopy.iterrows():
        gap_px = _compute_actual_gap_distance_filtered(row, likelihood_threshold, rightward)
        if not np.isnan(gap_px):
            # Convert pixels to cm if ppcm is available
            if 'ppcm' in row and not np.isnan(row['ppcm']):
                safecopy.at[idx, 'Actual_Gap_Dist'] = gap_px / row['ppcm']
            else:
                safecopy.at[idx, 'Actual_Gap_Dist'] = gap_px
    
    if 'Actual_Gap_Dist' not in safecopy.columns:
        safecopy['Actual_Gap_Dist'] = np.nan
    
    distances = safecopy['Actual_Gap_Dist']
    mask = distances.notna()
    
    if mask.sum() < 3:
        safecopy['Actual_Gap_Class'] = np.nan
        return safecopy
    
    data = distances[mask].values.reshape(-1, 1)
    
    # Apply KMeans clustering
    kmeans = KMeans(n_clusters=distanceCount, random_state=42, n_init='auto')
    kmeans.fit(data)
    centers = kmeans.cluster_centers_.flatten()
    
    # Order clusters from shortest to longest
    order = np.argsort(centers)
    
    # Set default labels if none provided
    if labels is None:
        labels = ['Very Short', 'Short', 'Medium', 'Long', 'Very Long', 'Extra Long', 'Extreme'][:distanceCount]
    elif len(labels) != distanceCount:
        raise ValueError(f"Labels must be a list of {distanceCount} items: e.g. ['Short', 'Medium', 'Long']")
    
    # Map cluster indices to labels
    cluster_label_map = {cluster_idx: labels[pos] for pos, cluster_idx in enumerate(order)}

    df['Actual_Gap_Class'] = np.nan

    for idx, cluster_idx in zip(df[mask].index, kmeans.labels_):
        df.at[idx, 'Actual_Gap_Class'] = cluster_label_map[cluster_idx]

    return df

def propogate_platform_size(df, rightward, platformCount=3, labels=None, likelihood_threshold=0.9):
    """
    Cluster the measured platform sizes into Small/Medium/Large categories
    using KMeans, and add a 'Platform_Category' column to the dataframe.

    Args:
    df -- DataFrame containing the trial data.
    likelihood_threshold -- Threshold for keypoint confidence to consider valid data (default: 0.9).
    labels -- List of labels for the platform categories (default: None, which means it will use ['Small', 'Medium', 'Large']).

    Returns:
    df -- DataFrame with the 'Platform_Category' column added.
    -- The DataFrame will have a new column 'Platform_Category' which contains the category of the platform size (Small, Medium, Large).

    """
    safecopy = df.copy()

    def _compute_landing_platform_pixels(row, likelihood_threshold, rightward):
        if rightward:
            top = np.atleast_1d(row["landingTL y"]).astype(float)
            bot = np.atleast_1d(row["landingBL y"]).astype(float)
            lik_top = np.atleast_1d(row["landingTL likelihood"])
            lik_bot = np.atleast_1d(row["landingBL likelihood"])

        else:
            top = np.atleast_1d(row["landingTR y"]).astype(float)
            bot = np.atleast_1d(row["landingBR y"]).astype(float)
            lik_top = np.atleast_1d(row["landingTR likelihood"])
            lik_bot = np.atleast_1d(row["landingBR likelihood"])
        
        top[lik_top < likelihood_threshold] = np.nan
        bot[lik_bot < likelihood_threshold] = np.nan

        top = np.nanmean(top)
        bot = np.nanmean(bot)

        return np.abs(top - bot) if not np.isnan(top) and not np.isnan(bot) else np.nan

    for idx, row in safecopy.iterrows():
        safecopy.at[idx, 'Platform_Size'] = _compute_landing_platform_pixels(row, likelihood_threshold, rightward)

    if 'Platform_Size' not in safecopy.columns:
        safecopy['Platform_Size'] = np.nan

    sizes = safecopy['Platform_Size']
    mask = sizes.notna()
    if mask.sum() < 3:
        safecopy['Platform_Category'] = np.nan
        return safecopy

    data = sizes[mask].values.reshape(-1, 1)

    kmeans = KMeans(n_clusters=platformCount, random_state=42, n_init='auto')
    kmeans.fit(data)
    centers = kmeans.cluster_centers_.flatten()

    order = np.argsort(centers)
    if labels is None:
        labels = ['Small', 'Medium', 'Large']
    elif len(labels) != platformCount:
        raise ValueError(f"Labels must be a list of {platformCount} items: e.g. ['Small', 'Medium', 'Large']")
    cluster_label_map = {cluster_idx: labels[pos] for pos, cluster_idx in enumerate(order)}

    df['Platform_Category'] = 'NaN'#np.nan

    for idx, cluster_idx in zip(df[mask].index, kmeans.labels_):
        df.at[idx, 'Platform_Category'] = cluster_label_map[cluster_idx]

    return df


def merge_top_and_side_dataframes(top_df, side_df, merge_keys=['date', 'subject', 'sex', 'condition', 'experimenter', 'trial_num', 'platform', 'distance', 'laser', 'outcome', 'audio_file', 'vid_width', 'vid_height'], 
                                  side_prefix='side_'):
    """
    Merge the top and side dataframes based on merge keys, handling common columns by renaming.
    
    Args:
    top_df -- DataFrame containing the top view data.
    side_df -- DataFrame containing the side view data.
    merge_keys -- List of columns to merge on (default: predefined set of keys).
    side_prefix -- Prefix to add to side view columns that exist in both dataframes (default: 'side_').

    Returns:
    merged_df -- Merged DataFrame with top and side data combined.
    """

    # Identify common columns excluding merge keys
    common_cols = set(top_df.columns).intersection(set(side_df.columns)) - set(merge_keys)
    
    # Create temporary DataFrames with renamed columns
    df_top_temp = top_df.copy()
    df_side_temp = side_df.copy()
    
    # Rename common columns to avoid conflicts
    for col in common_cols:
        df_side_temp = df_side_temp.rename(columns={col: f"{side_prefix}{col}"})
    
    # Merge the temporary DataFrames
    merged_df = pd.merge(df_top_temp, df_side_temp, on=merge_keys)
    
    return merged_df

def ppcm_gui(df, ppcm):
    ## to-do: add in a GUI to manually review ppcm value for all unique vid dimensions]
    ## ppcm based off of takeoff platform
    pass

def calculate_head_velocities():
    ## to-do: 
    pass
