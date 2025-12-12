import numpy as np
import pandas as pd
from matplotlib.widgets import Slider, Button
import seaborn as sns
from pathlib import Path
import cv2
import warnings
from typing import Dict, List, Tuple, Union, Optional
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, HoverTool, Slider as BkSlider
from bokeh.layouts import column, row
from bokeh.io import curdoc
import sys

import matplotlib.pyplot as plt


class TrajectoryValidator:
    """
    A class for validating and visualizing trajectory data from animal tracking.
    Supports validation functions for likelihood thresholds, feature trails,
    and outcome detection.
    """
    
    def __init__(self, data_path: str, video_path: Optional[str] = None):
        """Initialize the validator with trajectory data and optional video."""
        self.data_path = Path(data_path)
        self.video_path = Path(video_path) if video_path else None
        self.data = self._load_data()
        self.video = None
        if self.video_path and self.video_path.exists():
            self._load_video()
            
    def _load_data(self) -> pd.DataFrame:
        """Load trajectory data from file."""
        if self.data_path.suffix == '.csv':
            return pd.read_csv(self.data_path)
        elif self.data_path.suffix == '.h5':
            return pd.read_hdf(self.data_path)
        else:
            raise ValueError(f"Unsupported file format: {self.data_path.suffix}")
            
    def _load_video(self) -> None:
        """Load video for visualization."""
        self.video = cv2.VideoCapture(str(self.video_path))
        self.total_frames = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    def get_frame(self, frame_idx: int) -> np.ndarray:
        """Get a specific frame from the video."""
        if self.video is None:
            raise ValueError("No video loaded")
        
        self.video.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = self.video.read()
        if not ret:
            raise ValueError(f"Could not read frame {frame_idx}")
        
        # Convert BGR to RGB
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
    def visualize_likelihood_trails(self, 
                                   feature_cols: List[str],
                                   likelihood_threshold: float = 0.6,
                                   random_frame: bool = True,
                                   frame_idx: Optional[int] = None):
        """
        Visualize feature trails with color indicating likelihood.
        """
        if self.video is None:
            fig, ax = plt.subplots(figsize=(10, 8))
            background = None
        else:
            if random_frame and frame_idx is None:
                frame_idx = np.random.randint(0, self.total_frames)
            elif frame_idx is None:
                frame_idx = 0
                
            background = self.get_frame(frame_idx)
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.imshow(background)
            
        # Process each feature
        for i in range(0, len(feature_cols), 2):
            if i + 1 >= len(feature_cols):
                continue  # Skip if we don't have y coordinate
                
            x_col = feature_cols[i]
            y_col = feature_cols[i+1]
            likelihood_col = x_col.replace('_x', '_likelihood')
            
            # Filter by likelihood threshold
            if likelihood_col in self.data.columns:
                valid_data = self.data[self.data[likelihood_col] >= likelihood_threshold]
                
                # Create a colormap for likelihood
                scatter = ax.scatter(valid_data[x_col], valid_data[y_col], 
                                   c=valid_data[likelihood_col], 
                                   alpha=0.7, s=5, cmap='viridis',
                                   vmin=likelihood_threshold, vmax=1.0)
                
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Likelihood')
        
        # Set title and labels
        frame_text = f"Random Frame: {frame_idx}" if random_frame else f"Frame: {frame_idx}"
        ax.set_title(f"Feature Trails with Likelihood >= {likelihood_threshold}\n{frame_text}")
        
        if background is None:
            ax.set_xlabel('X position')
            ax.set_ylabel('Y position')
        else:
            ax.set_xlim(0, self.width)
            ax.set_ylim(self.height, 0)  # Invert y-axis to match image coordinates
            
        return fig, ax
        
    def visualize_features_frozen(self, 
                                 feature_cols: List[str],
                                 frame_idx: int,
                                 likelihood_threshold: float = 0.6):
        """
        Visualize all features frozen at a specific frame.
        """
        if self.video is None:
            fig, ax = plt.subplots(figsize=(10, 8))
            background = None
        else:
            background = self.get_frame(frame_idx)
            fig, ax = plt.subplots(figsize=(10, 8))
            ax.imshow(background)
            
        # Filter data for the specific frame
        frame_data = self.data.iloc[frame_idx] if frame_idx < len(self.data) else None
        
        if frame_data is None:
            raise ValueError(f"Frame index {frame_idx} is out of bounds")
            
        # Process each feature
        for i in range(0, len(feature_cols), 2):
            if i + 1 >= len(feature_cols):
                continue  # Skip if we don't have y coordinate
                
            x_col = feature_cols[i]
            y_col = feature_cols[i+1]
            likelihood_col = x_col.replace('_x', '_likelihood')
            
            # Skip if likelihood is below threshold
            if likelihood_col in frame_data and frame_data[likelihood_col] >= likelihood_threshold:
                ax.scatter(frame_data[x_col], frame_data[y_col], 
                         s=50, label=x_col.replace('_x', ''))
                
        ax.set_title(f"Features at Frame {frame_idx}")
        ax.legend(loc='best')
        
        if background is None:
            ax.set_xlabel('X position')
            ax.set_ylabel('Y position')
        else:
            ax.set_xlim(0, self.width)
            ax.set_ylim(self.height, 0)
            
        return fig, ax
    
    def compare_variance(self, 
                        data2_path: str,
                        features: List[str]) -> pd.DataFrame:
        """Compare variance between two tracking datasets."""
        # Load second dataset
        data2_path = Path(data2_path)
        if data2_path.suffix == '.csv':
            data2 = pd.read_csv(data2_path)
        elif data2_path.suffix == '.h5':
            data2 = pd.read_hdf(data2_path)
        else:
            raise ValueError(f"Unsupported file format: {data2_path.suffix}")
        
        # Check if datasets have the same length
        if len(self.data) != len(data2):
            warnings.warn(f"Datasets have different lengths: {len(self.data)} vs {len(data2)}")
            min_len = min(len(self.data), len(data2))
            data1_subset = self.data.iloc[:min_len]
            data2_subset = data2.iloc[:min_len]
        else:
            data1_subset = self.data
            data2_subset = data2
            
        # Calculate variance and differences
        results = []
        for feature in features:
            if feature not in data1_subset.columns or feature not in data2_subset.columns:
                continue
                
            results.append({
                'feature': feature,
                'var_dataset1': data1_subset[feature].var(),
                'var_dataset2': data2_subset[feature].var(),
                'var_diff': abs(data1_subset[feature].var() - data2_subset[feature].var()),
                'mse': ((data1_subset[feature] - data2_subset[feature]) ** 2).mean()
            })
            
        return pd.DataFrame(results)
    
    def compare_binning_vs_raw(self,
                              feature_x: str,
                              feature_y: str,
                              bin_size: int = 10,
                              likelihood_threshold: float = 0.6):
        """Compare binned vs raw data for a given feature."""
        # Extract likelihood column
        likelihood_col = feature_x.replace('_x', '_likelihood')
        
        # Filter by likelihood
        if likelihood_col in self.data.columns:
            valid_data = self.data[self.data[likelihood_col] >= likelihood_threshold]
        else:
            valid_data = self.data
            
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
        
        # Raw data scatter plot
        ax1.scatter(valid_data[feature_x], valid_data[feature_y], alpha=0.5, s=5)
        ax1.set_title('Raw Data')
        ax1.set_xlabel(feature_x)
        ax1.set_ylabel(feature_y)
        
        # Create 2D histogram (binned data)
        h, xedges, yedges = np.histogram2d(
            valid_data[feature_x], 
            valid_data[feature_y], 
            bins=bin_size
        )
        
        # Plot binned data as heatmap
        im = ax2.imshow(h.T, origin='lower', aspect='auto', 
                       extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                       cmap='viridis')
        ax2.set_title(f'Binned Data (bin_size={bin_size})')
        ax2.set_xlabel(feature_x)
        ax2.set_ylabel(feature_y)
        
        cbar = plt.colorbar(im, ax=ax2)
        cbar.set_label('Count')
        
        return fig, (ax1, ax2)
    
    def detect_outcome(self,
                      start_position: Tuple[float, float],
                      gap_midpoint: Tuple[float, float],
                      target_zone: Tuple[float, float, float, float],
                      feature_x: str,
                      feature_y: str,
                      likelihood_threshold: float = 0.6) -> str:
        """
        Detect if a trial was successful, failed, or aborted.
        
        - abort: doesn't cross the halfway point of the gap
        - failure: crosses halfway but doesn't reach target zone
        - success: reaches target zone
        """
        # Extract likelihood column
        likelihood_col = feature_x.replace('_x', '_likelihood')
        
        # Filter by likelihood
        if likelihood_col in self.data.columns:
            valid_data = self.data[self.data[likelihood_col] >= likelihood_threshold]
        else:
            valid_data = self.data
            
        # Define target zone
        x_min, y_min, x_max, y_max = target_zone
        
        # Check if any point entered the target zone (success)
        in_target = ((valid_data[feature_x] >= x_min) & 
                     (valid_data[feature_x] <= x_max) &
                     (valid_data[feature_y] >= y_min) & 
                     (valid_data[feature_y] <= y_max))
        
        if in_target.any():
            return "success"
            
        # Calculate distance to gap midpoint for each frame
        distances_to_midpoint = np.sqrt(
            (valid_data[feature_x] - gap_midpoint[0])**2 + 
            (valid_data[feature_y] - gap_midpoint[1])**2
        )
        
        # Calculate distance from start to midpoint
        start_to_mid_distance = np.sqrt(
            (start_position[0] - gap_midpoint[0])**2 + 
            (start_position[1] - gap_midpoint[1])**2
        )
        
        # Check if any point crossed the midpoint
        if (distances_to_midpoint < start_to_mid_distance / 2).any():
            return "failure"  # Crossed midpoint but didn't reach target
        else:
            return "abort"    # Didn't even cross midpoint
    
    def create_interactive_visualization(self, feature_cols: List[str], likelihood_threshold: float = 0.6):
        """Create an interactive Bokeh visualization for trajectory data."""
        # Create data sources for each feature
        sources = {}
        
        for i in range(0, len(feature_cols), 2):
            if i + 1 >= len(feature_cols):
                continue
                
            x_col = feature_cols[i]
            y_col = feature_cols[i+1]
            feature_name = x_col.replace('_x', '')
            likelihood_col = f"{feature_name}_likelihood"
            
            if likelihood_col in self.data.columns:
                valid_data = self.data[self.data[likelihood_col] >= likelihood_threshold]
                
                source_data = {
                    'x': valid_data[x_col],
                    'y': valid_data[y_col],
                    'likelihood': valid_data[likelihood_col],
                    'frame': valid_data.index
                }
                
                sources[feature_name] = ColumnDataSource(data=source_data)
        
        # Create figure
        tooltips = [
            ("Frame", "@frame"),
            ("X", "@x"),
            ("Y", "@y"),
            ("Likelihood", "@likelihood")
        ]
        
        p = figure(width=800, height=600, 
                 tools="pan,wheel_zoom,box_zoom,reset,save",
                 title="Interactive Trajectory Visualization",
                 tooltips=tooltips)
        
        # Add trajectories for each feature
        colors = plt.cm.tab10.colors
        for i, (feature_name, source) in enumerate(sources.items()):
            color_hex = f"#{int(colors[i % len(colors)][0]*255):02x}{int(colors[i % len(colors)][1]*255):02x}{int(colors[i % len(colors)][2]*255):02x}"
            p.line('x', 'y', source=source, color=color_hex, alpha=0.7, line_width=2, legend_label=feature_name)
            p.circle('x', 'y', source=source, color=color_hex, alpha=0.5, size=5, legend_label=feature_name)
        
        p.legend.click_policy = "hide"
        
        return p


def create_validation_gui(data_path: str, video_path: Optional[str] = None):
    """Create a validation GUI for trajectory data."""
    validator = TrajectoryValidator(data_path, video_path)
    feature_cols = [col for col in validator.data.columns if col.endswith('_x') or col.endswith('_y')]
    p = validator.create_interactive_visualization(feature_cols)
    
    doc = curdoc()
    doc.add_root(p)
    doc.title = "Trajectory Validation GUI"
    
    return doc


if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print("Usage: python validation.py <data_path> [video_path]")
        sys.exit(1)
        
    data_path = sys.argv[1]
    video_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    create_validation_gui(data_path, video_path)