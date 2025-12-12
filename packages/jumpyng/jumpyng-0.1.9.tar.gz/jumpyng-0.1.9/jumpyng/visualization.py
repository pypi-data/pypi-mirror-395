import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import ray
import jumpyng.utils as ju
import jumpyng.algorithm as ja
    

def generate_pdf_report_no_human(df,
                        experiment_path,
                        filename,
                        subhyperfeatures,
                        all_features,
                        likelihood_threshold=0.6,
                        logic=False,
                        use_largest_peak=False):
    pp = PdfPages(filename)
    # stats = {"decisionLoss": [], "endLoss": []}

    df = df.reset_index(drop=True)

    ray.shutdown()

    # starts a local cluster *and* the dashboard
    ctx = ray.init(
        include_dashboard=True,
        dashboard_host="127.0.0.1",
        dashboard_port=8854,
        ignore_reinit_error=True,
    )

    print("→ Dashboard running at", ctx.dashboard_url)
    
    fut = [ja.calculate_decision_end_algorithm.remote(row, likelihood_threshold=0.6, sigma=2, k=3, baseline_window=200, features=subhyperfeatures, logic=logic, use_largest_peak=use_largest_peak) for idx, row in df.iterrows()]
    calc_jump_distances = ray.get(fut)

    ray.shutdown()
    
    for idx, row in df.iterrows():
        try:
            vid_file = ju.get_unambiguous_vidname_from_row(row, experiment_path)

            js, je, agg_pos, diff_pos, threshold, smooth_diff = calc_jump_distances[idx]

            pjd = js[-1] if js else None
            pen = je[-1] if je else None

            fig, axes = plt.subplots(1, 3, figsize=(30, 5))

            # — panel 1: decision frame
            frame_dec = None 
            if pjd is not None:
                frame_dec = pjd
                img1 = ju.get_vid_frame(vid_file, pjd)
                axes[0].imshow(img1.astype(np.uint8))
                axes[0].axis('off')
                axes[0].set_title('Frame at Algorithmic Decision')
                axes[2].axvline(pjd, color='orange', linestyle='--', label='Algorithmic Decision')
                df.loc[idx, 'Algorithm_Decision'] = pjd
            # — panel 2: end frame

            frame_end = None
            if pen is not None:
                frame_end = pen
                img2 = ju.get_vid_frame(vid_file, pen)
                axes[1].imshow(img2.astype(np.uint8))
                axes[1].axis('off')
                axes[1].set_title('Frame at Algorithmic End')
                axes[2].axvline(pen, color='midnightblue', linestyle='--', label='Algorithmic End')
                df.loc[idx, 'Algorithm_End'] = pen

            # — panel 3: velocity + thresholds
            axv = axes[2]
            axv.plot(
                np.arange(1, len(agg_pos)),
                smooth_diff,
                lw=2,
                color='black',
                rasterized=True,
                zorder=5,
                label='Velocity (Gaussian)'
            )
            axv.axhline(threshold, linestyle='--', label='Spike Threshold')
            # vertical lines
            axv.set_xlabel('Frame')
            axv.set_ylabel('Velocity')
            axes[2].set_title(label='Velocity vs Time', loc='left')
            axv.legend()
        
            # — mask low‐likelihood keypoints in the row (no new HDF reads)
            masked = {}
            for kp in all_features:
                lik = row[f"{kp} likelihood"]
                x_arr = row[f"{kp} x"].copy()
                y_arr = row[f"{kp} y"].copy()
                mask = lik < likelihood_threshold
                x_arr[mask] = np.nan
                y_arr[mask] = np.nan
                masked[f"{kp} x"] = x_arr
                masked[f"{kp} y"] = y_arr
                arr = masked[f"{kp} x"]
                vel = np.concatenate(([np.nan], np.diff(arr))) # x-velocities
                axv.plot(vel, linewidth=1, alpha=0.7)

            # — scatter keypoints on panels 1–2
            for ax, frame in zip(axes[:2], (frame_dec, frame_end)):
                xs = [masked[f"{kp} x"][frame] for kp in all_features]
                ys = [masked[f"{kp} y"][frame] for kp in all_features]
                ax.scatter(xs, ys, rasterized=True)


            # — title & save
            fig.suptitle(
                f"{row['subject']} {row['date']}  "
                f"Trial {int(row['trial_num'])} -- "
                f"Algo. Decision: {pjd} -- Algo. End: {pen}"
            )
            pp.savefig(fig)
            plt.close(fig)

        except Exception as e:
            print(f"Error processing trial {idx}: {e}")
    
    ray.shutdown()
    pp.close()

    print("→ PDF report generated:", filename)

def generate_likelihood_pdf_report(df,
                        filename,
                        subhyperfeatures,
                        first_threshold=0.9,
                        second_threshold=0.5):

    df = df.reset_index(drop=True)
    pp = PdfPages(filename)
    for idx, row in df.iterrows():
        fig, axes = plt.subplots(2, 5, figsize=(20, 10))
        axes = axes.flatten()
        
        for ax, key in zip(axes, subhyperfeatures):
            likelihood_col = f"{key} likelihood"
            if likelihood_col in df.columns:
                likelihood_data = row[likelihood_col]
                ax.plot(likelihood_data, color='purple')
                ax.axhline(first_threshold, color='red', linestyle='--', label=f'Threshold: {first_threshold}')
                ax.axhline(second_threshold, color='blue', linestyle='--', label=f'Secondary Threshold: {second_threshold}')
                ax.fill_between(np.arange(len(likelihood_data)), 0, likelihood_data, 
                                where=(likelihood_data > first_threshold), color='green', alpha=0.3, label='Above Threshold')
                ax.set_title(key)
                ax.set_xlabel("Frame")
                ax.set_ylabel("Likelihood")
                ax.set_ylim(0, 1)
                ax.legend()
            else:
                ax.text(0.5, 0.5, f"No column\n{likelihood_col}", 
                        horizontalalignment='center', verticalalignment='center')
                ax.axis('off')
        
        fig.suptitle(f"Subject: {row['subject']}, Date: {row['date']}, Trial: {row['trial_num']}")
        pp.savefig(fig)
        plt.close(fig)

    pp.close()
    print("PDF of likelihood graphs saved as:", filename)

def generate_pdf_report_with_start(df,
                                   experiment_path,
                                   filename,
                                   subhyperfeatures,
                                   all_features,
                                   side_features,
                                   likelihood_threshold=0.6,
                                   logic=True,
                                   use_largest_peak=True,
                                   debug=False):
    """
    Generate a PDF report for the jumping algorithm with algorithim start, decision, and end frames.
    -- This is useful for visually verifying the algorithm's performance, with frames pulled from the human start, decision, and end frames.

    """
    pp = PdfPages(filename)

    df = df.reset_index(drop=True)

    # starts a local cluster *and* the dashboard
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
    
    fut = [ja.calculate_decision_end_algorithm.remote(row, likelihood_threshold=0.6, sigma=2, k=3, baseline_window=200, features=subhyperfeatures, logic=logic, use_largest_peak=use_largest_peak) for idx, row in df.iterrows()]
    calc_jump_distances = ray.get(fut)
    
    for idx, row in df.iterrows():
        try:
            vid_file = ju.get_unambiguous_vidname_from_row(row, experiment_path)

            pst = row['Algorithm_Start']

            js, je, agg_pos, diff_pos, threshold, smooth_diff = calc_jump_distances[idx]

            pjd = js[-1] if js else None
            pen = je[-1] if je else None

            fig, axes = plt.subplots(1, 4, figsize=(40, 5))

            frame_start = None

            # - panel 1: start frame
            if pst is not None:
                frame_start = pst
                side_vid = vid_file.replace('_TOP_', '_SIDE_')
                img0 = ju.get_vid_frame(side_vid, pst)
                axes[0].imshow(img0.astype(np.uint8))
                axes[0].axis('off')
                axes[0].set_title('Frame at Algorithmic Start')
                axes[3].axvline(pst, color='green', linestyle='--', label='Algorithmic Start')
                df.loc[idx, 'Algorithm_Start'] = pst

            # — panel 2: decision frame
            frame_dec = None 
            if pjd is not None:
                frame_dec = pjd
                img1 = ju.get_vid_frame(vid_file, pjd)
                axes[1].imshow(img1.astype(np.uint8))
                axes[1].axis('off')
                axes[1].set_title('Frame at Algorithmic Decision')
                axes[3].axvline(pjd, color='orange', linestyle='--', label='Algorithmic Decision')
                df.loc[idx, 'Algorithm_Decision'] = pjd

            # — panel 3: end frame
            frame_end = None
            if pen is not None:
                frame_end = pen
                # TODO: get CUDA optimized frame
                img2 = ju.get_vid_frame(vid_file, pen)
                axes[2].imshow(img2.astype(np.uint8))
                axes[2].axis('off')
                axes[2].set_title('Frame at Algorithmic End')
                axes[3].axvline(pen, color='midnightblue', linestyle='--', label='Algorithmic End')
                df.loc[idx, 'Algorithm_End'] = pen

            # — panel 3: velocity + thresholds
            axv = axes[3]
            axv.plot(
                np.arange(1, len(agg_pos)),
                smooth_diff,
                lw=2,
                color='black',
                rasterized=True,
                zorder=5,
                label='Velocity (Gaussian)'
            )
            axv.axhline(threshold, linestyle='--', label='Spike Threshold')
            # vertical lines
            axv.set_xlabel('Frame')
            axv.set_ylabel('Velocity')
            axes[3].set_title(label='Velocity vs Time', loc='left')
            axv.legend()

            masked_side = {}
            for kp in side_features:
                lik = row[f"{kp} likelihood"]
                x_arr = row[f"{kp} x"].copy()
                y_arr = row[f"{kp} y"].copy()
                mask = lik < likelihood_threshold
                x_arr[mask] = np.nan
                y_arr[mask] = np.nan
                masked_side[f"{kp} x"] = x_arr
                masked_side[f"{kp} y"] = y_arr

            # — mask low‐likelihood keypoints in the row (no new HDF reads)
            masked = {}
            for kp in all_features:
                lik = row[f"{kp} likelihood"]
                x_arr = row[f"{kp} x"].copy()
                y_arr = row[f"{kp} y"].copy()
                mask = lik < likelihood_threshold
                x_arr[mask] = np.nan
                y_arr[mask] = np.nan
                masked[f"{kp} x"] = x_arr
                masked[f"{kp} y"] = y_arr
                arr = masked[f"{kp} x"]
                vel = np.concatenate(([np.nan], np.diff(arr))) # x-velocities
                axv.plot(vel, linewidth=1, alpha=0.7)

            # — scatter keypoints on panels 1–3
            for ax, frame in zip(axes[0:3], (frame_start, frame_dec, frame_end)):
                if frame is not None:  # Only process if frame is not None
                    frame = int(frame)  # Convert to integer to ensure valid indexing
                    if ax == axes[0]:  # Start frame uses side view keypoints
                        xs = [masked_side[f"{kp} x"][frame] for kp in side_features]
                        ys = [masked_side[f"{kp} y"][frame] for kp in side_features]
                        ax.scatter(xs, ys, rasterized=True)
                    else:
                        xs = [masked[f"{kp} x"][frame] for kp in all_features]
                        ys = [masked[f"{kp} y"][frame] for kp in all_features]
                        ax.scatter(xs, ys, rasterized=True)

            # — title & save
            fig.suptitle(
                f"{row['subject']} {row['date']}  "
                f"Trial {int(row['trial_num'])} -- "
                f"Algo. Start: {int(pst)} -- Algo. Decision: {pjd} -- Algo. End: {pen}"
            )
            pp.savefig(fig)
            plt.close(fig)

        except Exception as e:
            print(f"Error processing trial {idx}: {e}")
    
    ray.shutdown()
    pp.close()

    print("→ PDF report generated:", filename)

    ray.shutdown()
