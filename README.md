# Girl Power Club

A social platform for elementary school girls in Singapore to connect, share experiences, and empower each other.

## Features

- Membership application system
- Admin approval process
- User login and profiles
- Social media posting and commenting

## Technologies Used

- Django web framework
- TailwindCSS for styling
- SQLite database

## Setup Instructions

1. Clone the repository
2. Create a virtual environment:
   ```
   python3 -m venv venv
   ```
3. Activate the virtual environment:
   ```
   source venv/bin/activate
   ```
4. Install dependencies:
   ```
   pip install django django-tailwind
   ```
5. Apply database migrations:
   ```
   python manage.py migrate
   ```
6. Create a superuser (admin account):
   ```
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```
   python manage.py runserver
   ```
8. Access the site at: http://127.0.0.1:8000/

## Admin Access

1. Go to http://127.0.0.1:8000/admin/
2. Log in with the superuser credentials
3. You can manage users, membership applications, posts, and comments from the admin panel

## Using the Platform

### For Admins
1. View pending applications at: http://127.0.0.1:8000/admin/applications/
2. Approve applications and create user accounts for new members

### For Users
1. Students apply to join at: http://127.0.0.1:8000/join/
2. Once approved, they can log in with the credentials provided by admin
3. They can create and comment on posts, and update their profiles

## Powerpuff Girls Color Scheme

The site uses a color scheme inspired by the Powerpuff Girls:
- Pink (Blossom): #FF99CC
- Blue (Bubbles): #72C8F8  
- Green (Buttercup): #98D46D
- Purple (Accent): #8E6BB5
- Yellow (Accent): #FFF06A