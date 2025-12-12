class Customer:
    def __init__(
        self,
        email,
        first_name="",
        last_name="",
        company="",
        phone="",
        address="",
        city="",
        state="",
        country="",
        postcode="",
        reference="",
        metadata={},
    ):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.company = company
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postcode = postcode
        self.reference = reference
        self.metadata = metadata
