

function draw(mapDataFile) {
  const windowWidth = window.innerWidth;

  const width = windowWidth > 1200 ? 1200 : windowWidth;
  const height = width / 1.5;

  const projection = d3
    .geoMercator()
    .scale(width * 1.8)
    .center([-103.34034978813841, 30.012062015793])
    .translate([width / 2.2, height / 6]);

  const path = d3.geoPath().projection(projection);

  // Selecciona el contenedor específico para el mapa
  const mapContainer = d3.select("#vis");

  // Elimina el mapa existente antes de dibujar uno nuevo
  mapContainer.selectAll("svg#map").remove();

  const map = mapContainer
    .append("svg")
    .attr("id", "map")
    .attr("width", width)
    .attr("height", height);

  const tooltip = d3
    .select("body")
    .append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);
  
    const colorDomain = [1, 5, 10, 15, 20];
    const extColorDomain = [1, 5, 10, 15, 20];
    const legendLabels = [
      "1 - 5",
      "5 - 10",
      "10 - 15",
      "15 - 20",
      "20 - 25"
    ];
    const colorRange = [
      "#ffcc00",
      "#ff9f00",
      "#ff7900",
      "#ff4d00",
      "#ff2400"
    ];
  
    const legend = map
      .selectAll("g.legend")
      .data(colorDomain)
      .enter()
      .append("g")
      .attr("class", "legend")
      .attr("transform", "translate(5,300)");
  
    const legendLength = legendLabels.length;
    const legendBoxSize = 20;
    const legendMarginTop = height / 10;
  
    const color = d3
      .scaleThreshold()
      .domain(colorDomain)
      .range(colorRange);
  
    legend
      .append("rect")
      .attr("x", 40)
      .attr("y", (_d, i) => {
        return (legendLength - i) * legendBoxSize + legendMarginTop;
      })
      .attr("width", legendBoxSize)
      .attr("height", legendBoxSize)
      .style("fill", color)
      .style("opacity", 0.8);
  
    legend
      .append("text")
      .attr("x", 70)
      .attr("y", (_d, i) => {
        return (legendLength + 1 - i) * legendBoxSize - 4 + legendMarginTop;
      })
      .text((_d, i) => legendLabels[i]);

  try {
    (async () => {
      const mexico = await d3.json(
        "https://raw.githubusercontent.com/PDNMX/viz-cuestionario-estados/master/data/mexico.json",
      );

      const dataS1vsS3 = await d3.json(mapDataFile);

      mexico.objects.collection.geometries.forEach(function (element) {
        let dataInhabilitados = [];
        dataS1vsS3.forEach(function (newElement) {
          if (
            parseInt(element.properties.clave) ==
            parseInt(newElement.claveEntidadFederativa)
          ) {
            dataInhabilitados = [newElement, ...dataInhabilitados];
            element.properties.totalContratacion = dataInhabilitados.length;
            element.properties.dataInhabilitados = dataInhabilitados;
          }
        });
    
        // Filtra las claves que tienen un valor en totalContratacion
        /* if (element.properties.totalContratacion !== undefined) {
          const index = highlightedKeys.indexOf(element.properties.clave);
          if (index !== -1) {
            highlightedKeys.splice(index, 1);
          }
        } */
      });

      const geojson = topojson.feature(mexico, mexico.objects.collection);
      //const color = d3.scaleThreshold().domain(colorDomain).range(colorRange);
      const color = d3.scaleThreshold().domain(colorDomain).range(colorRange);

      map
      .selectAll("path")
      .data(geojson.features)
      .enter()
      .append("path")
      .attr("d", path)
      .style("stroke", "black")
      .style("fill", (d) => {
        const { totalContratacion } = d.properties;
    
        // Si el valor es undefined, devuelve el color gris
        if (totalContratacion === undefined) {
          return "white"; // o cualquier otro color gris que desees
        }
    
        return color(totalContratacion);
      }) 
      
        .on('click', (_, d) => {
          const { dataInhabilitados } = d.properties;
    
          // Obtén el elemento que contiene la lista de inhabilitados en la modal
          const modalBody = document.querySelector('.modal-body');
      
          // Limpia el contenido existente en la modal
          modalBody.innerHTML = '';
      
          // Itera sobre los datos de inhabilitados y crea elementos para mostrarlos en la modal
          dataInhabilitados.forEach((inhabilitado, index) => {
              const inhabilitadoElement = document.createElement('div');
              inhabilitadoElement.innerHTML = `
                  <h2>Persona #${index + 1}</h2>
                  <p><strong>Nombre:</strong> ${inhabilitado.nombre_declaracion}</p>
                  <p><strong>Tipo de falta:</strong> ${inhabilitado.tipoFalta}</p>
                  <p><strong>Tipo de persona:</strong> ${inhabilitado.tipo_persona}</p>
                  <!-- Agrega más líneas según las propiedades que quieras mostrar -->
              `;
              modalBody.appendChild(inhabilitadoElement);
          });
        
            // Muestra la modal después de llenarla con los datos
            currentModal = new bootstrap.Modal(document.getElementById('mapaModal'));
            currentModal.show();
          
        })
        .on("mouseover", (event, d) => {
          const { entidad, totalContratacion } = d.properties;
          tooltip.transition().duration(300).style("opacity", 0.9);
          tooltip
            .html(`<b>${entidad}</b><br/><b>Total Contrataciones Indebidas: ${totalContratacion}</b>`)
            .style("left", `${event.pageX - 30}px`)
            .style("top", `${event.pageY - 40}px`);
        })
        .on("mousemove", (event) => {
          tooltip
            .style("left", `${event.pageX - 30}px`)
            .style("top", `${event.pageY - 40}px`);
        })
        .on("mouseout", () => {
          tooltip.transition().duration(300).style("opacity", 0);
        });

    })();
  } catch (e) {
    console.error(e);
  }
}

// Llamada inicial para cargar el primer mapa
draw("s1-vs-s3.json");

// Función para cambiar entre mapas y mostrar la modal correspondiente

function changeMap(newMapDataFile) {
  clear();
  draw(newMapDataFile);

}

// Evento de cambio en el menú desplegable
document.getElementById('mapSelector').addEventListener('change', function () {
  const selectedMap = this.value;
  changeMap(selectedMap);
});

// Función para limpiar el mapa
function clear() {
  // Elimina el mapa existente antes de dibujar uno nuevo
  d3.selectAll("svg#map").remove();
}

// Función para manejar el redimensionamiento de la ventana
function handleResize() {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    clear();
    draw(document.getElementById('mapSelector').value);
  }, 100);
}

// Asigna el evento de redimensionamiento
let resizeTimer;
window.onresize = handleResize;
