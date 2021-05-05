import os
import shutil
from pathlib import Path
import pickle

#The below section is to pickle/serialize the data using pickle format
#So that we can alter the file_structure dict whenever needed and save it
#Post that we can reterive the data using pickle_load function and use it

#This function is used to reset file_structure dict to default condition
def reset_to_default():
    file_structure = {
    'Documents': ['.txt', '.doc', '.pdf', '.docx'],
    'Pictures': ['.jpg', '.jpeg', '.png', '.svg'],
    'Videos': ['.mp4', '.avi', '.mvk', '.mov', '.webm', '.gif', '.gifv', '.wmv', '.yuv', '.viv', '.amv'],
    'Music': ['.mp3', '.wav', '.raw', '.3gp']
    }
    #reset dictionary is saved in file_formats file as bytes using pickle module
    pickle_out = open('file_formats','wb')
    pickle.dump(file_structure, pickle_out)
    pickle_out.close()

    #Reset file_structure is returned to developer_mode function
    return file_structure


def developer_mode(file_structure):
    print("************************************************")
    print("When more power comes...more responsibility comes!!!\n")
    print("List of file types the application will organize")
    for key in file_structure:
        print(key)
        print(file_structure[key])
    print("***File types other than these will be organized under Others***")

    #User has to choose the required option to execute that operation
    print("Choose one from below options:\n1) Add new extension inside existing file types\n"
          "2) Add new file type\n"
          "3) Reset to default condition\n"
          "4) Everything fine...exit out of developer mode")
    dev_option = input()

    #Checking for the option 1
    if int(dev_option) == 1:
        print("Enter the file type: (Case Sensitive)")
        file_type = input()
        if file_type in file_structure:
            print("Enter all the new extensions to be added: \n"
                  "(Please enter in lower case & start with '.' eg: .txt\n"
                  "enter each extension seperated by space)")
            ext = input()

            #extensions provided by the user is appended to respective key of the dict (file_structure)
            for e in ext.split():
                file_structure[file_type].append(e)
            print(file_structure[file_type])

            #Once it is done the changes are being saved
            pickle_out = open('file_formats', 'wb')
            pickle.dump(file_structure, pickle_out)
            pickle_out.close()
            print("Changes have been saved to memory")
            print("Exiting out of Dev mode!!!")
        else:
            print("File type doesn't exist!!!")
            print("Exiting out of Dev mode!!!")

    #Checking for option 2
    elif int(dev_option) == 2:
        print("Enter the file type name to be created: ")
        keyname = input()

        #The new filetype is created as a key element in dict(file_structure)
        file_structure[keyname] = []
        print("Enter all the new extensions to be added inside this new file type: \n"
              "(Please enter in lower case & start with '.' eg: .txt\n"
              "enter each extension seperated by space)")
        ext = input()
        for e in ext.split():
            file_structure[keyname].append(e)
        print("Please find the new file type created:\n",keyname,"\n",file_structure[keyname])

        #Changes are being saved
        pickle_out = open('file_formats', 'wb')
        pickle.dump(file_structure, pickle_out)
        pickle_out.close()
        print("Changes have been saved to memory")
        print("Exiting out of Dev mode!!!")

    elif int(dev_option) == 3:

        #Getting confirmation from the user inorder to reset the dictionary
        print("Please confirm once again to proceed with reset: (y/n)")
        confirm = input()
        if confirm.lower() == 'y':
            file_structure = reset_to_default()
            print(f"File Structure reset to default condition")
            for key in file_structure:
                print(key,"\n",file_structure[key])
        else:
            print("Current Condition:\n")
            for key in file_structure:
                print(key,"\n",file_structure[key])
        print("\nExiting out of Dev mode!!!")
    else:
        print("Lost your powers!!!")
    print("******************************************\n")
    #Returning the file_structure dict to the main function
    return file_structure

if __name__ == '__main__':

    #Reading the dictionary from file_formats file which contains data in bytes
    pickle_in = open('file_formats', 'rb')
    file_structure = pickle.load(pickle_in)
    pickle_in.close()
    #The data read is being stored to the local dictionary 'file_structure'

    #Option to enter into dev mode, to commit any changes
    print("Press 404 & ENTER to get into developer mode:\n(If not press 'n' & ENTER)")
    dev = input()
    if dev == '404':
        file_structure = developer_mode(file_structure)

    #File Organizing part starts, by default it picks system downloads path
    downloads_path = str(Path.home() /"Downloads")
    print(f"Files in '{downloads_path}' are going to be organized\n")
    path_change = 1
    while path_change:
        #Asking for path change
        print("Do you want to change the path ? y/n")
        path_change_option = input()
        if path_change_option.lower() == 'y':
            print("Please enter the path:")
            downloads_path = input()
        else:
            path_change = 0
        #Checking for path existance
        if not os.path.exists(downloads_path):
            print("Path doesn't exist. Please verify once!!!\n")
            print(downloads_path)
        else:
            path_change = 0
            print(f"Files in '{downloads_path}' are going to be organized\n")
    #Changing the working directory to required path
    os.chdir(downloads_path)
    print(f"List of files and folders in current working directory: {os.listdir('.')}")
    print(f"Total files and folder present {len(os.listdir('.'))}")
    Other_type = "Others"
    print("Want to start organizing ? y/n")
    option = input()
    option.lower()
    f1 = 1
    while f1:
        files = [f for f in os.listdir(".") if os.path.isfile(f)]
        if option == 'y':
            for f in files:
                folders = os.listdir()
                print(folders)
                filename,fileext = os.path.splitext(f)
                fileext.lower()
                for key in file_structure:
                    others = 1
                    if fileext in file_structure[key]:
                        if key in folders:
                            destination_path = os.path.join(os.getcwd(), key)
                            shutil.move(f, destination_path)
                            others = 0
                            break
                        else:
                            os.mkdir(key)
                            destination_path = os.path.join(os.getcwd(), key)
                            shutil.move(f, destination_path)
                            others = 0
                            break
                if others == 1:
                    if Other_type in folders:
                        destination_path = os.path.join(os.getcwd(), Other_type)
                        shutil.move(f, destination_path)
                    else:
                        os.mkdir(Other_type)
                        destination_path = os.path.join(os.getcwd(), Other_type)
                        shutil.move(f, destination_path)
        else:
            f1 = 0
        if option == 'y':
            print("Files has been organized!!!")
            print("Do you want to organize again? y/n")
            option2 = input().lower()
            if option2 == 'n':
                option = 'n'
                f1 = 0
    print(os.listdir("."))