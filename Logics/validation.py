
import re

class Valid:
    @staticmethod
    def verify_Year(year):
        if not (year.isdigit() and len(year) == 4):
            print("Enter a valid year.")
            return False
        else:
            return True

    @staticmethod
    def verify_phone_number(phone_number):
        if not (phone_number.isdigit() and len(phone_number) == 10):
            print("Phone Number must be exactly 10 digits.")
            return False
        else:
            return True

    @staticmethod
    def verify_admission_year(admission_year):
        if not (admission_year.isdigit() and len(admission_year) == 4):
            print("Enter a valid academic year.")
            return False
        else:
            return True

    @staticmethod
    def is_valid_format(email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z.-]+\.[a-zA-Z]{2,}$'
        match = re.match(regex, email)
        return match

    @staticmethod
    def verify_email(email):
        if not Valid.is_valid_format(email):
            print("Please Enter A Valid E-mail.")
            return False
        else:
            print("done")
            return True
        



    

    @staticmethod
    def is_valid_password(password):
        if len(password) < 8:
            return False
        if not re.search("[A-Z]", password):
            return False
        if not re.search("[a-z]", password):
            return False
        if not re.search("[0-9]", password):
            return False
        if not re.search("[@#$%^&+=]", password):
            return False
        return True

# Valid.is_valid_format("kunaldas")
# Valid.verify_email('kunaldas532001@gmail.com')