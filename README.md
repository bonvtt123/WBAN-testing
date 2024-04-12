# Active Learning for WBAN-based Health Monitoring: Prototype Implementation


## Authors: 
Tuan Nguyen, Cho-Chun Chiu, Ting He

## Project Description:

### Overview:
<p align="center">
  <img src="https://github.com/bonvtt123/WBAN-testing/assets/69983102/dce1bc42-4bc3-4d2c-871b-d214170a7e08">
</p>

This project serves as the prototype implementation of *Algorithm 1*, utilizing a smartphone (Google Pixel 6) as the coordinator and a Fitbit device (Versa 2) as the sensing device. We also employ a workstation running PyTorch as the server, which is used for training and testing both the forecasting model and the target model.

This setup ensures a comprehensive evaluation of the algorithm's performance across different hardware environments, enhancing the predictive accuracy and reliability of the proposed method. The integration of these technologies provides a efficient solution for real-time data analysis and data collection.
### Code components:
- Fitbit environment code:

  -  App (index.js): runs on Fitbit, collecting data when receive request from the phone.

  - Companion (index.js): runs on the smartphone, handling data collection and sending request.
    
  - package.json:  manages app information, access permission, and other configurations necessary for the Fitbit app.

- Sever code:

  - scaler.pkl: This file contains the scaler information used for normalizing the data before predictions.

  - prediction model: Pre-trained model file to predict the next 5 minute data (13 dimensions each minute).

  - sever.py: Sever for running the prediction model and implementing proposed sampling algorithm for data collection.
 


### Data Structure:
- List data (prediction and ground truth):
  - Items 1-12: heart rate data collected over 1 minute (5 seconds apart).
  - Item 13: step count.

- Additional data:
  - Timestamp: collected in the form mm/dd/yy H:M:S.

### Implementation: 
Initially, the smartphone collects data over a specified window size (n = 5 minutes). After this period, the phone sends the data to the server. The server then predicts the next 5 minutes of data and runs a sampling algorithm to determine the data collection decisions, which are sent back to the phone.
After that, at the start of each 5-minute prediction window, the server uses the data from the previous window to make predictions (replacing assumptions with actual observed data). The sever then runs sampling algorithm to select sampling epochs (each of 1
minute) in this window and sends the decision to the phone via
WiFi. The phone then sends a sampling request to FitBit at the
beginning of each selected sampling epoch via Bluetooth. When requested, FitBit reports the collected sample at the end of the epoch,
which is then buffered at the phone and sent back to the server
together with other collected samples at the end of the window. 
![image](https://github.com/bonvtt123/testing/assets/69983102/84db02b6-14d8-49cc-af02-237374d9a982)

## Getting started:

**Important: The Smartphone and sever should be on the same wifi network.**

### Running the sever (Python):
1. Replace the path for prediction model and scaler with your path.
2. in the termial type:
`py sever.py`
### Set up Fitbit Environment (JavaScript):
Read about setting up your environment at: https://dev.fitbit.com/getting-started/

**Important:**

- For Fitbit Versa 2 app, use `npx create-fitbit-app myVersa2Project --sdk-version 4.3.0` instead of `npx create-fitbit-app myVersa2Project` to have correct version

- Include the companion file when setting up your envinronment

### Prepare the app:
Replace the content of app and companion file.

In package.json, change access permission to `["access_activity","access_exercise","access_heart_rate", "access_internet", "run_background"]`
###  Installing the app in Phone Fitbit app:
If you're using a Fitbit device, you need to enable the Developer Bridge. On the watch, go to Settings and tap Developer Bridge, then wait until it says Connected to Server.

NOTE: WiFi must be configured on the device.

The simulator or device should now be connected to the developer bridge.

Now type:

`npx fitbit`

This will launch the interactive Fitbit Shell and your command prompt should now display fitbit$.
From the Fitbit Shell, type `bi` to build and install the app.

(Source: [Fitbit Developer](https://dev.fitbit.com/getting-started/))
### Running the app:
The phone will now connect to the sever, and run the prototype.

**Important: Run the sever before running Fitbit environment to avoid data delay.**

## More information:
### Change experienment type:
In sever.py, change `switch=0` if you want to collect all the ground truth data, `switch=1` to only collect the sampling data. 
### More about out research:
Cho-Chun Chiu, Tuan Nguyen, Ting He, Shiqiang Wang, Beom-Su Kim, and Ki-Il
Kim. 2024. [Active Learning for WBAN-based Health Monitoring](https://bpb-us-e1.wpmucdn.com/sites.psu.edu/dist/a/74125/files/2024/04/Active_Learning_WBAN_report-06c5b5f80ce53888.pdf).
### Fitbit Developer API:
[Device API](https://dev.fitbit.com/build/reference/device-api/)

[Companion API](https://dev.fitbit.com/build/reference/companion-api/)

[Intensity](https://dev.fitbit.com/build/reference/web-api/intraday/get-activity-intraday-by-date/)
