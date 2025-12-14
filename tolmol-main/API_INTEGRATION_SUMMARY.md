# API Integration Summary

This document summarizes how the frontend and backend APIs are connected.

## API Service Layer

The frontend uses a centralized API service located at `src/services/api.js` that handles all backend communication using Axios.

### Base Configuration

- **Base URL**: Configurable via `VITE_API_BASE_URL` environment variable
- **Default**: `http://localhost:5050`
- **Credentials**: Cookies/sessions enabled with `withCredentials: true`

## Connected Endpoints

### Authentication APIs

| Frontend Method | Backend Endpoint | Method | Status |
|----------------|------------------|--------|--------|
| `authAPI.register()` | `/api/auth/register` | POST | ✅ Connected |
| `authAPI.login()` | `/api/auth/login` | POST | ✅ Connected |
| `authAPI.logout()` | `/api/auth/logout` | POST | ✅ Connected |
| `authAPI.getCurrentUser()` | `/api/auth/me` | GET | ✅ Connected |

### Auction APIs

| Frontend Method | Backend Endpoint | Method | Status |
|----------------|------------------|--------|--------|
| `auctionsAPI.getAll()` | `/api/auctions` | GET | ✅ Connected |
| `auctionsAPI.getById()` | `/api/auctions/{id}` | GET | ✅ Connected |
| `auctionsAPI.create()` | `/api/auctions` | POST | ✅ Connected |
| `auctionsAPI.placeBid()` | `/api/auctions/{id}/bid` | POST | ✅ Connected |

### Utility APIs

| Frontend Method | Backend Endpoint | Method | Status |
|----------------|------------------|--------|--------|
| `categoriesAPI.getAll()` | `/api/categories` | GET | ✅ Connected |
| `statesAPI.getAll()` | `/api/states` | GET | ✅ Connected |
| `dashboardAPI.getData()` | `/api/dashboard` | GET | ✅ Connected |

## Context Integration

### AuthContext (`src/contexts/AuthContext.jsx`)

- ✅ Uses `authAPI` for all authentication operations
- ✅ Automatically loads user on mount via `authAPI.getCurrentUser()`
- ✅ Handles login, register, and logout through API calls
- ✅ Stores user data in localStorage for persistence

### AuctionContext (`src/contexts/AuctionContext.jsx`)

- ✅ Uses `auctionsAPI` for all auction operations
- ✅ Automatically loads auctions on mount
- ✅ Reloads auctions when filters change (debounced)
- ✅ Handles auction creation, bidding, and updates
- ✅ Fetches individual auctions from API when not in state

## Filter Integration

The search and filter functionality is fully integrated:

1. **Search**: Debounced API calls when search term changes
2. **Category Filter**: Passed as query parameter to backend
3. **Location Filter**: Passed as query parameter to backend
4. **Client-side Filtering**: Additional filtering for price range and status

## Data Flow

```
User Action → Context Function → API Service → Backend API → Response → Context Update → UI Update
```

### Example: Loading Auctions

1. Component mounts → `AuctionProvider` initializes
2. `useEffect` triggers → `loadAuctions()` called
3. `auctionsAPI.getAll(filters)` → Axios request to `/api/auctions`
4. Backend processes request → Returns JSON response
5. Context updates state → Components re-render with new data

### Example: Placing a Bid

1. User submits bid → `placeBid(auctionId, amount)` called
2. `auctionsAPI.placeBid(auctionId, bidData)` → POST to `/api/auctions/{id}/bid`
3. Backend validates and saves bid → Returns bid data
4. Context updates auction state → UI shows new bid immediately

## Error Handling

- All API calls use try-catch blocks
- Errors are captured and displayed to users
- API interceptor handles common error scenarios
- Context provides error state for UI feedback

## Environment Configuration

### Frontend

Create `.env` file in `bid-bazaar-frontend/`:

```env
VITE_API_BASE_URL=http://localhost:5050
```

For production, set this to your deployed backend URL.

### Backend

Update CORS settings in `app.py` to include your frontend URL:

```python
FRONTEND_URL=https://your-frontend.vercel.app
```

## Testing the Integration

1. **Start Backend**: `python main.py` (runs on port 5050)
2. **Start Frontend**: `npm run dev` (runs on port 5173)
3. **Test Authentication**:
   - Register a new user
   - Login with credentials
   - Check user profile
4. **Test Auctions**:
   - View auction list
   - Search and filter auctions
   - View auction details
   - Place a bid (requires login)

## Common Issues

### CORS Errors

- Ensure backend CORS includes frontend URL
- Check `FRONTEND_URL` environment variable in backend

### Authentication Not Working

- Verify `withCredentials: true` in API config
- Check session cookies are being sent
- Ensure backend session management is configured

### API Calls Failing

- Verify `VITE_API_BASE_URL` is set correctly
- Check backend is running and accessible
- Review browser console for error messages
- Check network tab for request/response details

## Next Steps

- [ ] Add SocketIO integration for real-time bid updates
- [ ] Implement pagination for large auction lists
- [ ] Add request caching to reduce API calls
- [ ] Implement retry logic for failed requests
- [ ] Add loading states for better UX

