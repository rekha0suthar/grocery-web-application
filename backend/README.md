# Grocery Store Backend - PostgreSQL Version

## Render Deployment Instructions

### 1. Environment Variables
Make sure to set these environment variables in your Render service:

- `DATABASE_URL`: Your PostgreSQL connection string from Render
- `FLASK_ENV`: `production`
- `JWT_SECRET_KEY`: Your secret key for JWT tokens

### 2. Database Setup
The application will automatically create the required tables when it starts up.

### 3. API Endpoints
- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /get_token` - User registration
- `POST /user/login` - User login
- `POST /admin/login` - Admin login
- `POST /store_manager/login` - Manager login request
- `GET /admin/login_requests` - Get pending login requests
- `POST /approve_login_requests/<token>` - Approve login request
- `POST /reject_login_requests/<token>` - Reject login request
- `POST /logout` - Logout

### 4. Database Tables
- `users` - User accounts
- `login_requests` - Pending manager login requests
- `categories` - Product categories
- `products` - Product information
- `cart_items` - Shopping cart items
- `orders` - Order information
- `order_items` - Order line items

### 5. Getting Database URL from Render
1. Go to your PostgreSQL service in Render dashboard
2. Copy the "External Database URL"
3. Add it as `DATABASE_URL` environment variable in your web service
