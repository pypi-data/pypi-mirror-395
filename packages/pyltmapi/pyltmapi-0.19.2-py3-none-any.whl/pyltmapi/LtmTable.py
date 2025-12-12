import os

import matplotlib.pyplot as plt

from pyltmapi import LtmSession


def make_table_cnes(arg):
    """
    Read the FBMC result summary file fbmc_stats.txt and creates a summary table of
    results. Two types of arguments are accepted. 1. 'LtmSession' or
    2. 'str' with path to result file.
    """

    cne_name = []

    # Determine file folder and extract CNE names if applicable
    if isinstance(arg, str):
        file_folder = arg
    elif isinstance(arg, LtmSession):
        try:
            file_folder = arg.model.global_settings.output_path
            cne_name = [cne.name for cne in arg.model.cnes()]
        except AttributeError as e:
            print("Invalid LtmSession structure:", e)
            return
    else:
        raise TypeError("Unsupported argument type. Must be str or LtmSession.")

    # Build file path
    result_file = 'fbmc_stats.txt'
    file_path = os.path.join(file_folder, result_file)

    # Read and parse the file
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()[1:]
    except FileNotFoundError:
        print(f"File not found at: {os.path.abspath(file_path)}")
        return
    except Exception as e:
        print("Error reading file:", e)
        return

    # Parse and convert the data
    parsed_data = [[int(row[0]), float(row[1]), int(row[2])] for row in (line.strip().split() for line in lines)]
    highest_cne_number = max(row[0] for row in parsed_data)

    if cne_name:
        if len(cne_name) >= highest_cne_number:
            # Map CNE numbers to their data
            data_dict = {row[0]: row for row in parsed_data}

            filtered_rows = []
            filtered_names = []
            for idx, name in enumerate(cne_name):
                cne_number = idx + 1
                if cne_number in data_dict:
                    filtered_names.append(name)
                    filtered_rows.append(data_dict[cne_number])

            # Add CNE names as the first column
            table_data = [[name] + row for name, row in zip(filtered_names, filtered_rows)]

            # Column labels
            columns = ["CNE name", "CNE number", "Mean dual value", "No. of times constraint is binding"]

    else:
        table_data = parsed_data
        # Column labels
        columns = ["CNE number", "Mean dual value", "No. of times constraint is binding"]

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(14, 2))

    # Hide axes
    ax.axis('off')
    ax.axis('tight')

    # Create the table
    table = ax.table(cellText=table_data, colLabels=columns, loc='center', cellLoc='center', colColours=['#d3d3d3']*4)

    # Style the header
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold')
            cell.set_facecolor('#a9a9a9')
        else:
            cell.set_facecolor('#f0f0f0')

    # Adjust layout
    fig.tight_layout()

    # Display the table
    plt.show()
