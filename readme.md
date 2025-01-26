# Book Library

The Book Library project is a web-based system built using Python Flask for the back-end and Jinja for server-side rendering. This project is designed to manage the operations of a university library, providing an efficient and user-friendly interface for both students and administrators.

## Screenshot

![App Screenshot](https://raw.githubusercontent.com/SherazAsghar37/Book-Library/refs/heads/main/screenshots/image.png)

[All Screenshots](https://github.com/SherazAsghar37/Book-Library/tree/main/screenshots)

## Appendix

This project is designed to give university students a solid foundation and valuable insight into building a library management system for their upcoming projects. It helps them understand key concepts like book management, borrowing tracking, and system functionality in a real-world context.

## Technologies Used

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, Bootstrap, and Jinja for templating
- **Database**: SQLite
- **Authentication**: Flask Login for user authentication

## Features

### For Students:

- **Registration & Login**: Students can register, log in, and manage their accounts.
- **Book Search & Cart**: Students can browse available books, add them to their cart, and borrow them.

### For Administrators:

- **Admin Panel**: Admins can manage the entire library system from a dedicated panel.
- **Book Management**: Add, edit, and remove books from the library collection.
- **Student Management**: View all students, their details, and which books are assigned to them.
- **Order Management**: Admins can fulfill student orders and monitor the status of borrowed books.

## Setup

1. Create virutal enviroment

   ```
   python -m venv .venv
   ```

2. Navigate to this virtual enviroment
   ```
   cd .venv
   ```
3. Clone this repository
   ```
   git clone https://github.com/SherazAsghar37/Book-Library
   ```
4. Navigate to the cloned code
   ```
   cd book-library
   ```
5. Install requirements
   ```
   pip install -r requirements.txt
   ```
6. Finally run the project

```
   flask run
```
