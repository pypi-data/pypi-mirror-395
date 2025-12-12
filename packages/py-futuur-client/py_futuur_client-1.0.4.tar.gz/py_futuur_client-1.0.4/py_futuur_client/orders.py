class LimitOrderAPI:

    def __init__(self, client):
        self.client = client
    
    def list(self, params: dict = {}):
        """
        Retrieve a list of all limit orders placed by Outcome or Question for Real Money or Play Money.
        Endpoint: GET /api/v1/orders/
        """
        return self.client._make_request(endpoint='orders/', params=params)
    
    def create(self, payload: dict):
        """
        Place a limit order in the order book.
        Endpoint: POST /api/v1/orders/
        """
        return self.client._make_request(endpoint='orders/', method='POST', payload=payload)
    
    def cancel(self, id: int):
        """
        This action will remove the order from the order book, making it unavailable for matching.
        Endpoint: PATCH /api/v1/orders/{id}/
        """
        # A API usa PATCH para cancelar uma ordem, passando o ID na URL.
        # Geralmente, o payload é vazio ou contém um status de cancelamento.
        return self.client._make_request(endpoint=f'orders/{id}/cancel/', method='PATCH')
