# DA
Code pour #datascience-appliquee

#Challenge JSON
The script download a realtime generated geoJSON file from Lyon'Town open data platform, transform it to a GeoDataFrame, make some changes on datas before loading it to a flat table on a postgre db.
Files : Veloader.py et Veloader_datastruct.py
Need python -m pip install following packages : sqlalchemy, geopandas, urllib
In case you are unfamiliar with geopandas and running windows, tricks for installing it, step by step, are described here : http://geoffboeing.com/2014/09/using-geopandas-windows/
