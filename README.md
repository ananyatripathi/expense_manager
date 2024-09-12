# Expense Manager

## Project Description
The Expense Manager is a Flask-based application designed to manage group expenses. Users can create groups, add expenses, and settle up with other group members. This project uses SQLAlchemy for ORM, Marshmallow for schema validation, and PostgreSQL as the database.

## Folder Structure
expense_manager/ 
│ 
├── app/ 
    │ 
    ├── pycache/ 
    │ 
    ├── init.py 
    │ 
    ├── config.py 
    │ 
    ├── extensions.py 
    │ 
    ├── models.py 
    │ 
    ├── routes.py 
    │ 
    ├── schema.py 
    │ 
    ├── service.py 
    │ 
├── migrations/ 
├── app.py 
├── docker-compose.yml 
├── requirements.txt 
└── .gitignore

## Environment Variables
Set the following environment variable:
DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>


## How to Run the Application
1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd expense_manager
    ```

2. **Create a virtual environment**
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On MacOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Set the environment variables**
    ```bash
    export DATABASE_URL=postgresql://<username>:<password>@<host>:<port>/<database>
    ```

5. **Install the requirements**
    ```bash
    pip install -r requirements.txt
    ```

6. **Run the application**
    ```bash
    python app.py
    ```

## API Endpoints

### Create User
- **URL**: `/user`
- **Method**: `POST`
- **Description**: Create a new user.
- **Request**:
    ```json
    {
        "name": "John Doe"
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "name": "John Doe"
    }
    ```

### Get User
- **URL**: `/user`
- **Method**: `GET`
- **Description**: Get user details by user_id.
- **Request**: `user_id` as query parameter.
- **Response**:
    ```json
    {
        "id": 1,
        "name": "John Doe"
    }
    ```

### Create Group
- **URL**: `/group`
- **Method**: `POST`
- **Description**: Create a new group with users.
- **Request**:
    ```json
    {
        "name": "Friends",
        "members": [1, 2]
    }
    ```
- **Response**:
    ```json
    {
        "id": 1,
        "name": "Friends",
        "members": [1, 2]
    }
    ```

### Get Group
- **URL**: `/group`
- **Method**: `GET`
- **Description**: Get group details by group_id.
- **Request**: `group_id` as query parameter.
- **Response**:
    ```json
    {
        "id": 1,
        "name": "Friends",
        "members": [1, 2]
    }
    ```

### Create Expense
- **URL**: `/expense`
- **Method**: `POST`
- **Description**: Create a new expense.
- **Request**:
    ```json
    {
        "group_id": 1,
        "reason": "Dinner",
        "amount": 100,
        "expense_by": 1,
        "settleups": [
            {
                "expense_to": 2,
                "amount": 50
            },
            {
                "expense_to": 1,
                "amount": 50
            }
        ]
    }
    ```
- **Response**:
    ```json
    {
        "expense_id": 1,
        "reason": "Dinner",
        "amount": 100,
        "expense_by": 1,
        "group_id": 1,
        "settleups": [
            {
                "expense_to": 2,
                "amount_to": 50
            },
            {
                "expense_to": 1,
                "amount_to": 50
            }
        ]
    }
    ```

### Get Expenses
- **URL**: `/expense`
- **Method**: `GET`
- **Description**: Get expenses for a group by group_id.
- **Request**: `group_id` as query parameter.
- **Response**:
    ```json
    {
        "group": {
            "group_id": 1,
            "name": "Friends"
        },
        "expenses": [
            {
                "expense_id": 1,
                "reason": "Dinner",
                "amount": 100,
                "expense_by": 1,
                "settleups": [
                    {
                        "expense_to": 2,
                        "amount_to": 50
                    },
                    {
                        "expense_to": 1,
                        "amount_to": 50
                    }
                ]
            }
        ]
    }
    ```

### Settle Up
- **URL**: `/settleup`
- **Method**: `GET`
- **Description**: Get settle-up details for a user in a group.
- **Request**: `user_id` and `group_id` as query parameters.
- **Response**:
    ```json
    {
        "total_money_get": {
            "2": 200
        },
        "total_money_pay": {
            "2": 600
        },
        "final_settle": {
            "2": -400
        }
    }
    ```

## Contribution
Feel free to fork this repository and make any changes. Pull requests are welcome.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
