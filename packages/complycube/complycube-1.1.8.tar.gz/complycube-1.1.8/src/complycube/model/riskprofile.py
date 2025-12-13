from complycube.model.complycubeobject import ComplyCubeObject

class RiskProfile(ComplyCubeObject):
    """[A Risk Profile provides you with an AML risk score for a given client. 
        It facilitates a risk-based framework for Client Due Diligence (CDD) 
        and Enhanced Due Diligence (EDD). Furthermore, the risk profile will 
        assist you in shaping your ongoing client relationship.The risk 
        profile is calculated by ComplyCube's proprietary risk model. The 
        value of the overall score, or a constituent risk score, will be 
        not_set if the client does not have sufficient details.]

    Attributes:
        overall_risk (str): [The overall risk score. Valid values are: 
                                1. low
                                2. medium
                                3. high
                                4. not_set]
        country_risk (CountryRisk): [This contains the country risk score and breakdown. See CountryRisk class documentation]
        political_exposure_risk (dict): [This contains the political exposure risk score and breakdown.]
        occupation_risk (dict): [This contains the occupation risk score and breakdown.]
        created_at (str): [The date and time when the risk profile was created.]
        updated_at (str): [The date and time when the risk profile was updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.client_id = None
        self.document_id = None
        self.live_photo_id = None
        self.entity_name = None
        self.type = None
        self.status = None
        self.result = None
        super(RiskProfile, self).__init__(*args,**kwargs)