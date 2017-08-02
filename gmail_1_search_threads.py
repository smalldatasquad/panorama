import panorama

def get_query_user_input(myprofile):
    print(" ===== Type in text to search.")
    print("     = For example: 'from:", myprofile['emailAddress'], "friend'")
    print("     = For example: 'from:", myprofile['emailAddress'], "to:otheremailaddress@email.com'")
    print("     = Queries 'from' you are usually better as they filter out spam.")
    print(" ===== Or to exit, hit control-C. ")
    print(" ")
    inp = input(" ---> ")
    return inp


def queryrun(service):

    querystring = get_query_user_input(myprofile)
    
    print(" === USING QUERY: ", querystring)
    
    print(" === GETTING MESSAGES: ", querystring)

    filename = panorama.query_to_filename(querystring)

    all_results = panorama.get_all_threads(service, querystring)
    filename += "threads"

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


    CLIENT_SECRET_FILE = panorama.autodetect_client_secret_filename()

    if(CLIENT_SECRET_FILE):
        print(" === LOADED SECRET FILE: ", CLIENT_SECRET_FILE)

        print(" === CONNECTING TO GMAIL... ")

        GMAIL = panorama.start_gmail_service(CLIENT_SECRET_FILE)

        print(" === CONNECTED! ")

        myprofile = panorama.get_myprofile(GMAIL)


        while True:
            queryrun(GMAIL)


if __name__ == '__main__':
    main()
