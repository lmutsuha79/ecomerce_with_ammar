// #######################################
// for oppen and close the links_nav bar :
let mb_nav_btn = document.getElementById('mb_nav_btn');
let main_nav_of_links = document.getElementById('main_nav_of_links');





function change_nav_style() {
    main_nav_of_links.classList.toggle('open_mb_nav');



}
mb_nav_btn.onclick = function () {
    change_nav_style();
    // change nav btn bolets style
    mb_nav_btn.classList.toggle('mb_nav_open_style');

}

// ############################################
// slider js 



swip_index = 0; // initiall value;
let slider_items = document.querySelectorAll('.slider_content .item');
let slider = document.querySelector('.slider');
let slider_controller_bolets = document.querySelectorAll('.bolet_controll');
let slider_content = document.querySelector('.slider_content');
slider_controller_bolets.forEach((bolet, index) => {
    bolet.onclick = function () {
        swip_index = index;
        // slider_content.style.left = `${-index * 100}%`;
        // slider_controller_bolets.forEach(bol => { bol.classList.remove('bolet_active') });
        // bolet.classList.add('bolet_active');
        swip();
    }
});


let touch_end_position;
let touch_start_position;
slider.addEventListener('touchstart', touch_start);
slider.addEventListener('touchmove', touch_move);
slider.addEventListener('touchend', touch_end);

function touch_start(ev) {
    touch_start_position = ev.touches[0].clientX;
}
function touch_move(ev) {
    touch_end_position = ev.touches[0].clientX;
}
function check_swip_index_value() {
    if (swip_index > 2) {
        swip_index = 0;
    }
    if (swip_index < 0) {
        swip_index = 2;
    }
    else {

    }
}
function touch_end(ev) {
    if (touch_start_position - touch_end_position > 0) {
        console.log('swip to the left');
        swip_index++;
        swip();
    }
    if (touch_start_position - touch_end_position < 0) {
        console.log('swip to the right');
        swip_index--;
        swip();
    }
}

function swip() {

    check_swip_index_value();

    slider_content.style.left = `${-swip_index * 100}%`;

    bolet_style_when_swip()
    // slider_controller_bolets.forEach(bol => { bol.classList.remove('bolet_active') });
}
function bolet_style_when_swip() {
    slider_controller_bolets.forEach(bol => {
        bol.classList.remove('bolet_active');
        console.log('roce')

    });
    slider_controller_bolets[swip_index].classList.add('bolet_active');

}
auto_slid = 1;
window.setInterval(function () {
    if (auto_slid == 1) {

        swip_index++;
        swip();
    }

}, 2500);

slider.addEventListener('mouseleave', function () {
    auto_slid = 1;
})

slider.addEventListener('mouseover', function () {
    auto_slid = 0;
})


// ##############################################





