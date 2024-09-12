from .extensions import db

user_group = db.Table('user_group', 
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
                      )

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(120), nullable=False)
    groups=db.relationship('Group', secondary=user_group, backref=db.backref('users', lazy='dynamic'))
    expenses=db.relationship('Expense', backref='user', lazy=True, foreign_keys='Expense.expense_by', cascade="all,delete",)
    settleups=db.relationship('Settleup', backref='user', lazy=True, foreign_keys='Settleup.expense_to')
    
    def __repr__(self):
        return f'<User {self.name}>'

class Group(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.String(120), nullable=False)
    expenses=db.relationship('Expense', backref='group', lazy=True, foreign_keys='Expense.group_id')
    
    def __repr__(self):
        return f'<Group {self.name}>'

class Expense(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_id=db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    reason=db.Column(db.String(200), nullable=True)
    amount=db.Column(db.Float, nullable=False)
    expense_by=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    settleups=db.relationship('Settleup', backref='expense', lazy=True)
    
    def __repr__(self):
        return f'<Expense Id {self.id}>'

class Settleup(db.Model):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    expense_id=db.Column(db.Integer, db.ForeignKey('expense.id'), nullable=False)
    expense_to=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    amount=db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<Expense Id {self.id}>'

    
    
    