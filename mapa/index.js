/* import * as d3 from "d3";
import * as topojson from "topojson"; */

//const dataS1vsS3 =  require("./s1-vs-s3.json");

function draw() {

    const mapaModal = new bootstrap.Modal(document.getElementById('mapaModal')); 
    const windowWidth = window.innerWidth;
  
    const width = windowWidth > 800 ? 800 : windowWidth;
    const height = width / 1.5;
  
    const projection = d3
      .geoMercator()
      .scale(width * 1.8)
      .center([-103.34034978813841, 30.012062015793]) // strange magic
      .translate([width / 2.2, height / 6]);
    /* .precision(0.1); */
  
    const path = d3.geoPath().projection(projection);
  
    const colorDomain = [5, 10, 15];
    const colorRange = [
      "#fae9a8",
      "#ffba00",
      "#ff7d73",
      "#ff1300"
    ];
    const color = d3.scaleThreshold().domain(colorDomain).range(colorRange);
  
    const map = d3
      .select("body")
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
  
        const dataS1vsS3 =  await d3.json("s1-vs-s3.json");
        //console.log(dataS1vsS3)
        mexico.objects.collection.geometries.forEach(function (element) {
          let dataInhabilitados = [];
          dataS1vsS3.forEach(function (newElement) {
            //console.log(newElement)
            if (
              parseInt(element.properties.clave) ==
              parseInt(newElement.claveEntidadFederativa)
            ) {
              dataInhabilitados = [newElement, ...dataInhabilitados]
              element.properties.totalContratacion = dataInhabilitados.length;
              element.properties.dataInhabilitados = dataInhabilitados;
            }
          });
        });
  
        const geojson = topojson.feature(mexico, mexico.objects.collection);
        //console.log(geojson.features);
  
        map
          .selectAll("path")
          .data(geojson.features)
          .enter()
          .append("path")
          .attr("d", path)
          .style("stroke", "gray")
          .style("fill", (d) => {
            console.log(d)
            const { totalContratacion } = d.properties;
            if (totalContratacion == undefined){
              return "#adfcad"
            }
            return color(totalContratacion);
            
          })
          .on('click', (_, d) => {
            const { dataInhabilitados } = d.properties;
            console.log(dataInhabilitados)
            mapaModal.show();
          })
          .on("mouseover", (event, d) => {
            console.log(d)
            const { entidad, totalContratacion } = d.properties;
            //const value = data[id];
  
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
  
  function clear() {
    d3.selectAll("svg#map").remove();
  }
  
  draw();
  
  let resizeTimer;
  window.onresize = () => {
    clearTimeout(resizeTimer);
  
    resizeTimer = setTimeout(() => {
      clear();
      draw();
    }, 100);
  };
  