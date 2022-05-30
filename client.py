import xmlrpc.client
import re
import os

# connects to the database via xmlrpc
while True:
    try:
        host = input("Please input host address: ")
        s = xmlrpc.client.ServerProxy('http://'+host+':8000')
        print(s.Connect())
        break
    except:
        print("Connection failed!, Please try again")

# welcome messages
print("Welcome to the Honours student self evaluation service!")
print(" ")

# system is in a loop so that it doesnt end
while True:
    student = input("Are you currently a student? Y/N: ")

    # if the student has a account with the uni
    if student.upper() == "Y":
        # used the clear the commandline
        os.system('CLS')

        # inputs to use for functions
        username = input("Please enter username: ")
        password = input("Please enter password: ")

        # checks if the user is in the database through remote calls
        if s.Authenticate(username, password):
            while True:
                # menu displays
                os.system('CLS')

                print("Selections: ")
                print(" ")
                print("1. Display individual unit scores")
                print("2. Calculate course average")
                print("3. Display average of the best 8 marks")
                print("4. Check if qualify for Honours")
                print("5. Log out")
                print(" ")

                choice = input("Select: ")

                # passes the menu choice onto the server
                if choice == '1' or choice == '2' or choice == '3' or choice == '4':
                    print(s.MenuOptions(choice))
                    input("Press enter to continue.")
                    os.system('CLS')
                    continue

                # ends the session and resets the program
                elif choice == '5':
                    s.LogOut()
                    os.system('CLS')
                    break

                else:
                    print("Invalid selection")

        else:
            # message for when the username or password is incorrect
            print("Username or Password incorrect")
            continue

    # when the student does not have a account with the uni
    elif student.upper() == "N":
        os.system('CLS')

        # results will be stored in dictionary format
        results = {}
        results['f_name'] = input("Please enter your name: ")
        units = 0

        # loop will to till the user decides to end it.
        while True:
            os.system('CLS')

            # tracker so that the user knows if they have entered the right amount of units
            print("You currently have: " + str(units) + '/12-30')

            code = input("Please enter a unit code (-1 to stop): ")
            pattern = re.compile("[A-Z]{3}\d{4}")
            # code uses regex to validate that the unit code is in the right format
            while re.fullmatch(pattern, code) == None:
                # code also checks if the user would like to stop adding units
                if code == "-1":
                    break
                print("Invalid unit code.")
                code = input("Please enter a unit code (-1 to stop): ")

            if code == "-1":
                os.system('CLS')
                for key in results: #all None results must be removed for rpc message passing
                    if key !='f_name':
                        try:
                            results[key].remove(None)
                            results[key].remove(None)
                        except ValueError:
                            continue
                print(s.Evaluate(results))
                s.LogOut()
                break

            # code to check that the unit code has not been used before
            if code in results:
                print("Scores for this unit have already been submitted")
                continue
            else:
                units += 1
            scores = [None, None, None]
            newScore = 0
            count = 1

            # input validation for uni marks.
            # users can have 3 attempts with 2 failing and 1 passing grade
            while True:
                try:
                    while int(newScore) < 50:
                        os.system('CLS')
                        print("Attempt", count)
                        newScore = float(input("Please enter a unit mark for " + code + ": "))

                        # code to chekc that the input is not > 100 and < 0
                        while int(newScore) > 100 or int(newScore) < 0:
                            print("Score must be between 0 and 100")
                            newScore = float(input("Please enter a unit mark for " + code + ": "))

                        # code to check that the user passes on the last attempt
                        while count == 3 and newScore < 50:
                            print("No more than 3 fails allowed, please enter new grade for 3rd attempt")
                            print("Attempt", count)
                            newScore = float(input("Please enter a unit mark for " + code + ": "))

                            # code to chekc that the input is not > 100 and < 0
                            while int(newScore) > 100 or int(newScore) < 0:
                                print("Score cannot be over 100")
                                newScore = float(input("Please enter a unit mark for " + code + ": "))
                        scores[count-1] = newScore
                        count += 1
                    results[code] = scores
                    break
                except:
                    print("This is not a valid input!")


    else:
        print("Invalid input")
