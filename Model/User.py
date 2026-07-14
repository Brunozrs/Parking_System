class User:
    def __init__(self, id=None, name=None,phone_number = None, email= None,document= None, address = None):
        self._id = id # set after DB insert
        self._name = name
        self._phoneNumber = phone_number
        self._email = email
        self._document = document
        self._address = address

    @property
    def id(self):
        return self._id
    @id.setter
    def id(self, value):
        self._id = value

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, name):
        self._name = name

    @property
    def phonenumber(self):
        return self._phoneNumber
    @phonenumber.setter
    def phonenumber(self, phone_number):
        self._phoneNumber = phone_number

    @property
    def email(self):
        return self._email
    @email.setter
    def email(self, email):
        self._email = email

    @property
    def document(self):
        return self._document
    @document.setter
    def document(self, document):
        self._document = document

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value