import sys
import re
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog

"""
TO USE, CREATE NEW TEXT FILE, DO CTRL+SHIFT+P AND TYPE IN 'EXTRACT TEXT FROM PDF', THEN SELECT BANK STATEMENT PDF FILE
"""

def write_final_list(final_list: list) -> None:
    """
    This function is used to take the final list and put it towards the writing list function
    """
    enter_file_name = "Select the Final File to Output (Or cancel to create a default file)"
    write_file(final_list, enter_file_name)


def write_to_categories_txt(categories_to_add: list, categories_csv_list: list) -> None:
    """
    This Function has 4 Stages:
    1. Grabbing category list used in previous function & instantiating the a just category list
    2. Retreiving each category from the full list into its own list
    3. Retreiving each transaction place to add and the corresponding category and matching it to see if it is present. 
    Either way it is added into the list either into the first slot of the matching category, or into its own new category.
    4. Writing the list over top of the categories.txt file
    """

    # Inst all categories into a list, to ensure checking is smooth
    just_categories = []
    
    # Retrieving each line in the list
    for indx, line in enumerate(categories_csv_list):

        # Capturing all categories and putting them into one list
        just_categories.append(categories_csv_list[indx][len(line)-1])


    # Retrieving each line in list of cats to add
    for line_to_add in categories_to_add:

        # Retrieving each item in list of cats to add
        #for item_to_add in line_to_add:
            
        # Checking if the category retreived matches any category in the cat list
        if line_to_add[1] in just_categories:

            # Retreiving the index where they match
            indx_of_category = just_categories.index(line_to_add[1])

            # Inserting transaction place into the first column of the matching category
            categories_csv_list[indx_of_category].insert(0, line_to_add[0])

        # If there is no category matching 
        else: 
            # Adds new category to ongoing category list
            just_categories.append(line_to_add[1])

            # Adds new items to ongoing transaction place and category list
            categories_csv_list.append([line_to_add[0], line_to_add[1]])

    #TEST
    for i in categories_csv_list:
        print(i)

    write_file(categories_csv_list, "Enter the file to write over csv database")


def write_file(contents_to_write: list, enter_file_name: str) -> None:
    
    # Opens a file explorer so the user may choose the file to upload 
    file_path = filedialog.askopenfilename(title=enter_file_name,
    filetypes=[("Comma-Separated Values files", "*.csv"), ("All Files", "*.*")])

    # Checks if user cancelled, will then create a new file
    if not file_path:

        # Creating new file
        default_file_name = "new_file.csv"

        # Asking for where they want the file to be saved
        file_path = filedialog.askdirectory(title="Enter where the file will be saved")

        # Putting the users desired path and the name together
        file_path += "/"
        file_path += default_file_name
    
    #Opening file to write over
    file_open = open(file_path, "w")

    # Writing out full new category database
    for indx, line in enumerate(contents_to_write):
    # Write only the items in the line joined by commas
        file_open.write(','.join([str(item) for item in line]))
    
        # Add a newline unless it's the last line
        if indx != (len(contents_to_write) - 1):
            file_open.write('\n')

def category_list(cleaned_list: list) -> list:
    """
    This category's function is to take the list and determine of every transaction is in the database, if it isnt
    it calls the user_input function to grab the transaction name and category
    """
    # Inst final list
    list_w_cats = []

    # Inst list of categories and places to add into txt file
    categories_to_write = []

    # Retrieve category database file
    categories_txt_list = read_file("Enter the Category Database ", "Database")
    
    categories_txt_list = clean_database_list(categories_txt_list)
    

    # Retreieve the index of the cleaned_list
    for i in range(len(cleaned_list)):

        # Retreive the transaction place from the current line
        transaction_place = cleaned_list[i][1]

        # Inst/reset checker for which category the trans place belongs to
        category_to_append = ""

        # Inst/reset transaction from the line with the corresponding category
        transaction_to_append = ""

        # Retreive line from txt file
        for line in categories_txt_list:
            
            # Retreive item from txt file
            for item in line:
                
                # If the transaction place is present in the line
                if item in transaction_place:

                    # Makes category_to_append the last item in the list, which is the category
                    category_to_append = line[len(line) - 1]
                    
                    # Making the transaction looked cleaned up
                    transaction_to_append = item
                    break

        # If category_to_append has something in it, it means the transaction has a corresponding category
        if category_to_append:
            
            # Adds all of the items from the cleaned_list to the new list, with the category at the end
            list_w_cats.append([cleaned_list[i][0], transaction_to_append, category_to_append, cleaned_list[i][2]])

        else:

            user_answer = user_input(cleaned_list[i][1], categories_txt_list)
            if user_answer[0]:
                # Adds the transaction place and new category from user into a list to later be given to the writing function
                categories_to_write.append([user_answer[0], user_answer[1]])
                #categories_txt_list.append(user_answer[1])
                # Adds all of the items from the cleaned_list to the new list, with the category at the end
                list_w_cats.append([cleaned_list[i][0], user_answer[0], user_answer[1], cleaned_list[i][2]])
                
    # Calls writing function and gives a list that contains every transaction place and category to be put into database
    write_to_categories_txt(categories_to_write, categories_txt_list)

    return list_w_cats

def user_input(transaction: str, categories: list) -> list:
    """
    This function serves to give the transaction and category list to the user, who will
    enter in what the transaction should be called, and what corresponding category 
    """
    
    # inst user answer (will be 2)
    user_answer = []

    # For readability
    print()

    # Asking the user what the transaction is called, for simplicity
    user_answer_transaction = simpledialog.askstring("Input", "Transaction Place: " + "\n" + transaction + "\n" + "\n" + "Type in the name of this transaction that is included in the above line" + "\n" + "(Or, enter it blank to get rid of it)").upper()
    
    # For Testing
    print(user_answer_transaction)

    string_of_cats = ""

    # Going through each indicies of the Category Text List
    for line in range(len(categories)):

        # Printing all of the last index of in each line, which is each category
        string_of_cats += categories[line][len(categories[line])-1]
        string_of_cats += "\n"

    # Checking each user answer if they answered 'remove' or nothing
    if user_answer_transaction:
        # Asking the user which category it belongs to, and making it uppercase
        user_answer_category = simpledialog.askstring("Input", string_of_cats + "\n" + "What category does this transaction belong to?" + "\n" + "(Or, type in a new category)").upper()
        #user_answer_category = input("What category does this transaction belong to? ").upper()
    else:
        user_answer_category = ""

    # Adding the users answers to a line
    user_answer.append(user_answer_transaction)
    user_answer.append(user_answer_category)

    return user_answer

"""
def clean_initial_list(file_contents: list, debitOrCredit: str) -> list:
    
    #Removing all of the money coming in and blank spaces in remaining expenses.
    
    
    cleaned_list = [] # Instantiating the cleaned list

    # Indexing through each line of the file contents
    for i in range(len(file_contents)):
        if(debitOrCredit == "Credit"):
            if i != 
        # If the 3rd line has nothing in it, it means it is a money deposit and not needed for this program
        if file_contents[i][2] != '':
            # Adds to the cleaned list
            cleaned_list.append(file_contents[i])

    return cleaned_list
"""
def clean_database_list(file_contents: list) -> list:

    cleaned_list = []
    
    for line in file_contents:
        cleaned_list_line = []
        for item in line:
            str(item)
            if item:
                cleaned_list_line.append(item)
        cleaned_list.append(cleaned_list_line)
    
    return cleaned_list

def read_file(enter_file_name: str, debitOrCredit: str) -> list:
    """
    To read the file and return its contents
    """

    # Opens a file explorer so the user may choose the file to upload 
    file_path = filedialog.askopenfilename(title=enter_file_name, 
    filetypes=[("Comma-Separated Values files", "*.csv"), ("All Files", "*.*")])
    
    # Opens the file with a variable name 
    file_open = open(file_path, "r")

    # Reads the files contents
    input_file = file_open.readlines()

    # Inst a list to store full file contents
    file_list = []
    
    # Indexing through list line by line
    for line in input_file:
        # Splits all lines by the comma and strips 
        
        item = line.strip().split(',')
        if (debitOrCredit == "Debit" or debitOrCredit == "Credit"):
            if item[2] == '':
                continue

        if (debitOrCredit == "Credit"):
            # Runs when item has Province abrev in it
            if (len(item) == 6):
                del item[5]
                del item[4]
                del item[2]
            # Runs when item has no Province in it
            else: 
                del item[4]
                del item[3]
        # TEST
        print(item)
        # Add final item to list
        file_list.append(item)

    # Closes file
    file_open.close()

    return file_list

import tkinter as tk

def ask_transaction_type() -> str:

    selected_option = None

    def on_select(option):
        nonlocal selected_option  # Access the outer scope variable
        selected_option = option
        root.quit()  # Close the window after selection
        root.destroy()  # Ensure window is fully destroyed
        print(f"Selected transaction type: {option}")

    root = tk.Tk()
    root.title("Select Transaction Type")
    
    # Create a button for "Debit"
    debit_button = tk.Button(root, text="Debit", command=lambda: on_select("Debit"))
    debit_button.pack(padx=500, pady=50)
    
    # Create a button for "Credit"
    credit_button = tk.Button(root, text="Credit", command=lambda: on_select("Credit"))
    credit_button.pack(padx=500, pady=50)

    # Run the Tkinter event loop
    root.mainloop()

    return selected_option

def main() -> None:
    """
    Here is where everything starts and ends. 
    All functions will be called in this function
    """

    debitOrCredit = ask_transaction_type()

    #Takes the contents of the file and adds it to a list where every index is a line
    file_contents = read_file("Enter the Bank Transaction List", debitOrCredit)

    #cleaned_initial_list = clean_initial_list(file_contents)

    list_w_categories = category_list(file_contents)

    write_final_list(list_w_categories)

    print("Enjoy :)")

main()