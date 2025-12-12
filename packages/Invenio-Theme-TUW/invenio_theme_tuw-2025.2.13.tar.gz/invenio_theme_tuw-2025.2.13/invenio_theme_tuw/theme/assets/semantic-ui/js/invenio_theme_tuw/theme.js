import $ from "jquery";

// close the mobile menu when clicking outside (on the overlay)
const darkeningOverlay = $("#mobile-menu-darkener");
if (darkeningOverlay.length) {
  darkeningOverlay.on("click", () => {
    $("#invenio-nav").toggleClass("active");
  });
}

// move the mobile sidebar menu below any banners
const invenioNav = $("#invenio-nav");
const outerNavbar = $("nav.outer-navbar");
if (invenioNav.length && outerNavbar.length) {
  invenioNav.css("top", outerNavbar.position().top);
}
