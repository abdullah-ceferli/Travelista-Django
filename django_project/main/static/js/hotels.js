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

async function loadHotels() {
    const container = document.getElementById('hotel-container')
    if (!container) return

    try {
        const response = await fetch('/api/hotels/')
        const data = await response.json()

        if (data.results && data.results.length > 0) {
            let hotelHtml = ''

            data.results.forEach(item => {
                let starsHtml = '';
                for (let i = 1; i <= 5; i++) {
                    starsHtml += `<span class="fa fa-star ${i <= item.stars ? 'checked' : ''}"></span>`
                }

                let amenitiesHtml = ''
                if (item.amenities_detail) {
                    item.amenities_detail.forEach(am => {
                        amenitiesHtml += `
                        <li>
                            <span>${am.name}</span>
                            <span>${am.is_available ? 'Yes' : 'No'}</span>
                        </li>`
                    })
                }

                hotelHtml += `
                <div class="popular-destinations-section-card">
                    <div class="single-destinations">
                        <div class="thumb">
                            <img src="${item.hotel_img}" alt="${item.name}">
                        </div>
                        <div class="details">
                            <h4>
                                <span>${item.name}</span>
                                <div class="star">${starsHtml}</div>
                            </h4>
                            <p>View on map | ${item.review_count} Reviews</p>
                            <ul class="package-list">
                                ${amenitiesHtml}
                                <li>
                                    <span>Price per night</span>
                                    <a href="#" class="price-btn">$${Math.round(item.price_per_night)}</a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>`
            })

            container.innerHTML = hotelHtml

            console.log(`Successfully loaded ${data.count} hotels.`)

        }
        else {
            container.innerHTML = '<p>No hotels available.</p>'
        }
    }
    catch (error) {
        console.error("Error loading hotels:", error)
        container.innerHTML = '<p>Failed to load hotels.</p>'
    }
}