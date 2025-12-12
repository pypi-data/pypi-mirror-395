import os
import geopandas as gpd

dg = gpd.read_file(r'D:\Users\ritvik\projects\GEOGLAM\Input\Global_Datasets\Regions\Shps\adm_shapefile.shp')
print(dg.head())
# Get names of all countries in ADMIN0, if ADMIN2 for a country is all None, then
# set scales = ['admin_1'] else set scales = ['admin_2'], output should look like this:

# Determine scales for each ADMIN0
result = dg.groupby("ADMIN0")["ADMIN2"].apply(
    lambda admin2_values: "['admin_1']" if admin2_values.isnull().all() else "['admin_2']"
).reset_index()

# Rename columns for clarity
result.columns = ["Country", "Scales"]

# convert Country to lower case and replace spaces with underscores
result["Country"] = result["Country"].str.lower().str.replace(" ", "_")
print(result)
breakpoint()
