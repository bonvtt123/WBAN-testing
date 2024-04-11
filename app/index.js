
import { me } from "appbit";

me.appTimeoutEnabled = false;
import { me as appbit } from "appbit";
import { minuteHistory} from "user-activity";
import * as messaging from "messaging";
import { HeartRateSensor } from "heart-rate";
const index=12;

function heartRateData(){
    
    if (messaging.peerSocket.readyState === messaging.peerSocket.OPEN) {
	if (HeartRateSensor) {
	    const time = new Date();
	    const hrm = new HeartRateSensor({ frequency: 1, batch: 60 });
	    var data;
	    hrm.addEventListener("reading", () => {
	    	var x = [];
	    	for ( let i=0; i< index; i++){
	    		x.push(hrm.readings.heartRate[i*5]);
	    	}
	    	let steps = 0;
    		if (appbit.permissions.granted("access_activity")) {
        		const minuteRecords = minuteHistory.query({ limit: 1 });
        		minuteRecords.forEach((minute, index) => {
            		console.log(`${minute.steps|| 0} steps. ${index} minute(s) ago.`);
            		steps = minute.steps;
            		x.push(steps);
        	});
    		}
                data = {
                  heart: x,
                  timestamp: time.toLocaleString()
               }
               messaging.peerSocket.send(data);
               hrm.stop();
            });
   	    hrm.start();
   	    
	}
    }
    else {
	console.error("Error: Connection is not open");
    }
}

messaging.peerSocket.addEventListener("message", (evt) => {
  	if (evt.data && evt.data.command === "heart") {
  		heartRateData();
  	}
});

messaging.peerSocket.addEventListener("error", (err) => {
  console.error(`Connection error: ${err.code} - ${err.message}`);
});
