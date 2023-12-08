// Server Side Events
// const eventSource = new EventSource("/events");
// eventSource.onmessage = (event) => {
//   console.log(event.data);
// };

// Send gamepad commands to drone every INTERVAL_MSECS
const INTERVAL_MSECS = 200
setInterval(sendDroneCommandFromGamepadState, INTERVAL_MSECS);

/* 
  Drone commands conform to:
  https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf
*/
function sendDroneCommandFromGamepadState() {
  const controller = navigator.getGamepads ? navigator.getGamepads()[0] : false;

  if (controller) {
    let command = "";

    if (controller.buttons[3].pressed) command = "takeoff"; // X
    else if (controller.buttons[0].pressed) command = "land"; // B
    else if (controller.buttons[1].pressed) command = "streamon"; // A
    else if (controller.buttons[2].pressed) command = "streamoff"; // Y
    else if (controller.buttons[6].pressed) command = "flip l"; // ZL
    else if (controller.buttons[7].pressed) command = "flip r"; // ZR
    else { // Just send an rc command wth the axes data
      const MAX = 60, DECIMALS = 4;
      const a = (controller.axes[0]*MAX).toFixed(DECIMALS);
      const b = (-controller.axes[1]*MAX).toFixed(DECIMALS);
      const d = (controller.axes[2]*MAX).toFixed(DECIMALS);
      const c = (-controller.axes[3]*MAX).toFixed(DECIMALS);
      command = `rc ${a} ${b} ${c} ${d}`;
      //if (rc != "rc 0.0000 0.0000 0.0000 0.0000") command = rc;
    }

    if (command) {
      sendDroneCommand(command);
    }
    
  }
}

/**
 * Sends a drone command to the web server
 */
function sendDroneCommand(command) {
  // console.log("Sending drone command: ", command);
  fetch(`/drone?command=${command}`);
}
