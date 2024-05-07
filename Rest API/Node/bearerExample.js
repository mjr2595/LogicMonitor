// Import required libraries
import axios from "axios";
import dotenv from "dotenv";

dotenv.config();

// Account Info
const portal = process.env.PORTAL;
const bearer = process.env.BEARER;

// Request Info: Get all devices
const httpVerb = "GET";
const resourcePath = "/device/devices";

// Dynamic queryParams
const size = 1;
const offset = 0;
const queryParams = `?fields=id,displayName&size=${size}&offset=${offset}`;

// Construct URL
const url = `https://${portal}.logicmonitor.com/santaba/rest${resourcePath}${queryParams}`;

// Construct headers
const headers = {
  "Content-Type": "application/json",
  "X-version": "3",
  Authorization: `Bearer ${bearer}`,
};

// Function to make the HTTP request
async function fetchDevices() {
  try {
    const response = await axios.get(url, { headers: headers, timeout: 15000 });
    console.log(response.data);
  } catch (error) {
    console.error("Error making HTTP request:", error);
  }
}

// Call the function
fetchDevices();
