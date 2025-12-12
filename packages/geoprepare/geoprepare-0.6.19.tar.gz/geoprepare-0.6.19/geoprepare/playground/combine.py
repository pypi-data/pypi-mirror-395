import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

def main():
    """
    Demonstrates how to create a lookup table that identifies:
      (1) the dominant region (largest overlap) per state,
      (2) other regions that overlap each state,
      (3) the area of overlap for those secondary regions, and
      (4) the percentage overlap of each state for the dominant region.
    """

    # -------------------------------------------------------------------------
    # 1. Read the shapefiles
    # -------------------------------------------------------------------------
    # Example file paths (replace with your own)
    states_fp = r"C:\Users\ritvik\Downloads\CM Region Shapefiles-20241224T204131Z-001\CM Region Shapefiles\gaul1_asap_v04.shp"
    regions_fp = r"C:\Users\ritvik\Downloads\CM Region Shapefiles-20241224T204131Z-001\CM Region Shapefiles\Global_Regions_2024-06.shp"

    # Read the data using GeoPandas
    gdf_states = gpd.read_file(states_fp)
    gdf_regions = gpd.read_file(regions_fp)

    # -------------------------------------------------------------------------
    # 2. Check and align Coordinate Reference Systems (CRS)
    # -------------------------------------------------------------------------
    if gdf_states.crs != gdf_regions.crs:
        print(f"Different CRS detected. Converting regions to match states' CRS.")
        gdf_regions = gdf_regions.to_crs(gdf_states.crs)

    # -------------------------------------------------------------------------
    # 3. (Optional) Project to an equal-area projection
    #     - This step is important if your current CRS is geographic (e.g. EPSG:4326)
    #     - Choose an appropriate equal-area projection for your region of interest
    # -------------------------------------------------------------------------
    # Example: If these are US states, you might use EPSG:5070
    # (Comment out or remove if your shapefiles are already in a suitable projection)
    # states_equal_area = gdf_states.to_crs("EPSG:5070")
    # regions_equal_area = gdf_regions.to_crs("EPSG:5070")
    # gdf_states = states_equal_area
    # gdf_regions = regions_equal_area

    # -------------------------------------------------------------------------
    # 4. Compute spatial intersections
    # -------------------------------------------------------------------------
    # The 'intersection' overlay will result in new polygons representing
    # the portion of a state that falls within a region.
    print("Performing spatial overlay for intersection...")
    gdf_intersect = gpd.overlay(gdf_states, gdf_regions, how="intersection")

    # -------------------------------------------------------------------------
    # 5. Calculate area of each intersection
    # -------------------------------------------------------------------------
    # If your CRS is truly equal-area, .area will give you accurate areas.
    gdf_intersect["area_intersection"] = gdf_intersect.geometry.area

    # -------------------------------------------------------------------------
    # 5a. Calculate total area for each state (for percentage calculations)
    # -------------------------------------------------------------------------
    # 'name1_shr' appears to be your unique state identifier;
    # Adjust if needed for your data.
    gdf_states["state_area"] = gdf_states.geometry.area

    # Create a simple lookup of state -> total area
    df_state_area = gdf_states[["name1_shr", "state_area"]].copy()

    # -------------------------------------------------------------------------
    # 6. Summarize intersection area by state and region
    # -------------------------------------------------------------------------
    # Replace column names as needed to match your data
    df_area_sum = (
        gdf_intersect
        .groupby(["name1_shr", "ADM0_NAME", "Name", "Key"], as_index=False)["area_intersection"]
        .sum()
    )

    # Merge the total state area onto this DataFrame
    df_area_sum = df_area_sum.merge(df_state_area, on="name1_shr", how="left")

    # -------------------------------------------------------------------------
    # 6a. Compute the percentage of the state’s area for each overlap
    # -------------------------------------------------------------------------
    df_area_sum["percentage_intersection"] = (
        df_area_sum["area_intersection"] / df_area_sum["state_area"] * 100
    )

    # -------------------------------------------------------------------------
    # 7. Identify dominant (largest) overlap region for each state
    #    (based on absolute area, not percentage — but you can change if desired)
    # -------------------------------------------------------------------------
    idx_max_overlap = df_area_sum.groupby("name1_shr")["area_intersection"].idxmax()

    df_largest_overlap = df_area_sum.loc[idx_max_overlap].copy()
    # Rename columns for clarity
    df_largest_overlap.rename(
        columns={
            "name1_shr": "dominant_state",
            "area_intersection": "dominant_area"
        },
        inplace=True
    )

    # -------------------------------------------------------------------------
    # 7a. Sort (optional) and save final table
    # -------------------------------------------------------------------------
    df_largest_overlap.sort_values(["ADM0_NAME", "Name"], inplace=True)

    # Optionally, select the columns you want in the final CSV
    # (Below includes the new 'percentage_intersection' column)
    df_final = df_largest_overlap[
        [
            "dominant_state",
            "ADM0_NAME",
            "Name",
            "Key",
            "dominant_area",
            "state_area",
            "percentage_intersection"
        ]
    ]

    # -------------------------------------------------------------------------
    # 8. Save or export the final table
    # -------------------------------------------------------------------------
    output_csv = "lookup_table.csv"
    df_final.to_csv(output_csv, index=False)
    print(f"Lookup table saved to '{output_csv}'.")

    print("\n--- Preview of final lookup table ---")
    print(df_final.head(10))

if __name__ == "__main__":
    main()
