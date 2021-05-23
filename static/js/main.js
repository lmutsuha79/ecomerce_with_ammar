// #######################################
// for oppen and close the links_nav bar :
let mb_nav_btn = document.getElementById('mb_nav_btn');
let main_nav_of_links = document.getElementById('main_nav_of_links');




function change_nav_style() {
    main_nav_of_links.classList.toggle('open_mb_nav');



}
mb_nav_btn.onclick = change_nav_style;


