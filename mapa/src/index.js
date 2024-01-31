import "./index.css";

import { draw, clear } from "./draw";

draw();

let resizeTimer;
window.onresize = () => {
  clearTimeout(resizeTimer);

  resizeTimer = setTimeout(() => {
    clear();
    draw();
  }, 100);
};
