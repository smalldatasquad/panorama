# Panorama

## What this is

These are two Python scripts.

`gmail_1_search_threads.py` searches your Gmail account for 'threads' and saves it to a file. This is very fast.

`gmail_2_expand_threads_to_messages.py` converts the output file from above and looks up each individual message. This is more slow.

## Python setup

1. Python 3 
    1. First, you need Python 3.
    2. (further installations to come here)
2. Install the required libraries with pip.
    1. Type `pip3 install -r requirements.txt`
    
## Gmail API setup

We'll be following [these instructions](GMAIL_API_SETUP.md) **this is important**    

## How to use `gmail_1_search_threads.py`

1. Run the script with `python3 gmail_1_search_threads.py`.

2. Enter in a query. You can use any of the [Gmail search query terms here.](https://developers.google.com/gmail/api/quickstart/python)

3. For example, try `trampoline before:2016/01/01`.

4. The script will output a short summary of all of your messages into one file starting with `threads_from_gmail`.

## How to use `gmail_2_expand_threads_to_messages.py`

1. Make sure you've already run `gmail_1_search_threads.py`. This relies on the output.

2. Run the script with with your filename at the end. For example, for `trampoline before:2016/01/01`, try the command: `python3 gmail_2_expand_threads_to_messages.py threads_from_gmail_search__trampoline-before20160101.json`

3. This will go through each message and expand the from/to/cc/subject of each message. This may take a long time.
