from enum import Enum


class TransactionTypes(Enum):

    EXPENSE = 'expense'
    INCOME = 'income'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]


class TransactionCategories(Enum):

    FOOD = 'food'
    BILLS = 'bills'
    CAR = 'car'
    TRANSPORT = 'transport'
    INCOME = 'income'
    TRANSFER = 'transfer'

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]
