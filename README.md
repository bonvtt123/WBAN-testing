# Active Learning for WBAN-based Health Monitoring: Prototype


## Authors: 
Tuan Nguyen, Cho-Chun Chiu, Ting He

## Project Description:

### Overview:


### Code components:
- Fitbit environment code:

  -  App (index.js): designs for Fitbit, collecting data when recieve request from the phone.

  - Companion (index.js): runs on the smartphone, handling data collection and sending request.
    
  - package.json: 

- Sever code:

  - scaler.pkl: This file contains the scaler information used for normalizing the data before predictions.

  - prediction model: Pre-trained model file to predict the next 5 minute data (13 dimensions each).

  - sever.py: sever for running the prediction model and implementing proposed sampling algorithm for data collection.
 


### Data Structure:
List data (prediction and ground truth):
- Items 1-12: Represent heart rate data collected over various intervals.
- Item 13: Represents the step count.

Additional data:
- Timestamp: collected in the form mm/dd/yy H:M:S

### Implementation: 

At the beginning of every prediction window of 5 minutes (𝑛 = 5),
the server predicts the next 5 data, runs sampling algorithm to select sampling epochs (each of 1
minute) in this window and sends the decision to the phone via
WiFi. The phone then sends a sampling request to FitBit at the
beginning of each selected sampling epoch via Bluetooth. When requested, FitBit reports the collected sample at the end of the epoch,
which is then buffered at the phone and sent back to the server
together with other collected samples at the end of the window. 
![image](https://github.com/bonvtt123/testing/assets/69983102/84db02b6-14d8-49cc-af02-237374d9a982)

## Getting started:

**Important: Phone and sever should be on the same wifi network**
### Running the sever (Python):
1. Replace the path for prediction model and scaler with your path
2. in the termial type:
`py sever.py`
### Set up Fitbit Environment (JavaScript):
Read about setting up your environment at: https://dev.fitbit.com/getting-started/

**Important:**

- For Fitbit Versa 2, use `npx create-fitbit-app myVersa2Project --sdk-version 4.3.0` instead of `npx create-fitbit-app myVersa2Project` to have correct version

- Include the companion file when set up your envinronment

### Prepare the app:
Replace the content of app and companion file, package.json with the new content 
###  Installing the app in Phone Fitbit app:
If you're using a Fitbit device, you need to enable the Developer Bridge. On the watch, go to Settings and tap Developer Bridge, then wait until it says Connected to Server.

NOTE: WiFi must be configured on the device.

The simulator or device should now be connected to the developer bridge.

Now type:

`npx fitbit`

This will launch the interactive Fitbit Shell and your command prompt should now display fitbit$.
From the Fitbit Shell, type `bi` to build and install the app .

(SourceL: [Fitbit Developer](https://dev.fitbit.com/getting-started/)
### Running the app:
The phone will now connect to the sever, and run the prototype.
## More information:
### Change experienment type:
In sever change `switch=0` if you want to collect all the grouth truth data, `switch=1` to only collect the sampling data. 
### More about out research:
Cho-Chun Chiu, Tuan Nguyen, Ting He, Shiqiang Wang, Beom-Su Kim, and Ki-Il
Kim. 2024. [Active Learning for WBAN-based Health Monitoring](https://sites.psu).
### Fitbit Developer API:
[Device API](https://dev.fitbit.com/build/reference/device-api/)

[Companion API](https://dev.fitbit.com/build/reference/companion-api/)

[Intensity](https://dev.fitbit.com/build/reference/web-api/intraday/get-activity-intraday-by-date/)
