function nav_bar(){
    const menu = document.getElementById('menu');
    const hamburger = document.getElementById('hamburger');
    const btns = document.querySelectorAll('.nav-link');
    // InTransit prevents multiple clicks on the burger from breaking the toolbar
    let inTransit = false;

    hamburger.addEventListener('click', function() {
        if (inTransit) return;
        inTransit = true;
        if (menu.classList.contains('max-h-0') && menu.classList.contains('fixed') && !menu.classList.contains('max-h-screen')) {
            //menu.classList.remove('max-h-0');
            menu.classList.add('max-h-screen');
            menu.classList.remove('fixed');
            setTimeout(() => {
            btns.forEach(btn => {btn.classList.remove('opacity-0');btn.classList.add('opacity-100')})
            // Reset isAnimating after the longest duration (transition + staggered effect)
            inTransit = false;
            }, 10)
        } else {
            menu.classList.remove('max-h-screen');
            btns.forEach(btn => {btn.classList.add('opacity-0');btn.classList.remove('opacity-100')})
            setTimeout(() => {
            menu.classList.add('fixed');
            // Reset isAnimating after the longest duration (transition + staggered effect)
            inTransit = false;
            }, 600); // Match the duration of the transition
        }
    });
}

function navbar_active_link(){
    const url = window.location.href
    const navbar_links = document.querySelectorAll(".nav-link")
    
    navbar_links.forEach(link => {
        console.log(link.href,url)
        if (url === link.href) {
            // highlights the button text-white border-white border-blue-900
            if (link.classList.contains('d-nav')){
                link.classList.remove('text-blue-900', 'border-blue-900', 'hidden')
            }
            else {
                link.classList.remove('text-blue-900', 'border-blue-900')
            }
            link.classList.add('text-white', 'border-white', 'font-bold')
        } else if (link.href !== url) {
            if (link.classList.contains('d-nav')){
                link.classList.add('text-blue-900', 'border-blue-900', 'hidden')
            }
            else {
                link.classList.add('text-blue-900', 'border-blue-900')
            }
            link.classList.remove('text-white', 'border-white')
        }

    });
};

function trust_navbar_active_link(){
    const url = window.location.href
    const navbar_links = document.querySelectorAll(".nav-link")
    
    navbar_links.forEach(link => {
        if (url === link.href) {
            link.classList.add('bg-white', 'border-none', 'text-green-700')
            link.classList.remove('bg-green-700', 'text-gray-50', 'border-green-900')
        } else if (link.href !== url) {
            link.classList.remove('bg-white', 'border-none', 'text-green-700')
            link.classList.add('bg-green-700', 'text-gray-50', 'border-green-900')
        }

    });
};
nav_bar();
navbar_active_link();
trust_navbar_active_link();