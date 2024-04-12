import * as messaging from "messaging";

// function to send request to the watch
function heartRate() {
    return new Promise((resolve, reject) => {
        if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
            console.log("sending request");
            const messageListener = (evt) => {
                if (evt.data && evt.data.heart) {
                    messaging.peerSocket.removeEventListener("message", messageListener);
                    resolve(evt.data); 
                }
            };
            messaging.peerSocket.addEventListener("message", messageListener);

            // Send the heart rate request
            messaging.peerSocket.send({command: "heart"});
            setTimeout(() => {
                messaging.peerSocket.removeEventListener("message", messageListener);
                reject(new Error("Heart rate data timeout"));
            }, 70000); // timeout set up (only if there is an error)
        } else {
            console.log("unavailable connection");
            reject(new Error("Connection is closed"));
        }
    });
}
const win_size=5
async function fetchIndicatorsAndCollectData() {
    const response = await fetch('http://192.168.1.9:3000/get-indicators');
    const { indicators } = await response.json();
    console.log(`indi: ${indicators}`);
    let heartData = [];
    let timeData = [];
    for (let i = 0; i < win_size; i++) {
        // if indicators =1 then collect data, else wait for next minute
        if (indicators[i] === 1) {
            try {
                // Attempt to collect heart rate data
                const heartRateData = await heartRate();
                heartData.push(heartRateData.heart);
                timeData.push(heartRateData.timestamp);
  		console.log(`The heart rate is: ${heartData} `);
  		console.log(`Time is: ${timeData}`);
            } catch(error) {
                console.error("Error collecting heart rate data:", error.message);
            }
        }
        else{
      	    console.log('waiting');
            await new Promise(resolve => setTimeout(resolve, 60000));
        }
    }

    // After collecting data, send it back to the server
    await fetch('http://192.168.1.9:3000/submit-data', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({hearts: heartData,
            timestamp: timeData})
    })
    .then(response => response.json())
    .then(data => {
       console.log('Response from server:', data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
}
// Initial call to start the process, and then set intervals or recursive calls to continue the process
setInterval(fetchIndicatorsAndCollectData, win_size*60000)
messaging.peerSocket.addEventListener("open", (evt) => {
	fetchIndicatorsAndCollectData();
});
