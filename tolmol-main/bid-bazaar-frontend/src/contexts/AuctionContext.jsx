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
      
    case AUCTION_ACTIONS.LOAD_AUCTIONS_SUCCESS:
      const sortedAuctions = sortAuctions(action.payload, state.sortBy);
      const filteredAuctions = filterAuctions(sortedAuctions, state.filters);
      return {
        ...state,
        isLoading: false,
        auctions: action.payload,
        filteredAuctions,
        error: null
      };
      
    case AUCTION_ACTIONS.CREATE_AUCTION_SUCCESS:
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
      
    case AUCTION_ACTIONS.PLACE_BID_SUCCESS:
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
      
    case AUCTION_ACTIONS.UPDATE_AUCTION:
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
      
    case AUCTION_ACTIONS.LOAD_AUCTIONS_FAILURE:
    case AUCTION_ACTIONS.CREATE_AUCTION_FAILURE:
    case AUCTION_ACTIONS.PLACE_BID_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.payload
      };
      
    case AUCTION_ACTIONS.SET_FILTERS:
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
      
    case AUCTION_ACTIONS.SET_SORT:
      const newSortBy = action.payload;
      const sortedWithNewSort = sortAuctions(state.auctions, newSortBy);
      const filteredWithNewSort = filterAuctions(sortedWithNewSort, state.filters);
      return {
        ...state,
        sortBy: newSortBy,
        filteredAuctions: filteredWithNewSort
      };
      
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
      const auctions = response.auctions || [];
      
      dispatch({
        type: AUCTION_ACTIONS.LOAD_AUCTIONS_SUCCESS,
        payload: auctions
      });
    } catch (error) {
      const errorMessage = error.message || 'Failed to load auctions';
      dispatch({
        type: AUCTION_ACTIONS.LOAD_AUCTIONS_FAILURE,
        payload: errorMessage
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

