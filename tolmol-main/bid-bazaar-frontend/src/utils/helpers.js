import { formatDistanceToNow, format, isAfter } from 'date-fns';

// Format currency in Indian Rupees
export const formatCurrency = (amount) => {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(amount);
};

// Format time remaining for auction
export const formatTimeRemaining = (endTime) => {
  const now = new Date();
  const end = new Date(endTime);
  
  if (isAfter(now, end)) {
    return 'Expired';
  }
  
  return formatDistanceToNow(end, { addSuffix: true });
};

// Format date for display
export const formatDate = (date) => {
  return format(new Date(date), 'MMM dd, yyyy HH:mm');
};

// Check if auction is expired
export const isAuctionExpired = (endTime) => {
  return isAfter(new Date(), new Date(endTime));
};

// Calculate time remaining in seconds
export const getTimeRemainingSeconds = (endTime) => {
  const now = new Date();
  const end = new Date(endTime);
  const diff = end.getTime() - now.getTime();
  return Math.max(0, Math.floor(diff / 1000));
};

// Validate email format
export const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
};

// Validate phone number (Indian format)
export const isValidPhone = (phone) => {
  const phoneRegex = /^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$/;
  return phoneRegex.test(phone.replace(/\s/g, ''));
};

// Generate random ID for mock data
export const generateId = () => {
  return Math.random().toString(36).substr(2, 9);
};

// Debounce function for search
export const debounce = (func, wait) => {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
};

// Local storage helpers
export const storage = {
  get: (key) => {
    try {
      const item = localStorage.getItem(key);
      return item ? JSON.parse(item) : null;
    } catch (error) {
      console.error('Error reading from localStorage:', error);
      return null;
    }
  },
  
  set: (key, value) => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error('Error writing to localStorage:', error);
    }
  },
  
  remove: (key) => {
    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error('Error removing from localStorage:', error);
    }
  }
};

// API error handler
export const handleApiError = (error) => {
  if (error.response) {
    // Server responded with error status
    return error.response.data.message || 'Server error occurred';
  } else if (error.request) {
    // Request was made but no response received
    return 'Network error. Please check your connection.';
  } else {
    // Something else happened
    return 'An unexpected error occurred';
  }
};

// Format auction status
export const getAuctionStatus = (auction) => {
  if (!auction.is_active) {
    return { status: 'inactive', label: 'Inactive', color: 'gray' };
  }
  
  if (isAuctionExpired(auction.end_time)) {
    return { status: 'expired', label: 'Expired', color: 'red' };
  }
  
  const timeLeft = getTimeRemainingSeconds(auction.end_time);
  if (timeLeft < 3600) { // Less than 1 hour
    return { status: 'ending_soon', label: 'Ending Soon', color: 'orange' };
  }
  
  if (auction.is_hot_deal) {
    return { status: 'hot_deal', label: 'Hot Deal', color: 'red' };
  }
  
  return { status: 'active', label: 'Active', color: 'green' };
};

// Sort auctions by various criteria
export const sortAuctions = (auctions, sortBy) => {
  const sorted = [...auctions];
  
  switch (sortBy) {
    case 'newest':
      return sorted.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    case 'oldest':
      return sorted.sort((a, b) => new Date(a.created_at) - new Date(b.created_at));
    case 'ending_soon':
      return sorted.sort((a, b) => new Date(a.end_time) - new Date(b.end_time));
    case 'lowest_bid':
      return sorted.sort((a, b) => (a.current_bid || a.starting_bid) - (b.current_bid || b.starting_bid));
    case 'highest_bid':
      return sorted.sort((a, b) => (b.current_bid || b.starting_bid) - (a.current_bid || a.starting_bid));
    default:
      return sorted;
  }
};

// Filter auctions based on criteria
export const filterAuctions = (auctions, filters) => {
  return auctions.filter(auction => {
    // Search filter
    if (filters.search) {
      const searchLower = filters.search.toLowerCase();
      const matchesSearch = 
        auction.title.toLowerCase().includes(searchLower) ||
        auction.description.toLowerCase().includes(searchLower) ||
        auction.location.toLowerCase().includes(searchLower);
      if (!matchesSearch) return false;
    }
    
    // Category filter
    if (filters.category && auction.category !== filters.category) {
      return false;
    }
    
    // Location filter
    if (filters.location) {
      const locationLower = filters.location.toLowerCase();
      const matchesLocation = 
        auction.location.toLowerCase().includes(locationLower) ||
        auction.city.toLowerCase().includes(locationLower) ||
        auction.state.toLowerCase().includes(locationLower);
      if (!matchesLocation) return false;
    }
    
    // Price range filter
    if (filters.minPrice || filters.maxPrice) {
      const currentBid = auction.current_bid || auction.starting_bid;
      if (filters.minPrice && currentBid < filters.minPrice) return false;
      if (filters.maxPrice && currentBid > filters.maxPrice) return false;
    }
    
    // Status filter
    if (filters.status) {
      const auctionStatus = getAuctionStatus(auction);
      if (auctionStatus.status !== filters.status) return false;
    }
    
    return true;
  });
};

