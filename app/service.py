
from sqlalchemy import and_
from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Group, Expense, Settleup
from app.schema import ExpenseSchema,UserSchema, GroupSchema
from marshmallow import ValidationError

def create_user_logic(data):
    schema = UserSchema()
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        raise Exception(err)
    
    username=validated_data.get('name')
    
    if not username:
        raise Exception('Name is required')
    
    new_user=User(name=username)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_user_logic(user_id):
    if not user_id:
        raise Exception('Pass user_id as query parameter')
    
    user_id = int(user_id)
    user = User.query.get(user_id)
    
    if not user:
        raise Exception('Could not find user')
    return user

def create_group_logic(data):
    schema = GroupSchema()
    
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        raise Exception(err)
    
    group_name=validated_data.get('name')
    member_ids=validated_data.get('members')
    
    if not group_name:
        raise Exception('Group name is required')
    
    if not member_ids or len(member_ids) == 0:
        raise Exception('Atleast add one member in the group')
    
    members = User.query.filter(User.id.in_(member_ids)).all()
    if len(members) != len(member_ids):
        raise Exception('One or more user IDs are invalid')
    
    new_group = Group(name=group_name)
    db.session.add(new_group)
    db.session.commit()
    
    for user in members:
        new_group.users.append(user)
    
    db.session.commit()
    return new_group, members

def get_group_logic(group_id):
    if not group_id:
        raise Exception('Pass group_id as query parameter')
    
    group_id = int(group_id)
    group = Group.query.get(group_id)
    members = [{'id':user.id, 'name':user.name} for user in group.users]
    if not group:
        raise  Exception('Could not find group')
    return group, members

def create_expense_logic(data):
    schema = ExpenseSchema()
    
    try:
        validated_data = schema.load(data)
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    reason = validated_data.get('reason')
    expense_by = validated_data.get('expense_by')
    expense_to = validated_data.get("expense_to")
    amount = validated_data.get("amount")
    group_id = validated_data.get("group_id")

    # Validate expense_by user
    payer = User.query.get(expense_by)
    if not payer:
        raise Exception('expense_by user not found')
    
    # Validate users in expense_to
    expense_to_user_ids = [entry['user_id'] for entry in expense_to]
    payees = User.query.filter(User.id.in_(expense_to_user_ids)).all()
    if len(payees) != len(expense_to_user_ids):
        raise Exception('One or more expense_to users not found')
    
    group = Group.query.get(group_id)
    if not group:
        raise Exception('group_id not found')

    new_expense = Expense(reason=reason, amount=amount, expense_by=expense_by, group_id=group_id)
    db.session.add(new_expense)
    db.session.commit()
    
    for entry in expense_to:
        settleup = Settleup(expense_id=new_expense.id, expense_to=entry["user_id"], amount=entry["amount"])
        db.session.add(settleup)
    
    db.session.commit()
    return new_expense

def get_expense_logic(group_id):
    if not group_id:
        raise Exception('Pass group_id as query parameter')
    
    group = Group.query.get(group_id)
    if not group:
        raise Exception('Group not found')

    # Fetch expenses for the group
    expenses = Expense.query.filter_by(group_id=group_id).all()
    expenses_list = []
    for expense in expenses:
        settleups = [{'expense_to': s.expense_to, 'amount': s.amount} for s in expense.settleups]
        expenses_list.append({
            'id': expense.id,
            'reason': expense.reason,
            'amount': expense.amount,
            'expense_by': expense.expense_by,
            'settleups': settleups
        })
    return group, expenses_list

def settle_up_logic(user_id, group_id):
    if not user_id or not group_id:
        raise Exception("user_id and group_id are required parameters")
    
    try:
        user_id = int(user_id)
        group_id = int(group_id)
    except ValueError:
        raise Exception('user_id and group_id must be integers')
    
    user = User.query.get(user_id)
    group = Group.query.get(group_id)
    
    if not user or not group:
        raise Exception('Invalid user_id or group_id')
    
    if user not in group.users:
        raise Exception('User is not a member of the group')
    
    result = calculate_settle_up(user_id, group_id)
    return result

def calculate_settle_up(user_id, group_id):
    expenses = Expense.query.filter(and_(Expense.group_id==group_id, Expense.expense_by==user_id)).all()
    total_money_get = {} #people who need to pay me
    

    for expense in expenses:
        settleups = Settleup.query.filter(and_(Settleup.expense_id == expense.id, Settleup.expense_to != user_id )).all()
        
        for settleup in settleups:
            if(settleup.expense_to in total_money_get):
                total_money_get[settleup.expense_to]+=settleup.amount
            else:
                total_money_get[settleup.expense_to]=settleup.amount
    
    total_money_pay = {}
    expenses_new = Expense.query.filter(and_(Expense.group_id==group_id, Expense.expense_by!=user_id)).all()
    for expense in expenses_new:
        settleups = Settleup.query.filter(and_(Settleup.expense_id == expense.id, Settleup.expense_to == user_id )).all()
        
        for settleup in settleups:
            if(expense.expense_by in total_money_pay):
                total_money_pay[expense.expense_by]+=settleup.amount
            else:
                total_money_pay[expense.expense_by]=settleup.amount
    
    

    # Calculate final amounts
    final_settle_up = {}

    # Subtract total money pay from total money get
    for user in total_money_get:
        if user in total_money_pay:
            final_settle_up[user] = total_money_get[user] - total_money_pay[user]
        else:
            final_settle_up[user] = total_money_get[user]

    for user in total_money_pay:
        if user not in total_money_get:
            final_settle_up[user] = -total_money_pay[user]

    return {
        "total_owed_to_user": sum(total_money_get.values()),
        "total_owing_by_user": sum(total_money_pay.values()),
        "final_settle_up": final_settle_up
    }
