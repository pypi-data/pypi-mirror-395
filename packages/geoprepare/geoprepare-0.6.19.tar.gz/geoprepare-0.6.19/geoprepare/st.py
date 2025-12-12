import pandas as pd
import matplotlib.pyplot as plt

with plt.style.context("science"):
    data = {
        "State": [
            "Illinois",
            "Indiana",
            "Iowa",
            "Kansas",
            "Michigan",
            "Minnesota",
            "Missouri",
            "Nebraska",
            "North Dakota",
            "Ohio",
            "South Dakota",
            "Wisconsin",
        ],
        "May": [
            62.3,
            61.45,
            60.41,
            43.15,
            52.25,
            52.91,
            50.94,
            60.8,
            40.52,
            58.9,
            47.95,
            53.84,
        ],
        "Jun": [
            58.13,
            57.07,
            58.66,
            43.31,
            49.85,
            49.75,
            51.4,
            59.8,
            37.97,
            56.12,
            43.66,
            52.84,
        ],
        "Jul": [
            60.88,
            60.97,
            58.5,
            42.34,
            53.42,
            48.5,
            52.46,
            60.88,
            39.04,
            55.78,
            46.48,
            52.15,
        ],
        "Aug": [
            62.57,
            60.72,
            59.09,
            43.24,
            53.43,
            49.45,
            50.57,
            60.88,
            41.33,
            57.78,
            49.28,
            52.08,
        ],
        "Sep": [
            63.12,
            60.98,
            60.16,
            43.24,
            53.6,
            50.51,
            50.77,
            61.83,
            42.48,
            55.26,
            50.05,
            52.27,
        ],
        "USDA_August": [65, 63, 63, 39, 50, 49, 50, 59, 38, 55, 47, 54],
        "USDA_September": [67, 60, 64, 39, 52, 48, 51, 59, 38, 52, 47, 53],
    }

    df = pd.DataFrame(data)

    # Create a list of months for plotting
    months = ["May", "Jun", "Jul", "Aug", "Sep"]

    # Determine the number of rows and columns for the subplots
    n_cols = 6
    n_rows = (
        len(df) + n_cols - 1
    ) // n_cols  # This ensures the correct number of rows based on number of states

    # Plotting the time-series data with 3 columns
    fig, axes = plt.subplots(
        nrows=n_rows, ncols=n_cols, figsize=(15, 8), sharex=True, sharey=True
    )

    # Flatten axes for easier iteration
    axes = axes.flatten()

    for i, state in enumerate(df["State"]):
        axes[i].plot(months, df.loc[i, months], color="blue", marker="o", label=None)
        # Add USDA Forecasts for August and September and connect them
        axes[i].plot(
            ["Aug", "Sep"],
            [df.loc[i, "USDA_August"], df.loc[i, "USDA_September"]],
            color="black",
            marker="o",
            label="USDA",
        )
        axes[i].set_title(f"{state}", fontsize=16)
        axes[i].set_ylabel("")
        # if i%6 == 0:
        #     print(i, state)
        #     axes[i].set_ylabel('Yield Forecast (bu/ac)', fontsize=16)

        # Set tick label font size to 12 for both x and y axes
        axes[i].tick_params(axis="both", which="major", labelsize=12)

    # Add a legend to the top-left plot
    axes[0].legend(loc="upper left", title=None, frameon=True)

    # Remove x-axis labels (no "Month" label) and y-axis labels on all other subplots
    for ax in axes:
        ax.set_xlabel("")
        # ax.set_ylabel('')

    # Calculate the index for the middle row in the first column
    middle_row_index = (n_rows // 2) * n_cols  # The middle row's first column index

    # Set the y-axis label only for the first column, centered on the middle row
    # axes[2].set_ylabel('Yield Forecast (bu/ac)', labelpad=30)

    # Remove empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])
    fig.supylabel("Yield Forecast (bu/ac)", fontsize=16)
    # Add a legend outside the plot
    # fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.02), ncol=2)

    # Set common x-axis label
    # axes[6].set_ylabel('Yield Forecast (bu/ac)')
    # axes[-1].set_xlabel('Month')

    plt.tight_layout(rect=[0, 0, 1, 0.97])  # Adjust layout to fit legend
    plt.show()
