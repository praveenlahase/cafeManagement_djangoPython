function openNav() {
    document.getElementById("myNav").classList.toggle("menu_width");
    document.querySelector(".custom_menu-btn").classList.toggle("menu_btn-style");
}

function closeNav() {
    document.getElementById("myNav").classList.remove("menu_width");
    document.querySelector(".custom_menu-btn").classList.remove("menu_btn-style");
}
