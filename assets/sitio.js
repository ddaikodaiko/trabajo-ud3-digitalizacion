(function () {
  "use strict";

  var barra = document.querySelector(".barra");
  var boton = document.querySelector(".barra__boton");
  var lista = document.querySelector(".barra__lista");

  // Menú móvil
  function cerrarMenu() {
    if (!barra || !boton) return;
    barra.classList.remove("abierta");
    boton.setAttribute("aria-expanded", "false");
  }
  if (barra && boton && lista) {
    boton.addEventListener("click", function () {
      var abierta = barra.classList.toggle("abierta");
      boton.setAttribute("aria-expanded", abierta ? "true" : "false");
    });
    lista.addEventListener("click", function (e) {
      if (e.target.closest("a")) cerrarMenu();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") cerrarMenu();
    });
  }

  // Apartado actual
  var enlaces = document.querySelectorAll(".barra__lista a");
  var secciones = document.querySelectorAll("section.seccion[id]");
  function marcarActual(id) {
    enlaces.forEach(function (a) {
      if (a.getAttribute("href") === "#" + id) a.setAttribute("aria-current", "true");
      else a.removeAttribute("aria-current");
    });
  }
  if ("IntersectionObserver" in window && secciones.length) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (en.isIntersecting) marcarActual(en.target.id);
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    secciones.forEach(function (s) { obs.observe(s); });
  }

  // Fotos que no cargan
  function ocultarFoto(img) {
    var fig = img.closest("figure.foto");
    if (fig) fig.classList.add("sin-foto");
  }
  document.querySelectorAll("img[data-foto]").forEach(function (img) {
    img.addEventListener("error", function () { ocultarFoto(img); });
    if (img.complete && img.naturalWidth === 0) ocultarFoto(img);
  });
})();
