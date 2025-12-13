from complycube.model.complycubeobject import ComplyCubeObject

class Document(ComplyCubeObject):
    """[Documents can be created for a given client for the following purposes:
            Secure and centralised document storage.
            Perform checks such as Document Checks and Identity Checks.]

    Attributes:
        id (str): [The unique identifier for a document.]
        client_id (str): [The ID of the client associated with this document.]
        type (str): [The type of document. Valid values are:
                        1. passport
                        2. driving_license
                        3. national_insurance_number
                        4. social_security_number
                        5. tax_identification_numbe
                        6. national_identity_card
                        7. visa
                        8. polling_card
                        9. residence_permit
                        10. birth_certificate
                        11. bank_statement
                        12. change_of_name
                        13. tax_document
                        14. company_confirmation_statement
                        15. company_annual_accounts
                        16. company_statement_of_capital
                        17. company_change_of_address
                        18. company_incorporation
                        19. company_change_of_officers
                        20. company_change_of_beneficial_owners
                        21. unknown
                        22. other]
        classification (:obj: `str`, optional): [The classification or purpose of this document. Valid values include:
                                                    1. proof_of_identity
                                                    2. source_of_wealth
                                                    3. source_of_funds
                                                    4. proof_of_address
                                                    5. company_filing
                                                    6. other]
        issuing_country (:obj: `str`, optional): [The document's issuing country. This will be the two-letter country ISO code.]
        images (:obj:`list` of :obj:`Image`): [The images or attachments associated with the document. This will only appear once a document image is upload. Also see: The image object below.]
        created_at (str): [The date and time when the document was created.]
        updated_at (str): [The date and time when the document was updated.]
    """
    def __init__(self, *args, **params):
        self.id = None
        self.client_id = None
        self.type = None
        self.classification = None
        self.issuing_country = None
        self.images = None
        super(Document, self).__init__(*args,**params)
        
class Image(ComplyCubeObject):
    pass