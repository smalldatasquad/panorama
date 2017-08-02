import panorama
import argparse
import sys
import json

class DefaultHelpParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def exit_handler(signal, frame):
    print("")
    print(" *** Exiting! ***")
    sys.exit(0)

def parseargs():
    args = sys.argv
    return args



def queryrun(service):

    
    print(" === USING QUERY: ", querystring)
    
    print(" === GETTING MESSAGES: ", querystring)

    filename = panorama.query_to_filename(querystring)

    all_results = panorama.get_all_threads(service, querystring)
    filename += "threads_"

    # all_messages = panorama.get_all_messages(service, querystring)

    print(" === SAVING TO JSON (filename): ", filename + ".json")
    panorama.jsonsave(filename + ".json", all_results)
    print(" === SAVED!")

    print(" === SAVING TO CSV (filename): ", filename + ".csv")
    panorama.csvsave(filename + ".csv", all_results)
    print(" === SAVED!")
    print(" ")

def main():
    global service
    global myprofile

    args = parseargs()
    inputfilename = args[1]

    CLIENT_SECRET_FILE = panorama.autodetect_client_secret_filename()

    if(CLIENT_SECRET_FILE):
        print(" === LOADED SECRET FILE: ", CLIENT_SECRET_FILE)

        print(" === CONNECTING TO GMAIL... ")

        GMAIL = panorama.start_gmail_service(CLIENT_SECRET_FILE)

        print(" === CONNECTED! ")

        myprofile = panorama.get_myprofile(GMAIL)

        with open(inputfilename) as data:
            all_threads = json.load(data)

            all_results = panorama.threads_to_messages(GMAIL, all_threads)

            filename = inputfilename.split("__threads_")[0] + "__messages"

            print(" === SAVING TO JSON (filename): ", filename + ".json")
            panorama.jsonsave(filename + ".json", all_results)
            print(" === SAVED!")

            print(" === SAVING TO CSV (filename): ", filename + ".csv")
            panorama.csvsave(filename + ".csv", all_results)
            print(" === SAVED!")
            print(" ")


if __name__ == '__main__':
    main()
