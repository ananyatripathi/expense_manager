import os

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://admin:admin@localhost/expense-manager"
    SQLALCHEMY_TRACK_MODIFICATIONS = False