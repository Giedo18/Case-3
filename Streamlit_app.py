#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[ ]:


def intro():
    import streamlit as st

    st.write("""# Case 3 – Van data naar informatie:
             Een dashboard over elektrisch mobiliteit en laadpalen""")

    st.markdown(
    """
    Streamlit is een open-source app framework wat specifiek is gemaakt voor
    Machine Learning en Data Science projecten.
    In dit project is een dashboard gemaakt over elektrisch mobiliteit en laadpalen.
    Deze is gemaakt aan de hand van meerdere datasets:
    * Een dataset die verkregen is via OpenChargeMap
    * Laadpaaldata.csv (gekregen van docenten van de HvA)
    * 2 Datasets van de RDW
        1. Open-Data-RDW-Gekentekende_voertuigen
        2. Open-Data-RDW-Gekentekende_voertuigen_brandstof
    
    Om vervolgens meer informatie over het project te lezen
    
    *👈 Selecteer dan een keuze uit de balk hiernaast*.""")


# In[2]:


def OpenChargeMap():
    import streamlit as st
    import pandas as pd
    import requests
    from streamlit_folium import st_folium
    import folium

    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        # Laadpaaldata OpenChargeMap
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset die is verkregen
        met behulp van de OpenChargeMap.""")
    
    Laadpalen = pd.read_csv("Laadpalen.csv")
    Locatiedata = {'Plaats': ['Nederland',
                   'Amsterdam',
                   'Maastricht',
                   'Haarlem',
                   'Arnhem',
                   'Utrecht',
                   'Leeuwarden',
                   'Groningen',
                   'Den Haag',
                   'Middelburg',
                   'Zwolle',
                   'Den Bosch',
                   'Assen',
                   'Lelystad'],
        
            'Lon': ['52.15130368472897',
                    '52.371258078794135',
                    '50.85300767449641',
                    '52.386845554591645',
                    '51.98338138653844',
                    '52.09037942657452',
                    '53.201233006887016',
                    '53.218657498787515',
                    '52.07175202820417',
                    '51.49981853843821',
                    '52.51607891882432',
                    '51.6992652579386',
                    '52.99242186078035',
                    '52.51709903811563'],
               
            'Lat' : ['5.849065006968685',
                    '4.912201662823863',
                    '5.687171406171752',
                    '4.639415458023007',
                    '5.898966059104855',
                    '5.125935086923146',
                    '5.79944975573854',
                    '6.571457904196551',
                    '4.299396831574714',
                    '3.615749790361903',
                    '6.0891464381897045',
                    '5.296904176783719',
                    '6.564924557157714',
                    '5.462285327853063'
                    ]}


    st.write(Laadpalen.head(3))
  
    ####################################################################################################################

    def add_categorical_legend(folium_map, title, colors, labels):
        if len(colors) != len(labels):
            raise ValueError("colors and labels must have the same length.")

        color_by_label = dict(zip(labels, colors))
        
        legend_categories = ""     
        for label, color in color_by_label.items():
            legend_categories += f"<li><span style='background:{color}'></span>{label}</li>"
        
        legend_html = f"""
        <div id='maplegend' class='maplegend'>
          <div class='legend-title'>{title}</div>
          <div class='legend-scale'>
            <ul class='legend-labels'>
            {legend_categories}
            </ul>
          </div>
        </div>
        """
        script = f"""
            <script type="text/javascript">
            var oneTimeExecution = (function() {{
                        var executed = false;
                        return function() {{
                            if (!executed) {{
                                 var checkExist = setInterval(function() {{
                                           if ((document.getElementsByClassName('leaflet-top leaflet-right').length) || (!executed)) {{
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.display = "flex"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].style.flexDirection = "column"
                                              document.getElementsByClassName('leaflet-top leaflet-right')[0].innerHTML += `{legend_html}`;
                                              clearInterval(checkExist);
                                              executed = true;
                                           }}
                                        }}, 100);
                            }}
                        }};
                    }})();
                oneTimeExecution()
        </script>
          """
   

        css = """
    
        <style type='text/css'>
          .maplegend {
            z-index:9999;
            float:right;
            background-color: rgba(255, 255, 255, 1);
            border-radius: 5px;
            border: 2px solid #bbb;
            padding: 10px;
            font-size:12px;
            positon: relative;
          }
          .maplegend .legend-title {
            text-align: left;
            margin-bottom: 5px;
            font-weight: bold;
            font-size: 90%;
            }
          .maplegend .legend-scale ul {
            margin: 0;
            margin-bottom: 5px;
            padding: 0;
            float: left;
            list-style: none;
            }
          .maplegend .legend-scale ul li {
            font-size: 80%;
            list-style: none;
            margin-left: 0;
            line-height: 18px;
            margin-bottom: 2px;
            }
          .maplegend ul.legend-labels li span {
            display: block;
            float: left;
            height: 16px;
            width: 30px;
            margin-right: 5px;
            margin-left: 0;
            border: 0px solid #ccc;
            }
          .maplegend .legend-source {
            font-size: 80%;
            color: #777;
            clear: both;
            }
          .maplegend a {
            color: #777;
            }
        </style>
        """

        folium_map.get_root().header.add_child(folium.Element(script + css))

        return folium_map

    #########################################################################################################################

    def kleuren(type):
    
        if type > 1200:
            return "green"
        elif type > 1000:
            return "lime"
        elif type > 800:
            return "greenyellow"
        elif type > 600:
            return "yellow"
        elif type > 400:
            return "darkorange"
        elif type > 200:
            return "red"
        else:
            return "darkred"
    
    ################################################################################################################
#     plaatsnaam = 'Amsterdam'
    
#     lon1 = Locatiedata[Locatiedata['Plaats'] == plaatsnaam]['Lon'].values
#     lat1 = Locatiedata[Locatiedata['Plaats'] == plaatsnaam]['Lat'].values

    lon = ["53.5", "5.4"]
    lat = ["50.8", "5.3"]
    
    #plaatsnaam = 'Amsterdam'
    #long_lat = Locatiedata[Locatiedata['Plaats'] == plaatsnaam]['Locatie'].values
    
    m = folium.Map(tiles = 'cartodbpositron')
    
    m.fit_bounds([[lon],[lat]])
    

    for index, row in Laadpalen.iterrows():
    
        color_circle = kleuren(row['Aantal_Laadpalen'])
        marker=(folium.CircleMarker(location =[row['AddressInfo.Latitude'], row['AddressInfo.Longitude']],
                                    popup = row["Postcode_Groep"],
                                    radius = 1,
                                    color = color_circle))
        marker.add_to(m)
    

        m = add_categorical_legend(m,
                               'Aantal laadpalen per postcode groep',
                               colors = ['green', 'lime', 'greenyellow', 'yellow', 'darkorange',
                                         'red', 'darkred'],
                               labels = ['> 1200', '> 1000', '> 800', '> 600', '> 400',
                                         '> 200', '0-200'])

    st_data = st_folium(m, width = 725)


# In[ ]:


page_names_to_funcs = {
    "Opdrachtomschrijving": intro,
    "Laadpaaldata OpenChargeMap": OpenChargeMap}

demo_name = st.sidebar.selectbox("Kies een pagina", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

