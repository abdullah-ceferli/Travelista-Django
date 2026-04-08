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

let activeThreadId = null
let chatInterval = null
let lastMessageCount = 0

const currentUserId = "{{ request.session.user_id }}"

if (Notification.permission !== "granted" && Notification.permission !== "denied") {
    Notification.requestPermission()
}

document.getElementById('user-search')?.addEventListener('input', function(e) {
    const term = e.target.value.toLowerCase()
    const users = document.querySelectorAll('.user-item')
    
    users.forEach(user => {
        const name = user.querySelector('strong').innerText.toLowerCase()
        user.style.display = name.includes(term) ? 'flex' : 'none'
    });
});

async function openPrivateChat(userId, displayName) {
    document.getElementById('chat-header').innerText = displayName
    
    document.querySelectorAll('.user-item').forEach(i => i.classList.remove('active'))
    document.getElementById('user-' + userId)?.classList.add('active')

    try {
        const res = await fetch(`/api/get-or-create-thread/${userId}/`)
        const data = await res.json()

        if (!res.ok) {
            alert("Error: " + data.error)
            return
        }

        activeThreadId = data.thread_id
        lastMessageCount = 0
        
        await loadMessages()

        if (chatInterval) clearInterval(chatInterval)
        chatInterval = setInterval(loadMessages, 2500)

    } catch (e) {
        console.error("Connection error:", e)
    }
}

async function loadMessages() {
    if (!activeThreadId) return

    try {
        const res = await fetch(`/api/messages/${activeThreadId}/`)
        const messages = await res.json()
        const display = document.getElementById('messages-display')
        
        const wasAtBottom = display.scrollHeight - display.scrollTop <= display.clientHeight + 100

        if (messages.length > lastMessageCount && lastMessageCount !== 0) {
            const lastMsg = messages[messages.length - 1];
            if (String(lastMsg.user_id) !== String(currentUserId)) {
                showNotification(lastMsg.username, lastMsg.message)
            }
        }
        lastMessageCount = messages.length

        display.innerHTML = ''
        messages.forEach(m => {
            const isMe = String(m.user_id) === String(currentUserId)
            const type = isMe ? 'sent' : 'received'
            
            const div = document.createElement('div')
            div.className = `bubble ${type}`

            const nameEl = document.createElement('small')
            nameEl.className = 'message-username'
            nameEl.style.fontWeight = 'bold'
            nameEl.style.display = 'block'
            nameEl.style.marginBottom = '2px'
            nameEl.style.fontSize = '10px'
            nameEl.style.color = isMe ? '#2e7d32' : '#555'
            nameEl.innerText = isMe ? 'You' : m.username

            const textEl = document.createElement('span')
            textEl.innerText = m.message

            div.appendChild(nameEl)
            div.appendChild(textEl)
            display.appendChild(div)
        })

        if (wasAtBottom) {
            display.scrollTop = display.scrollHeight
        }
    } 
    catch (e) {
        console.error("Fetch error:", e)
    }
}

document.getElementById('send-btn').onclick = async function() {
    const input = document.getElementById('message-input')
    const messageText = input.value.trim()

    if (!messageText || !activeThreadId) return

    if (messageText.includes('@')) {
        console.log("Mentioning someone...")
    }

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

    try {
        const response = await fetch('/api/messages/send/', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json', 
                'X-CSRFToken': csrftoken 
            },
            body: JSON.stringify({ 
                thread_id: activeThreadId, 
                message: messageText 
            })
        })

        if (response.ok) {
            input.value = '';
            await loadMessages();
            const display = document.getElementById('messages-display')
            display.scrollTop = display.scrollHeight
        }
    } 
    catch (e) {
        console.error("Send error:", e)
    }
}

function showNotification(sender, text) {
    if (Notification.permission === "granted" && document.visibilityState !== "visible") {
        new Notification(`Message from ${sender}`, {
            body: text,
            icon: 'https://ui-avatars.com/api/?name=' + sender
        })
    }
}

document.getElementById('message-input').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') document.getElementById('send-btn').click()
})

