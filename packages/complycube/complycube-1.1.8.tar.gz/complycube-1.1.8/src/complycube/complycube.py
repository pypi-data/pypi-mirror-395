import json
import requests
from complycube.error import ComplyCubeAPIError
import complycube
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class TimeoutHTTPAdapter(HTTPAdapter):
    timeout = 60

    def __init__(self, *args, **kwargs):
        self.timeout = 60
        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']
            del kwargs['timeout']
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

class ComplyCubeClient(object):
    def __init__(self, api_key=None, proxy=None, retries=None, timeout=None):
        if not api_key or not isinstance(api_key, str):
            raise KeyError('Please provide a Key')
        
        self.base_url = complycube._base_url
        self.api_key = api_key
        self.client_session = requests.Session()
        self.proxy = proxy or {}
        retry_strategy = None
        if retries is not None:
            retry_strategy = Retry( 
                                    total=retries,
                                    status_forcelist=[429, 500, 502, 503, 504],
                                    allowed_methods=["HEAD", "GET", "OPTIONS"],
                                    backoff_factor=1)

        adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)
        self.client_session.mount("https://", adapter)
        self.client_session.mount("http://", adapter)


    @property
    def clients(self):
        """[The clients api allows you to create, retrieve, update, and delete your clients. You can retrieve a specific clients as well as a list of all your clients.]

        Returns:
            [api_resources.client.Client]: [Client API interface]
        """
        from complycube.api_resources import client
        return client.Client(self)
    
    @property
    def documents(self):
        """[The documents api allows you to create, update, retrieve, upload, and delete documents. You can retrieve a specific document as well as a list of all your client's documents.]

        Returns:
            [api_resources.document.Document]: [Document API interface]
        """
        from complycube.api_resources import document
        return document.Document(self)

    @property
    def addresses(self):
        """[The addresses api allows you to create, retrieve, update, and delete your clients' addresses. You can retrieve a specific address as well as a list of all your client's addresses.]

        Returns:
            [api_resources.address.Address]: [Address API interface]
        """
        from complycube.api_resources import address
        return address.Address(self)

    @property
    def livephotos(self):
        """[The live photos api allows you to upload, retrieve, download, and delete live photos. You can retrieve a specific live photo as well as a list all your client's live photos.]

        Returns:
            [api_resources.livephoto.LivePhoto]: [Live Photo API interface]
        """
        from complycube.api_resources import livephoto
        return livephoto.LivePhoto(self)

    @property
    def livevideos(self):
        """[The live videos API allows you to retrieve, download, and delete live photos. You can retrieve a specific live video as well as a list of all your client's live videos.]

        Returns:
            [api_resources.livevideo.LiveVideo]: [Live Video API interface]
        """
        from complycube.api_resources import livevideo
        return livevideo.LiveVideo(self)

    @property
    def checks(self):
        """[The checks api allows you to create and retrieve checks. You can retrieve a specific check as well as a list all your client's checks.]

        Returns:
            [api_resources.check.Check]: [Check API interface]
        """
        from complycube.api_resources import check
        return check.Check(self)

    @property
    def riskprofiles(self):
        """[The risk profile API allows you to get the risk profile for a given client.]

        Returns:
            [api_resources.riskrprofile.RiskProfile]: [Risk Profile API interface]
        """
        from complycube.api_resources import riskprofile
        return riskprofile.RiskProfile(self)

    @property
    def webhooks(self):
        """[The webhooks api allows you to create, retrieve, update, and delete your webhooks. You can retrieve a specific webhook as well as a list of all your webhooks.]

        Returns:
            [api_resources.webhook.Webhook]: [Webhook API interface]
        """
        from complycube.api_resources import webhook
        return webhook.Webhook(self)

    @property
    def tokens(self):
        """[The tokens api allows you to create JWT tokens that can be issued to client applications that send persondata data to ComplyCube via our SDKs]

        Returns:
            [api_resources.token.Token]: [Token API interface]
        """
        from complycube.api_resources import token
        return token.Token(self)


    @property
    def reports(self):
        """[The reports api allows you to create client and check reports]

        Returns:
            [api_resources.report.Report]: [Report API interface]
        """
        from complycube.api_resources import report
        return report.Report(self)

    @property
    def teammembers(self):
        """[A team member object provides information on your team members. Team members can be added and manged through the Web Portal]

        Returns:
            [api_resources.teammember.TeamMember]: [Team Member API interface]
        """
        from complycube.api_resources import teammember
        return teammember.TeamMember(self)

    @property
    def auditlogs(self):
        """[The API allows you to retrieve audit logs for a given client, action, resource, or trigger.]

        Returns:
            [api_resources.auditlogs.AuditLog]: [Audit Log API interface]
        """
        from complycube.api_resources import auditlog
        return auditlog.AuditLog(self)

    @property
    def flow(self):
        """[The API allows you to rcreated hosted solution Flow sessions for client redirection.]

        Returns:
            [api_resources.flow.Flow]: [Flow API interface]
        """
        from complycube.api_resources import flow
        return flow.Flow(self)

    @property
    def workflow_sessions(self):
        """[The API allows you to retrieve and manage workflow sessions for clients.]

        Returns:
            [api_resources.workflowsessions.WorkflowSession]: [Workflow Session API interface]
        """
        from complycube.api_resources import workflowsessions
        return workflowsessions.WorkflowSession(self)

    @property
    def static(self):
        """[Allows you to retrieve static data such as list of all Sanctions and Watchlists available as part of a Screening Check.]

        Returns:
            [api_resources.static.Static]: [Static API interface]
        """
        from complycube.api_resources import static
        return static.Static(self)
    
    @property
    def account_info(self):
        """[Account Info API allows you to get account info around usage and credits.]

        Returns:
            [api_resources.accountinfo.AccountInfo]: [AccountInfo API interface]
        """
        from complycube.api_resources import accountinfo
        return accountinfo.AccountInfo(self)

    def _execute_api_request(self, endpoint, method='GET', **kwargs):
        request_args = {}
        content = {}    
        method = method.lower()        
        url = '%s/%s' % (self.base_url, endpoint)
        params = kwargs if method=='get' else {}
        self.client_session.headers['Authorization'] = kwargs.pop('api_key',self.api_key)
        self.client_session.headers['User-Agent'] = '%s-python/%s' % (__package__,complycube.__version__)
        
        if method in ['post','put','patch']:
            request_args['headers'] = {'Content-Type': 'application/json'}
            request_args['data'] = json.dumps(kwargs)        

        request_function = getattr(self.client_session, method)
        try:
            response = request_function(url, params=params, **request_args)
        except requests.RequestException as e:
            raise ComplyCubeAPIError(e)
        content = response.content.decode('utf-8')

        if response.status_code != 204:
            content = json.loads(content)
        
        if response.status_code >= 400:
            raise ComplyCubeAPIError(content['message'])
        return content , response.status_code
