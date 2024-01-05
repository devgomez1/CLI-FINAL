from models.user import User
from models.report import Report
import openai
import os
from tqdm import tqdm
import time


def generate_report_with_gpt(income, rent, food, other_expenses, state):
    # Set your OpenAI API key
    openai.api_key = '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'

    # Construct the prompt
    prompt = f"Generate a financial report based on the following data:\n"\
             f"Income: ${income}\n"\
             f'State: ${state}\n'\
             f"Average Monthly Rent: ${rent}\n"\
             f"Average Monthly Food Spending: ${food}\n"\
             f"Other Monthly Expenses: ${other_expenses}\n\n"\
             "Provide a summary and financial advice, critique if they are spending too much money on food or rent and dont have a stable enough income to be affording those big of expenses. as well as clever ways to save money. The most important thing is to take into account what state they live in and how much they are making, from this I want you to estimate how much they lose from taxes and how much they should be saving state what numbers you used and state your caculations. After listing the calculations, give a summary of the report and provide financial advice, make it long. At the very end of the report provide ten ways to save money"

    # Generate the report
    response = openai.Completion.create(
        engine="text-davinci-003",  # or the latest GPT model
        prompt=prompt,
        max_tokens=3000
    )

    return response.choices[0].text.strip()

def clear_screen():
    if os.name == 'nt':  # for windows
        _ = os.system('cls')
    else:  # for mac and linux(here, os.name is 'posix')
        _ = os.system('clear')

def main():
    menu()
    while True:

        choice = input("\nEnter your choice: ")
        clear_screen()
        if choice == "0":
            print("\nExiting the program...\n")
            break

        elif choice == "1":

            print("\nListing all Users...")
            for user in User.all_users():
                print(user)
            print("\n")  # Add space after the list

        elif choice == "2":

            print("\nListing all Reports...")
            Report.fetch_all()  # Add this line
            for report in Report.all.values():
                print('-' * 200)
                print('\n')
                print(report)
                print('\n')
            print("\n")  # Add space after the list

        elif choice == "3":

            name = input("\nEnter the name of the report: ")
            print("\nFinding Report by Name...")
            report = Report.find_by_paragraph_overview(name)
            if report:
                print("\n", report, "\n")
            else:
                print("Report not found.\n")

        elif choice == "4":
            name = input("\nEnter the name of the user: ")
            print("\nFinding Reports by User...")
            user = User.find_by_name(name)
            if user:
                print(f"Found user: {user}")
                reports = Report.find_by_user_id(user.id)
                if reports:  # Check if any reports were found
                    print(f"Found reports:")
                    for report in reports:
                        print(report)
                        print('\n')
                        print('-' * 200)
                else:
                    print("No reports found for this user.")
                print("\n")
            else:
                print("User not found.")


        elif choice == "5":

            print("\nCreating Report...")
            paragraph_overview = input("Enter Report Title: ")
            income = input("Enter your monthly income: ")
            state = input('Enter your state of residence:')
            rent = input("Enter your average monthly rent as well as bills and utilities: ")
            food = input("Enter your average monthly spending on Groceries: ")
            other_expenses = input("Enter your monthly expenses on personal entertainment: ")
            
            print("Generating report, please wait...")
            with tqdm(total=100) as pbar:
                for i in range(100):
                    time.sleep(0.25)  # adjust this to match the expected time
                    pbar.update(1)

            report_text = generate_report_with_gpt(income, state, rent, food, other_expenses)
            user_id = int(input("Enter the user ID: "))
            report = Report.create(paragraph_overview, user_id, report_text)
            print(f"\nCreated report: {report}\n")


        elif choice == "6":
            print("\nDeleting Report...")
            id = int(input("Enter the ID of the report to delete: "))
            report = Report.find_by_id(id)
            if report:
                report.delete_by_id(id)
                print("\nReport deleted.\n")
            else:
                print("Report not found.\n")

        elif choice == "7":

            print("\nCreating User...")
            name = input("Enter the name of the user: ")
            user = User.create(name)
            print(f"\nCreated user: {user}\n")

        elif choice == "8":

            print("\nDeleting User...")
            id = int(input("Enter the ID of the user to delete: "))
            user = User.find_by_id(id)
            if user:
                user.drop_table()
                print("\nUser deleted.\n")
            else:
                print("User not found.\n")
        else:
            print("\nInvalid choice. Please try again.\n")

        menu()



def menu():
    print('-' * 200)
    print("Please select an option:")
    print("0. Exit the program")
    print("1. List all Users")
    print("2. List all Reports")
    print("3. Find Report by Name")
    print("4. List Reports by User")
    print("5. Create Report")
    print("6. Delete Report")
    print("7. Create User")
    print("8. Delete User")

if __name__ == "__main__":
    main()
