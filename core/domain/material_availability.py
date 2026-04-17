

class MaterialAvailability(object):
    is_available: bool
    avail_amt: int
    error: str

    def __init__(self, is_available: bool):
        self.is_available = is_available
        avail_amt = 0

    def __init__(self, error:str):
       self.is_available = False
       self.error = error

    def __init__(self, is_available: bool, avail_amt: int):
        self.is_available = is_available
        self.avail_amt = avail_amt


    def get_avail_amt(self):
        return self.avail_amt

    def get_is_available(self):
        return self.is_available