function navBarLinksChilds() {
    document.querySelectorAll('.menu-has-children').forEach(function (menu) {
        let timeout
        const submenu = menu.querySelector('ul')

        menu.addEventListener('mouseenter', function () {
            clearTimeout(timeout)
            submenu.classList.add('is-visible')
        })

        menu.addEventListener('mouseleave', function () {
            timeout = setTimeout(function () {
                submenu.classList.remove('is-visible')
            }, 200)
        })
    })
}

function navBarMovement() {
    const headerSticky = document.getElementById("nav-bar")
    const navBarMainMenu = document.querySelector(".nav-bar-main-menu")

    window.addEventListener("scroll", () => {
        if (window.scrollY > 80) {
            headerSticky.classList.add("nav-bar-scrolled")
            navBarMainMenu.style.background = "transparent"
        }
        else {
            headerSticky.classList.remove("nav-bar-scrolled")
            navBarMainMenu.style.background = "rgba(255, 255, 255, 0.15)"
        }
    })
}

function hotDealCarusel() {
    const slider = document.getElementById('slider')
    const dots = document.querySelectorAll('.hot-deal-section-carusel-dot')
    const cards = document.querySelectorAll('.hot-deal-section-carusel-card')
    let autoSlideInterval;

    function goToSlide(index) {
        const cardWidth = slider.offsetWidth + 20
        slider.scrollTo({
            left: cardWidth * index,
            behavior: 'smooth'
        });
        resetAutoSlide()
    }

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index))
    })

    slider.addEventListener('scroll', () => {
        const cardWidth = slider.offsetWidth + 20
        const activeIndex = Math.round(slider.scrollLeft / cardWidth)

        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === activeIndex)
        })
    })

    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            let currentIndex = Math.round(slider.scrollLeft / (slider.offsetWidth + 20))
            let nextIndex = (currentIndex + 1) % dots.length
            goToSlide(nextIndex)
        }, 8000)
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval)
        startAutoSlide()
    }

    startAutoSlide()
}

function smoothUp() {
    document.querySelectorAll('a[href="#"]').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault()
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            })
        })
    })
}

function cardDest() {
    async function refreshDestinations() {
        const response = await fetch('/api/destinations/')
        const data = await response.json()
        const container = document.getElementById('api-destinations-list')

        container.innerHTML = ''

        data.results.forEach(item => {
            let amenitiesHTML = '';
            item.amenities_detail.forEach(amenity => {
                amenitiesHTML += `
                <li>
                    <span>${amenity.name}</span>
                    <span>${amenity.text}</span>
                </li>`
            })

            container.innerHTML += `
            <div class="destinations-section-card">
                <div class="single-destinations">
                    <div class="thumb">
                        <img src="${item.destinations_img}" alt="${item.name}">
                    </div>
                    <div class="details">
                        <h4>${item.name}</h4>
                        <p>${item.location}</p>
                        <ul class="package-list">
                            ${amenitiesHTML}
                            <li>
                                <span>Price per person</span>
                                <a href="#" class="price-btn">$${Math.round(item.price_per_person)}</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>`
        })
    }

    refreshDestinations()
}


