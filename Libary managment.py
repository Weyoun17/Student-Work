from datetime import date, timedelta # imports a way to track how long the  book has been out for and when it is due back
import hashlib # import a hashing algorithm to secure passwords

# creates the users 
class Member:
    def __init__(self, memberID, memberName, password):
        self._memberID = memberID
        self._memberName = memberName
        self.__password = hashlib.sha256(password.encode()).hexdigest()
        self._borrowedBooks = []
        self._borrowHistory = []

    def validatePassword(self, enteredPassword):
        hashed = hashlib.sha256(enteredPassword.encode()).hexdigest()
        return self.__password == hashed


    def borrowBook(self, book):

        self._borrowedBooks.append(book)
        self._borrowHistory.append(book)

    def returnBook(self, book):

        if book in self._borrowedBooks:
            self._borrowedBooks.remove(book)

    # Makes it easier to print the members name and ID when needed
    def __str__(self):

        return f"{self._memberID} - {self._memberName}"  
    
    # Member user Options
    def memberMenu(self, library):
        while True:
            print("\n--- MEMBER MENU ---")
            print("1. Search for a Book")
            print("2. Borrow a Book")
            print("3. Return a Book")
            print("4. View Borrowed Books")
            print("5. Log Out")

            choice = input("Enter Choice: ")

            if choice == "1":
                title = input("Please enter the title of the book ")
                book = library.bookSearch(title)
                print(book if book else "Book not found.")
            elif choice == "2":
                bookID = int(input("Enter Book ID to borrow: "))
                library.issue_book(self, bookID)

            elif choice == "3":
                bookID = int(input("Enter Book ID to return: "))
                library.return_book(self, bookID)
            elif choice == "4":
                print("\nYour Borrowed Books are:")
                for b in self._borrowedBooks:
                    print(b)

            elif choice == "5":
                print("Logging out now...")
                break

            else:
                print("Invalid choice.")
                break

class Librarian:
    def __init__(self, librarianID, staffName, password):
        self._librarianID = librarianID 
        self._staffName = staffName
        self.__password = hashlib.sha256(password.encode()).hexdigest()



    def add_book(self, library, book):
        library.add_book(book)

    def issue_book(self, library, member, bookID):
        library.issue_book(member, bookID)

    def record_return(self, library, member, bookID):
        library.return_book(member, bookID)

    def __str__(self):
        return f"Librarian: {self._staffName} (Librarian ID: {self._librarianID})"
    
#creates the Book class
class Book:
    def __init__(self, bookID: int, title: str, author: str):
        self.bookID= bookID
        self.title = title
        self.author = author
        self.available = True

    def MARKissued(self):
        self.available = False

    def MARKreturned(self):
        self.available = True

    def __str__(self):
        status = "Available" if self.available else "Issued"
        return f"{self.title} by {self.author} [{status}]"


class Loan:
    def __init__(self, loan_id: int, member, book, issue_days=14):
        self.loan_id = loan_id
        self.member = member
        self.book = book
        self.issue_date = date.today()
        self.due_date = self.issue_date + timedelta(days=issue_days)
        self.return_date = None

    def calculateFine(self):
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            return days_late * 1  # makes the fine   wroth £1 per day late
        return 0

    def closeLoan(self):
        self.return_date = date.today()

    def __str__(self):
        return (
            f"Loan ID: {self.loan_id}, "
            f"Book: {self.book.title}, "
            f"Member: {self.member.memberName}"
        )


class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.librarians = []
        self.loans = []

#securing passowrds 
    def validatePassword(self, enteredPassword):
        hashed = hashlib.sha256(enteredPassword.encode()).hexdigest()
        return self.__password == hashed

    #Continuing of Membership sign up
    def sign_up_member(self):

        print("Welcome to the library, let's create your membership account.")

        try:

            name = input("Enter your name: ")
            password = input("Create your password: ")
            memberID = int(input("Create your member ID: "))


            member = Member(memberID, name, password)

            self.members.append(member)

            print("Member account created successfully.")

        except ValueError:

            print("Invalid input.")
    #Continuing of Membership log in
    def memberLogIn(self):

        print("\n--- Member Log In ---")

        try:

            memberID = int(input("Enter member ID: "))
            password = input("Enter password: ")

            for member in self.members:

                if member.memberID == memberID:

                    
                    if member.validatePassword(password):

                        print(f"\nWelcome back {member.memberName}")

                        return member

                    else:

                        print("Incorrect password.")
                        return None

            print("Member not found.")
            return None

    # crates an eror message
        except ValueError:

            print("Invalid input.")
            return None

    #Continuing of Librarian log in
    def librarianLogIn(self):

        print("Welcome Librarian, please log in to access your account.")

        try:

            librarianID = int(input("Enter librarian ID: "))
            password = input("Enter password: ")

            for librarian in self.librarians:

                if librarian.librarianID == librarianID:
                    if librarian.validatePassword(password):
                        print(f"\nWelcome Librarian {librarian.staffName}")
                        return librarian
                    else:
                        print("Incorrect password.")
                        return None
            else:
                print("Librarian ID not found.")
                return None



        except ValueError:

            print("Invalid input.")
        return None

    def register_member(self, member):
        self.members.append(member)
        print(f"Member registered: {member.memberName}")

    def bookSearch(self, title):
        print(f"Would you like to search using the book title or book ID? \n 1. Book Title \n 2. Book ID")
        choice = input("Please enter your choice (1 or 2): ")
        for book in self.books:
            if choice == "1" and title.lower() in book.title.lower():
                return book
            elif choice == "2" and title == str(book.bookID):
                return book
        return None

    def issue_book(self, member, bookID):
        for book in self.books:
            if book.bookID == bookID and book.available:
                book.MARKissued()
                member.borrowBook(book)

                loan = Loan(
                    loan_id=len(self.loans) + 1,
                    member=member,
                    book=book
                )

                self.loans.append(loan)

                print(f"Book '{book.title}' issued to {member.memberName}")
                return
        print("Book not available.")

    def return_book(self, member, bookID):
        for loan in self.loans:
            if (loan.book.bookID == bookID and loan.member == member  and loan.return_date is None):
                loan.closeLoan()
                loan.book.MARKreturned()
                member.returnBook(loan.book)

                fine = loan.calculateFine()

                print(f"Book '{loan.book.title}' returned.")
                if fine > 0:
                    print(f"Fine due: {fine}")

                return

        print("Loan record not found.")



library = Library()

# Pre-populated data for testing
library.books.append(Book(1, "Python Programming", "John Smith"))
library.books.append(Book(2, "Data Structures", "Jane Doe"))
library.books.append(Book(3, "Computer Networks", "James Brown"))

 # Librarian account for testing
mainLibrarian = Librarian(1001, "Alice", "admin123")
library.librarians.append(mainLibrarian)

# Member account for testing
testMember = Member(2001, "Bob", "password123")
library.members.append(testMember)



# start of the text based interface for the library system
print("Welcome to the library's digital system \n May I ask you to log in or sign up to use this system \n 1. Log in \n 2. Sign up ")

firstQuestion = input("Please enter your choice (1 or 2): ")

# start of the login 
if firstQuestion == "1":
    print("Welcome back, are you a member or a librarian? \n 1. Member \n 2. Librarian")
    secondQuestion = input("Please enter your choice (1 or 2): ")
    if secondQuestion == "1":
        print("Welcome, may I first take your user ID?")
    elif secondQuestion == "2":
        print("Welcome, may I first take your staff ID?")
    else:
        print("Error, please only enter 1 or 2")


#  Start of the sign up

elif firstQuestion == "2":
    print("Welcome, are you signing up as a member or a librarian? \n 1. Member \n 2. Librarian")
    
    secondQuestion = input("Please enter your choice (1 or 2): ")
    if secondQuestion == "1":
        print("Welcome, may I first take your Name?")
    elif secondQuestion == "2":
        
        quit("I am sorry we are not currently accepting new librarian sign-ups.")
    else:
        quit("Error, please only enter 1 or 2")

else:
    quit("Error, please only enter 1 or 2")