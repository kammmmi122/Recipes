console.clear();

function button_click(){
  if (wakeLockButton.checked == 1){
    requestWakeLock()
  } else {
    wakeLock.release()
        .then(() => {
          wakeLock = null;
        })
  }
}

// create an async function to request a wake lock
const requestWakeLock = async () => {
  try {
    wakeLock = await navigator.wakeLock.request('screen');

    // change up our interface to reflect wake lock active
    changeUI();

    // listen for our release event
    wakeLock.onrelease = function(ev) {
      console.log(ev);
    }
    wakeLock.addEventListener('release', () => {
      // if wake lock is released alter the button accordingly
      changeUI('released');
    });

  } catch (err) {
    // if wake lock request fails - usually system related, such as battery
    wakeButton.dataset.status = 'off';
    wakeButton.textContent = 'Wake Lock OFF';

  }
} // requestWakeLock()
