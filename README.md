# API Stress Testing Tool

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

This Python tool allows you to perform stress testing on APIs by sending multiple concurrent requests and monitoring response times in real-time using dynamic plots. The tool also logs the results of the test in a CSV file for further analysis.
![Python](http://ForTheBadge.com/images/badges/made-with-python.svg)

> [!WARNING]
> This tool is designed for legitimate stress testing and performance analysis of APIs under your control or with proper authorization. Misuse of this tool to target APIs without permission is illegal and may result in severe consequences.

## Features

- Concurrent Requests: Send multiple simultaneous API requests using ThreadPoolExecutor.
- Real-Time Monitoring: Displays real-time graphs for response time and requests per second.
- Customizable Requests: Supports custom request bodies from a JSON file and optional Bearer token for authorization.
- Error Handling & Retries: Automatically retries failed requests a configurable number of times.
- CSV Export: Logs all responses and response times into a CSV file.
- Thread-Safe: Ensures accurate results by protecting shared data with thread locks.

## Prerequisites

````
pip install requests matplotlib
````

## Usage

### 1. Clone the repository:

````
git clone https://github.com/yourusername/api-stress-test.git
cd api-stress-test
````

### 2. Prepare your JSON request body:
Save the request body as a .json file, which will be passed to the tool.

````
python stress_test.py
````

### 3. Input required parameters:
When prompted, input the following:

| Input | Description |
| --- | --- |
| API Endpoint | The API URL you want to stress test. |
| Total Requests | The number of total requests to send. |
| Concurrent Requests | The number of simultaneous requests to make at once. |
| JSON File | The path to the JSON file containing the request body. |
| Bearer Token (Optional) | Authorization token for APIs that require it. |
| Output CSV | The name of the CSV file where the results will be saved.|

### 4. Monitor real-time graphs:

Two plots are displayed during the test:

| Input | Description |
| --- | --- |
| Response Times | Displays response times for each request. |
| Requests per Second | Displays the number of requests completed per second. |

#### Results:

 * Once the test is complete, the results are saved in the specified CSV file. Each row contains:
    * HTTP Status Code
    * Response Body
    * Response Time

### 5. Real-Time Monitoring

The script displays real-time graphs while the stress test is running. You will see:

* **Response Time**: How long each request takes to complete.
* **Requests per Second**: How many requests are processed per second over time.

### 6. Error Handling
The script retries failed requests up to 3 times. If the request fails after the retries, the error is logged in the CSV file.

### 7. Customization
You can customize the script to suit your needs:

Change the number of retries for failed requests by modifying the `max_retries` parameter in the `make_request()` function.
Adjust the graph update interval (default is 1 second) in the `FuncAnimation()` call.


> [!CAUTION]
> You are fully responsible for how you use this tool. Unauthorized testing of APIs or websites, such as DDoS (Distributed Denial of Service) attacks, could cause service disruptions, financial losses, and legal actions against you. Only use this tool on APIs that you have explicit permission to test.The creator(s) and maintainer(s) of this tool are not responsible for any damages, penalties, or legal issues arising from improper or unlawful use of this tool. Always comply with legal and ethical guidelines when conducting stress testing. 
