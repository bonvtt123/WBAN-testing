# Active Learning for WBAN-based Health Monitoring: Prototype


## Authors: 
Tuan Nguyen, Cho-Chun Chiu, Ting He

## Introduction:

### Description:
talk about the project description +components

The project used Google Pixel 6 and Fitbit Versa 2 for running.
![image](https://github.com/bonvtt123/testing/assets/69983102/84db02b6-14d8-49cc-af02-237374d9a982)

### Code components:
- Phone code (Javascript):

  -  App: index.js: the code for running for watches.

  - Companion:index.js:  the code for running for phone.

- Sever code(Python):

  - Scaler.pkl: Scaler information for data prediction

  - Prediction model: Pre-trained model file

  - sever.py sever for running prediction and sampling algorithm

### Data return:

Data item in list 1-12: heart rate data  , 13: step counts




## Getting started:
### Running the sever (Python):
1. Replace the path for prediction model and scaler with your path
2. in the termial type:
`py sever.py`
### Set up Fitbit Environment (JavaScript):
Read about set up your environment at: https://dev.fitbit.com/getting-started/

**Important:**

- For Fitbit Versa 2, use `npx create-fitbit-app myVersa2Project --sdk-version 4.3.0` instead of `npx create-fitbit-app myVersa2Project` to have correct version

- Include the companion file when set up your envinronment

### Prepare the app:
Replace the content of app and companion file, package.json with the new content 
###  Installing the app in Phone Fitbit app:
If you're using a Fitbit device, you need to enable the Developer Bridge. On the watch, go to Settings and tap Developer Bridge, then wait until it says Connected to Server.

NOTE: WiFi must be configured on the device. The first connection attempt can take up to 20 seconds before it's fully established, but subsequent attempts should be instantaneous.

The simulator or device should now be connected to the developer bridge.

Now type:

`npx fitbit`

This will launch the interactive Fitbit Shell and your command prompt should now display fitbit$.

From the Fitbit Shell, type `bi` to build and install the app .
### Running the app:
The phone will now connect to the sever, and run the prototype.
## More information:
### Change experienment type:
In sever change `switch=0` if you want to collect all the grouth truth data, `switch=1` to only collect the sampling data. 
