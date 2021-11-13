"""
This module provides Transaction and Account classes
"""

import pickle


class SaveError(BaseException): pass
class LoadError(BaseException): pass


class Transaction:

    def __init__(self, amount, date, currency='USD', usd_conversion_rate=1.0, description=None):
        """Characteristics of transaction

        >>> trans = Transaction(75000, '20:11:2020', 'RUB', 0.015, 'Salary')
        >>> trans.amount
        75000
        >>> trans.date
        '20:11:2020'
        >>> trans.currency
        'RUB'
        >>> trans.usd_conversion_rate
        0.015
        >>> trans.description
        'Salary'
        >>> trans.usd
        1125.0
        """
        self.__amount = amount
        self.__date = date
        self.__currency = currency
        self.__usd_conversion_rate = usd_conversion_rate
        self.__description = description


    @property
    def amount(self):
        """Returns sum of transaction"""
        return self.__amount


    @property
    def date(self):
        """Returns date of transaction"""
        return self.__date


    @property
    def currency(self):
        """Returns currency of transaction"""
        return self.__currency


    @property
    def usd_conversion_rate(self):
        """Returns dollar's conversion rate for currency"""
        return self.__usd_conversion_rate


    @property
    def description(self):
        """Returns description of transaction"""
        return self.__description


    @property
    def usd(self):
        """Returns amount of transaction by dollars"""
        return self.__amount * self.__usd_conversion_rate


class Account:

    def __init__(self, number, name):
        """Creates object Account which contains number of bill,
        name of account.

        All transactions are saved in account. Balance of bill is
        sum of transactions.
        >>> import os
        >>> mikhail = Account(238013435414, 'Mikhail')
        >>> mikhail.balance
        0
        >>> mikhail.name
        'Mikhail'
        >>> mikhail.name = 'Misha'
        >>> mikhail.name
        'Misha'
        >>> salary = Transaction(90000, '04:11:2020', 'RUB', 0.015, 'Salary')
        >>> purchase = Transaction(-1500, '05:11:2020', 'RUB', 0.015,
        ...                        'Purchase in Piterochka')
        >>> mikhail.apply(salary)
        >>> mikhail.apply(purchase)
        >>> mikhail.balance  # by dollars
        1327.5
        >>> mikhail.all_usd
        False
        >>> mikhail.save()
        >>> internet = Transaction(-500, '01:12:2020', 'RUB', 0.015)
        >>> mikhail.apply(internet)
        >>> mikhail.load()
        >>> len(mikhail)
        2
        >>> mikhail.balance  # by dollars
        1327.5
        >>> try:
        ...     os.remove(mikhail.number + ".acc")
        ... except OSError:
        ...     pass
        """
        self.__number = str(number)
        self.name = name
        self.__transactions = []
        self.__balance = 0
        self.__all_usd = True


    @property
    def number(self):
        """Returns number of account"""
        return self.__number


    @property
    def name(self):
        """Returns name of account"""
        return self.__name


    @name.setter
    def name(self, name):
        """Changes name of account"""
        assert len(name) >= 4, "account's name must consist not less four symbols"
        self.__name = name


    def __len__(self):
        """Returns amount of transactions"""
        return len(self.__transactions)


    @property
    def balance(self):
        """Returns balance of account by dollars"""

        return self.__balance


    @property
    def all_usd(self):
        """Returns True if all transactions are made by dollars"""
        return self.__all_usd


    def apply(self, transaction):
        """Adds transaction in account"""
        assert isinstance(transaction, Transaction), 'added object is not transaction'
        self.__transactions.append(transaction)
        self.__balance += transaction.usd
        if transaction.currency.upper() != 'USD':
            self.__all_usd = False


    def save(self):
        """Saves account and its transactions in file"""
        fh = None
        try:
            data = [self.__number, self.__name]
            fh = open(self.__number + ".acc", 'wb')
            pickle.dump(data, fh, pickle.HIGHEST_PROTOCOL)
            for trans in self.__transactions:
                trans_data = [trans.amount, trans.date, trans.currency,
                              trans.usd_conversion_rate, trans.description]
                pickle.dump(trans_data, fh, pickle.HIGHEST_PROTOCOL)
        except (OSError, pickle.PickleError) as err:
            raise SaveError(str(err))
        finally:
            if fh is not None:
                fh.close()


    def load(self):
        """Loads account and its transactions from file"""
        fh = None
        try:
            fh = open(self.__number + ".acc", "rb")
            data = pickle.load(fh)
            self.__init__(*data)
            while True:
                trans_data = pickle.load(fh)
                trans = Transaction(*trans_data)
                self.apply(trans)
        except (OSError, pickle.PickleError) as err:
            raise LoadError(str(err))
        except EOFError:
            pass
        finally:
            if fh is not None:
                fh.close()


if __name__ == "__main__":
    import doctest
    doctest.testmod()
