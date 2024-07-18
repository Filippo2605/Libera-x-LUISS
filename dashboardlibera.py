import pandas as pd
import json
import plotly.express as px
import folium
import geopandas as gpd
import plotly.graph_objects as go
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import time
import json
import re
from folium.plugins import HeatMap
import jenkspy
import numpy as np
import seaborn as sns
import matplotlib.colors as mcolors
from matplotlib.patches import Patch
import streamlit as st
from streamlit_folium import st_folium
from streamlit_option_menu import option_menu
from streamlit_folium import folium_static

st.sidebar.image('logo_luiss.png', width=150)


with st.sidebar:
    page = option_menu("Seleziona la pagina", ["Mappe", "Line Plot", "Andamenti Temporali","Riutilizzo dei Beni"], 
        icons=["globe", "bar-chart-line", "hourglass-split", "recycle"], menu_icon="house", default_index=0)
    

if page == "Mappe":


    
    st.image('logolibera.jpeg', width=700)

    # Display the second image in the second column
    
    st.write('''
      
    ## GAP 2 ACTIVITY - A.Y. 2023-2024  
     
    # LUISS x LIBERA   
   
    Coviello Matteo, Cufari Alberta, Da Vià Giovanni, Di Biasi Torquato, Morroni Alessandro, Navarra Filippo  
    ***''')

    
    st.write("""
Questa dashboard è dedicata all'analisi dei beni confiscati alle mafie in Italia e il loro riutilizzo. L'associazione LIBERA, fondata da Don Luigi Ciotti nel 1995, è un'organizzazione antimafia che si impegna nella lotta contro le mafie, la corruzione e l'illegalità. LIBERA promuove la cultura della legalità e della giustizia sociale attraverso l'uso sociale dei beni confiscati alle mafie.

In questa pagina della dashboard, esploriamo diverse visualizzazioni geografiche e temporali dei beni confiscati, utilizzando i dati di Openregio.
""")

    province_con_coordinate = pd.read_csv("province_con_coordinate.csv")
    geojson_path = "limits_IT_provinces.geojson"

    # Mappa Beni Trasferiti da Openregio per provincia
    province_aggregate = province_con_coordinate.groupby("Provincia Estesa").agg({"Numero beni trasferiti da Openregio": "sum"}).reset_index()

    # Carica il geojson
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Crea una mappa centrata sull'Italia
    mappa = folium.Map(location=[42.5, 12.5], zoom_start=6)

    # Creare un dizionario per accedere rapidamente al numero di beni per regione
    beni_dict = pd.Series(province_aggregate['Numero beni trasferiti da Openregio'].values, index=province_aggregate['Provincia Estesa']).to_dict()

    # Calcola i breakpoints per la colorazione
    breaks = jenkspy.JenksNaturalBreaks(n_classes=10)
    breaks.fit(province_aggregate['Numero beni trasferiti da Openregio'].values)
    bins = np.unique(np.array(breaks.breaks_).round(0))

    # Aggiungi il layer Choropleth alla mappa
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=province_aggregate,
        columns=["Provincia Estesa", "Numero beni trasferiti da Openregio"],
        key_on="feature.properties.prov_name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Numero beni confiscati",
        highlight=True,
        nan_fill_color="white",
        bins=bins.tolist()
    ).add_to(mappa)

    # Aggiungi tooltip per mostrare il numero di beni trasferiti quando si passa sopra una regione
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': 'transparent',
            'color': 'transparent',
            'weight': 0,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['prov_name'],
            aliases=['Provincia Estesa:'],
            localize=True,
            sticky=True,
            labels=True,
            toLocaleString=True
        )
    ).add_to(mappa)

    # Aggiungi popups personalizzati per ciascuna regione
    for feature in geojson_data['features']:
        provincia = feature['properties']['prov_name']
        beni = beni_dict.get(provincia, 0)
        popup = folium.Popup(f"{provincia}: {beni} beni", parse_html=True)
        folium.GeoJson(
            feature,
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': 'transparent',
                'weight': 0,
                'fillOpacity': 0
            },
            highlight_function=lambda x: {'weight': 0, 'color': 'blue', 'fillOpacity': 0},
            popup=popup
        ).add_to(mappa)

    # Aggiungi il controllo layer
    folium.LayerControl().add_to(mappa)

    # Configura Streamlit
    st.title("Mappa dei Beni Trasferiti da Openregio per Provincia")
    st.write("Questa mappa mostra il numero di beni trasferiti da Openregio per ciascuna provincia in Italia.")

    # Visualizza la mappa con Streamlit
    folium_static(mappa, width=700, height=500)


    st.title("Mappe dei Beni Trasferiti da Openregio per Regione")


    regioni_aggregate = province_con_coordinate.groupby("Regione").agg({"Numero beni trasferiti da Openregio": "sum"}).reset_index()

    # Carica il geojson
    with open(geojson_path) as f:
        geojson_data = json.load(f)

    # Crea una mappa centrata sull'Italia
    mappa = folium.Map(location=[42.5, 12.5], zoom_start=6)

    # Creare un dizionario per accedere rapidamente al numero di beni per regione
    beni_dict = pd.Series(regioni_aggregate['Numero beni trasferiti da Openregio'].values, index=regioni_aggregate['Regione']).to_dict()

    # Calcola i breakpoints per la colorazione
    breaks = jenkspy.JenksNaturalBreaks(n_classes=10)
    breaks.fit(regioni_aggregate['Numero beni trasferiti da Openregio'].values)
    bins = np.unique(np.array(breaks.breaks_).round(0))

    # Aggiungi il layer Choropleth alla mappa
    choropleth = folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=regioni_aggregate,
        columns=["Regione", "Numero beni trasferiti da Openregio"],
        key_on="feature.properties.reg_name",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Numero beni confiscati",
        bins=bins.tolist(),
        highlight=True,
        nan_fill_color="white"
    ).add_to(mappa)

    # Aggiungi tooltip per mostrare il numero di beni trasferiti quando si passa sopra una regione
    folium.GeoJson(
        geojson_data,
        style_function=lambda feature: {
            'fillColor': 'transparent',
            'color': 'transparent',
            'weight': 0,
            'fillOpacity': 0
        },
        tooltip=folium.GeoJsonTooltip(
            fields=['reg_name'],
            aliases=['Regione:'],
            localize=True,
            sticky=True,
            labels=True,
            toLocaleString=True
        )
    ).add_to(mappa)

    # Aggiungi popups personalizzati per ciascuna regione
    for feature in geojson_data['features']:
        regione = feature['properties']['reg_name']
        beni = beni_dict.get(regione, 0)
        popup = folium.Popup(f"{regione}: {beni} beni", parse_html=True)
        folium.GeoJson(
            feature,
            style_function=lambda x: {
                'fillColor': 'transparent',
                'color': 'transparent',
                'weight': 0,
                'fillOpacity': 0
            },
            highlight_function=lambda x: {'weight': 0, 'color': 'blue', 'fillOpacity': 0},
            popup=popup
        ).add_to(mappa)

    # Aggiungi il controllo layer
    folium.LayerControl().add_to(mappa)

    # Configura Streamlit
    

    # Visualizza la mappa con Streamlit
    folium_static(mappa, width=700, height=500)

    boolean_columns = ['Elenco pubblicato?',
                    'Sono indicati foglio, particella e subpartice',
                    "Tipologia dell'immobile È indicato, per ogni bene, se si tratta di un terreno, una villa, un appartamento, un box, un fabbricato rurale ecc.?",
                    "Ubicazione È indicato l'indirizzo e il numero civico di ogni bene?",
                    '\xa0È indicata la consistenza del bene in mq o in ettari?',
                    'È specificata quale sia la destinazione del bene tra istituzionale e sociale?',
                    'Utilizzazione 1 - È specificato se il bene è già riutilizzato?',
                    "Utilizzazione 2 - È indicato l'utilizzo specifico?",
                    'È indicata la ragione sociale specifica del soggetto gestore?',
                    "\xa0È inserito un riferimento all'atto amministrativo di concessione?",
                    "È indicato l'oggetto dell'atto di concessione?",
                    "\xa0È specificata la durata dell'affidamento al concessionario?"]

    for column in boolean_columns:
        province_con_coordinate[column] = province_con_coordinate[column].map({"si": 1, "no": 0})

    # Funzione per ottenere il colore in base alla colormap
    def get_colormap_color(value, colormap, min_value, max_value):
        if min_value == max_value:
            norm_value = 0.5  # Centro della colormap
        else:
            norm_value = (value - min_value) / (max_value - min_value)
        rgba_color = colormap(norm_value)
        return f'rgba({int(rgba_color[0]*255)}, {int(rgba_color[1]*255)}, {int(rgba_color[2]*255)}, {rgba_color[3]})'

    # Funzione per calcolare il contributo normalizzato e determinare il colore
    def calculate_and_color_normalized(province_con_coordinate, column, colormap):
        region_success_rate = province_con_coordinate.groupby('Regione')[column].sum().reset_index()
        total_success = region_success_rate[column].sum()
        
        # Calcola il contributo normalizzato in modo che la somma faccia 100
        region_success_rate['Normalized'] = (region_success_rate[column] / total_success) * 100
        
        # Determina il colore in base alla colormap
        min_value = region_success_rate['Normalized'].min()
        max_value = region_success_rate['Normalized'].max()
        region_success_rate['Color'] = region_success_rate['Normalized'].apply(lambda x: get_colormap_color(x, colormap, min_value, max_value))
        region_success_rate['Popup'] = region_success_rate.apply(lambda row: f"Contributo: {row[column]:.2f}<br>Proporzione: {row['Normalized']:.2f}%", axis=1)
        
        return region_success_rate, min_value, max_value

    def valid_filename(s):
        return re.sub(r'[^A-Za-z0-9_-]', '_', s)

    # Funzione per creare la mappa
    def create_map(column):
        colors = ['#d73027', '#fc8d59', '#fee08b', '#d9ef8b', '#91cf60', '#1a9850']
        colormap = mcolors.LinearSegmentedColormap.from_list('custom_colormap', colors)
        
        region_aggregate, min_value, max_value = calculate_and_color_normalized(province_con_coordinate, column, colormap)
        
        gdf_regions = gpd.read_file('limits_IT_regions.geojson')
        gdf_regions = gdf_regions.merge(region_aggregate, left_on='reg_name', right_on='Regione', how='left')
        gdf_regions['color'] = gdf_regions['Color']
        
        # Converti il GeoDataFrame in GeoJSON
        geojson_data = json.loads(gdf_regions.to_json())
        
        mappa = folium.Map(location=[42.5, 12.5], zoom_start=6)
        
        # Aggiungi i dati di popup al geojson_data
        for feature in geojson_data['features']:
            reg_name = feature['properties']['reg_name']
            if reg_name in region_aggregate['Regione'].values:
                feature['properties']['popup'] = f"Regione: {reg_name}<br>{region_aggregate[region_aggregate['Regione'] == reg_name]['Popup'].values[0]}"
                feature['properties']['color'] = gdf_regions.loc[gdf_regions['reg_name'] == reg_name, 'color'].values[0]
            else:
                feature['properties']['popup'] = "Dati non disponibili"
                feature['properties']['color'] = 'gray'
        
        # Aggiungi lo strato GeoJSON alla mappa con i colori personalizzati e i pop-up
        folium.GeoJson(
            geojson_data,
            name="choropleth",
            style_function=lambda feature: {
                'fillColor': feature['properties']['color'],
                'color': 'black',
                'weight': 1,
                'fillOpacity': 0.6,
            },
            highlight_function=lambda feature: {'weight': 3, 'color': 'blue'},
            tooltip=folium.GeoJsonTooltip(
                fields=['reg_name', 'popup'],
                aliases=['Regione:', 'Dettagli:'],
                localize=True,
                sticky=True,
                labels=True,
                toLocaleString=True,
                max_width=800,
            )
        ).add_to(mappa)
        
        # Aggiungi la legenda con colormap
        legend_html = f'''
        <div style="
            position: fixed; 
            bottom: 50px; left: 50px; width: 270px; height: 170px; 
            background-color: white; z-index:9999; font-size:14px;
            border:2px solid grey; border-radius:8px; padding: 10px;">
            <h4>{column}</h4>
            <div><i style="background: {get_colormap_color(min_value, colormap, min_value, max_value)}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;"></i> Minimo</div>
            <div><i style="background: {get_colormap_color((min_value + max_value) / 2, colormap, min_value, max_value)}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;"></i> Medio</div>
            <div><i style="background: {get_colormap_color(max_value, colormap, min_value, max_value)}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;"></i> Massimo</div>
        </div>
        '''
        mappa.get_root().html.add_child(folium.Element(legend_html))
        
        # Aggiungi il controllo layer
        folium.LayerControl().add_to(mappa)
        
        return mappa


        # Pagina delle Mappe
    
    st.title("La Trasparenza delle regioni")
    st.write("Questa mappa mostra il numero di beni trasferiti da Openregio per ciascuna regione in Italia. Quanto ogni regione riesce ad essere trasparente?")
        
    selected_column = st.selectbox("Seleziona la variabile da visualizzare sulla mappa", boolean_columns)
        
    mappa = create_map(selected_column)
    st_folium(mappa, width=700, height=500)


    st.header("Problema")
    st.write("""
    Immagina di confrontare il successo del riutilizzo dei beni confiscati tra diverse regioni. Alcune regioni, come la Basilicata, hanno solo pochi beni confiscati, mentre altre, come la Sicilia, ne hanno molti di più. Se confrontassimo semplicemente il tasso di successo senza alcuna modifica, le regioni con pochi beni sembrerebbero avere sempre risultati migliori, anche se questo non riflette necessariamente una gestione migliore.
    """)

    # Descrizione della soluzione
    st.header("Soluzione: Ponderazione")
    st.write("""
    Per risolvere questo problema, utilizziamo una tecnica chiamata "ponderazione". La ponderazione ci aiuta a bilanciare il confronto tra le regioni con pochi e molti beni confiscati. In pratica, diamo un peso maggiore ai risultati delle regioni con più osservazioni, rendendo il confronto più equo.
    """)

    # Esempio
    st.header("Esempio")
    st.write("""
    **Basilicata:** Ha 3 beni confiscati, tutti riutilizzati con successo (tasso di successo del 100%).

    **Sicilia:** Ha 3000 beni confiscati, 1500 dei quali riutilizzati con successo (tasso di successo del 50%).

    Senza ponderazione, sembrerebbe che la Basilicata stia facendo un lavoro molto migliore della Sicilia. Tuttavia, con la ponderazione, il contributo della Sicilia al confronto complessivo è proporzionato al suo numero di beni, dando una visione più realistica e rappresentativa della situazione.
    """)





if page == "Line Plot":

    st.title("Visualizzazione delle Pubblicazioni nel Tempo")

    st.write("""
    Questa pagina della dashboard presenta un'analisi visiva del numero cumulativo di pubblicazioni nel tempo. Il grafico fornisce un'idea chiara di come le pubblicazioni sono aumentate con il passare degli anni. 

    **Grafico 1:** Numero Cumulativo di Pubblicazioni nel Tempo - Questo grafico mostra il numero totale di pubblicazioni accumulate nel tempo, fornendo una visione d'insieme della crescita delle pubblicazioni.

    **Grafico 2:** Numero Cumulativo di Pubblicazioni nel Tempo per Formato - Questo grafico suddivide il numero cumulativo di pubblicazioni in base al formato, permettendo di vedere quale formato di pubblicazione è stato più utilizzato nel tempo.

    Puoi interagire con i grafici per ottenere maggiori dettagli, utilizzare i controlli di animazione per visualizzare l'evoluzione delle pubblicazioni e analizzare come diversi formati di pubblicazione si sono sviluppati nel corso degli anni.
    """)

    

    df = pd.read_csv("province_con_coordinate.csv")

    # Line Plot nel tempo
    df['Data di pubblicazione, se disponibile'] = pd.to_datetime(df['Data di pubblicazione, se disponibile'], errors='coerce')

    # Rimuovi le righe con date non valide
    df2 = df.dropna(subset=['Data di pubblicazione, se disponibile'])

    # Raggruppa per data e conta il numero di pubblicazioni per ogni data
    pubblicazioni_per_data = df2['Data di pubblicazione, se disponibile'].value_counts().sort_index()

    # Calcola la somma cumulativa delle pubblicazioni
    pubblicazioni_cumulative = pubblicazioni_per_data.cumsum().reset_index()
    pubblicazioni_cumulative.columns = ['Data di Pubblicazione', 'Numero Cumulativo di Pubblicazioni']

    # Assicurati che le date siano ordinate
    pubblicazioni_cumulative = pubblicazioni_cumulative.sort_values('Data di Pubblicazione')

    # Crea i frame per l'animazione
    frames = []
    for i in range(1, len(pubblicazioni_cumulative) + 1):
        frame = go.Frame(
            data=[go.Scatter(x=pubblicazioni_cumulative['Data di Pubblicazione'][:i], 
                            y=pubblicazioni_cumulative['Numero Cumulativo di Pubblicazioni'][:i], 
                            mode='lines', line=dict(color='royalblue', width=4))],
            name=str(i)
        )
        frames.append(frame)

    # Crea il grafico di base
    fig_cumulative = go.Figure(
        data=[go.Scatter(x=pubblicazioni_cumulative['Data di Pubblicazione'], 
                        y=pubblicazioni_cumulative['Numero Cumulativo di Pubblicazioni'], 
                        mode='lines', line=dict(color='royalblue', width=4))],
        layout=go.Layout(
            title={
                'text': 'Numero Cumulativo di Pubblicazioni nel Tempo',
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
            xaxis_title="Data di Pubblicazione",
            yaxis_title="Numero Cumulativo di Pubblicazioni",
            paper_bgcolor='white',
            plot_bgcolor='white',
            font=dict(
                family="Arial, sans-serif",
                size=14,
                color="black"
            ),
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=False,
                showline=True,
                linewidth=2,
                linecolor='black'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgrey',
                zeroline=False,
                showline=True,
                linewidth=2,
                linecolor='black'
            ),
            updatemenus=[{
                'buttons': [
                    {
                        'label': 'Play',
                        'method': 'animate',
                        'args': [None, {'frame': {'duration': 100, 'redraw': True}, 'fromcurrent': True}]
                    },
                    {
                        'label': 'Pause',
                        'method': 'animate',
                        'args': [[None], {'frame': {'duration': 0, 'redraw': True}, 'mode': 'immediate', 'transition': {'duration': 0}}]
                    }
                ],
                'direction': 'left',
                'pad': {'r': 10, 't': 87},
                'showactive': False,
                'type': 'buttons',
                'x': 0.1,
                'xanchor': 'right',
                'y': 0,
                'yanchor': 'top'
            }]
        ),
        frames=frames
    )

    # LinePlot formato
    # Raggruppa per data e formato, e conta il numero di pubblicazioni per ogni combinazione
    pubblicazioni_per_data_formato = df.groupby(['Data di pubblicazione, se disponibile', 'Formato di pubblicazione']).size().reset_index(name='Count')

    # Calcola la somma cumulativa delle pubblicazioni per ogni formato
    pubblicazioni_per_data_formato['Cumulative Count'] = pubblicazioni_per_data_formato.groupby('Formato di pubblicazione')['Count'].cumsum()

    # Assicurati che le date siano ordinate
    pubblicazioni_per_data_formato = pubblicazioni_per_data_formato.sort_values('Data di pubblicazione, se disponibile')

    # Crea il grafico animato
    fig_formato = px.line(pubblicazioni_per_data_formato, 
                        x='Data di pubblicazione, se disponibile', 
                        y='Cumulative Count', 
                        color='Formato di pubblicazione', 
                        title='Numero Cumulativo di Pubblicazioni nel Tempo per Formato')

    # Aggiungi l'animazione temporale'yanchor': 'top'
    

    fig_formato.update_layout({
        'paper_bgcolor': 'white',  # Sfondo bianco per la carta
        'plot_bgcolor': 'white',   # Sfondo bianco per il grafico
        'xaxis': {'showgrid': True, 'gridcolor': 'black'},
        'yaxis': {'showgrid': True, 'gridcolor': 'black'}
    })

    # Configura Streamlit
    st.title("Visualizzazione delle Pubblicazioni nel Tempo")
    st.write("Questa dashboard mostra il numero cumulativo di pubblicazioni nel tempo.")

    # Visualizza i grafici con Streamlit
    st.plotly_chart(fig_cumulative)
    st.plotly_chart(fig_formato)



    



if page == "Andamenti Temporali":

    st.title("Andamenti Temporali dei Beni Confiscati")


    st.write("""
## Andamenti Temporali dei Beni Confiscati

In questa sezione, potete esplorare l'andamento temporale dei beni confiscati in base a diverse caratteristiche. Utilizzando i dati disponibili, abbiamo creato grafici che mostrano il conteggio cumulativo delle caratteristiche specifiche dei beni confiscati nel tempo. 

### Selezione delle Caratteristiche:

- **Sono indicati foglio, particella e subpartice**: Verifica se sono specificati i dettagli catastali.
- **Tipologia dell'immobile**: Indica se è specificato il tipo di immobile (terreno, villa, appartamento, ecc.).
- **Ubicazione**: Verifica se è indicato l'indirizzo e il numero civico.
- **Consistenza del bene**: Indica se la dimensione del bene è specificata in metri quadrati o ettari.
- **Destinazione del bene**: Specifica se il bene è destinato ad uso istituzionale o sociale.
- **Utilizzazione 1**: Verifica se il bene è già riutilizzato.
- **Utilizzazione 2**: Specifica l'uso esatto del bene.
- **Ragione sociale del gestore**: Indica se è specificato il nome del gestore del bene.
- **Riferimento all'atto amministrativo di concessione**: Verifica se è presente un riferimento all'atto di concessione.
- **Oggetto dell'atto di concessione**: Indica se è specificato l'oggetto dell'atto di concessione.
- **Durata dell'affidamento al concessionario**: Verifica se è specificata la durata dell'affidamento.

### Come utilizzare la sezione:

1. **Seleziona una caratteristica dal menu a tendina**: Usate il menu per selezionare la caratteristica di interesse.
2. **Visualizza l'andamento temporale**: Il grafico mostrerà il conteggio cumulativo dei beni confiscati che presentano (o non presentano) la caratteristica selezionata nel corso del tempo.
3. **Colori distintivi**: I grafici utilizzano colori distintivi per mostrare la presenza ("sì" in blu) e l'assenza ("no" in rosso) della caratteristica selezionata.

Questa visualizzazione fornisce una chiara comprensione dell'evoluzione delle caratteristiche dei beni confiscati nel tempo, aiutando a identificare trend e cambiamenti significativi.
""")

    # Carica i dati
    df = pd.read_csv("province_con_coordinate.csv")


    def create_cumulative_time_series(df, column):
    # Raggruppa i dati per data e conteggia i "sì" e "no"
        time_series = df.groupby([df['Data di pubblicazione, se disponibile'].dt.to_period('M'), column]).size().unstack(fill_value=0)
        
        # Calcola il cumulativo
        cumulative_time_series = time_series.cumsum()
        
        # Crea un grafico a linee cumulative
        fig = px.line(cumulative_time_series, 
                    x=cumulative_time_series.index.to_timestamp(), 
                    y=cumulative_time_series.columns, 
                    labels={'value': 'Conteggio Cumulativo', 'index': 'Data'})
        
        # Imposta i colori per "sì" e "no"
        fig.update_traces(line=dict(color="blue"), selector=dict(name="si"))
        fig.update_traces(line=dict(color="red"), selector=dict(name="no"))

        fig.update_layout(title=f"Andamento Temporale Cumulativo di '{column}'", 
                        xaxis_title='Data', 
                        yaxis_title='Conteggio Cumulativo')
        return fig

        # Andamenti Temporali *
    boolean_columns = [
        'Sono indicati foglio, particella e subpartice',
        "Tipologia dell'immobile È indicato, per ogni bene, se si tratta di un terreno, una villa, un appartamento, un box, un fabbricato rurale ecc.?",
        "Ubicazione È indicato l'indirizzo e il numero civico di ogni bene?",
        '\xa0È indicata la consistenza del bene in mq o in ettari?',
        'È specificata quale sia la destinazione del bene tra istituzionale e sociale?',
        'Utilizzazione 1 - È specificato se il bene è già riutilizzato?',
        "Utilizzazione 2 - È indicato l'utilizzo specifico?",
        'È indicata la ragione sociale specifica del soggetto gestore?',
        "\xa0È inserito un riferimento all'atto amministrativo di concessione?",
        "È indicato l'oggetto dell'atto di concessione?",
        "\xa0È specificata la durata dell'affidamento al concessionario?"
    ]

    df['Data di pubblicazione, se disponibile'] = pd.to_datetime(df['Data di pubblicazione, se disponibile'])

    # Filtra i dati per rimuovere le righe senza data
    df = df.dropna(subset=['Data di pubblicazione, se disponibile'])

    selected_boolean_column = st.selectbox("Selezionando una delle variabili si potrà visualizzare l'andamento nel tempo della presenza o mancanza della specifica caratteristica", boolean_columns)
    
    if selected_boolean_column:
        fig = create_cumulative_time_series(df, selected_boolean_column)
        st.plotly_chart(fig)


    st.write(''' ## Qui segue un bar chart race delle pubblicazioni nel tempo per ogni regione
             ''')
    st.video("pubblicazioni per regione over time.mp4")




if page == "Riutilizzo dei Beni":



    st.write("""
# Benvenuti alla Dashboard di Analisi dei Beni Confiscati alle Aziende

Questa dashboard offre una panoramica dettagliata sulla distribuzione e lo stato delle aziende confiscate in Italia. Utilizzando i dati più recenti, forniamo diverse visualizzazioni per comprendere meglio l'andamento, la distribuzione geografica e la tipologia delle aziende coinvolte. 

### Sezioni della Dashboard:

1. **Distribuzione delle Aziende per Codice ATECO**:
   - Questo grafico a barre mostra i primi 10 codici ATECO con il maggior numero di aziende confiscate, permettendo di identificare i settori più colpiti.

2. **Confronto tra Aziende Attive e Cessate per Codice ATECO**:
   - Un grafico a barre comparativo che evidenzia la differenza tra le aziende attualmente attive e quelle cessate, suddivise per codice ATECO.

3. **Distribuzione delle Aziende Confiscate per Regione**:
   - Un altro grafico a barre che illustra il numero di aziende confiscate per ciascuna regione italiana, fornendo una visione chiara della distribuzione geografica.

4. **Distribuzione delle Aziende per Stato Attuale**:
   - Un grafico a torta che rappresenta la percentuale di aziende confiscate attive rispetto a quelle cessate, dando una visione immediata dello stato delle aziende.

5. **Mappe delle Aziende Confiscate per Regione e Provincia**:
   - Mappe interattive che mostrano la tipologia ATECO predominante in ogni regione e provincia. Queste mappe sono colorate in base alla tipologia ATECO, permettendo una facile identificazione delle aree di interesse.

""")
    


    ateco_descriptions = {
    '2363': 'Produzione di calcestruzzo pronto per l\'uso',
    '3511': 'Produzione di energia elettrica',
    '412': 'Costruzione di edifici residenziali e non residenziali',
    '4312': 'Preparazione del cantiere edile e sistemazione del terreno',
    '451101': 'Commercio all\'ingrosso e al dettaglio di autovetture e di autoveicoli leggeri',
    '473': 'Commercio al dettaglio di carburante per autotrazione',
    '4941': 'Trasporto di merci su strada',
    '561011': 'Ristorazione con somministrazione',
    '563': 'Bar e altri esercizi simili senza cucina',
    '681': 'Compravendita di beni immobili effettuata su beni propri',
    '682001': 'Locazione immobiliare di beni propri o in leasing (affitto)'
}


# Funzione per ottenere la descrizione del codice ATECO
    def get_ateco_description(ateco_code):
        return ateco_descriptions.get(ateco_code, "Descrizione non disponibile")

    # Titolo della sezione
    st.write("""
    ## Ricerca Codici ATECO

    Inserisci un codice ATECO per visualizzare la descrizione corrispondente.
    """)

    # Barra di ricerca per il codice ATECO
    ateco_code = st.text_input("Inserisci il codice ATECO:")

    # Mostra la descrizione del codice ATECO
    if ateco_code:
        description = get_ateco_description(ateco_code)
        st.write(f"**Codice ATECO {ateco_code}:** {description}")




# Carica i dati
    df_aziende_confiscate = pd.read_csv("aziende_confiscate_merged.csv")
    file_path_geojson_regions = 'limits_IT_regions.geojson'
    file_path_geojson_provinces = 'limits_IT_provinces.geojson'

    # Carica i GeoDataFrame
    gdf_regions = gpd.read_file(file_path_geojson_regions)
    gdf_provincia = gpd.read_file(file_path_geojson_provinces)

    # Prepara i dati
    df_aziende_confiscate['sedeLegale.regione'] = df_aziende_confiscate['sedeLegale.regione'].str.upper()
    gdf_regions['reg_name'] = gdf_regions['reg_name'].str.upper()
    df_aziende_confiscate['sedeLegale.provincia'] = df_aziende_confiscate['sedeLegale.provincia'].str.upper()
    gdf_provincia['prov_name'] = gdf_provincia['prov_name'].str.upper()

    # Calcola la distribuzione ATECO
    ateco_distribution_regions = df_aziende_confiscate.groupby(['sedeLegale.regione', 'ateco.sezioneAteco']).size().unstack(fill_value=0)
    ateco_majority_regions = ateco_distribution_regions.idxmax(axis=1)
    ateco_distribution_provinces = df_aziende_confiscate.groupby(['sedeLegale.provincia', 'ateco.sezioneAteco']).size().unstack(fill_value=0)
    ateco_majority_provinces = ateco_distribution_provinces.idxmax(axis=1)

    # Crea mappa di colori per le tipologie ATECO
    

    # Funzione per creare un barplot
    def create_barplot(data, x, y, title, xlabel, ylabel):
        fig, ax = plt.subplots(figsize=(14, 8))
        sns.barplot(x=x, y=y, data=data, palette='viridis', ax=ax)
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_facecolor('#f0f0f0')
        st.pyplot(fig)

    # Funzione per creare un pie chart
    def create_piechart(data, labels, title):
        fig, ax = plt.subplots(figsize=(10, 7))
        ax.pie(data, labels=labels, autopct='%1.1f%%', colors=sns.color_palette('viridis', len(data)))
        ax.set_title(title)
        ax.set_facecolor('#f0f0f0')
        st.pyplot(fig)

    # Grafico a barre per il numero di aziende per codice ATECO
    st.header("Distribuzione delle Aziende per Codice ATECO")
    ateco_counts = df_aziende_confiscate['ateco.codiceAteco'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(14, 8))
    sns.barplot(x=ateco_counts.values, y=ateco_counts.index, palette='viridis', ax=ax)
    ax.set_title('Distribuzione delle Aziende per Codice ATECO')
    ax.set_xlabel('Numero di Aziende')
    ax.set_ylabel('Codice ATECO')
    ax.set_facecolor('#f0f0f0')
    st.pyplot(fig)

    # Filtriamo i dati per aziende attive e cessate
    attive = df_aziende_confiscate[df_aziende_confiscate['statoAttivita'] == 'ATTIVA']
    cessate = df_aziende_confiscate[df_aziende_confiscate['statoAttivita'] == 'CESSATA']

    # Contiamo i codici ATECO per aziende attive e cessate
    ateco_attive_counts = attive['ateco.codiceAteco'].value_counts().head(10)
    ateco_cessate_counts = cessate['ateco.codiceAteco'].value_counts().head(10)

    # Creiamo un DataFrame per il confronto
    confronto_ateco = pd.DataFrame({
        'Attive': ateco_attive_counts,
        'Cessate': ateco_cessate_counts
    }).fillna(0)

    # Grafico a barre per il confronto tra aziende attive e cessate
    st.header("Confronto tra Aziende Attive e Cessate per Codice ATECO")
    fig, ax = plt.subplots(figsize=(14, 8))
    confronto_ateco.plot(kind='bar', ax=ax)
    ax.set_title('Confronto tra Aziende Attive e Cessate per Codice ATECO')
    ax.set_xlabel('Codice ATECO')
    ax.set_ylabel('Numero di Aziende')
    ax.set_facecolor('#f0f0f0')
    fig.patch.set_facecolor('#e0e0e0')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
    st.pyplot(fig)

    # Grafico a barre per il numero di aziende per regione
    st.header("Distribuzione delle Aziende Confiscate per Regione")
    region_counts = df_aziende_confiscate['sedeLegale.regione'].value_counts().reset_index()
    region_counts.columns = ['Regione', 'Numero di Aziende']
    create_barplot(region_counts, 'Numero di Aziende', 'Regione', 'Distribuzione delle Aziende Confiscate per Regione', 'Numero di Aziende', 'Regione')

    # Grafico a torta per lo stato delle aziende
    st.header("Distribuzione delle Aziende per Stato Attuale")
    stato_counts = df_aziende_confiscate['statoAttivita'].value_counts()
    create_piechart(stato_counts.values, stato_counts.index, 'Distribuzione delle Aziende per Stato Attuale')


    unique_ateco = pd.concat([ateco_majority_regions, ateco_majority_provinces]).unique()
    colors = plt.cm.get_cmap('tab20', len(unique_ateco)).colors
    ateco_color_map = {ateco: f'#{int(colors[i][0]*255):02x}{int(colors[i][1]*255):02x}{int(colors[i][2]*255):02x}' for i, ateco in enumerate(unique_ateco)}

    # Aggiungi la maggioranza ATECO e i colori al GeoDataFrame delle regioni
    gdf_regions['majority_ateco'] = gdf_regions['reg_name'].map(ateco_majority_regions)
    gdf_regions['color'] = gdf_regions['majority_ateco'].map(ateco_color_map)

    # Converti il GeoDataFrame delle regioni in GeoJSON
    geojson_data_regions = json.loads(gdf_regions.to_json())

    # Crea la mappa con Folium per le regioni
    mappa_regions = folium.Map(location=[42.5, 12.5], zoom_start=5)

    for feature in geojson_data_regions['features']:
        reg_name = feature['properties']['reg_name']
        if reg_name in ateco_majority_regions.index:
            feature['properties']['popup'] = f"Regione: {reg_name}<br>ATECO predominante: {ateco_majority_regions[reg_name]}"
            feature['properties']['color'] = gdf_regions.loc[gdf_regions['reg_name'] == reg_name, 'color'].values[0]
        else:
            feature['properties']['popup'] = "Dati non disponibili"
            feature['properties']['color'] = 'gray'

    folium.GeoJson(
        geojson_data_regions,
        name="choropleth",
        style_function=lambda feature: {
            'fillColor': feature['properties']['color'],
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        },
        highlight_function=lambda feature: {'weight': 3, 'color': 'blue'},
        tooltip=folium.GeoJsonTooltip(
            fields=['popup'],
            aliases=['Dettagli:'],
            localize=True,
            sticky=True,
            labels=True,
            toLocaleString=True,
            max_width=800,
        )
    ).add_to(mappa_regions)

    # Aggiungi il controllo layer
    folium.LayerControl().add_to(mappa_regions)

    # Visualizza la mappa delle regioni
    st.header("Mappa delle Aziende Confiscate per Regione")
    st_folium(mappa_regions, width=700, height=500)

    

    # Aggiungi la maggioranza ATECO e i colori al GeoDataFrame delle province
    gdf_provincia['majority_ateco'] = gdf_provincia['prov_name'].map(ateco_majority_provinces)
    gdf_provincia['color'] = gdf_provincia['majority_ateco'].map(ateco_color_map)

    # Converti il GeoDataFrame delle province in GeoJSON
    geojson_data_provinces = json.loads(gdf_provincia.to_json())

    # Crea la mappa con Folium per le province
    mappa_provinces = folium.Map(location=[42.5, 12.5], zoom_start=6)

    for feature in geojson_data_provinces['features']:
        prov_name = feature['properties']['prov_name']
        if prov_name in ateco_majority_provinces.index:
            feature['properties']['popup'] = f"Provincia: {prov_name}<br>ATECO predominante: {ateco_majority_provinces[prov_name]}"
            feature['properties']['color'] = gdf_provincia.loc[gdf_provincia['prov_name'] == prov_name, 'color'].values[0]
        else:
            feature['properties']['popup'] = f"Provincia: {prov_name}<br>Dati non disponibili"
            feature['properties']['color'] = 'gray'

    folium.GeoJson(
        geojson_data_provinces,
        name="choropleth",
        style_function=lambda feature: {
            'fillColor': feature['properties']['color'],
            'color': 'black',
            'weight': 1,
            'fillOpacity': 0.6,
        },
        highlight_function=lambda feature: {'weight': 3, 'color': 'blue'},
        tooltip=folium.GeoJsonTooltip(
            fields=['popup'],
            aliases=['Dettagli:'],
            localize=True,
            sticky=True,
            labels=True,
            toLocaleString=True,
            max_width=50,
        )
    ).add_to(mappa_provinces)

    # Aggiungi il controllo layer
    folium.LayerControl().add_to(mappa_provinces)

    # Visualizza la mappa delle province
    st.header("Mappa delle Aziende Confiscate per Provincia")
    st_folium(mappa_provinces, width=700, height=500)

    # Legenda dinamica
    legend_html = '''
    <div style="
        position: fixed; 
        bottom: 50px; left: 50px; width: 250px; height: auto; 
        background-color: white; z-index:9999; font-size:13px;
        border:2px solid grey; border-radius:8px; padding: 10px;">
        <h4>Tipologia ATECO Predominante</h4>
    '''

    for ateco, color in ateco_color_map.items():
        legend_html += f'<div><i style="background: {color}; width: 20px; height: 20px; display: inline-block; margin-right: 10px;"></i> {ateco}</div>'

    legend_html += '</div>'
    mappa_regions.get_root().html.add_child(folium.Element(legend_html))
    mappa_provinces.get_root().html.add_child(folium.Element(legend_html))