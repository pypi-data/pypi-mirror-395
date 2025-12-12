import inspect
from typing import Optional, List, no_type_check
from sqlmodel import SQLModel, Field, Relationship

#
# Private Models

class UserIdEntry(SQLModel, table=True):
    __tablename__ = 'users'
    email: str = Field(nullable=False, primary_key=True)
    name: str = Field(nullable=False)
    # Ajout d'une relation (back_populates pour la relation inverse)
    #buffers: List["BufferEntry"] = Relationship(back_populates="owner")
    #objects: List["UserObjEntry"] = Relationship(back_populates="owner")

    def matches(self, subject):
        return subject == self.email

    @no_type_check
    def __setattr__(self, name, value):
        """
        To be able to use properties with setters
        """
        try:
            super().__setattr__(name, value)
        except ValueError as e:
            setters = inspect.getmembers(
                self.__class__,
                predicate=lambda x: isinstance(x, property) and x.fset is not None
            )
            for setter_name, func in setters:
                if setter_name == name:
                    object.__setattr__(self, name, value)
                    break
            else:
                raise e

#setattr(UserIdEntry, 'buffers', Relationship(back_populates="owner"))
#UserIdEntry.__annotations__['buffers'] = List["BufferEntry"]
