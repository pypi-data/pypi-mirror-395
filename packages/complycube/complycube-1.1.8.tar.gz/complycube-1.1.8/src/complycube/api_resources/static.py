from complycube.api_resources.complycuberesource import ComplyCubeResource


class Static(ComplyCubeResource):

    @property
    def endpoint(self):
        return 'static' 

    def screening_lists(self):
        response , _  = self.client._execute_api_request(f'{self.endpoint}/screeningLists','GET')
        return response