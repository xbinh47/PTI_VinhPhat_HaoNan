class User():
    def __init__(self, name, email, password, nationality, age, gender, avatar):
        self.name = name
        self.email = email
        self.password = password
        self.nationality = nationality
        self.age = age
        self.gender = gender
        self.avatar = avatar

    def __str__(self):
        return f"name: {self.name}, email: {self.email}, password: {self.password}, nationality: {self.nationality}, age: {self.age}, gender: {self.gender}, avatar: {self.avatar}"