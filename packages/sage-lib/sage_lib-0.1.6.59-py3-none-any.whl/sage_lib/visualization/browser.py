# sage_lib/visualization/browser.py
# ------------------------------------------------------------
# Interactive GUI launcher for structure visualization
# ------------------------------------------------------------
from .PartitionProvider import PartitionProvider
from .visualizer import browse_structures


def gui(partition, start_index: int = 0, replicas=(0, 0, 0),
        draw_boxes_for_all: bool = False, verbose: bool = True):
    """
    Launch an interactive GUI visualization for the given Partition object.

    Parameters
    ----------
    partition : Partition
        The Partition object containing atomic structures.
    start_index : int, optional
        Index of the first structure to display. Default is 0.
    replicas : tuple(int, int, int), optional
        Periodic replicas to visualize (nx, ny, nz). Default is (100, 100, 0).
    draw_boxes_for_all : bool, optional
        If True, draw bounding boxes for all structures. Default is False.
    verbose : bool, optional
        If True, print progress and summary messages to the console.

    Behavior
    --------
    Opens an interactive 3D visualization window for exploring atomic structures.
    """
    if verbose:
        print("==============================================")
        print(" Sage-Lib Visualization Interface")
        print("==============================================")
        print("Initializing PartitionProvider...")

    # Initialize provider
    provider = PartitionProvider(partition)
    n_structs = len(provider)
    print( partition.get_all_energies().shape )
    if verbose:
        print(f" → Loaded Partition with {n_structs} structures.")
        print(f" → Starting visualization from index {start_index}.")
        print(f" → Periodic replicas: {replicas}")
        print(f" → Bounding boxes for all: {draw_boxes_for_all}")
        print("----------------------------------------------")
        print("Launching visualization window...")
        print("Use arrow keys or navigation controls to browse.")
        print("Close the window to return to terminal.")
        print("==============================================")

    # Launch the visualization
    browse_structures(
        provider,
        start_index=start_index,
        replicas=replicas,
        draw_boxes_for_all=draw_boxes_for_all
    )

    if verbose:
        print("\nVisualization session ended.")
        print(f"Displayed {n_structs} structures in total.")
        print("Returning to CLI context.\n")
