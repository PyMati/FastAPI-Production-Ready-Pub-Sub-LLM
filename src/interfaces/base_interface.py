from sqlmodel import Session


class BaseInterface:
    def __init__(self, session: Session):
        self.session = session
