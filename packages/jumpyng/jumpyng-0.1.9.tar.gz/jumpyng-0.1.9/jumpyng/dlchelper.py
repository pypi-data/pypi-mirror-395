import os
import fnmatch
import pandas as pd
import pickle
import random
import shutil
from datetime import datetime, timedelta
import numpy as np
import soundfile as sf
from tkinter import Tk, filedialog
import tdt


def _require_dlc():
    try:
        import deeplabcut as dlc  # type: ignore
        return dlc
    except ImportError as exc:
        raise ImportError(
            "deeplabcut is required for DLC helper functions. "
            "Install it separately (e.g., pip install deeplabcut or jumpyng[dlc])."
        ) from exc


def batch_analyze_videos(dlc_config_path, experiment_path, shuffle=1, filter=True):
    """
    Example usage:
        Args:
        dlc_config_path = r"C:\Users\plab\Desktop\extended_features_wtsummer2023-kevin-2025-04-29\config.yaml"
        experiment_path = r'D:\jumping\experiments\WT summer 2023'
    """
    def find(pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files: 
                if fnmatch.fnmatch(name,pattern): 
                    result.append(os.path.join(root,name))
        if len(result)==1:
            result = result[0]
        return result

    vid_files = find('*TOP*.avi', experiment_path)

    # analyze the videos with DLC (ignore ones it's already done with the above network)
    dlc = _require_dlc()
    dlc.analyze_videos(dlc_config_path, vid_files, shuffle=shuffle, save_as_csv=False, gputouse=0)

    # looping through the DLC files and filtering them to make them smoother
    if(filter):
        for vid_file in vid_files:
            print(f"Filtering predictions using {experiment_path}...")
            dlc.filterpredictions(dlc_config_path, vid_file, shuffle=shuffle)

    # uncomment the lines below if you want to create labeled videos
    #   print('making labeled videos')
    #   dlc.create_labeled_video(dlc_config_path, vid_files, save_frames = False)

    print(f"Finished analyzing all the videos in {experiment_path}!")

def pre_processing_dlc_randomized_vid_selector(experiment_path, subjects, dlc_folder_path, start_date, end_date, numVids=12):
    candidates = []

    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        for subject in subjects:
            subject_dir = os.path.join(experiment_path, date_str, subject)
            if not os.path.isdir(subject_dir):
                continue

            trial_files = [
                f for f in os.listdir(subject_dir)
                if f.endswith(".avi") and "_TOP_" in f and f.startswith(f"{date_str}_{subject}")
            ]

            for trial_file in trial_files:
                candidates.append({
                    "date": date_str,
                    "subject": subject,
                    "filename": trial_file,
                    "source_path": os.path.join(subject_dir, trial_file)
                })
        current_date += timedelta(days=1)

    # Randomly select 12 unique trials
    if len(candidates) < numVids:
        print(f"❌ Only {len(candidates)} available videos. Cannot select {numVids}.")
        exit(1)

    selected_trials = random.sample(candidates, numVids)

    # Copy selected trials
    for trial in selected_trials:
        dest_path = os.path.join(dlc_folder_path, trial["filename"])
        try:
            shutil.copy2(trial["source_path"], dest_path)
            print(f"✅ Copied: {trial['filename']}")
        except Exception as e:
            print(f"❌ Failed to copy {trial['filename']}: {e}")

    print("\n🎯 Done. Total files copied:", len(selected_trials))


def convert_to_wav():
    # Use a GUI to select the directory
    Tk().withdraw()  # Hide the root window
    data_path = filedialog.askdirectory(title="Select TDT Data Directory")
    if not data_path:
        print("No directory selected.")
        return
    
    folder_name = os.path.basename(data_path)

    try:
        # Load the TDT data
        data = tdt.read_block(data_path)

        # Get the audio data and sampling rate
        wav = data.streams['Wav1']
        audio_data = wav.data.flatten()
        fs = int(round(wav.fs))

        # Normalize audio data (if desired)
        # audio_data = audio_data / np.max(np.abs(audio_data))

        # Specify the output path and filename
        output_filename = os.path.join(data_path, f"{folder_name}.wav")

        # Save the audio data as a WAV file to the selected directory
        sf.write(output_filename, audio_data, fs)
        print(f"Audio saved to {output_filename}")

    except Exception as e:
        print(f"Error: {e}")
