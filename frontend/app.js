// Archivo: app.js
// Lógica para enviar requests al backend de Flask mediante Fetch API

document.addEventListener('DOMContentLoaded', () => {
    // Cargar listas iniciales
    fetchOwners();
    fetchPets();

    // Eventos de Submit de formularios
    document.getElementById('owner-form').addEventListener('submit', handleOwnerSubmit);
    document.getElementById('pet-form').addEventListener('submit', handlePetSubmit);
});

// Función de utilidad para mostrar mensajes de éxito/error debajo del formulario
function showMessage(elementId, text, isError=false) {
    const el = document.getElementById(elementId);
    el.textContent = text;
    el.className = 'message ' + (isError ? 'msg-error' : 'msg-success');
    setTimeout(() => { el.textContent = ''; }, 4000); // limpiar a los 4 segs
}

// --- LOGICA DUEÑOS --- //

async function fetchOwners() {
    try {
        const res = await fetch('http://localhost:5000/api/owners');
        const owners = await res.json();
        const container = document.getElementById('owners-list');
        container.innerHTML = '';

        if(owners.length === 0) {
            container.innerHTML = '<p class="item-text">Aún no hay dueños registrados.</p>';
            return;
        }

        owners.forEach(o => {
            const div = document.createElement('div');
            div.className = 'item-card';
            div.innerHTML = `
                <div class="item-title">ID #${o.id} - ${o.name}</div>
                <div class="item-text">Residencia: ${o.residence} | Tel: ${o.phone}</div>
            `;
            container.appendChild(div);
        });
    } catch (e) {
        console.error("Error trayendo dueños", e);
    }
}

async function handleOwnerSubmit(e) {
    e.preventDefault(); // Evita recargar página

    const payload = {
        name: document.getElementById('owner-name').value,
        residence: document.getElementById('owner-residence').value,
        phone: document.getElementById('owner-phone').value,
    };

    try {
        const res = await fetch('http://localhost:5000/api/owners', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
            showMessage('owner-msg', `¡Dueño registrado exitosamente (ID: ${data.id})!`);
            e.target.reset(); // Limpia formulario
            fetchOwners(); // Actualiza lista
        } else {
            showMessage('owner-msg', 'Error: ' + data.error, true);
        }
    } catch (err) {
        showMessage('owner-msg', 'Error de red.', true);
    }
}


// --- LOGICA MASCOTAS --- //

async function fetchPets() {
    try {
        const res = await fetch('http://localhost:5000/api/pets');
        const pets = await res.json();
        const container = document.getElementById('pets-list');
        container.innerHTML = '';

        if(pets.length === 0) {
            container.innerHTML = '<p class="item-text">Aún no hay mascotas registradas.</p>';
            return;
        }

        pets.forEach(p => {
            const div = document.createElement('div');
            div.className = 'item-card pet-item';
            div.innerHTML = `
                <div class="item-title">ID #${p.id} - ${p.breed} (Dueño #${p.owner_id})</div>
                <div class="item-text">Peso: ${p.weight}kg | Color: ${p.color} | Edad: ${p.age} años | Tamaño: ${p.size}</div>
            `;
            container.appendChild(div);
        });
    } catch (e) {
        console.error("Error trayendo mascotas", e);
    }
}

async function handlePetSubmit(e) {
    e.preventDefault(); 

    const payload = {
        owner_id: document.getElementById('pet-owner-id').value,
        breed: document.getElementById('pet-breed').value,
        weight: document.getElementById('pet-weight').value,
        color: document.getElementById('pet-color').value,
        age: document.getElementById('pet-age').value,
        size: document.getElementById('pet-size').value,
    };

    try {
        const res = await fetch('http://localhost:5000/api/pets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();

        if (res.ok) {
            showMessage('pet-msg', `¡Mascota registrada exitosamente (ID: ${data.id})!`);
            e.target.reset();
            fetchPets(); 
        } else {
            showMessage('pet-msg', 'Error: ' + data.error, true);
        }
    } catch (err) {
        showMessage('pet-msg', 'Error de red.', true);
    }
}
