const dateInput = document.getElementById('dateInput');
const predictBtn = document.getElementById('predictBtn');
const errorBox = document.getElementById('errorBox');
const resultPanel = document.getElementById('resultPanel');
const resultTitle = document.getElementById('resultTitle');
const visitorsValue = document.getElementById('visitorsValue');
const levelBadge = document.getElementById('levelBadge');
const tempValue = document.getElementById('tempValue');
const rainValue = document.getElementById('rainValue');
const weekendValue = document.getElementById('weekendValue');

function formatDate(dateString) {
  if (!dateString) return '--';
  const date = new Date(`${dateString}T00:00:00`);
  return new Intl.DateTimeFormat('es-PE', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  }).format(date);
}

function setError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove('hidden');
  resultPanel.classList.add('hidden');
}

function clearError() {
  errorBox.textContent = '';
  errorBox.classList.add('hidden');
}

async function fetchPrediction(dateValue) {
  const response = await fetch(`/api/v1/prediction?date=${encodeURIComponent(dateValue)}`);
  const payload = await response.json();

  if (!response.ok) {
    throw new Error(payload.detail || 'No fue posible obtener la predicción.');
  }

  return payload;
}

predictBtn.addEventListener('click', async () => {
  const selectedDate = dateInput.value;

  if (!selectedDate) {
    setError('Debe seleccionar una fecha válida.');
    return;
  }

  clearError();
  predictBtn.disabled = true;
  predictBtn.textContent = 'Procesando...';

  try {
    const result = await fetchPrediction(selectedDate);
    resultTitle.textContent = `Predicción para ${formatDate(result.date)}`;
    visitorsValue.textContent = result.prediction.visitors;
    levelBadge.textContent = result.prediction.level;
    levelBadge.style.background = result.prediction.level === 'Alta'
      ? 'rgba(220, 38, 38, 0.12)'
      : result.prediction.level === 'Media'
        ? 'rgba(234, 179, 8, 0.2)'
        : 'rgba(14, 165, 233, 0.12)';
    levelBadge.style.color = result.prediction.level === 'Alta'
      ? '#b91c1c'
      : result.prediction.level === 'Media'
        ? '#a16207'
        : '#0f766e';

    tempValue.textContent = `${result.weather.temperature} °C`;
    rainValue.textContent = `${result.weather.rain_probability} %`;
    weekendValue.textContent = result.factors.weekend ? 'Sí' : 'No';

    resultPanel.classList.remove('hidden');
  } catch (error) {
    setError(error.message);
  } finally {
    predictBtn.disabled = false;
    predictBtn.textContent = 'PREDECIR';
  }
});

const today = new Date();
const minDate = today.toISOString().split('T')[0];
dateInput.min = minDate;
dateInput.value = minDate;
