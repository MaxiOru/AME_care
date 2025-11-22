// State
let currentView = 'home';
let emergencyActive = false;

let medications = [
    { id: 1, name: 'Spinraza', time: '10:00', taken: false },
    { id: 2, name: 'Vitamina D', time: '14:00', taken: true },
    { id: 3, name: 'Evrysdi', time: '20:00', taken: false }
];

let symptoms = {
    breathing: 2,
    fatigue: 1,
    mobility: 2
};

const symptomsData = [
    { name: 'Respiración', key: 'breathing', emoji: '🫁' },
    { name: 'Fatiga', key: 'fatigue', emoji: '😴' },
    { name: 'Movilidad', key: 'mobility', emoji: '🦿' }
];

const moodEmojis = ['😊', '🙂', '😐', '😟', '😰'];

// Initialization
document.addEventListener('DOMContentLoaded', () => {
    if (window.lucide) lucide.createIcons();
    renderMedications();
    renderSymptoms();
    
    console.log(">>> AME APP LISTA Y ESPERANDO COMANDOS...");
});

// Navigation
function switchView(viewId) {
    currentView = viewId;

    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    const view = document.getElementById(`${viewId}-view`);
    if (view) view.classList.add('active');

    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    
    // Selección robusta del botón
    const navBtns = document.querySelectorAll('.nav-item');
    navBtns.forEach(btn => {
        if(btn.getAttribute('onclick').includes(viewId)) {
            btn.classList.add('active');
        }
    });
}

// Emergency Logic
function handleEmergency(type) {
    console.log(">>> EJECUTANDO PROTOCOLO DE EMERGENCIA:", type);
    
    const modal = document.getElementById('emergency-modal');
    if (modal) {
        modal.classList.remove('hidden');
        
        // Sonido de alerta (Opcional pero recomendado)
        // const audio = new Audio('https://assets.mixkit.co/sfx/preview/mixkit-alarm-digital-clock-beep-989.mp3');
        // audio.play().catch(e => console.log("Audio bloqueado por navegador"));

        // Auto hide after 3 seconds
        setTimeout(() => {
            modal.classList.add('hidden');
        }, 5000); // Le damos 5 segundos para que se vea bien
    } else {
        console.error("ERROR: No encuentro el modal 'emergency-modal'");
    }
}

// Medication Logic
function renderMedications() {
    const container = document.getElementById('medication-list');
    if (!container) return;
    
    container.innerHTML = '';

    medications.forEach(med => {
        const div = document.createElement('div');
        div.className = `medication-item ${med.taken ? 'taken' : ''}`;
        
        div.innerHTML = `
            <div class="med-info">
                <i data-lucide="pill" class="${med.taken ? 'text-green' : 'text-blue'}"></i>
                <div>
                    <h3>${med.name}</h3>
                    <p class="text-gray">Hora: ${med.time}</p>
                </div>
            </div>
            ${med.taken 
                ? '<div class="badge-taken">✓ Tomado</div>' 
                : `<button class="btn-take" onclick="toggleMedication(${med.id})">Marcar</button>`
            }
        `;
        container.appendChild(div);
    });
    if (window.lucide) lucide.createIcons();
}

function toggleMedication(id) {
    medications = medications.map(med => 
        med.id === id ? {...med, taken: true} : med
    );
    renderMedications();
}

// Symptoms Logic
function renderSymptoms() {
    const container = document.getElementById('symptoms-list');
    if (!container) return;
    
    container.innerHTML = '';

    symptomsData.forEach(symptom => {
        const div = document.createElement('div');
        div.className = 'symptom-row';
        
        const currentVal = symptoms[symptom.key];
        const currentEmoji = moodEmojis[currentVal];

        let buttonsHtml = '';
        moodEmojis.forEach((emoji, index) => {
            const isSelected = currentVal === index;
            buttonsHtml += `
                <button 
                    class="mood-btn ${isSelected ? 'selected' : ''}" 
                    onclick="setSymptom('${symptom.key}', ${index})"
                >
                    ${emoji}
                </button>
            `;
        });

        div.innerHTML = `
            <div class="symptom-header">
                <div style="display:flex; gap:0.5rem; align-items:center;">
                    <span style="font-size:1.5rem;">${symptom.emoji}</span>
                    <span style="font-weight:600;">${symptom.name}</span>
                </div>
                <span style="font-size:1.5rem;">${currentEmoji}</span>
            </div>
            <div class="mood-selector">
                ${buttonsHtml}
            </div>
        `;
        container.appendChild(div);
    });
}

function setSymptom(key, value) {
    symptoms[key] = value;
    renderSymptoms();
}

// --- PUENTE DE CONEXIÓN (TECLADO) ---
// Este es el secreto para que Python funcione
document.addEventListener('keydown', function(event) {
    console.log(">>> TECLA RECIBIDA:", event.key);

    // Normalizamos a minúscula para evitar problemas de Mayús
    const key = event.key.toLowerCase();

    // EMERGENCIA (Tecla E)
    if (key === 'e') {
        console.log("🚨 ¡SEÑAL DE EMERGENCIA DETECTADA!");
        handleEmergency('general');
    }
    
    // SCROLL ABAJO (Tecla S)
    if (key === 's') {
        console.log("⏬ SCROLL DOWN");
        window.scrollBy({ top: 200, behavior: 'smooth' });
    }
    
    // SCROLL ARRIBA (Tecla W)
    if (key === 'w') {
        console.log("⏫ SCROLL UP");
        window.scrollBy({ top: -200, behavior: 'smooth' });
    }
});