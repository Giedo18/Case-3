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
        ## Inleiding van de pagina
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset die is verkregen
        met behulp van de OpenChargeMap.
        """)
        
    st.write("""
        Eerst is er een data analyse gedaan over de gehele dataset. Aangezien het doel was om een kaart te tonen van een
        gebied naar keuze waarin de laadpunten weergegeven worden, is er een data selectie gemaakt van de data die hiervoor
        nodig is. Er is gekeken naar provinciale data zodat het aantal laadpalen per gebied gekoppeld konden worden aan 
        de provincie, helaas ontbrak hier teveel data voor. Daaorm is gekozen om op basis van postcode, postcode groepen
        te maken. Aan de hand hiervan is te zien hoeveel laadpalen er per postcode groep is. Hieronder is een head te zien
        van de gemaakte dataset. Hierin is ook al cleaning gedaan.
        """)
    
    Laadpalen = pd.read_csv("Laadpalen.csv")
#     Locatiedata = {'Plaats':  ['Nederland','Amsterdam'],
        
#                     'Lon': [["53.5", "5.4"],
#                             ["52.2", "4.66"]],
               
#                     'Lat' : [["50.8", "5.3"]
#                              ["52.46", "5.10"]]}


    st.write(Laadpalen.head(3))
  

    st.write("""
        ## Kaart met laadpalen
        Hier zijn alle laadpalen te zien in Nederland. De kleur geeft aan waar in Nederland veel of weinig laadpalen zijn.
        Wanneer de stipjes per laadpaal groen zijn, betekend dat er in diezelfde postcode soort veel laadpalen zijn. Hoe
        roder het stipje wordt, hoe minder laadpalen er in de postcode groep zullen zijn.
        
        De kaart is ingeladen d.m.v. folium
        """)
    
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

   #lon = ["53.5", "5.4"]
    #lat = ["50.8", "5.3"]
    
    #plaatsnaam = 'Amsterdam'
    #long_lat = Locatiedata[Locatiedata['Plaats'] == plaatsnaam]['Locatie'].values
    
    m = folium.Map(tiles = 'cartodbpositron')
    
    m.fit_bounds([[53.5, 5.4], [50.8, 5.3]])
    

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
    
    st.write("""
        ##Conclusie
        Er is duidelijk te zien op de kaart dat hoe dichter je bij de randstad komt hoe meer laadpalen er zullen zijn in
        het gebied. Een logische uitkomst aangezien de randstad dichterbevolkt is, en de aannamen gemaakt kan worden dat
        hierdoor dus meer elektrische auto's zullen rijden in deze gebieden. Die natuurlijk allemaal opgeladen dienen te
        worden
        """)


# In[ ]:


page_names_to_funcs = {
    "Opdrachtomschrijving": intro,
    "Laadpaaldata OpenChargeMap": OpenChargeMap}

demo_name = st.sidebar.selectbox("Kies een pagina", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()

