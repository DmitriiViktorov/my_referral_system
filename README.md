

# Referral System API
## Create table and user

Make sure that PostgreSQL is installed and running on your local device. Check its status using the command:

  ```bash
    sudo systemctl status postgresql
  ```

After ensuring that PostgreSQL is running, execute the `init.sql` script to create the user, database, and assign the necessary permissions.

1. Connect to PostgreSQL as an administrator:
   ```bash
   sudo -u postgres psql

2. Execute the init.sql script:
   ```sql
   \i init.sql 
 
3. Verify that the database and user were created:
   ```sql
   \l -- List of databases
   \du -- List of users

### Running the Application

Once the database is initialized, you can start the Django application by following these steps:

1. Cloning a repository:

    To install, clone the repository using the following command:
      ```bash
      https://github.com/DmitriiViktorov/my_referral_system.git

2. Create virtual environment and install requirements:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   cd my_referral_system/
   pip install -r requirements.txt

3. Apply migrations to set up the database schema:
   ```bash
   python manage.py migrate

4. Start the development server:
   ```bash
   python manage.py runserver

5. Open your browser and navigate to:
   ```bash
   http://127.0.0.1:8000

## Endpoints

### Authentication

- **URL:** `/api/auth/`
- **Method:** `POST`
- **Description:** Sends a 4-digit authentication code to the provided phone number.
- **Request Body:**
  ```json
  {
    "phone_number": "1234567890"
  }
  ```
  
- **Response:**
  ```json
  {
    "code": "1234"
  }
  ```
### Verify Code

- **URL:** `/api/verify/`
- **Method:** `POST`
- **Description:** Verifies the authentication code and authenticates the user.
- **Request Body:**
  ```json
  {
    "phone_number": "1234567890",
    "code": "1234"
  }
  ```

- **Response:**
  ```json
  {
    "message": "User authenticated",
    "user_id": 1
  }
  ```

### Profile

- **URL:** `/api/profile/<user_id>/`
- **Method:** `GET`
- **Description:** Retrieves the user profile.
- **Response:**
  ```json
  {
    "phone_number": "1234567890",
    "invite_code": "ABC123",
    "referred_by": "9876543210",
    "referred_users": ["5555555555", "6666666666"]
  }
  ```

## Apply Invite Code

- **URL:** `/api/profile/<user_id>/`
- **Method:** `POST`
- **Description:** Applies an invite code to the user's profile.
- **Request Body:**
  ```json
  {
    "invite_code": "ABC123"
  }
  ```
  
- **Response:**
  ```json
  {
    "message": "Invite code applied"
  }
  ```


