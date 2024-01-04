from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np
import folium 
from folium.plugins import HeatMap, MarkerCluster

app = Flask(__name__, template_folder="templates")

@app.route('/')
def home():
    merge_df = pd.read_csv("data/merge_df.csv")
    columnsKeep = ["year","carrier","carrier_name","airport","airport_name","per_delayed"]
    years = list(merge_df["year"].unique())
    merge_df["per_delayed"] = (merge_df["arr_del15"] / merge_df["arr_flights"])
    clean_merge_df = pd.DataFrame(merge_df, columns=columnsKeep)

    def avg_by_airport(year):
        avgByAirport = clean_merge_df[clean_merge_df["year"] == year].groupby("airport")["per_delayed"].mean()
        return avgByAirport
    def percentify(data):
        percentified = round((data * 100), 2)
        return percentified
    
    y_vals = []
    for i in years:
        loop_val = np.mean(list(avg_by_airport(i)))
        y_vals.append(loop_val)
    for i, val in enumerate(y_vals):
        y_vals[i] = percentify(val)

    x = years
    y = y_vals

    fig = px.line(x=x, y=y, labels={'x':'Year', 'y':'Percent of Delayed Flights'} )
    fig.update_yaxes(range=[1, 40])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON=graphJSON)

@app.route("/airports")
def airports():
    merge_df = pd.read_csv("data/merge_df.csv")
    columnsKeep = ["year","carrier","carrier_name","airport","airport_name","per_delayed"]
    years = list(merge_df["year"].unique())
    merge_df["per_delayed"] = (merge_df["arr_del15"] / merge_df["arr_flights"])
    clean_merge_df = pd.DataFrame(merge_df, columns=columnsKeep)

    def avg_by_airport(year):
        avgByAirport = clean_merge_df[clean_merge_df["year"] == year].groupby("airport")["per_delayed"].mean()
        return avgByAirport
    def percentify(data):
        percentified = round((data * 100), 2)
        return percentified

    delaysByAirports = pd.DataFrame( columns=list(clean_merge_df["airport"].unique()) )
    for i in years:
        delaysByAirports.loc[i] = avg_by_airport(i)
    delaysByAirports = percentify(delaysByAirports)
    delaysByAirports = delaysByAirports.transpose().reset_index()
    delaysByAirports.columns = ['Airport'] + list(years)
    melted_df = pd.melt(delaysByAirports, id_vars=['Airport'], var_name='Year', value_name='Delay')

    fig = px.line(melted_df, x='Year', y='Delay', color='Airport', labels={'Year': 'Year', 'Delay': 'Percentage of Delayed Flights'}, )
    fig.update_yaxes(range=[1, 50])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("airport.html", graphJSON=graphJSON)

@app.route("/carriers")
def carriers():
    merge_df = pd.read_csv("data/merge_df.csv")
    columnsKeep = ["year","carrier","carrier_name","airport","airport_name","per_delayed"]
    years = list(merge_df["year"].unique())
    merge_df["per_delayed"] = (merge_df["arr_del15"] / merge_df["arr_flights"])
    clean_merge_df = pd.DataFrame(merge_df, columns=columnsKeep)

    def avg_by_carrier(year):
        avgByCarrier = clean_merge_df[clean_merge_df["year"] == year].groupby("carrier_name")["per_delayed"].mean()
        return avgByCarrier
    def percentify(data):
        percentified = round((data * 100), 2)
        return percentified
    
    delaysByCarrier = pd.DataFrame( columns=list(clean_merge_df["carrier_name"].unique()) )
    for i in years:
        delaysByCarrier.loc[i] = avg_by_carrier(i)
    delaysByCarrier = percentify(delaysByCarrier)
    delaysByCarrier = delaysByCarrier.transpose().reset_index()
    delaysByCarrier.columns = ['Carrier'] + list(years)
    melted_df = pd.melt(delaysByCarrier, id_vars=['Carrier'], var_name='Year', value_name='Delay')

    fig = px.line(melted_df, x='Year', y='Delay', color='Carrier', labels={'Year': 'Year', 'Delay': 'Percentage of Delayed Flights'} )
    fig.update_yaxes(range=[1, 75])

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("carrier.html", graphJSON=graphJSON)

@app.route("/heatmap")
def heatmap():
    m_airports = folium.Map(location=(39.8283, -98.5795),tiles="Cartodb dark_matter", zoom_start=4)

    data = pd.read_csv("data/joined_raw_airports.csv")
    airports_table = pd.read_csv("data/top25_airport_codes.csv")
    map_df = data.drop(columns=["id","carrier_ct", "carrier", "carrier_name", "weather_ct", "nas_ct","security_ct","late_aircraft_ct", "arr_diverted", "arr_delay","carrier_delay", "weather_delay","nas_delay", "security_delay", "late_aircraft_delay", "id-2","country_code"])

    delay_percents = round((map_df.groupby('iata')['arr_del15'].sum()/map_df.groupby('iata')["arr_flights"].sum())*100, 3)
    cancel_percents = round((map_df.groupby('iata')['arr_cancelled'].sum()/map_df.groupby('iata')["arr_flights"].sum())*100, 3)

    lat = map_df.groupby('iata')['latitude'].unique().astype(float).tolist()
    lng = map_df.groupby('iata')['longitude'].unique().astype(float).tolist()

    delay = delay_percents.astype(float).tolist()
    cancel = cancel_percents.astype(float).tolist()

    delay_heat = list(zip(lat, lng, delay))
    cancel_heat = list(zip(lat, lng, cancel))

    marker_cluster = MarkerCluster(name="Airports").add_to(m_airports)

    for row in airports_table.itertuples():
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=(f"{row.iata}: {row.airport}"),
            icon=folium.Icon(color="blue", icon="plane")
        ).add_to(marker_cluster)

    fg1 = folium.FeatureGroup(name="Delays", control=True).add_to(m_airports)
    HeatMap(delay_heat, gradient={0.2:'blue', 0.4:'green', 0.6:'yellow', 0.8:'orange', 1: 'red'}).add_to(fg1)

    fg2 = folium.FeatureGroup(name="Cancellations", control=True).add_to(m_airports)
    HeatMap(cancel_heat, gradient={0.2:'blue', 0.4:'green', 0.6:'yellow', 0.8:'orange', 1: 'red'}).add_to(fg2)

    folium.LayerControl(collapsed=False).add_to(m_airports)

    m_airports.get_root().width = "800px"
    m_airports.get_root().height = "600px"
    iframe = m_airports.get_root()._repr_html_()
    
    return render_template("heatmap.html", iframe=iframe)

if __name__ == "__main__":
    app.run()