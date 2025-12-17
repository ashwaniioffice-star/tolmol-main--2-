import React, { createContext, useContext, useReducer, useEffect, useCallback } from 'react';
import { filterAuctions, sortAuctions } from '../utils/helpers';
import { auctionsAPI } from '../services/api';

// Auction context
const AuctionContext = createContext();

// Auction actions
const AUCTION_ACTIONS = {
  LOAD_AUCTIONS_START: 'LOAD_AUCTIONS_START',
  LOAD_AUCTIONS_SUCCESS: 'LOAD_AUCTIONS_SUCCESS',
  LOAD_AUCTIONS_FAILURE: 'LOAD_AUCTIONS_FAILURE',
  CREATE_AUCTION_START: 'CREATE_AUCTION_START',
  CREATE_AUCTION_SUCCESS: 'CREATE_AUCTION_SUCCESS',
  CREATE_AUCTION_FAILURE: 'CREATE_AUCTION_FAILURE',
  PLACE_BID_START: 'PLACE_BID_START',
  PLACE_BID_SUCCESS: 'PLACE_BID_SUCCESS',
  PLACE_BID_FAILURE: 'PLACE_BID_FAILURE',
  UPDATE_AUCTION: 'UPDATE_AUCTION',
  SET_FILTERS: 'SET_FILTERS',
  SET_SORT: 'SET_SORT',
  CLEAR_ERROR: 'CLEAR_ERROR'
};

// Initial state
const initialState = {
  auctions: [],
  filteredAuctions: [],
  isLoading: false,
  error: null,
  filters: {
    search: '',
    category: '',
    location: '',
    minPrice: '',
    maxPrice: '',
    status: ''
  },
  sortBy: 'newest'
};

// Auction reducer
const auctionReducer = (state, action) => {
  switch (action.type) {
    case AUCTION_ACTIONS.LOAD_AUCTIONS_START:
    case AUCTION_ACTIONS.CREATE_AUCTION_START:
    case AUCTION_ACTIONS.PLACE_BID_START:
      return {
        ...state,
        isLoading: true,
        error: null
      };
      
    case AUCTION_ACTIONS.LOAD_AUCTIONS_SUCCESS: {
      const sortedAuctions = sortAuctions(action.payload, state.sortBy);
      const filteredAuctions = filterAuctions(sortedAuctions, state.filters);
      return {
        ...state,
        isLoading: false,
        auctions: action.payload,
        filteredAuctions,
        error: null
      };
    }
      
    case AUCTION_ACTIONS.CREATE_AUCTION_SUCCESS: {
      const newAuctions = [action.payload, ...state.auctions];
      const newSortedAuctions = sortAuctions(newAuctions, state.sortBy);
      const newFilteredAuctions = filterAuctions(newSortedAuctions, state.filters);
      return {
        ...state,
        isLoading: false,
        auctions: newAuctions,
        filteredAuctions: newFilteredAuctions,
        error: null
      };
    }
      
    case AUCTION_ACTIONS.PLACE_BID_SUCCESS: {
      const updatedAuctions = state.auctions.map(auction =>
        auction.id === action.payload.auctionId
          ? {
              ...auction,
              current_bid: action.payload.amount,
              bids: [action.payload.bid, ...auction.bids]
            }
          : auction
      );
      const updatedSortedAuctions = sortAuctions(updatedAuctions, state.sortBy);
      const updatedFilteredAuctions = filterAuctions(updatedSortedAuctions, state.filters);
      return {
        ...state,
        isLoading: false,
        auctions: updatedAuctions,
        filteredAuctions: updatedFilteredAuctions,
        error: null
      };
    }
      
    case AUCTION_ACTIONS.UPDATE_AUCTION: {
      const auctionsWithUpdate = state.auctions.map(auction =>
        auction.id === action.payload.id
          ? { ...auction, ...action.payload.updates }
          : auction
      );
      const sortedWithUpdate = sortAuctions(auctionsWithUpdate, state.sortBy);
      const filteredWithUpdate = filterAuctions(sortedWithUpdate, state.filters);
      return {
        ...state,
        auctions: auctionsWithUpdate,
        filteredAuctions: filteredWithUpdate
      };
    }
      
    case AUCTION_ACTIONS.LOAD_AUCTIONS_FAILURE:
    case AUCTION_ACTIONS.CREATE_AUCTION_FAILURE:
    case AUCTION_ACTIONS.PLACE_BID_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.payload
      };
      
    case AUCTION_ACTIONS.SET_FILTERS: {
      const newFilters = { ...state.filters, ...action.payload };
      // Filter locally for immediate UI update, but API will be called via useEffect
      const filteredWithNewFilters = filterAuctions(
        sortAuctions(state.auctions, state.sortBy),
        newFilters
      );
      return {
        ...state,
        filters: newFilters,
        filteredAuctions: filteredWithNewFilters
      };
    }
      
    case AUCTION_ACTIONS.SET_SORT: {
      const newSortBy = action.payload;
      const sortedWithNewSort = sortAuctions(state.auctions, newSortBy);
      const filteredWithNewSort = filterAuctions(sortedWithNewSort, state.filters);
      return {
        ...state,
        sortBy: newSortBy,
        filteredAuctions: filteredWithNewSort
      };
    }
      
    case AUCTION_ACTIONS.CLEAR_ERROR:
      return {
        ...state,
        error: null
      };
      
    default:
      return state;
  }
};

// Auction provider component
export const AuctionProvider = ({ children }) => {
  const [state, dispatch] = useReducer(auctionReducer, initialState);

  // Mock auctions for fallback when API is unavailable
  const getMockAuctions = () => {
    const now = new Date();
    return [
      {
        id: 1,
        title: 'Professional House Cleaning - 3BHK Apartment',
        description: 'Need professional deep cleaning for a 3BHK apartment in Koramangala. Kitchen, bathrooms, and all rooms. Eco-friendly products preferred. Available this weekend.',
        category: 'cleaning',
        location: 'Koramangala, Bangalore',
        starting_bid: 3000,
        current_bid: 2500,
        end_time: new Date(now.getTime() + 24 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: true,
        created_at: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(),
        creator_id: 1,
        location_type: 'city',
        city: 'Bangalore',
        state: 'karnataka',
        radius_km: 50,
        creator: { username: 'homeowner_bangalore', email: 'home@example.com' },
        bids: [
          { id: 1, amount: 2800, created_at: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(), bidder: { username: 'cleanpro1' } },
          { id: 2, amount: 2500, created_at: new Date(now.getTime() - 1 * 60 * 60 * 1000).toISOString(), bidder: { username: 'cleanpro2' } }
        ]
      },
      {
        id: 2,
        title: 'Math & Physics Tutoring - Class 12 CBSE',
        description: 'Looking for experienced tutor for Class 12 CBSE student. Need help with advanced mathematics and physics. Prefer home visits in Noida. 2-3 sessions per week.',
        category: 'tutoring',
        location: 'Sector 62, Noida',
        starting_bid: 2000,
        current_bid: 1800,
        end_time: new Date(now.getTime() + 48 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: false,
        created_at: new Date(now.getTime() - 5 * 60 * 60 * 1000).toISOString(),
        creator_id: 2,
        location_type: 'local',
        city: 'Noida',
        state: 'uttar-pradesh',
        radius_km: 10,
        creator: { username: 'parent_noida', email: 'parent@example.com' },
        bids: [
          { id: 3, amount: 1900, created_at: new Date(now.getTime() - 4 * 60 * 60 * 1000).toISOString(), bidder: { username: 'tutor_expert' } },
          { id: 4, amount: 1800, created_at: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(), bidder: { username: 'tutor_pro' } }
        ]
      },
      {
        id: 3,
        title: 'Logo & Brand Identity Design for Tech Startup',
        description: 'Need complete brand identity design for new fintech startup. Logo, color palette, typography, and brand guidelines. Modern, professional, and trustworthy feel. Deliverables: Logo variations, style guide, and brand book.',
        category: 'design',
        location: 'Pune, Maharashtra',
        starting_bid: 15000,
        current_bid: 12000,
        end_time: new Date(now.getTime() + 72 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: true,
        created_at: new Date(now.getTime() - 6 * 60 * 60 * 1000).toISOString(),
        creator_id: 3,
        location_type: 'state',
        city: 'Pune',
        state: 'maharashtra',
        radius_km: 500,
        creator: { username: 'startup_founder', email: 'founder@startup.com' },
        bids: [
          { id: 5, amount: 13000, created_at: new Date(now.getTime() - 5 * 60 * 60 * 1000).toISOString(), bidder: { username: 'design_studio' } },
          { id: 6, amount: 12000, created_at: new Date(now.getTime() - 3 * 60 * 60 * 1000).toISOString(), bidder: { username: 'creative_agency' } }
        ]
      },
      {
        id: 4,
        title: 'Home Repair - Plumbing & Electrical Work',
        description: 'Need comprehensive home repair service. Fix leaking pipes in kitchen and bathroom, install new electrical outlets in living room, and repair broken tiles. Professional work required with warranty.',
        category: 'home_repair',
        location: 'Andheri West, Mumbai',
        starting_bid: 5000,
        current_bid: 4500,
        end_time: new Date(now.getTime() + 36 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: false,
        created_at: new Date(now.getTime() - 3 * 60 * 60 * 1000).toISOString(),
        creator_id: 4,
        location_type: 'city',
        city: 'Mumbai',
        state: 'maharashtra',
        radius_km: 50,
        creator: { username: 'mumbai_homeowner', email: 'home@mumbai.com' },
        bids: [
          { id: 7, amount: 4800, created_at: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(), bidder: { username: 'repair_expert' } },
          { id: 8, amount: 4500, created_at: new Date(now.getTime() - 1 * 60 * 60 * 1000).toISOString(), bidder: { username: 'handyman_pro' } }
        ]
      },
      {
        id: 5,
        title: 'Website Development - E-commerce Platform',
        description: 'Build a complete e-commerce website for fashion retail. Features needed: Product catalog, shopping cart, payment gateway integration, admin dashboard, and mobile responsive design. Tech stack: React/Next.js preferred.',
        category: 'tech_support',
        location: 'Gurgaon, Haryana',
        starting_bid: 50000,
        current_bid: 45000,
        end_time: new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: true,
        created_at: new Date(now.getTime() - 12 * 60 * 60 * 1000).toISOString(),
        creator_id: 5,
        location_type: 'state',
        city: 'Gurgaon',
        state: 'haryana',
        radius_km: 500,
        creator: { username: 'business_owner', email: 'business@gurgaon.com' },
        bids: [
          { id: 9, amount: 48000, created_at: new Date(now.getTime() - 10 * 60 * 60 * 1000).toISOString(), bidder: { username: 'dev_agency' } },
          { id: 10, amount: 45000, created_at: new Date(now.getTime() - 8 * 60 * 60 * 1000).toISOString(), bidder: { username: 'tech_studio' } }
        ]
      },
      {
        id: 6,
        title: 'Beauty & Spa Services - Wedding Package',
        description: 'Complete bridal beauty package for wedding day. Includes: Hair styling, makeup, mehendi, and pre-wedding facial. Need experienced beautician for home service in South Delhi. Date: Next month.',
        category: 'beauty',
        location: 'South Delhi',
        starting_bid: 8000,
        current_bid: 7000,
        end_time: new Date(now.getTime() + 20 * 24 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: false,
        created_at: new Date(now.getTime() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        creator_id: 6,
        location_type: 'city',
        city: 'Delhi',
        state: 'delhi',
        radius_km: 30,
        creator: { username: 'bride_to_be', email: 'bride@example.com' },
        bids: [
          { id: 11, amount: 7500, created_at: new Date(now.getTime() - 20 * 60 * 60 * 1000).toISOString(), bidder: { username: 'beauty_salon' } },
          { id: 12, amount: 7000, created_at: new Date(now.getTime() - 18 * 60 * 60 * 1000).toISOString(), bidder: { username: 'spa_expert' } }
        ]
      },
      {
        id: 7,
        title: 'Car Service & Maintenance - Annual Service',
        description: 'Complete annual service for Honda City 2020. Includes: Oil change, filter replacement, brake inspection, AC service, and general checkup. Need authorized service center or experienced mechanic.',
        category: 'automotive',
        location: 'Whitefield, Bangalore',
        starting_bid: 3500,
        current_bid: 3000,
        end_time: new Date(now.getTime() + 5 * 24 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: false,
        created_at: new Date(now.getTime() - 8 * 60 * 60 * 1000).toISOString(),
        creator_id: 7,
        location_type: 'local',
        city: 'Bangalore',
        state: 'karnataka',
        radius_km: 15,
        creator: { username: 'car_owner', email: 'car@example.com' },
        bids: [
          { id: 13, amount: 3200, created_at: new Date(now.getTime() - 6 * 60 * 60 * 1000).toISOString(), bidder: { username: 'auto_service' } },
          { id: 14, amount: 3000, created_at: new Date(now.getTime() - 4 * 60 * 60 * 1000).toISOString(), bidder: { username: 'mechanic_pro' } }
        ]
      },
      {
        id: 8,
        title: 'Content Writing - Blog Articles (10 Articles)',
        description: 'Need 10 high-quality blog articles (1000 words each) on technology and business topics. SEO optimized, original content, and well-researched. Topics will be provided. Deadline: 2 weeks.',
        category: 'other',
        location: 'Remote/Online',
        starting_bid: 8000,
        current_bid: 6500,
        end_time: new Date(now.getTime() + 10 * 24 * 60 * 60 * 1000).toISOString(),
        is_active: true,
        is_hot_deal: false,
        created_at: new Date(now.getTime() - 4 * 60 * 60 * 1000).toISOString(),
        creator_id: 8,
        location_type: 'state',
        city: 'Any',
        state: 'any',
        radius_km: 1000,
        creator: { username: 'content_seeker', email: 'content@example.com' },
        bids: [
          { id: 15, amount: 7000, created_at: new Date(now.getTime() - 3 * 60 * 60 * 1000).toISOString(), bidder: { username: 'writer_pro' } },
          { id: 16, amount: 6500, created_at: new Date(now.getTime() - 2 * 60 * 60 * 1000).toISOString(), bidder: { username: 'content_creator' } }
        ]
      }
    ];
  };

  // Load auctions function
  const loadAuctions = useCallback(async (customFilters = null) => {
    dispatch({ type: AUCTION_ACTIONS.LOAD_AUCTIONS_START });
    
    try {
      // Use custom filters if provided, otherwise use state filters
      const filtersToUse = customFilters || state.filters;
      
      // Map frontend filter keys to backend API parameters
      const apiParams = {
        search: filtersToUse.search || '',
        category: filtersToUse.category || '',
        location: filtersToUse.location || '',
        page: 1,
        per_page: 100 // Get more results for client-side filtering
      };

      const response = await auctionsAPI.getAll(apiParams);
      const auctions = response.auctions || response || [];
      
      // If API returns empty array or fails, use mock data as fallback
      if (auctions.length === 0) {
        console.warn('API returned no auctions, using mock data');
        const mockAuctions = getMockAuctions();
        dispatch({
          type: AUCTION_ACTIONS.LOAD_AUCTIONS_SUCCESS,
          payload: mockAuctions
        });
      } else {
        dispatch({
          type: AUCTION_ACTIONS.LOAD_AUCTIONS_SUCCESS,
          payload: auctions
        });
      }
    } catch (error) {
      console.warn('API call failed, using mock data as fallback:', error.message);
      // Use mock data as fallback when API fails
      const mockAuctions = getMockAuctions();
      dispatch({
        type: AUCTION_ACTIONS.LOAD_AUCTIONS_SUCCESS,
        payload: mockAuctions
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Load auctions on mount
  useEffect(() => {
    loadAuctions();
  }, [loadAuctions]);

  // Reload auctions when filters change (debounced)
  useEffect(() => {
    // Skip initial load (handled by first useEffect)
    if (state.auctions.length === 0) return;
    
    const timeoutId = setTimeout(() => {
      loadAuctions();
    }, 500); // Debounce API calls

    return () => clearTimeout(timeoutId);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [state.filters.search, state.filters.category, state.filters.location]);

  // Create auction function
  const createAuction = async (auctionData) => {
    dispatch({ type: AUCTION_ACTIONS.CREATE_AUCTION_START });
    
    try {
      const response = await auctionsAPI.create(auctionData);
      const newAuction = response.auction;
      
      dispatch({
        type: AUCTION_ACTIONS.CREATE_AUCTION_SUCCESS,
        payload: newAuction
      });
      
      return { success: true, auction: newAuction };
    } catch (error) {
      const errorMessage = error.message || 'Failed to create auction';
      dispatch({
        type: AUCTION_ACTIONS.CREATE_AUCTION_FAILURE,
        payload: errorMessage
      });
      return { success: false, error: errorMessage };
    }
  };

  // Place bid function
  const placeBid = async (auctionId, amount, description = '') => {
    dispatch({ type: AUCTION_ACTIONS.PLACE_BID_START });
    
    try {
      const response = await auctionsAPI.placeBid(auctionId, { amount, description });
      const newBid = response.bid;
      
      dispatch({
        type: AUCTION_ACTIONS.PLACE_BID_SUCCESS,
        payload: {
          auctionId,
          amount,
          bid: newBid
        }
      });
      
      return { success: true, bid: newBid };
    } catch (error) {
      const errorMessage = error.message || 'Failed to place bid';
      dispatch({
        type: AUCTION_ACTIONS.PLACE_BID_FAILURE,
        payload: errorMessage
      });
      return { success: false, error: errorMessage };
    }
  };

  // Update auction (for real-time updates)
  const updateAuction = (auctionId, updates) => {
    dispatch({
      type: AUCTION_ACTIONS.UPDATE_AUCTION,
      payload: { id: auctionId, updates }
    });
  };

  // Set filters
  const setFilters = (filters) => {
    dispatch({
      type: AUCTION_ACTIONS.SET_FILTERS,
      payload: filters
    });
  };

  // Set sort
  const setSort = (sortBy) => {
    dispatch({
      type: AUCTION_ACTIONS.SET_SORT,
      payload: sortBy
    });
  };

  // Clear error
  const clearError = () => {
    dispatch({ type: AUCTION_ACTIONS.CLEAR_ERROR });
  };

  // Get auction by ID - fetch from API if not in state
  const getAuctionById = async (id) => {
    // First check if auction is in state
    const localAuction = state.auctions.find(auction => auction.id === parseInt(id));
    if (localAuction) {
      return localAuction;
    }
    
    // If not found, fetch from API
    try {
      const response = await auctionsAPI.getById(id);
      return response.auction;
    } catch (error) {
      console.error('Error fetching auction:', error);
      return null;
    }
  };

  const value = {
    ...state,
    loadAuctions,
    createAuction,
    placeBid,
    updateAuction,
    setFilters,
    setSort,
    clearError,
    getAuctionById
  };

  return (
    <AuctionContext.Provider value={value}>
      {children}
    </AuctionContext.Provider>
  );
};

// Custom hook to use auction context
export const useAuction = () => {
  const context = useContext(AuctionContext);
  if (!context) {
    throw new Error('useAuction must be used within an AuctionProvider');
  }
  return context;
};

