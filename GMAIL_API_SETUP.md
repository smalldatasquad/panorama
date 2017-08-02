## GMAIL API SETUP

**Go to https://console.developers.google.com/start/api?id=gmail. We will use this wizard to create or select a project in the Google Developers Console and automatically turn on the API. Click Continue.**

![gmail_api_step_01.png](instruction_imgs/gmail_api_step_01.png)

**Click on the drop-down menu.**

![gmail_api_step_02.png](instruction_imgs/gmail_api_step_02.png)

**Click on a project named 'My Project'.**

![gmail_api_step_03.png](instruction_imgs/gmail_api_step_03.png)

**The drop-down will close. When you can do so, press the 'Go to credentials' button.**

![gmail_api_step_04.png](instruction_imgs/gmail_api_step_04.png)

**On the Add credentials to your project page, click the Cancel button.**

![gmail_api_step_05.png](instruction_imgs/gmail_api_step_05.png)

**Select the Credentials tab, click the Create credentials button**

![gmail_api_step_06.png](instruction_imgs/gmail_api_step_06.png)

**Select OAuth client ID.**

![gmail_api_step_07.png](instruction_imgs/gmail_api_step_07.png)

**At the top of the page, select the OAuth consent screen tab.**

![gmail_api_step_08.png](instruction_imgs/gmail_api_step_08.png)

**Select an Email address, enter a Product name if not already set, and click the Save button.**

![gmail_api_step_09.png](instruction_imgs/gmail_api_step_09.png)

**Select the application type Other, enter the name "Gmail API Quickstart", and click the Create button.**

![gmail_api_step_10.png](instruction_imgs/gmail_api_step_10.png)

**Click OK to dismiss the resulting dialog.**

![gmail_api_step_11.png](instruction_imgs/gmail_api_step_11.png)

**Click the file_download (Download JSON) button to the right of the client ID.**

![gmail_api_step_12.png](instruction_imgs/gmail_api_step_12.png)

This file should start with `client_secret_`. Move this file to the `Panorama` or `Panorama-master` directory (the directory this file is in, that you just downloaded).

**Lastly, execute `python3 gmail_0_setup.py`**

Note:
These instructions are adapted from [here](https://developers.google.com/gmail/api/quickstart/python).
