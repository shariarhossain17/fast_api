from sqlalchemy import Column, String, UniqueConstraint, integer

from .database import Base


class User(Base):
    __tablename__="users"

    id = Column (
        integer,
        primary_key=True,
        index=True
    )


    #email column
    email = Column (
        String(255),
        nullable=False,
        unique=True,
        index=True

    )


    #user_name column
    username = Column (
        String(50),
        nullable=False,
        unique=True,
        index=True

    )

    __table_args__= (
        UniqueConstraint("email",name='uq_users_email'),
        UniqueConstraint("username",name="uq_users_username"),
    )

    def __repr__(self):
        """String representation of user of user object"""
        return f"<User (id={self.id}),email='{self.email}',username='{self.username}'"
