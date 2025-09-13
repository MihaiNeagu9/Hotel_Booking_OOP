import pandas

df = pandas.read_csv("hotels.csv", dtype={"id": str})
df_cards = pandas.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_cards_security = pandas.read_csv("card_security.csv", dtype=str)

class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def available(self):
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotels.csv", index=False)


class ReservationTicketHotel:
    def __init__(self, name_customer, hotel_object):
        self.name_customer = name_customer
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are you booking data:
        Name: {self.name_customer}
        Hotel Name: {self.hotel.name}
        """
        return content

class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, "holder": holder, "cvc": cvc}
        if card_data in df_cards:
            return True
        else:
            return False

class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_cards_security.loc[df_cards_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False

class ReservationTicketSpa:
    def __init__(self, name_customer, hotel_object):
        self.name_customer = name_customer
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your SPA reservation
        Here are you booking data:
        Name: {self.name_customer}
        Hotel Name: {self.hotel.name}
        """
        return content


print(df)
hotel_ID = input("Enter a hotel id: ")
hotel = Hotel(hotel_ID)
if hotel.available():
    credit_card = SecureCreditCard(number="1234")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password="mypass"):
            hotel.book()
            name = input("Enter your name: ")
            reservation = ReservationTicketHotel(name_customer=name, hotel_object=hotel)
            print(reservation.generate())
        else:
            print("There was a problem with authentication.")
    else:
        print("There was a problem with your payment.")
    answer = input("Do you want to book a spa package? ")
    if answer == "yes":
        spa_ticket = ReservationTicketSpa(name_customer=name, hotel_object=hotel)
        print(spa_ticket.generate())
    elif answer == "no":
        print("Have a nice day!")
else:
    print("Hotel is not free.")
