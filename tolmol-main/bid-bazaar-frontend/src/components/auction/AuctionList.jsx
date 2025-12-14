import React from 'react';
import AuctionCard from './AuctionCard';
import { Loader2 } from 'lucide-react';

const AuctionList = ({ auctions, isLoading, error }) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <Loader2 className="h-8 w-8 animate-spin" />
        <span className="ml-2 text-muted-foreground">Loading auctions...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <div className="text-red-500 mb-2">Error loading auctions</div>
        <div className="text-sm text-muted-foreground">{error}</div>
      </div>
    );
  }

  if (!auctions || auctions.length === 0) {
    return (
      <div className="text-center py-12">
        <div className="text-muted-foreground mb-2">No auctions found</div>
        <div className="text-sm text-muted-foreground">
          Try adjusting your search criteria or check back later for new auctions.
        </div>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {auctions.map((auction) => (
        <AuctionCard key={auction.id} auction={auction} />
      ))}
    </div>
  );
};

export default AuctionList;

