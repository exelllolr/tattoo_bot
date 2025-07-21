const TelegramWebApp = window.Telegram.WebApp;

TelegramWebApp.ready();

async function loadMasters() {
    const response = await fetch('/api/masters');
    const masters = await response.json();
    
    const content = document.getElementById('content');
    content.innerHTML = masters.map(master => `
        <div class="card">
            <img src="${master.avatar_url}" alt="${master.name}" class="w-24 h-24 rounded-full mx-auto">
            <h2 class="text-xl font-bold">${master.name}</h2>
            <p>Стаж: ${master.experience} лет</p>
            <p>${master.description}</p>
            <div class="flex flex-wrap justify-center">
                ${master.portfolio_urls.map(url => `
                    <img src="${url}" alt="Portfolio" class="w-20 h-20 m-1 rounded">
                `).join('')}
            </div>
            <button class="button" onclick="showBooking(${master.id})">Записаться</button>
        </div>
    `).join('');
}

async function showBooking(masterId) {
    const today = new Date();
    const date = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
    const response = await fetch(`/api/slots?master_id=${masterId}&date=${date}`);
    const slots = await response.json();
    
    const content = document.getElementById('content');
    content.innerHTML = `
        <h2 class="text-xl font-bold">Выберите время</h2>
        <div id="time-slots" class="flex flex-wrap justify-center">
            ${slots.map(slot => `
                <div class="time-slot" onclick="bookSlot(${masterId}, '${date}', ${slot})">${slot}:00</div>
            `).join('')}
        </div>
    `;
}

async function bookSlot(masterId, date, time) {
    const response = await fetch('/api/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: TelegramWebApp.initDataUnsafe.user.id,
            master_id: masterId,
            date: date,
            time: time
        })
    });
    const result = await response.json();
    alert(result.message);
    if (result.success) {
        loadMasters();
    }
}

document.addEventListener('DOMContentLoaded', loadMasters);