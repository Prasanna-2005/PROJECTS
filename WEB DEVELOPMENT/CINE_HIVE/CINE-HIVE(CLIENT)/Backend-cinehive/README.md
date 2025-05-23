# Movie Catalog Web Application

A comprehensive web application for managing a movie database with admin and user roles, review functionality, and responsive design.

## Tech Stack Overview

### Database
- **MySQL**: Relational database to store movie information, user data, and reviews
  - Handles structured data with relationships between movies, users, and reviews
  - Provides robust transaction support for admin approval workflows
  - Stores image references (paths/URLs) rather than binary image data

### Backend
- **Node.js**: JavaScript runtime for server-side code
- **Express.js**: Web framework for building RESTful APIs
  - Handles HTTP requests and responses
  - Implements middleware for authentication, validation, etc.
  - Manages routing and controller logic
- **MySQL2**: Modern MySQL client for Node.js
- **JWT**: JSON Web Tokens for authentication
- **Multer**: Middleware for handling file uploads

### Frontend
- **React**: JavaScript library for building user interfaces
  - Component-based architecture for reusable UI elements
  - Virtual DOM for efficient rendering
- **React Router**: Client-side routing for single-page application
- **Tailwind CSS**: Utility-first CSS framework
  - Enables rapid UI development
  - Provides responsive design utilities
  - Minimal bundle size with purging unused styles
- **Axios**: Promise-based HTTP client for API requests

## Features

### Admin Portal
- Movie database management (add, edit, delete movies)
- Form-based movie information submission
- Review approval system
- User management

### User Features
- Browse movie catalog
- Search/filter movies by various criteria
- View detailed movie information
- Submit reviews (pending admin approval)
- User registration and authentication

## Database Schema

The application uses the following main tables:
- **users**: Store user account information and roles
- **movies**: Store movie details including references to image files
- **reviews**: Store user reviews with approval status

## File Structure

```
movie-catalog-app/
├── backend/
│   ├── config/         # Database and environment configuration
│   ├── controllers/    # Route handlers
│   ├── routes/         # API routes
│   ├── uploads/        # Storage for uploaded images
│   ├── .env            # Environment variables
│   └── server.js       # Entry point
|   │── package.json
|   │── package-lock.json
|   │── server.js
|
└── frontend/
    ├── public/         # Static assets
    └── src/
    |    ├── components/ # Reusable UI components
    |    ├── contexts/   # React Context for state management
    |    ├── hooks/      # Custom React hooks
    |    ├── pages/      # Page components
    |    ├── services/   # API integration
    |    ├── App.js      # Main component
    |    └── index.js    # Entry point
    │── package.json
    |── package-lock.json
```

## Getting Started

### Prerequisites
- Node.js and npm
- MySQL server
- Git

### Installation
1. Clone the repository
2. Set up the database using the provided SQL schema
3. Configure environment variables
4. Install dependencies for both frontend and backend
5. Run development servers

### Development Environment
- Backend server runs on port 5000
- Frontend development server runs on port 3000
- Local MySQL instance with configured user/password

## Image Storage Strategy

Images are stored as files in the filesystem or cloud storage, with only the references (paths/URLs) stored in the database. This approach:
- Keeps the database efficient
- Enables easier image optimization and CDN integration
- Simplifies backup procedures

## Authentication

The application uses JWT (JSON Web Tokens) for authentication:
- Tokens are issued upon successful login
- Role-based access control for admin vs regular users
- Secure routes using authentication middleware

## Future Enhancements

Potential areas for expansion:
- Advanced search with Elasticsearch
- Social login integration
- User watchlists/favorites
- Mobile app using the same backend API
- Real-time notifications
