# Bid Bazaar Frontend

React + Vite frontend for Bid Bazaar - India's premier reverse auction platform for services.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ 
- npm or pnpm

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

The app will be available at `http://localhost:5173`

## 📦 Build for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 Environment Variables

Create a `.env` file in the root directory:

```env
VITE_API_BASE_URL=http://localhost:5050
```

For production, set this to your deployed backend URL.

## 🏗️ Project Structure

```
src/
├── components/       # React components
│   ├── auth/        # Authentication components
│   ├── auction/     # Auction-related components
│   ├── common/      # Shared components
│   ├── layout/      # Layout components
│   └── ui/          # UI component library
├── contexts/        # React contexts (state management)
├── pages/           # Page components
├── services/        # API service layer
├── utils/           # Utility functions
└── types/           # Type definitions
```

## 🛠️ Tech Stack

- **React 19** - UI library
- **Vite** - Build tool
- **React Router** - Routing
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **Radix UI** - Component primitives
- **Lucide React** - Icons

## 📡 API Integration

All API calls are handled through the service layer in `src/services/api.js`.

### Available APIs

- `authAPI` - Authentication (login, register, logout)
- `auctionsAPI` - Auction operations (list, create, bid)
- `categoriesAPI` - Service categories
- `statesAPI` - Indian states list
- `dashboardAPI` - User dashboard data

## 🚢 Deployment

### Deploy to Vercel

See [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md) for detailed deployment instructions.

Quick steps:
1. Push code to Git repository
2. Import to Vercel
3. Set root directory to `bid-bazaar-frontend`
4. Add environment variable `VITE_API_BASE_URL`
5. Deploy!

## 📝 Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

## 🔍 Features

- ✅ User authentication (register, login, logout)
- ✅ Auction listing with search and filters
- ✅ Real-time bid updates
- ✅ Responsive design
- ✅ Error handling
- ✅ Loading states
- ✅ Form validation

## 🐛 Troubleshooting

### Build Errors

- Ensure Node.js version is 18+
- Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
- Check for missing dependencies

### API Connection Issues

- Verify `VITE_API_BASE_URL` is set correctly
- Check backend is running and accessible
- Verify CORS settings in backend

### Routing Issues

- Ensure `vercel.json` has correct rewrites for SPA routing
- Check that all routes are defined in `App.jsx`

## 📚 Documentation

- [Backend Documentation](../BACKEND_DOCUMENTATION.md)
- [API Integration Summary](../API_INTEGRATION_SUMMARY.md)
- [Deployment Guide](./VERCEL_DEPLOYMENT.md)

## 📄 License

MIT
