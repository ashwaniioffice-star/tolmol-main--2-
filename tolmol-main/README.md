# Bid Bazaar - Fullstack Application

This repository contains both the frontend (React.js) and backend (Flask) components of the Bid Bazaar service auction platform.

## Project Structure

```

tolmol-main/
├── bid-bazaar-frontend/  # React.js frontend application (Vite + React)
└── bid-bazaar-backend/   # Flask backend application with SocketIO

```

## Getting Started

Follow these steps to set up and run the fullstack application locally.

### Prerequisites

- **Node.js** (version 16 or higher)
- **pnpm** (recommended) or npm
- **Python 3.9+**
- **pip** (Python package installer)

### 1. Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd bid-bazaar-backend
```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the `bid-bazaar-backend/` directory (see `.env.example`):
   ```env
   SECRET_KEY=your-secret-key-change-in-production
   DATABASE_URL=sqlite:///bidding_platform.db
   FLASK_ENV=development
   FLASK_DEBUG=True
   FRONTEND_URL=http://localhost:5173
   ```

5. **Start the backend server**:
   ```bash
   python main.py
   ```

   The backend server will run on `http://localhost:5050` and automatically create database tables.

### 2. Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd bid-bazaar-frontend
   ```

2. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment variables**:
   Create a `.env` file in the `bid-bazaar-frontend/` directory:
   ```env
   VITE_API_BASE_URL=http://localhost:5050
   ```

4. **Start the frontend development server**:
   ```bash
   npm run dev
   ```

   The frontend application will be available at `http://localhost:5173`.

## Usage

Once both the frontend and backend servers are running:

- Open your web browser and navigate to `http://localhost:5173` to access the Bid Bazaar application.
- You can interact with the application, including browsing auctions, logging in, and registering.

## API Endpoints (Backend)

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user

### Auctions
- `GET /api/auctions` - Get auction listings (with filters)
- `GET /api/auctions/{id}` - Get auction details
- `POST /api/auctions` - Create auction (requires auth)
- `POST /api/auctions/{id}/bid` - Place bid (requires auth)

### Other
- `GET /api/categories` - Get service categories
- `GET /api/states` - Get Indian states list
- `GET /api/dashboard` - Get user dashboard data (requires auth)

For detailed API documentation, see `BACKEND_DOCUMENTATION.md`.

## Deployment

For deployment instructions, see `DEPLOYMENT.md`. The frontend can be deployed to Vercel, while the backend should be deployed to Railway, Render, or Heroku.

## Troubleshooting

- **Port conflicts**: Ensure no other applications are using ports `5050` (backend) or `5173` (frontend).
- **Backend issues**: Check the console output and ensure all dependencies are installed.
- **Frontend issues**: Check your browser's developer console and ensure the API URL is correct.
- **Database issues**: Ensure the database file has write permissions (for SQLite) or database credentials are correct (for PostgreSQL).
- **CORS errors**: Update the `FRONTEND_URL` environment variable in the backend to match your frontend URL.

## License

This project is licensed under the MIT License.

```

```
