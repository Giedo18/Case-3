#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st


# In[1]:


def OpenChargeMap():
    import pandas as pd
    import requests
    from streamlit_folium import st_folium
    import folium

    
    # Informatie over wat er te lezen is op deze pagina
    st.write("""
        # Laadpaaldata OpenChargeMap
        Op deze pagina is informatie te lezen over de informatie die is verkregen uit de dataset die is verkregen
        met behulp van de OpenChargeMap.""")
    
    laadpalen = pd.read_csv("Laadpalen.csv")
    laadpalen.head()
    
    locatiedata = pd.read_csv("Locatiedata.csv")

    st.write(Laadpalen.head(3))


# In[ ]:


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
    


# In[ ]:


plaatsnaam = 'Amsterdam'
long_lat = locatiedata[locatiedata['Plaats'] == plaatsnaam]['Locatie'].values


# In[ ]:


# district # geometry  # aantal
# 1        # polygon.. # 1677

m = folium.Map(location = long_lat,
              tiles = 'cartodbpositron')
# m.fit_bounds()

for index, row in Laadpalen.iterrows():
    
    color_circle = kleuren(row['Aantal_Laadpalen'])
    marker=(folium.CircleMarker(location =[row['AddressInfo.Latitude'], row['AddressInfo.Longitude']],
                                popup = row["Postcode_Groep"],
                                radius = 1,
                                color = color_circle))
    marker.add_to(m)
    
# Legenda toevoegen
m = add_categorical_legend(m,
                           'Aantal laadpalen per postcode groep',
                           colors = ['green', 'lime', 'greenyellow', 'yellow', 'darkorange',
                                     'red', 'darkred'],
                           labels = ['> 1200', '> 1000', '> 800', '> 600', '> 400',
                                     '> 200', '0-200'])

st_data = st_folium(m, width = 725)

