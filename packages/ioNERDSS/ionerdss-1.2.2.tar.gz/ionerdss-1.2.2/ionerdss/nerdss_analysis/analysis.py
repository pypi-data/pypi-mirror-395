"""
Refactored Analysis class for the ionerdss package.
This version uses the centralized data readers and implements a more efficient design.
"""

import os
import seaborn as sns
from .plot_figures import (
    plot_line_speciescopy_vs_time,
    plot_line_maximum_assembly_size_vs_time,
    plot_line_average_assembly_size_vs_time,
    plot_line_fraction_of_monomers_assembled_vs_time,
    plot_complex_count_vs_time,
    plot_hist_complex_species_size,
    plot_hist_monomer_counts_vs_complex_size,
    plot_hist_complex_species_size_3d,
    plot_hist_monomer_counts_vs_complex_size_3d,
    plot_heatmap_complex_species_size,
    plot_heatmap_monomer_counts_vs_complex_size,
    plot_heatmap_species_a_vs_species_b,
    plot_stackedhist_complex_species_size,
    plot_line_free_energy,
    plot_line_symmetric_association_probability,
    plot_line_asymmetric_association_probability,
    plot_line_symmetric_dissociation_probability,
    plot_line_asymmetric_dissociation_probability,
    plot_line_growth_probability,
    plot_line_liftime,
)

class Analysis:
    """
    A class for analyzing and visualizing NERDSS simulation results.
    
    This class provides methods to plot various types of figures and analyze
    data from one or more NERDSS simulations.
    """
    
    def __init__(self, save_dir: str = None):
        """
        Initialize the Analysis object.
        
        Parameters:
            save_dir (str, optional): Directory containing simulation results.
                If None, uses the current working directory.
        """
        # Resolve the directory path
        if save_dir is None:
            save_dir = os.getcwd()
        elif save_dir.startswith("~"):
            save_dir = os.path.expanduser(save_dir)

        self.save_dir = os.path.abspath(save_dir)
        
        # Initialize data IO handler
        # This function is not used now.
        # self.data_io = DataIO()

        # Determine if it's a single simulation or a batch
        if os.path.exists(os.path.join(self.save_dir, "DATA")):
            self.simulation_dirs = [self.save_dir]
            print("Detected a single simulation directory.")
        else:
            # Find parent directories containing a "DATA" folder
            self.simulation_dirs = [
                root for root, dirs, _ in os.walk(self.save_dir) if "DATA" in dirs
            ]
            print(f"Detected a batch of {len(self.simulation_dirs)} simulation directories.")
            
        # Create the figure_plot_data directory if it doesn't exist
        self.plot_data_dir = os.path.join(self.save_dir, "figure_plot_data")
        os.makedirs(self.plot_data_dir, exist_ok=True)

    def plot_figure(
        self,
        figure_type: str = "line",
        simulations: list = None,
        x: str = "time",
        y: str = "species",
        z: str = None,
        legend: list = None,
        user_file_name: str = None,
        bins: int = 10,
        time_bins: int = 10,
        time_frame: tuple = None,
        frequency: bool = False,
        normalize: bool = False,
        show_type: str = "both",
        font_size: int = 12,
        figure_size: tuple = (10, 6),
        seaborn_style: str = "ticks",
        seaborn_context: str = "paper",
    ):
        """
        Plot a figure based on the specified type and data.

        Parameters:
            figure_type (str): Type of figure to plot. Options are:
                - "line" (line plot)
                - "hist" (histogram)
                - "3dhist" (3D histogram)
                - "heatmap" (heatmap)
                - "stacked" (stacked histogram)
            
            simulations (list, optional): List of indices of simulation directories to include in the plot.
                If None, uses all available simulations.
            
            x (str): Variable for the x-axis.
            y (str): Variable for the y-axis.
            z (str, optional): Variable for the z-axis (only used in "3dhist" and "heatmap").
            
            legend (list, optional): Labels for the legend. If None, uses default labels.
            user_file_name(str, optional): gives the option of saving .csv output with a specific name. 
                Avoids save error for csvs plot_line_speciescopy_vs_time due to length. 
            bins (int): Number of bins for histograms. Default is 10.
            time_bins (int): Number of time bins for time-based 3d histograms. Default is 10.
            time_frame (tuple, optional): Time frame for the histogram. Default is None (uses full range).
            frequency (bool): If True, normalizes the histogram to show frequency. Default is False.
            normalize (bool): If True, normalizes the data for plotting. Default is False.
            
            show_type (str): Determines what data to display. Options are:
                - "individuals" → Shows all individual simulation results.
                - "average" → Shows only the averaged result.
                - "both" → Shows both individual and average results.

            font_size (int): Font size for the plot.
            figure_size (tuple): Size of the figure in inches.
            seaborn_style (str): Seaborn style for the plot. Default is "ticks".
                Options include "white", "dark", "whitegrid", "darkgrid", and "ticks".
            seaborn_context (str): Seaborn context for the plot. Default is "paper".
                Options include "paper", "notebook", "talk", and "poster".

        Raises:
            ValueError: If `figure_type` or `show_type` is invalid.
        """
        # Set seaborn styles
        sns.set_style(seaborn_style)
        sns.set_context(seaborn_context, rc={
            "font.size": font_size,
            "axes.titlesize": font_size,
            "axes.labelsize": font_size,
            "xtick.labelsize": font_size,
            "ytick.labelsize": font_size,
            "legend.fontsize": font_size,
            "font.family": "serif"
        })
        
        # Validate inputs
        valid_figure_types = {"line", "hist", "3dhist", "heatmap", "stacked"}
        valid_show_types = {"both", "individuals", "average"}

        if figure_type not in valid_figure_types:
            raise ValueError(f"Invalid figure_type '{figure_type}'. Must be one of {valid_figure_types}.")

        if show_type not in valid_show_types:
            raise ValueError(f"Invalid show_type '{show_type}'. Must be one of {valid_show_types}.")

        # Set default simulations if not provided
        simulations = simulations or list(range(len(self.simulation_dirs)))
        
        # Validate legend
        if not legend:
            raise ValueError("Legend must be provided.")

        # Print plot configuration
        print(f"Plotting {figure_type} with:")
        print(f"- x-axis: {x}")
        print(f"- y-axis: {y}")
        print(f"- z-axis: {z if z else 'None'}")
        print(f"- Simulations: {len(simulations)} selected")
        print(f"- Legend: {legend}")
        print(f"- Display mode: {show_type}")

        # Dispatch to the appropriate plotting function based on plot configuration
        plot_config = (figure_type, x, y, z)
        
        # Line plots
        if plot_config == ("line", "time", "species", None):
            plot_line_speciescopy_vs_time(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                user_file_name=user_file_name,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "time", "count", None):
            plot_complex_count_vs_time(
                save_dir=self.save_dir,
                simulations_index=simulations,
                target_complexes=legend,  # legend contains the complex specifications
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "time", "maximum_assembly", None):
            plot_line_maximum_assembly_size_vs_time(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "time", "average_assembly", None):
            plot_line_average_assembly_size_vs_time(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "time", "fraction_of_monomers_assembled", None):
            plot_line_fraction_of_monomers_assembled_vs_time(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "size", "free_energy", None):
            plot_line_free_energy(
                save_dir=self.save_dir,
                simulations_index=simulations,
                time_frame=time_frame,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "size", "symmetric_association_probability", None):
            plot_line_symmetric_association_probability(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                time_frame=time_frame,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "size", "asymmetric_association_probability", None):
            plot_line_asymmetric_association_probability(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                time_frame=time_frame,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "size", "symmetric_dissociation_probability", None):
            plot_line_symmetric_dissociation_probability(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                time_frame=time_frame,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "size", "asymmetric_dissociation_probability", None):
            plot_line_asymmetric_dissociation_probability(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                time_frame=time_frame,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "size", "growth_probability", None):
            plot_line_growth_probability(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                time_frame=time_frame,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("line", "size", "lifetime", None):
            plot_line_liftime(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                time_frame=time_frame,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
            
        # Histogram plots
        elif plot_config == ("hist", "size", "complex_count", None):
            plot_hist_complex_species_size(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_frame=time_frame,
                frequency=frequency,
                normalize=normalize,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("hist", "size", "monomer_count", None):
            plot_hist_monomer_counts_vs_complex_size(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_frame=time_frame,
                frequency=frequency,
                normalize=normalize,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
            
        # 3D histogram plots
        elif plot_config == ("3dhist", "size", "time", "complex_count"):
            plot_hist_complex_species_size_3d(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_bins=time_bins,
                frequency=frequency,
                normalize=normalize,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("3dhist", "size", "time", "monomer_count"):
            plot_hist_monomer_counts_vs_complex_size_3d(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_bins=time_bins,
                frequency=frequency,
                normalize=normalize,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
            
        # Heatmap plots
        elif plot_config == ("heatmap", "size", "time", "complex_count"):
            plot_heatmap_complex_species_size(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_bins=time_bins,
                frequency=frequency,
                normalize=normalize,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("heatmap", "size", "time", "monomer_count"):
            plot_heatmap_monomer_counts_vs_complex_size(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_bins=time_bins,
                frequency=frequency,
                normalize=normalize,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        elif plot_config == ("heatmap", "size", "size", "complex_count"):
            plot_heatmap_species_a_vs_species_b(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_bins=time_bins,
                frequency=frequency,
                normalize=normalize,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
            
        # Stacked histogram plots
        elif plot_config == ("stacked", "size", "complex_count", None):
            plot_stackedhist_complex_species_size(
                save_dir=self.save_dir,
                simulations_index=simulations,
                legend=legend,
                bins=bins,
                time_frame=time_frame,
                frequency=frequency,
                normalize=normalize,
                show_type=show_type,
                simulations_dir=self.simulation_dirs,
                figure_size=figure_size
            )
        else:
            raise ValueError(f"Unsupported plot configuration: {plot_config}")

    def visualize_trajectory(
        self, 
        trajectory_path: str = None, 
        save_gif: bool = False, 
        gif_name: str = "trajectory.gif", 
        fps: int = 10
    ):
        """
        Visualizes a trajectory from an XYZ file and optionally saves it as a GIF.

        Parameters:
            trajectory_path (str): Path to the XYZ trajectory file.
            save_gif (bool): If True, saves the trajectory animation as a GIF.
            gif_name (str): Name of the output GIF file (if save_gif is True).
            fps (int): Frames per second for the GIF animation.
        """
        import warnings
        import tempfile
        import imageio
        from PIL import Image
        
        # Ignore OVITO warning
        warnings.filterwarnings('ignore', message='.*OVITO.*PyPI')
        
        try:
            from ovito.io import import_file
            from ovito.vis import Viewport
        except ImportError:
            raise ImportError("OVITO is required for trajectory visualization. Please install it using 'pip install ovito'.")

        # Find trajectory file if not specified
        if trajectory_path is None:
            trajectory_path = os.path.join(self.simulation_dirs[0], "DATA", "trajectory.xyz")
        if not os.path.exists(trajectory_path):
            raise FileNotFoundError(f"Trajectory file '{trajectory_path}' not found.")
        
        # Import trajectory
        pipeline = import_file(trajectory_path)
        pipeline.add_to_scene()
        vp = Viewport(type=Viewport.Type.PERSPECTIVE)
        vp.zoom_all()

        # Create temporary directory for frames
        temp_dir = tempfile.mkdtemp()
        frame_paths = []

        # Render frames
        for frame in range(pipeline.source.num_frames):
            output_path = os.path.join(temp_dir, f"frame_{frame:04d}.png")
            vp.render_image(size=(800, 600), filename=output_path, frame=frame)
            frame_paths.append(output_path)

        # Create GIF
        gif_path = os.path.join(temp_dir, "trajectory.gif")
        imageio.mimsave(gif_path, [imageio.imread(frame) for frame in frame_paths], fps=fps)

        # Display GIF
        display(Image.open(gif_path))

        # Save GIF if requested
        if save_gif:
            gif_save_path = os.path.join(self.save_dir, gif_name)
            os.rename(gif_path, gif_save_path)
            print(f"Trajectory GIF saved at: {gif_save_path}")