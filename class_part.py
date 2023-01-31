from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    """Parent class for all fields"""

    def __init__(self, value):
        self.__value = None
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Name(Field):
    """Required field with username"""
    pass


class Phone(Field):
    """Optional field with phone numbers"""

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Birthday(Field):
    """Creating 'birthday' fields"""

    def __str__(self):
        return self.value.strftime("%d-%m-%Y")

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d-%m-%Y").date()
        except ValueError:
            raise ValueError("Birthday must be in 'DD-MM-YYYY' format")


class Email(Field):
    """Creating 'email fields'"""

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self)

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if not re.findall(r"\b[A-Za-z][\w+.]+@\w+[.][a-z]{2,3}", value):
            raise ValueError('Wrong format')
        self.__value = value


class Record:
    """Class for add, remove, change fields"""

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None, email: Email = None):

        self.birthday = birthday
        self.email = email
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)

    def __str__(self) -> str:
        return f'Name: {self.name} Phone: {", ".join([str(p) for p in self.phones])} {"Birthday: " + str(self.birthday) if self.birthday else ""} Email: {str(self.email) if self.email else ""}'

    def __repr__(self) -> str:
        return str(self)

    def add_phone(self, phone):
        self.phones.append(phone)
        return f"Phone {phone} was added successfully"

    def change(self, old_phone: Phone, new_phone: Phone):
        for phone in self.phones:
            if phone.value == old_phone.value:
                self.phones.remove(phone)
                self.phones.append(new_phone)
                return f"Phone {old_phone} was successfully changed to {new_phone}"
            return f"Phone number '{old_phone}' was not found in the record"

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday

    def add_email(self, email: Email):
        self.email = email

    def days_to_birthday(self):

        cur_date = datetime.now().date()
        cur_year = cur_date.year

        if self.birthday:
            bd = self.birthday.value
            this_year_bd = bd.replace(year=cur_year)
            delta = (this_year_bd - cur_date).days
            if delta > 0:
                return f"{self.name}'s birthday will be in {delta} days"
            else:
                next_year_bd = this_year_bd.replace(year=cur_year + 1)
                delta = (next_year_bd - cur_date).days
                return f"{self.name}'s birthday will be in {delta} days"
        else:
            return f"{self.name}'s birthday is unknown"

    def show_contact_info(self):
        phones = ", ".join([str(ph) for ph in self.phones])
        return {
            "name": str(self.name.value),
            "phone": phones,
            "birthday": self.birthday,
            "email": self.email,
        }

    def remove_phone(self, phone):
        phone = Phone(phone)
        for ph in self.phones:
            if ph.value == phone.value:
                self.phones.remove(ph)
                return f"Phone {ph} was successfully removed from {self.name}"
        return f"Number {phone} not found"


class AddressBook(UserDict):
    """Class for creating address book"""

    def open_file(self):
        with open('AddressBook.txt', 'rb') as open_file:
            self.data = pickle.load(open_file)
        return self.data

    def write_file(self):
        with open('AddressBook.txt', 'wb') as write_file:
            pickle.dump(self.data, write_file)

    def search_in_file(self, data):
        result = ""
        for record in self.data.values():
            if str(data).lower() in str(record.name).lower():
                result += f"Name: {record.name} Birthday: {record.birthday} Phone: {','.join([ph.value for ph in record.phones])}\n"
            else:
                for phone in record.phones:
                    if str(data).lower() in str(phone):
                        result += f"Name: {record.name} Birthday: {record.birthday} Phone: {','.join([ph.value for ph in record.phones])}\n"
        return result

    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def remove_record(self, record):
        self.data.pop(record.name.value, None)

    def show_one_record(self, name):
        return f"Name: {name}; Birthday: {self.data[name].birthday}; Phone: {', '.join([str(phone.value) for phone in self.data[name].phones])}"

    def show_all_records(self):
        return "\n".join(
            f"Name: {rec.name}; Birthday: {rec.birthday}; Phone: {', '.join([ph.value for ph in rec.phones])} Email: {rec.email}" for rec
            in self.data.values())

    def change_record(self, username, old_n, new_n):
        record = self.data.get(username)
        if record:
            record.change(old_n, new_n)

    def iterator(self, n):
        records = list(self.data.keys())
        records_num = len(records)
        count = 0
        result = ""
        if n > records_num:
            n = records_num
        for rec in self.data.values():
            if count < n:
                result += f'{rec.name} (B-day: {rec.birthday}): {", ".join([p.value for p in rec.phones])}\n'
                count += 1
        yield result


ADDRESSBOOK = AddressBook()
