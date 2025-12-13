from complycube.model.complycubeobject import ComplyCubeObject

class Address(ComplyCubeObject):
    """[Residential or business addresses can be linked to your client.]

    Attributes:
        id (str): [The unique identifier for an address.]
        client_id (str): [The ID of the client associated with this address.]
        type (str): [The type of address. Valid values are:
                        1. main
                        2. alternative
                        3. other]
        property_number (:obj: `str`, optional): [The property number of the client's address.]
        building_name (:obj: `str`, optional): [The building name of the client's address.]
        line (str): [The line of the client's address.]
        city (str): [The city or town of the client's address.]
        state (:obj: `str`, optional): [The county, state, or province of the client's address.]
        postal_code (:obj: `str`, optional): [The zip or post code of the client's address.]
        country (str): [The country of the client's address. This will be the two-letter country ISO code.]
        from_date (:obj: `str`, optional): [The date the client moved in to this address. The format is YYYY-MM-DD.]
        to_date (:obj: `str`, optional): [The date the client moved out of this address. The format is YYYY-MM-DD.]
        created_at (str): [The date and time when the address was created.]
        updated_at (str): [The date and time when the address was updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.client_id = None
        self.type = None
        self.property_number = None
        self.building_name = None
        self.line = None
        self.city = None
        self.state = None
        self.postal_code = None
        self.country = None
        self.from_date = None
        self.to_date = None
        super(Address, self).__init__(*args,**kwargs)