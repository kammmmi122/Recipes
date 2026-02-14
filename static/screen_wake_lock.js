
// Screen Wake Lock API robust handler
// This script ensures the wake lock is reacquired on visibility changes (e.g., card navigation)

const wakeButton = document.querySelector('[data-status]');
let wakeLock = null;
let wakeLockActive = false;

function updateButton(status) {
  if (!wakeButton) return;
  if (status === 'on') {
    wakeButton.dataset.status = 'on';
    wakeButton.textContent = 'Screen Wake: ON';
  } else {
    wakeButton.dataset.status = 'off';
    wakeButton.textContent = 'Screen Wake: OFF';
  }
}

async function requestWakeLock() {
  if (!('wakeLock' in navigator)) {
    if (wakeButton) wakeButton.disabled = true;
    return;
  }
  try {
    wakeLock = await navigator.wakeLock.request('screen');
    wakeLockActive = true;
    updateButton('on');
    wakeLock.addEventListener('release', () => {
      wakeLockActive = false;
      updateButton('off');
    });
  } catch (err) {
    wakeLockActive = false;
    updateButton('off');
  }
}

async function releaseWakeLock() {
  if (wakeLock && wakeLockActive) {
    try {
      await wakeLock.release();
    } catch (e) {}
    wakeLock = null;
    wakeLockActive = false;
    updateButton('off');
  }
}

if (wakeButton) {
  if (!('wakeLock' in navigator)) {
    wakeButton.disabled = true;
    updateButton('off');
  } else {
    updateButton('off');
    wakeButton.addEventListener('click', async () => {
      if (wakeLockActive) {
        await releaseWakeLock();
      } else {
        await requestWakeLock();
      }
    });
  }
}

// Reacquire wake lock on visibility change (e.g., card navigation)
document.addEventListener('visibilitychange', async () => {
  if (wakeLockActive && document.visibilityState === 'visible') {
    await requestWakeLock();
  }
});
