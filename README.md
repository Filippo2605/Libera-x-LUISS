# Libera-x-LUISS

LUISS "Guido Carli" ha permesso a noi studenti, relativamente alle GAP2 Activities, di collaborare con l'organizzazione LIBERA per un Progetto di data visualization relativamente ai beni confiscate alle mafie. Ci sono stati forniti alcuni dataset, e la loro visualizzazione è stata effettuata in Python con una dashboard (streamlit library). Il lavoro ha prima visto una fase di pulizia dei dataset e successiva visualizzazione dei dati.

Il file dashboardlibera.py contiene lo script della dashboard. Per la visualizzazione della dashboard è sufficiente runnare il file nel terminal in seguito al download della repository.

## Contenuto 

Il contenuto della repository vede tutto il necessario per l'esecuzione della dashboard. Dove:
 - Le varie mappa_(variabile).html, vedono specifiche variabili visualizzate sulla mappa dell'Italia divisa in regioni o province a seconda delle necessità di visualizzazione.
 - Datasets forniti da LIBERA: aziende-confiscate-anbsc.json, aziende-confiscate-unioncamere.json, opendata-aziendeconfiscate-catalog.json, dataset_rimanDATI_0.csv.
 - elenco_codici_comuni.json, elenco_codici_comuni.php, elenco_comuni_province.csv, sono stati utilizzati per risalire a sigle di province e per visualizzare sulla mappa.
 - italy_geo.csv, italy_geo.xlsx, limits_IT_provinces.geojson, limits_IT_regions.geojson. Informazioni necessarie per le coordinate e suddivisioni della mappa. Fonte --> https://github.com/openpolis/geojson-italy/tree/master
 - province_con_coordinate.csv, missing_provinces.csv, aziende_confiscate_merged.csv, sono datasets creati per la praticità del codice.
 - Il file pubblicazioni per regione over time.mp4 vede un bar plot race.
 - requirements.txt contiene le versioni delle librerie per una corretta esecuzione della dashboard.

# Dashboard di Analisi dei Beni Confiscati alle Mafie

## Pagine della Dashboard

### 1. Mappe
**Descrizione:**
Questa pagina fornisce una visualizzazione geografica dei beni confiscati, mostrando la distribuzione e il numero di beni trasferiti da Openregio per ciascuna regione e provincia in Italia.

**Caratteristiche:**

- **Mappa delle Aziende Confiscate per Regione:** Una mappa coropletica che evidenzia il numero di beni confiscati per regione, con pop-up informativi che mostrano la tipologia ATECO predominante in ogni regione.
- **Mappa delle Aziende Confiscate per Provincia:** Una mappa coropletica simile, ma focalizzata sulle province, mostrando informazioni dettagliate per ciascuna provincia.

**Tecnologie Utilizzate:**

- Folium per la visualizzazione delle mappe.
- GeoJSON per la rappresentazione dei confini geografici.
- Jenks Natural Breaks per la classificazione dei dati numerici.

### 2. Line Plot
**Descrizione:**
Questa pagina presenta l'andamento temporale del numero di pubblicazioni relative ai beni confiscati, offrendo una visione cumulativa delle pubblicazioni nel tempo.

**Caratteristiche:**

- **Numero Cumulativo di Pubblicazioni nel Tempo:** Un grafico che mostra il numero cumulativo di pubblicazioni sui beni confiscati, con la possibilità di animare l'andamento temporale.
- **Numero Cumulativo di Pubblicazioni per Formato:** Un grafico che suddivide le pubblicazioni per formato (PDF, XML, ecc.), mostrando l'evoluzione temporale di ciascun formato.

**Tecnologie Utilizzate:**

- Plotly per la creazione di grafici interattivi.
- Pandas per la manipolazione e l'aggregazione dei dati.

### 3. Andamenti Temporali
**Descrizione:**
Questa pagina analizza vari aspetti dei beni confiscati nel tempo, con la possibilità di selezionare specifiche variabili per visualizzare l'andamento temporale.

**Caratteristiche:**

- **Selezione Variabile:** Un menu a tendina che consente di selezionare diverse variabili (es. "Ubicazione", "Tipologia dell'immobile") per visualizzare il loro andamento nel tempo.
- **Grafico Cumulativo:** Un grafico che mostra l'andamento temporale cumulativo della variabile selezionata, con linee di colore diverso per "si" e "no".

**Tecnologie Utilizzate:**

- Plotly per i grafici interattivi.
- Pandas per la manipolazione e l'aggregazione dei dati.

### 4. Riutilizzo dei Beni
**Descrizione:**
Questa pagina è dedicata all'analisi del riutilizzo dei beni confiscati, confrontando il tasso di successo tra diverse regioni e ponderando i risultati per offrire un confronto più equo.

**Caratteristiche:**

- **Descrizione del Problema:** Spiega la difficoltà di confrontare direttamente i tassi di successo tra regioni con numeri di beni confiscati molto diversi.
- **Soluzione Ponderata:** Descrive come viene applicata la ponderazione per bilanciare i risultati e fornire un confronto più accurato.
- **Esempi Pratici:** Fornisce esempi concreti di come la ponderazione influenza i risultati.

**Tecnologie Utilizzate:**

- Streamlit per la creazione dell'interfaccia interattiva.
- Pandas per la manipolazione e l'aggregazione dei dati.
