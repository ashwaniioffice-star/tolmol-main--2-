import React, { useState, useEffect } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { 
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { Card, CardContent } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Search, 
  Filter, 
  X,
  SlidersHorizontal
} from 'lucide-react';
import { AUCTION_CATEGORIES } from '../../types';
import { useAuction } from '../../contexts/AuctionContext';
import { debounce } from '../../utils/helpers';

const SearchAndFilter = () => {
  const { filters, setFilters, setSort, sortBy } = useAuction();
  const [showFilters, setShowFilters] = useState(false);
  const [localSearch, setLocalSearch] = useState(filters.search);

  // Debounced search function that triggers API reload
  const debouncedSearch = debounce((searchTerm) => {
    setFilters({ search: searchTerm });
    // API will be called automatically via useEffect in AuctionContext
  }, 500);

  // Handle search input change
  useEffect(() => {
    debouncedSearch(localSearch);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [localSearch]);

  const handleFilterChange = (key, value) => {
    setFilters({ [key]: value });
  };

  const clearFilters = () => {
    setLocalSearch('');
    setFilters({
      search: '',
      category: '',
      location: '',
      minPrice: '',
      maxPrice: '',
      status: ''
    });
  };

  const hasActiveFilters = () => {
    return filters.category || filters.location || filters.minPrice || filters.maxPrice || filters.status;
  };

  const sortOptions = [
    { value: 'newest', label: 'Newest First' },
    { value: 'oldest', label: 'Oldest First' },
    { value: 'ending_soon', label: 'Ending Soon' },
    { value: 'lowest_bid', label: 'Lowest Bid' },
    { value: 'highest_bid', label: 'Highest Bid' }
  ];

  const statusOptions = [
    { value: '', label: 'All Status' },
    { value: 'active', label: 'Active' },
    { value: 'hot_deal', label: 'Hot Deals' },
    { value: 'ending_soon', label: 'Ending Soon' },
    { value: 'expired', label: 'Expired' }
  ];

  return (
    <div className="space-y-4">
      {/* Search and Sort Bar */}
      <div className="flex flex-col sm:flex-row gap-4">
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input
            type="text"
            placeholder="Search services, descriptions, locations..."
            value={localSearch}
            onChange={(e) => setLocalSearch(e.target.value)}
            className="pl-10"
          />
        </div>

        {/* Sort Dropdown */}
        <Select value={sortBy} onValueChange={setSort}>
          <SelectTrigger className="w-full sm:w-48">
            <SelectValue placeholder="Sort by" />
          </SelectTrigger>
          <SelectContent>
            {sortOptions.map((option) => (
              <SelectItem key={option.value} value={option.value}>
                {option.label}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        {/* Filter Toggle Button */}
        <Button
          variant="outline"
          onClick={() => setShowFilters(!showFilters)}
          className="flex items-center space-x-2"
        >
          <SlidersHorizontal className="h-4 w-4" />
          <span>Filters</span>
          {hasActiveFilters() && (
            <Badge variant="secondary" className="ml-2">
              {Object.values(filters).filter(Boolean).length}
            </Badge>
          )}
        </Button>
      </div>

      {/* Active Filters Display */}
      {hasActiveFilters() && (
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-sm text-muted-foreground">Active filters:</span>
          {filters.category && (
            <Badge variant="secondary" className="flex items-center space-x-1">
              <span>Category: {AUCTION_CATEGORIES.find(c => c.value === filters.category)?.label}</span>
              <X 
                className="h-3 w-3 cursor-pointer" 
                onClick={() => handleFilterChange('category', '')}
              />
            </Badge>
          )}
          {filters.location && (
            <Badge variant="secondary" className="flex items-center space-x-1">
              <span>Location: {filters.location}</span>
              <X 
                className="h-3 w-3 cursor-pointer" 
                onClick={() => handleFilterChange('location', '')}
              />
            </Badge>
          )}
          {filters.status && (
            <Badge variant="secondary" className="flex items-center space-x-1">
              <span>Status: {statusOptions.find(s => s.value === filters.status)?.label}</span>
              <X 
                className="h-3 w-3 cursor-pointer" 
                onClick={() => handleFilterChange('status', '')}
              />
            </Badge>
          )}
          {(filters.minPrice || filters.maxPrice) && (
            <Badge variant="secondary" className="flex items-center space-x-1">
              <span>
                Price: ₹{filters.minPrice || '0'} - ₹{filters.maxPrice || '∞'}
              </span>
              <X 
                className="h-3 w-3 cursor-pointer" 
                onClick={() => {
                  handleFilterChange('minPrice', '');
                  handleFilterChange('maxPrice', '');
                }}
              />
            </Badge>
          )}
          <Button variant="ghost" size="sm" onClick={clearFilters}>
            Clear all
          </Button>
        </div>
      )}

      {/* Filter Panel */}
      {showFilters && (
        <Card>
          <CardContent className="pt-6">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              {/* Category Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Category</label>
                <Select value={filters.category} onValueChange={(value) => handleFilterChange('category', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="All Categories" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="">All Categories</SelectItem>
                    {AUCTION_CATEGORIES.map((category) => (
                      <SelectItem key={category.value} value={category.value}>
                        {category.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Location Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Location</label>
                <Input
                  type="text"
                  placeholder="City, State"
                  value={filters.location}
                  onChange={(e) => handleFilterChange('location', e.target.value)}
                />
              </div>

              {/* Status Filter */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Status</label>
                <Select value={filters.status} onValueChange={(value) => handleFilterChange('status', value)}>
                  <SelectTrigger>
                    <SelectValue placeholder="All Status" />
                  </SelectTrigger>
                  <SelectContent>
                    {statusOptions.map((status) => (
                      <SelectItem key={status.value} value={status.value}>
                        {status.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Price Range */}
              <div className="space-y-2">
                <label className="text-sm font-medium">Price Range (₹)</label>
                <div className="flex space-x-2">
                  <Input
                    type="number"
                    placeholder="Min"
                    value={filters.minPrice}
                    onChange={(e) => handleFilterChange('minPrice', e.target.value)}
                  />
                  <Input
                    type="number"
                    placeholder="Max"
                    value={filters.maxPrice}
                    onChange={(e) => handleFilterChange('maxPrice', e.target.value)}
                  />
                </div>
              </div>
            </div>

            {/* Filter Actions */}
            <div className="flex justify-end space-x-2 mt-4">
              <Button variant="outline" onClick={clearFilters}>
                Clear Filters
              </Button>
              <Button onClick={() => setShowFilters(false)}>
                Apply Filters
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default SearchAndFilter;

