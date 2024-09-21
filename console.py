import cmd
import sys
from models.auth import Auth
import getpass



class MoseebCommand(cmd.Cmd):

    prompt = '(Moseeb) ' if sys.__stdin__.isatty() else ''


    def preloop(self):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb)')

    def postcmd(self, stop, line):
        """Prints if isatty is false"""
        if not sys.__stdin__.isatty():
            print('(hbnb) ', end='')
        return stop

    def do_quit(self, command):
        """ Method to exit the Moseeb console"""
        exit()

    def help_quit(self):
        """ Prints the help documentation for quit  """
        print("Exits the program with formatting\n")

    def do_EOF(self, arg):
        """ Handles EOF to exit program """
        print()
        exit()

    def help_EOF(self):
        """ Prints the help documentation for EOF """
        print("Exits the program without formatting\n")

    def emptyline(self):
        """ Overrides the emptyline method of CMD """
        pass

    def do_create(self, line):
        """creat new superuser"""
        fname = input("Enter your fist name: ")
        lname = input("Enter your last name: ")
        email = input("Enter your email: ")
        password = getpass.getpass("Enter password: ")
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match.")
            return
        
        user = Auth.SignUp(fname, lname, email, 0, password, superuser=True)
        if user == 'email':
            print(f"Error: email '{email}' already exists.")
        else:
            print(f"User '{email}' created successfully.")


if __name__ == "__main__":
    MoseebCommand().cmdloop()