This project is a web-based flight booking system called "AeroTrack" built with Flask and MySQL. It allows users to:

Sign up, log in, and manage their profiles.
Search for available flights by source, destination, and date.
Book flights with seat and meal selection.
Make payments using UPI or card.
Submit feedback and access support.
View a dashboard with navigation to all main features.
The backend uses MySQL for data storage, and the frontend uses Bootstrap for responsive design. All user and booking data is securely managed, including password hashing. The project structure includes templates for all user-facing pages and a SQL schema for the database. The main application logic is implemented in app.py.

Main Application (app.py):
This is the core of the Flask-based flight booking system. It handles routing and backend logic.

Database Schema (schema.sql):
This file contains the SQL commands to set up the database structure, including tables for users, flights, bookings, payments, and feedback.

Templates Directory:
Contains HTML files for various web pages:
User Authentication: login.html, signup.html
Flight Management: search_flight.html, book_flight.html
Booking Confirmation: booking_success.html
User Profile: profile.html
Feedback: feedback.html
Support: support.html
Dashboard: dashboard.html
Base Layout: base.html for consistent page structure

Server will start at http://127.0.0.1:5000/ by default
