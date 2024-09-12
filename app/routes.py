from flask import Blueprint, request, jsonify
from app import db
from app.models import User, Group, Expense, Settleup
from app.schema import ExpenseSchema,UserSchema, GroupSchema
from marshmallow import ValidationError
from sqlalchemy import and_
import app.service as service

routes = Blueprint('routes', __name__)

@routes.route("/user", methods=['POST'])
def create_user():
    try:
        data=request.get_json()
        new_user = service.create_user_logic(data)
        return jsonify({'id':new_user.id, 'name':new_user.name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

@routes.route("/user", methods=['GET'])
def get_user():
    try:
        user_id = request.args.get('user_id')
        user = service.get_user_logic(user_id)
        return jsonify({'id':user.id, 'name':user.name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 
  
@routes.route("/group", methods=['POST'])
def create_group():
    try:
        data=request.get_json()
        new_group, members = service.create_group_logic(data)
        return jsonify({'id': new_group.id, 'name': new_group.name, 'members': [user.id for user in members]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400 

@routes.route("/group", methods=['GET'])
def get_group():
    try:
        group_id = request.args.get('group_id')
        group, members = service.get_group_logic(group_id)
        return jsonify({'id':group.id, 'name':group.name, 'members':members}), 200
    except Exception as e:
            return jsonify({'error': str(e)}), 400 
    
@routes.route("/expense", methods=['POST'])
def create_expense():
    try:
        data=request.get_json()
        new_expense = service.create_expense_logic(data)
        return jsonify({
            'expense_id': new_expense.id,
            'reason': new_expense.reason,
            'amount': new_expense.amount,
            'expense_by': new_expense.expense_by,
            'group_id': new_expense.group_id,
            'settleups': [{'expense_to': s.expense_to, 'amount_to': s.amount} for s in new_expense.settleups]
        }), 200
    except Exception as e:
            return jsonify({'error': str(e)}), 400

@routes.route("/expense", methods=['GET'])
def get_expense():
    try:
        group_id = request.args.get('group_id')
        group, expenses_list = service.get_expense_logic(group_id)
        return jsonify({
            'group': {'group_id': group.id, 'name': group.name},
            'expenses': expenses_list,
        }), 200
    except Exception as e:
            return jsonify({'error': str(e)}), 400
    
@routes.route('/settleup', methods=['GET'])
def settle_up():
    try:
        user_id = request.args.get('user_id')
        group_id = request.args.get('group_id')
        result = service.settle_up_logic(user_id, group_id)
        return jsonify(result)
    except Exception as e:
            return jsonify({'error': str(e)}), 400

