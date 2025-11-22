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
    lucide.createIcons();
    renderMedications();
    renderSymptoms();
});

// Navigation
function switchView(viewId) {
    // Update state
    currentView = viewId;

    // Update UI - Views
    document.querySelectorAll('.view').forEach(el => el.classList.remove('active'));
    document.getElementById(`${viewId}-view`).classList.add('active');

    // Update UI - Nav Buttons
    document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
    // Find the button that calls this function with this viewId
    const navBtns = document.querySelectorAll('.nav-item');
    // Simple mapping based on index or onclick attribute
    // Let's just re-select based on the onclick attribute for simplicity
    const activeBtn = Array.from(navBtns).find(btn => btn.getAttribute('onclick').includes(viewId));
    if (activeBtn) activeBtn.classList.add('active');
}

// Emergency Logic
function handleEmergency(type) {
    const modal = document.getElementById('emergency-modal');
    modal.classList.remove('hidden');
    
    // Auto hide after 3 seconds
    setTimeout(() => {
        modal.classList.add('hidden');
    }, 3000);
}

// Medication Logic
function renderMedications() {
    const container = document.getElementById('medication-list');
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
    lucide.createIcons();
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
