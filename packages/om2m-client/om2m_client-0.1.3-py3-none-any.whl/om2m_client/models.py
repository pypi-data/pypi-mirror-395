# File name: models.py

class AE:
    """
    Application Entity resource model.
    """
    def __init__(self, rn: str, api: str, rr: bool = False, lbl=None, aei: str = None):
        self.rn = rn
        self.api = api
        self.rr = rr
        self.lbl = lbl or []
        self.aei = aei


class Container:
    """
    Container resource model.
    """
    def __init__(self, rn: str, lbl=None, cni: int = 0, cbs: int = 0):
        self.rn = rn
        self.lbl = lbl or []
        self.cni = cni
        self.cbs = cbs


class ContentInstance:
    """
    Content Instance resource model.
    """
    def __init__(self, cnf: str, con: str, rn: str = None):
        self.cnf = cnf
        self.con = con
        self.rn = rn


class Subscription:
    """
    Subscription resource model.
    """
    def __init__(self, rn: str, nu: str, nct: int = 2):
        self.rn = rn
        self.nu = nu
        self.nct = nct
