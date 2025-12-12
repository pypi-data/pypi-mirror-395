class CategoryAPI:

    def __init__(self, client):
        self.client = client
    
    def list(self, params: dict={}):
        """
        Return list of categories.
        """
        return self.client._make_request(endpoint='categories/', params=params)
    
    def get(self, id):
        """
        Return category detail.
        """
        return self.client._make_request(endpoint=f'categories/{id}')
    
    def list_featured(self):
        """
        Return top 10 featured categories highest volume first.
        Endpoint: GET /api/v1/categories/featured/
        """
        return self.client._make_request(endpoint='categories/featured/')
    
    def list_main(self):
        """
        List all active categories marked as main.
        Endpoint: GET /api/v1/categories/main/
        """
        return self.client._make_request(endpoint='categories/main/')
    
    def list_root(self):
        """
        Return root categories.
        Endpoint: GET /api/v1/categories/root/
        """
        return self.client._make_request(endpoint='categories/root/')
    
    def list_root_and_main_children(self, params: dict = {}):
        """
        Return root categories and main children.
        Endpoint: GET /api/v1/categories/root_and_main_children/
        """
        return self.client._make_request(endpoint='categories/root_and_main_children/', params=params)