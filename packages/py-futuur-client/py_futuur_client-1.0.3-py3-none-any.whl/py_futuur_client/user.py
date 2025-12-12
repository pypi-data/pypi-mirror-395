class UseAPI:

    def __init__(self, client):
        self.client = client
    
    def get_details(self):
        """
        The endpoint returns information about a user..
        Endpoint: GET /api/v1/me/
        """
        return self.client._make_request(endpoint='me/')