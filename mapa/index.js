// Variable global para almacenar la instancia del mapa actual
let currentMap;
let colorDomain; // Declarar la variable a nivel global
let currentModal; // Declarar la variable a nivel global para la modal actual
//Claves de entidades federativas que aparecen en el concentrado de los conectados
const highlightedKeys = ["02","03","04","09","05","06","10","11","12","13","17","18","19","20","22","24","25","26","27","28","30"];
const highlightColor = "#5b635b"; 

const colorDomains = {
  "s1-vs-s3.json": [0, 1, 5, 10, 15, 20],
  "s6-vs-s3_original.json": [0, 1, 2, 6, 11, 16] // Ajusta el dominio para el otro archivo
};

const colorRanges = {
  "s1-vs-s3.json": ["#808080", "#ffc0cb", "#ffff00", "#ffa500", "#ff0000"],
  "s6-vs-s3_original.json": ["#cfe8f3", "#ffc0cb", "#ffff00", "#ffa500", "#ff0000"] // Corregido aquí
};


function drawLegend(colorScale, colorDomain) {
  const legendContainer = d3.select("#leyenda");

  // Elimina cualquier leyenda existente
  legendContainer.selectAll("*").remove();

  const legend = legendContainer
    .append("svg")
    .attr("width", 300)
    .attr("height", 300);

  const legendWidth = 100;
  const legendHeight = 60;

  legend
    .selectAll("rect")
    .data(colorScale.range())
    .enter()
    .append("rect")
    .attr("x", (_, i) => i * legendWidth)
    .attr("y", 10)
    .attr("width", legendWidth)
    .attr("height", legendHeight)
    .style("fill", (d) => d);

  legend
    .selectAll("text")
    .data(colorScale.range())
    .enter()
    .append("text")
    .attr("x", (_, i) => i * legendWidth)
    .attr("y", 40)
    .text((d, i) => {
      const range = colorScale.invertExtent(d);
      return `${colorDomain[i]} - ${colorDomain[i + 1]}`;
    });
}

function draw(mapDataFile) {
  const windowWidth = window.innerWidth;

  const width = windowWidth > 800 ? 800 : windowWidth;
  const height = width / 1.5;

  const projection = d3
    .geoMercator()
    .scale(width * 1.8)
    .center([-103.34034978813841, 30.012062015793])
    .translate([width / 2.2, height / 6]);

  const path = d3.geoPath().projection(projection);

  // Selecciona el dominio y rango de colores según el mapa actual
  colorDomain = colorDomains[mapDataFile] || [0, 1, 2]; // Usar la variable global
  const colorRange = colorRanges[mapDataFile] || ["#adfcad"];

  const color = d3.scaleThreshold().domain(colorDomain).range(colorRange);

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
      const color = d3.scaleThreshold().domain(colorDomain).range(colorRange);
    
    /*
      const geojson = topojson.feature(mexico, mexico.objects.collection);
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
      }) */
      map
        .selectAll("path")
        .data(geojson.features)
        .enter()
        .append("path")
        .attr("d", path)
        .style("stroke", "black")
        .style("fill", (d) => {
          const { totalContratacion, clave } = d.properties;

          // Verifica si totalContratacion tiene un valor
          if (totalContratacion !== undefined && totalContratacion !== 0) {
            // Utiliza la escala de colores existente para totalContratacion
            return color(totalContratacion);
          }

          // Verifica si la clave de entidad está en la lista de claves que deseas resaltar
          if (highlightedKeys.includes(clave)) {
            return highlightColor;
          }

          // Si totalContratacion no tiene un valor y la entidad no está en highlightedKeys, devuelve color gris
          return "white"; // o cualquier otro color gris que desees
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

      // Almacena la instancia del mapa actual en la variable global
      currentMap = map;

      // Dibuja la leyenda
      drawLegend(color, colorDomain);
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

  // Destruye la instancia de la modal actual antes de asignar la nueva
  if (currentModal) {
    currentModal.dispose();
  }

  // Asigna la modal actual según el mapa seleccionado
  if (newMapDataFile === 's1-vs-s3.json') {
    currentModal = new bootstrap.Modal(document.getElementById('mapaModal'));
  } else if (newMapDataFile === 's6-vs-s3_original.json') {
    currentModal = new bootstrap.Modal(document.getElementById('mapaModal2'));
  }

  // Muestra la nueva modal después de asignarla
  //currentModal.show();
  drawLegend(color, colorDomain);
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