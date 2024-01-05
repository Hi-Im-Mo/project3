from flask import Flask, render_template, request
import pandas as pd
import json
import plotly
import plotly.express as px
import numpy as np
import folium 
from folium.plugins import HeatMap, MarkerCluster

app = Flask(__name__, template_folder="templates")

@app.route('/', methods=['GET','POST'])
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

    selected_year = request.form.get('selected_value')
    try:
        if selected_year.isnumeric() == False:
            selected_year = 2023
        else:
            pass
    except:
        selected_year = 2023

    def generate_hm(year):
        selectedDF = merge_df.loc[merge_df["year"] == int(year)]
        heatmap_data = selectedDF[['carrier_name', 'airport_name', 'arr_del15']]
        heatmap_matrix = heatmap_data.pivot_table(index='airport_name', columns='carrier_name', values='arr_del15', aggfunc='sum', fill_value=0)

        fig2 = px.imshow(heatmap_matrix.values,
                    labels=dict(x='Carrier', y='Airport', color='Delays'),
                    x=heatmap_matrix.columns,
                    y=heatmap_matrix.index,
                    color_continuous_scale='YlOrRd',
                    title=f'Heatmap of Delays by Carrier and Airport in {year}',
                    width=900,
                    height=900,
                    text_auto=True)
        return fig2
    
    heatMap = generate_hm(selected_year)
    heatJSON = json.dumps(heatMap, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON=graphJSON, heatJSON=heatJSON)

@app.route("/airports", methods=['GET','POST'])
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
    
    selected_value = request.form.get('selected_value')
    
    _2023df = pd.read_csv("data/rawYearlyData/clean_files/clean_2023.csv")
    del _2023df["Unnamed: 0"]
    def generate_bar(airport):
        selectedDF = _2023df.loc[_2023df["airport"] == airport].copy()
        selectedDF["proportion"] = round((selectedDF["arr_delay"]/selectedDF["arr_flights"]),2)
        selectedDF_grouped = selectedDF.groupby(["carrier_name"])['proportion'].sum().reset_index()

        plot = px.bar(selectedDF_grouped, x='carrier_name', y='proportion',
                labels={'carrier_name': 'Carrier Name', 'proportion': 'Avg min Delayed per Flight'},
                title=f"Avg min Delayed per Flight at {airport}")
        return plot
    
    plot = generate_bar(selected_value)
    plotJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)    

    selectedDF = _2023df.loc[_2023df["airport"] == selected_value]
    data = {
        "Carrier Name": selectedDF["carrier_name"],
        "Total Arriving Flights": selectedDF["arr_flights"]
    }
    table = pd.DataFrame(data)
    table_html = table.to_html(classes='table table-striped', index=False)
    
    selected_value2 = request.form.get('selected_value2')
    user_input = request.form.get('user_input')

    def generate_pie(airport, carrier):
        selectedDF = _2023df.loc[_2023df["airport"]==airport]
        data = selectedDF.loc[selectedDF["carrier_name"]== carrier]
        columns = ["carrier_delay","weather_delay","nas_delay","security_delay","late_aircraft_delay"]
        values = [(data[i]/data["arr_delay"]).to_numpy()[0] for i in columns]
        labels = ["Delay by Carrier Action","Delay by Inclement Weather","Delay by National Aviation System","Delay by Security Breach","Delay by Late Aircraft"]

        fig = px.pie(names=labels, values=values, labels=labels, title=f"Breakdown by delay type for {carrier} flights out of {airport}")
        return fig
    try:
        pie = generate_pie(selected_value2, user_input)
    except IndexError:
        pie = generate_pie("ATL", "United Air Lines Inc.")
    pieJSON = json.dumps(pie, cls=plotly.utils.PlotlyJSONEncoder)    

    return render_template("airport.html", graphJSON=graphJSON, plotJSON=plotJSON, table_html=table_html, pieJSON=pieJSON)

@app.route("/carriers", methods=['GET','POST'])
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

    selected_value = request.form.get('selected_value')
    _2023df = pd.read_csv("data/rawYearlyData/clean_files/clean_2023.csv")
    del _2023df["Unnamed: 0"]
    def generate_bar(carrier):
        selectedDF = _2023df.loc[_2023df["carrier_name"] == carrier].copy()
        selectedDF["proportion"] = round((selectedDF["arr_delay"]/selectedDF["arr_flights"]),2)
        selectedDF_grouped = selectedDF.groupby(["airport"])['proportion'].sum().reset_index()

        plot = px.bar(selectedDF_grouped, x='airport', y='proportion',
                labels={'airport': 'Airport Name', 'proportion': 'Avg min Delayed per Flight'},
                title=f"Avg min Delayed per Flight at {carrier}")
        return plot
    
    plot = generate_bar(selected_value)
    plotJSON = json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)    

    selectedDF = _2023df.loc[_2023df["carrier_name"] == selected_value]
    data = {
        "Airport Name": selectedDF["airport_name"],
        "Total Arriving Flights": selectedDF["arr_flights"]
    }
    table = pd.DataFrame(data)
    table_html = table.to_html(classes='table table-striped', index=False)

    selected_value2 = request.form.get('selected_value2')
    user_input = request.form.get('user_input')

    def generate_pie(airport, carrier):
        selectedDF = _2023df.loc[_2023df["airport"]==airport]
        data = selectedDF.loc[selectedDF["carrier_name"]== carrier]
        columns = ["carrier_delay","weather_delay","nas_delay","security_delay","late_aircraft_delay"]
        values = [(data[i]/data["arr_delay"]).to_numpy()[0] for i in columns]
        labels = ["Delay by Carrier Action","Delay by Inclement Weather","Delay by National Aviation System","Delay by Security Breach","Delay by Late Aircraft"]

        fig = px.pie(names=labels, values=values, labels=labels, title=f"Breakdown by delay type for {carrier} flights out of {airport}")
        return fig
    try:
        pie = generate_pie(user_input, selected_value2)
    except IndexError:
        pie = generate_pie("ATL", "United Air Lines Inc.")
    pieJSON = json.dumps(pie, cls=plotly.utils.PlotlyJSONEncoder)    

    return render_template("carrier.html", graphJSON=graphJSON, plotJSON=plotJSON, table_html=table_html, pieJSON=pieJSON)

@app.route("/heatmap")
def heatmap():
    m_airports = folium.Map(location=(39.8283, -98.5795),tiles="Cartodb dark_matter", zoom_start=4)

    data = pd.read_csv("data/rawYearlyData/clean_files/clean_2023.csv")
    airports_df = pd.read_csv("data/top25_airport_codes.csv")
    airports_table = airports_df.drop(columns=['Unnamed: 0'])
    map_df = data.drop(columns=["Unnamed: 0", "carrier_ct", "carrier", "carrier_name", "weather_ct", "nas_ct","security_ct","late_aircraft_ct", "arr_diverted", "arr_delay","carrier_delay", "weather_delay","nas_delay", "security_delay", "late_aircraft_delay"])
    delay_percents = round((map_df.groupby('airport')['arr_del15'].sum()/map_df.groupby('airport')["arr_flights"].sum())*100, 3)
    cancel_percents = round((map_df.groupby('airport')['arr_cancelled'].sum()/map_df.groupby('airport')["arr_flights"].sum())*100, 3)

    lat = airports_table['latitude'].astype(float).tolist()
    lng = airports_table['longitude'].astype(float).tolist()

    delay = delay_percents.astype(float).tolist()
    cancel = cancel_percents.astype(float).tolist()

    delay_heat = list(zip(lat, lng, delay))
    cancel_heat = list(zip(lat, lng, cancel))

    marker_cluster = MarkerCluster(name="Airports").add_to(m_airports)

    for row in airports_table.itertuples():
        html = f"""<div style="min-width: 200px; max-width: 400px;">
            <h3>{row.iata}</h3> {row.airport}</div>"""
        folium.Marker(
            location=[row.latitude, row.longitude],
            popup=folium.Popup(html, max_width=300),
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