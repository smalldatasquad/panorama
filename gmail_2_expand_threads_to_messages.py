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

            filename = "messages_" + inputfilename.split("threads_")[1]

            print(filename)

            all_results = panorama.threads_to_messages(GMAIL, all_threads)


            print(" === SAVING TO JSON (filename): ", filename + ".json")
            panorama.jsonsave(filename + ".json", all_results)
            print(" === SAVED!")

            print(" === SAVING TO CSV (filename): ", filename + ".csv")
            panorama.csvsave(filename + ".csv", all_results)
            print(" === SAVED!")
            print(" ")


if __name__ == '__main__':
    main()
