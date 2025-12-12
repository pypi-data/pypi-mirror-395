class Constraints:
    """
    Simple constraints class for WHOS API queries.
    Supports bounding box for now.
    """
    def __init__(self, bbox=None):
        """
        Parameters:
            bbox: tuple of (south, west, north, east)
        """
        self.bbox = bbox

    def to_query(self):
        """Convert constraints to URL query string."""
        query = ""
        if self.bbox:
            south, west, north, east = self.bbox
            query += f"&west={west}&south={south}&east={east}&north={north}"
        return query
