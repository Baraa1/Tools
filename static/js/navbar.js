function sidebar_active_link(){
    const url = window.location.href
    const navbar_links = document.querySelectorAll(".nav-link")
    
    navbar_links.forEach(link => {
        console.log(url === link.href, url, link.href)
        if (url === link.href) {
            // highlights the button text-white border-white border-blue-900
            if (link.classList.contains('d-nav')){
                link.classList.remove('text-blue-900', 'border-blue-900', 'hidden')
            }
            else {
                link.classList.remove('text-blue-900', 'border-blue-900')
            }
            link.classList.add('text-white', 'border-white')
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
sidebar_active_link();