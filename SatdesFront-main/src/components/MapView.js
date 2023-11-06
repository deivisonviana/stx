import React, { useRef, useEffect, useState } from 'react';
import mapboxgl from 'mapbox-gl';
import { styles } from '../data/stylesMap/styles';
import { stationsDefesa } from '../data/stations-lat.lng/DefesaCivil'; // Importe os dados das estações
import { stationsIncaper } from '../data/stations-lat.lng/Incaper'; // Importe os dados das estações

mapboxgl.accessToken = 'pk.eyJ1Ijoic2F0ZGVzIiwiYSI6ImNsbWd1eGJrZjBjamozcnNlbDVhN2c0M2MifQ.PS-DD0vWP5d1X8e-VfuTfQ';

function MapView() {
  const mapContainer = useRef(null);
  const map = useRef(null);
  const [lng, setLng] = useState(-40.3381);
  const [lat, setLat] = useState(-20.3222);
  const [zoom, setZoom] = useState(11.15);
  const [selectedStyle, setSelectedStyle] = useState(styles[0]);

  useEffect(() => {
    if (!map.current) {
      map.current = new mapboxgl.Map({
        container: mapContainer.current,
        style: selectedStyle.style,
        center: [lng, lat],
        zoom: zoom,
      });

      map.current.on('load', () => {
        map.current.addSource('defesaCivil', {
          type: 'geojson',
          data: {
            type: 'FeatureCollection',
            features: stationsDefesa.map((station) => ({
              type: 'Feature',
              properties: {
                description: `<strong>${station.city}</strong>`, // Use a propriedade city para a descrição
              },
              geometry: {
                type: 'Point',
                coordinates: [parseFloat(station.lng.replace(',', '.')), parseFloat(station.lat.replace(',', '.'))], // Converter lat e lng para números
              },
            })),
          },
        });

        // map.current.addSource('incaper', {
        //   type: 'geojson',
        //   data: {
        //     type: 'FeatureCollection',
        //     features: stationsIncaper.map((station) => ({
        //       type: 'Feature',
        //       properties: {
        //         description: `<strong>${station.city}</strong>`, // Use a propriedade city para a descrição
        //       },
        //       geometry: {
        //         type: 'Point',
        //         coordinates: [parseFloat(station.lng.replace(',', '.')), parseFloat(station.lat.replace(',', '.'))], // Converter lat e lng para números
        //       },
        //     })),
        //   },
        // });

        map.current.addLayer({
          id: 'placesDefesa',
          type: 'circle',
          source: 'defesaCivil',
          paint: {
            'circle-color': '#F78C45',
            'circle-radius': 6,
            'circle-stroke-width': 2,
            'circle-stroke-color': 'rgb(247,140,69)',
          },
        });

        // map.current.addLayer({
        //   id: 'placesIncaper',
        //   type: 'circle',
        //   source: 'incaper',
        //   paint: {
        //     'circle-color': '#006024',
        //     'circle-radius': 6,
        //     'circle-stroke-width': 2,
        //     'circle-stroke-color': 'rgb(247,140,69)',
        //   },
        // });

        const popup = new mapboxgl.Popup({
          closeButton: false,
          closeOnClick: false,
        });

        map.current.on('mouseenter', 'placesDefesa', (e) => {
          map.current.getCanvas().style.cursor = 'pointer';

          const coordinates = e.features[0].geometry.coordinates.slice();
          const description = e.features[0].properties.description;

          while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
          }

          popup.setLngLat(coordinates).setHTML(description).addTo(map.current);
        });

        map.current.on('mouseleave', 'placesDefesa', () => {
          map.current.getCanvas().style.cursor = '';
          popup.remove();
        });
      });
    }
  }, [selectedStyle, lng, lat, zoom]);

  const handleStyleChange = (event) => {
    const selectedStyleName = event.target.value;
    const newSelectedStyle = styles.find((style) => style.name === selectedStyleName);
    setSelectedStyle(newSelectedStyle);
  };

  return (
    <div>
      <div className="sidebar">
        <div>
          <label>Selecione o Estilo do Mapa:</label>
          <select onChange={handleStyleChange} value={selectedStyle.name}>
            {styles.map((style) => (
              <option key={style.name} value={style.name}>
                {style.name}
              </option>
            ))}
          </select>
        </div>
        <p>Longitude: {lng.toFixed(4)} | Latitude: {lat.toFixed(4)} | Zoom: {zoom.toFixed(2)}</p>
      </div>
      <div ref={mapContainer} className="map-container" />
    </div>
  );
}

export default MapView;
