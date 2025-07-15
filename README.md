# AutoApply Chrome Extension

This repository contains a simple Chrome extension that demonstrates how to auto-fill job application forms and optionally submit them automatically.

**Disclaimer:** Many job boards prohibit automated applications. Use this extension only on sites where automation is permitted and always comply with the website's terms of service.

## Installation
1. Open `chrome://extensions` in Google Chrome.
2. Enable **Developer mode**.
3. Click **Load unpacked** and select the `extension` folder from this repository.

## Usage
1. Navigate to a job application form.
2. Click the **AutoApply** extension icon.
3. Choose **Fill Form** to populate known fields with data from `content.js`.
4. Choose **Auto Apply** to fill the form and attempt to submit it automatically.

This example stores static data in `content.js`. In a real extension, you would collect user data and store it via `chrome.storage` or a secure backend.
