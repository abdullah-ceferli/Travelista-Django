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

document.addEventListener('DOMContentLoaded', function () {
    const tabLinks = document.querySelectorAll('.tab-link')
    const tabPanes = document.querySelectorAll('.tab-pane')

    tabLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault()

            tabLinks.forEach(item => item.classList.remove('active'))
            tabPanes.forEach(pane => {
                pane.classList.remove('show', 'active')
            })

            this.classList.add('active')

            const targetId = this.getAttribute('data-target')
            const targetPane = document.getElementById(targetId)

            if (targetPane) {
                targetPane.classList.add('active')
                setTimeout(() => {
                    targetPane.classList.add('show')
                }, 10)
            }
        })
    })
})


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

function recentBlogCarusel() {
    const slider = document.getElementById('blogSlider')
    const dots = document.querySelectorAll('.recent-blog-dot')
    const cards = document.querySelectorAll('.single-recent-blog-post:not(.clone)')
    let autoPlay

    const getWidth = () => cards[0].offsetWidth + 30

    const scrollToIndex = (i) => {
        slider.scrollTo({ left: getWidth() * i, behavior: 'smooth' })
    }

    const startAuto = () => {
        autoPlay = setInterval(() => {
            let current = Math.round(slider.scrollLeft / getWidth())
            let next = (current + 1) % 4

            if (current >= 3) {
                slider.scrollTo({ left: 0, behavior: 'auto' })
                next = 1;
            }
            scrollToIndex(next)
        }, 10000)
    }

    dots.forEach((dot, i) => {
        dot.addEventListener('click', () => {
            clearInterval(autoPlay)
            scrollToIndex(i)
            setTimeout(startAuto, 3000)
        })
    })

    slider.addEventListener('scroll', () => {
        const activeIdx = Math.round(slider.scrollLeft / getWidth()) % 4
        dots.forEach((d, i) => d.classList.toggle('active', i === activeIdx))
    })

    startAuto()

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


async function loadTestimonials() {
    const slider = document.getElementById('testimonial-slider')
    const dotContainer = document.getElementById('dotContainer')
    if (!slider || !dotContainer) return

    try {
        const response = await fetch('/api/user-contacts/')
        const data = await response.json()
        const items = data.results || data

        if (items.length > 0) {
            let cardsHtml = ''
            items.forEach(item => {
                let starsHtml = ''
                for (let i = 1; i <= 5; i++) {
                    starsHtml += i <= item.stars ? ' ★ ' : ' ☆ '
                }

                cardsHtml += `
                <div class="testimonial-card">
                    <img src="${item.user_img}" class="testimonial-card-img" alt="user">
                    <div>
                        <p class="testimonial-card-text">${item.message}</p>
                        <h4 class="testimonial-card-user-name">${item.name} ${item.surname}</h4>
                        <div class="testimonial-card-stars">${starsHtml}</div>
                    </div>
                </div>`
            })

            slider.innerHTML = cardsHtml;

            let dotsHtml = ''
            items.forEach((_, i) => {
                dotsHtml += `<div class="testimonial-nav-dot ${i === 0 ? 'active' : ''}"></div>`
            })
            dotContainer.innerHTML = dotsHtml

            testimonialCarusel()

        } else {
            slider.innerHTML = '<p>No testimonials available.</p>'
        }
    } catch (error) {
        console.error("Error:", error)
    }
}


function testimonialCarusel() {
    const slider = document.getElementById('testimonial-slider')
    const dotContainer = document.getElementById('dotContainer')
    if (!slider || !dotContainer) return

    const dots = dotContainer.querySelectorAll('.testimonial-nav-dot')
    const cards = slider.querySelectorAll('.testimonial-card')
    if (cards.length === 0) return

    let autoSlideInterval;
    const totalItems = dots.length

    function goToSlide(index) {
        const cardWidth = cards[0].offsetWidth + 20
        slider.scrollTo({ left: cardWidth * index, behavior: 'smooth' })
        resetAutoSlide()
    }

    dots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index))
    })

    slider.addEventListener('scroll', () => {
        const cardWidth = cards[0].offsetWidth + 20
        const activeIndex = Math.round(slider.scrollLeft / cardWidth) % totalItems
        dots.forEach((dot, i) => dot.classList.toggle('active', i === activeIndex))
    })

    function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
            const cardWidth = cards[0].offsetWidth + 20
            let currentIndex = Math.round(slider.scrollLeft / cardWidth)
            let nextIndex = (currentIndex + 1) % totalItems
            goToSlide(nextIndex)
        }, 10000)
    }

    function resetAutoSlide() {
        clearInterval(autoSlideInterval)
        startAutoSlide()
    }

    startAutoSlide()
}