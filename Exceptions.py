
class NotFoundObjectError(Exception):
    def __init__(self, entity_name):
        self.name = entity_name
        pass

    def __repr__(self):
        return F"{self.name} not found"

class ValidationError(Exception):
    def __init__(self, property_name):
        self.name = property_name
        pass

    def __repr__(self):
        return F"{self.name} is not valid"
