from sqlalchemy.orm import Session


class BaseInterface:
    def __init__(self, session: Session):
        self.session = session
