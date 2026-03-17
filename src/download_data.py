import pandas as pd
import requests
import os

os.makedirs("../data/raw", exist_ok=True)

# --- CO2 (NOAA) ---
co2_url = "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.csv"
co2 = pd.read_csv(co2_url, comment='#')

co2 = co2.rename(columns={
    "year": "Year",
    "month": "Month",
    "average": "co2"
})

co2 = co2[["Year", "Month", "co2"]]
co2.to_csv("../data/raw/co2.csv", index=False)

# --- CH4 (NOAA) ---
ch4_url = "https://gml.noaa.gov/webdata/ccgg/trends/ch4/ch4_mm_gl.csv"
ch4 = pd.read_csv(ch4_url, comment='#')

ch4 = ch4.rename(columns={
    "year": "Year",
    "month": "Month",
    "average": "ch4"
})

ch4 = ch4[["Year", "Month", "ch4"]]
ch4.to_csv("../data/raw/ch4.csv", index=False)

# --- Temperature (NASA GISS) ---
temp_url = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
temp = pd.read_csv(temp_url, skiprows=1)

temp = temp.rename(columns={"Year": "Year"})

temp = temp.melt(id_vars=["Year"], var_name="Month", value_name="temperature")

month_map = {
    "Jan":1,"Feb":2,"Mar":3,"Apr":4,"May":5,"Jun":6,
    "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12
}

temp["Month"] = temp["Month"].map(month_map)
temp = temp.dropna()

temp.to_csv("../data/raw/temperature.csv", index=False)

print("Datasets downloaded successfully.")
