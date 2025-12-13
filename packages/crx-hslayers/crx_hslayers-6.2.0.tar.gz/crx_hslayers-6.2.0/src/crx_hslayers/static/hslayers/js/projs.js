function initProjections() {
  proj4.defs(
    "EPSG:3035",
    "+proj=laea +lat_0=52 +lon_0=10 +x_0=4321000 +y_0=3210000 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +axis=neu +no_defs +type=crs"
  );
  proj4.defs(
    "http://www.opengis.net/gml/srs/epsg.xml#3035",
    proj4.defs("EPSG:3035")
  );

  proj4.defs(
    "EPSG:5514",
    "+proj=krovak +lat_0=49.5 +lon_0=24.83333333333333 +alpha=30.28813972222222 +k=0.9999 +x_0=0 +y_0=0 +ellps=bessel +towgs84=542.5,89.2,456.9,5.517,2.275,5.516,6.96 +units=m +no_defs"
  );
  proj4.defs(
    "http://www.opengis.net/gml/srs/epsg.xml#5514",
    proj4.defs("EPSG:5514")
  );

  proj4.defs(
    "EPSG:4258",
    "+proj=longlat +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +no_defs"
  );
  proj4.defs(
    "http://www.opengis.net/gml/srs/epsg.xml#4258",
    proj4.defs("EPSG:4258")
  );

  proj4.defs(
    "EPSG:32633",
    "+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs +type=crs"
  );
  proj4.defs(
    "http://www.opengis.net/gml/srs/epsg.xml#32633",
    proj4.defs("EPSG:32633")
  );
  proj4.defs(
    "EPSG:32634",
    "+proj=utm +zone=34 +datum=WGS84 +units=m +no_defs +type=crs"
  );
  proj4.defs(
    "http://www.opengis.net/gml/srs/epsg.xml#32634",
    proj4.defs("EPSG:32634")
  );

  proj4.defs(
    "EPSG:3995",
    "+proj=stere +lat_0=90 +lat_ts=71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
  );
  proj4.defs(
    "http://www.opengis.net/gml/srs/epsg.xml#3995",
    proj4.defs("EPSG:3995")
  );
  proj4.defs(
    "EPSG:3031",
    "+proj=stere +lat_0=-90 +lat_ts=-71 +lon_0=0 +k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
  );
  proj4.defs(
    "http://www.opengis.net/gml/srs/epsg.xml#3031",
    proj4.defs("EPSG:3031")
  );
}

initProjections();
