function draw(mapDataFile) {
  const mapaModal = new bootstrap.Modal(document.getElementById("mapaModal"));
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

  const t = d3.transition()
    .duration(1500)
    .ease(d3.easeLinear)
    .style("fill", "#fff");

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
  //const extColorDomain = [1, 5, 10, 15, 20];
  const legendLabels = ["1 - 5", "5 - 10", "10 - 15", "15 - 20", "> 20"];
  const colorRange = ["#ffcc00", "#ffcc00", "#ff9f00", "#ff7900", "#ff4d00", "#ff2400"];

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

  const color = d3.scaleThreshold().domain(colorDomain).range(colorRange);

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
    .style("fill", "#55575a")
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
        .attr("stroke-width", 1.5)
        .style("stroke", "#a3a3a3")
        .style("fill", "#fff")
        .style("cursor", (d) => {
          const { totalContratacion } = d.properties;
          if (totalContratacion != undefined) {
            return "pointer"
          } else {
            return "not-allowed"
          }

        })
        .on("click", (_, d) => {
          //console.log(mapDataFile);
          const { dataInhabilitados, entidad, totalContratacion } = d.properties;
          //console.log(dataInhabilitados);

          // Obtén el elemento que contiene la lista de inhabilitados en la modal
          const accordionFlush = document.getElementById("accordionFlush");
          const modalTitle = document.getElementById("modalTitulo");
          modalTitle.innerHTML = "";
          modalTitle.innerHTML = `<h4>${entidad}</h4> <h5 class="fw-light">Total de contrataciones indebidas: ${totalContratacion}</h5>`;
          d3.select(".modal-header").style("background", color(totalContratacion));
          // Limpia el contenido existente en la modal
          accordionFlush.innerHTML = "";

          // Itera sobre los datos de inhabilitados y crea elementos para mostrarlos en la modal
          dataInhabilitados.forEach((inhabilitado, index) => {
            const inhabilitadoElement = document.createElement("div");
            inhabilitadoElement.innerHTML = `
                <div class="accordion-item">
                  <h2 class="accordion-header">
                      <button class="accordion-button collapsed fw-bold" type="button" data-bs-toggle="collapse"
                          data-bs-target="#flush-${index}" aria-expanded="false"
                          aria-controls="flush-${index}">
                          ${mapDataFile == 's1-vs-s3.json' ? inhabilitado.nombreEntePublico : inhabilitado.procuring_entity}
                      </button>
                  </h2>
                  <div id="flush-${index}" class="accordion-collapse collapse"
                      data-bs-parent="#accordionFlush">
                      <div class="accordion-body">
                        <ul>
                          <li style="text-transform: capitalize;"><strong>Nombre: </strong>${ mapDataFile == 's1-vs-s3.json' ? inhabilitado.nombre_declaracion : inhabilitado.sancion_nombre}</li>
                          <li><strong>Cargo: </strong>${ mapDataFile == 's1-vs-s3.json' ? inhabilitado.empleoCargoComision : mapDataFile == 's6-vs-s3.json' ? inhabilitado.puesto : "<i>Dato no proporcionado</i>" }</li>
                          <li><strong>Tipo de falta: </strong>${ mapDataFile == 's1-vs-s3.json' ? inhabilitado.tipoFalta : "<i>Dato no proporcionado</i>"}</li>
                          <li><strong>Motivo: </strong>${ mapDataFile == 's1-vs-s3.json' || 's6-vs-s3.json' ? inhabilitado.causa_motivo_hechos : "<i>Dato no proporcionado</i>"}</li>

                          ${ mapDataFile == 's1-vs-s3.json' ? `<li><strong>Fecha de contratación: </strong>${inhabilitado.fechaTomaPosesion}`
                          : mapDataFile == 's6-vs-s3.json' ? `<li><strong>Fechas de contratación: </strong><ul><li><strong>Inicial: </strong>${inhabilitado.earliest_contractPeriod_startDate}</li><li><strong>Final: </strong>${inhabilitado.latest_contractPeriod_endDate}</li></ul></li>`
                          : "<i>Dato no proporcionado</i>"}</li>

                          <li><strong>Fechas de inhabilitación:</strong><ul>
                            <li><strong>Inicial: </strong>${ mapDataFile == 's1-vs-s3.json' ? inhabilitado.inhabilitacion_fechaInicial : mapDataFile == 's6-vs-s3.json' ? inhabilitado.inhabilitacion_fechaInicial :"<i>Dato no proporcionado</i>"}</li>
                            <li><strong>Final: </strong>${ mapDataFile == 's1-vs-s3.json' ? inhabilitado.inhabilitacion_fechaFinal : mapDataFile == 's6-vs-s3.json' ? inhabilitado.inhabilitacion_fechaFinal: "<i>Dato no proporcionado</i>"}</li>
                          </ul></li>
                        <ul>
                      </div>
                  </div>
                </div>
              `;
              accordionFlush.appendChild(inhabilitadoElement);
          });

          // Muestra la modal después de llenarla con los datos
          mapaModal.show();
        })
        .on("mouseover", (event, d) => {
          const { entidad, totalContratacion } = d.properties;
          let textTooltip;
          if (totalContratacion != undefined) {
            textTooltip = `<h5>${entidad}</h5><b>Total Contrataciones Indebidas: <br/>${totalContratacion}</b>`
          } else {
            textTooltip = `<h5>${entidad}</h5><b>No hay información</b>`
          }
          tooltip.transition().duration(300).style("opacity", 0.9);
          tooltip
            .html(textTooltip)
            .style("left", `${event.pageX + 25}px`)
            .style("top", `${event.pageY}px`);
        })
        .on("mousemove", (event) => {
          tooltip
            .style("left", `${event.pageX + 25}px`)
            .style("top", `${event.pageY}px`);
        })
        .on("mouseout", () => {
          tooltip.transition().duration(300).style("opacity", 0);
        })

        .transition(t)
        .style("fill", (d) => {
          const { totalContratacion } = d.properties;

          // Si el valor es undefined, devuelve el color gris
          if (totalContratacion === undefined) {
            return "white"; // o cualquier otro color gris que desees
          }

          return color(totalContratacion);
        })
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
document.getElementById("mapSelector").addEventListener("change", function () {
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
    draw(document.getElementById("mapSelector").value);
  }, 100);
}

// Asigna el evento de redimensionamiento
let resizeTimer;
//window.onresize = handleResize;
