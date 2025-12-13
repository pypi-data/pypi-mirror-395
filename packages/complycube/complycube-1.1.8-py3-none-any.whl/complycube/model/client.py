from complycube.model.complycubeobject import ComplyCubeObject

class Client(ComplyCubeObject):
    """[A client represents the person or company the various checks will be performed on. To initiate a check, a client must be created first.]

    Attributes:
        id (str): [The unique identifier for a client.]
        type (str): [The type of client. Valid values are: person, company]
        entity_name (str): [The client's full name.]
        email (:obj: `str`, optional): [The client's email address.]
        mobile (:obj: `str`, optional): [The client's mobile number.]
        telephone (:obj: `str`, optional): [The client's telephone number.]
        joined_date (:obj: `str`, optional): [The date and time when the client was registered with you. This is relevant for users that migrate existing clients. The format is YYYY-MM-DD.]
        person_details (PersonDetails): [See documentation of PersonDetails class]
        company_details (CompanyDetails): [See documentation of CompanyDetails class]
        created_at (str): [The date and time when the client was created.]
        updated_at (str): [The date and time when the client was updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.type = None
        self.entity_name = None
        self.email = None
        self.mobile = None
        self.telephone = None
        self.joined_date = None
        self.person_details = None
        self.company_details = None
        super(Client, self).__init__(*args,**kwargs)
        if self.person_details is not None:
            if self.type != 'person':
                raise TypeError('Attempting to create %s object with personDetails' % self.type)
        if self.company_details is not None:
            if self.type != 'company':
                raise TypeError('Attempting to create %s object with companyDetails' % self.type)
            
class PersonDetails(ComplyCubeObject):
    """[Details for a client of type person]

    Attributes:
        first_name (str): [The person's first name.]
        middle_name (str): [The person's middle name.]
        last_name (str): [The person's last name.]
        dob (str): [The person's date of birth. The format is YYYY-MM-DD.]
        gender (str): [The person's gender. Valid values are: male, female, other]
        nationality (str): [The person's nationality. This will be the two-letter country ISO code.]
        birth_country (str): [The person's bith country. This will be the two-letter country ISO code.]
        ssn (str): [The client's SSN (Social Security Number). This is for US clients. (Optional)]
        social_insurance_number (str): [The client's Social Insurance Number. (Optional)]
        national_identity_number (str): [The client's National Identity Number. (Optional)]
        tax_identification_number (str): [The client's Tax Identification Number (TIN). (Optional)]
    """
    def __init__(self, *args, **kwargs):
        self.first_name = None
        self.middle_name = None
        self.last_name = None
        self.dob = None
        self.gender = None
        self.nationality = None
        self.birth_country = None
        self.ssn = None
        self.social_insurance_number = None
        self.national_identity_number = None
        self.tax_identification_number = None
        super(PersonDetails, self).__init__(*args,**kwargs)
        

class CompanyDetails(ComplyCubeObject):
    """[summary]

    Attributes:
        name (str): [The company's name.]
        website (str): The company's website.
        registration_number (str): The company's registration or incorporation number.
        incorporation_country (str): The company's incorporation country. This will be the two-letter country ISO code.
        incorporation_type (str): The company's incorporation type. Valid values include: 
            1. sole_proprietorship
            2. private_limited_company
            3. public_limited_company
            4. limited_partnership
            5. holding_company
            6. non_government_organisation
            7. statutory_company
            8. subsidiary_company
            9. unlimited_partnership
            10. charitable_incorporated_organisation
            11. chartered_company
    """
    def __init__(self, *args, **kwargs):
        self.name = None
        self.website = None
        self.registration_number = None
        self.incorporation_country = None
        self.incorporation_type = None
        super(CompanyDetails, self).__init__(*args,**kwargs)