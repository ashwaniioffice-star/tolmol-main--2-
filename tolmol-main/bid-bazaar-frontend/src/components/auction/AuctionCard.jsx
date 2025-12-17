import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardFooter, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Clock, 
  MapPin, 
  User, 
  TrendingDown,
  Flame
} from 'lucide-react';
import { formatCurrency, formatTimeRemaining, getAuctionStatus } from '../../utils/helpers';

const AuctionCard = ({ auction }) => {
  const status = getAuctionStatus(auction);
  const currentBid = auction.current_bid || auction.starting_bid;
  const timeRemaining = formatTimeRemaining(auction.end_time);
  const isExpired = status.status === 'expired';

  const getCategoryIcon = () => {
    // You can add specific icons for each category
    return '🔧'; // Default icon
  };

  const getStatusColor = (status) => {
    switch (status.status) {
      case 'hot_deal':
        return 'destructive';
      case 'ending_soon':
        return 'destructive';
      case 'active':
        return 'default';
      case 'expired':
        return 'secondary';
      default:
        return 'default';
    }
  };

  return (
    <Card className={`h-full transition-all duration-200 hover:shadow-lg ${isExpired ? 'opacity-75' : ''}`}>
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-lg">{getCategoryIcon(auction.category)}</span>
            <Badge variant="outline" className="text-xs">
              {auction.category.replace('_', ' ')}
            </Badge>
          </div>
          <div className="flex items-center space-x-2">
            {auction.is_hot_deal && (
              <Badge variant="destructive" className="text-xs">
                <Flame className="h-3 w-3 mr-1" />
                Hot Deal
              </Badge>
            )}
            <Badge variant={getStatusColor(status)} className="text-xs">
              {status.label}
            </Badge>
          </div>
        </div>
        
        <div className="space-y-2">
          <h3 className="font-semibold text-lg leading-tight line-clamp-2">
            {auction.title}
          </h3>
          <p className="text-sm text-muted-foreground line-clamp-2">
            {auction.description}
          </p>
        </div>
      </CardHeader>

      <CardContent className="pb-3">
        <div className="space-y-3">
          {/* Location */}
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <MapPin className="h-4 w-4" />
            <span className="truncate">{auction.location}</span>
          </div>

          {/* Creator */}
          <div className="flex items-center space-x-2 text-sm text-muted-foreground">
            <User className="h-4 w-4" />
            <span>by {auction.creator?.username || 'Anonymous'}</span>
          </div>

          {/* Current Bid */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <TrendingDown className="h-4 w-4 text-green-600" />
              <span className="text-sm text-muted-foreground">Current Bid</span>
            </div>
            <div className="text-right">
              <div className="text-lg font-bold text-green-600">
                {formatCurrency(currentBid)}
              </div>
              {auction.current_bid && (
                <div className="text-xs text-muted-foreground line-through">
                  {formatCurrency(auction.starting_bid)}
                </div>
              )}
            </div>
          </div>

          {/* Time Remaining */}
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Clock className="h-4 w-4 text-orange-500" />
              <span className="text-sm text-muted-foreground">Time Left</span>
            </div>
            <span className={`text-sm font-medium ${
              isExpired ? 'text-red-500' : 
              status.status === 'ending_soon' ? 'text-orange-500' : 
              'text-foreground'
            }`}>
              {timeRemaining}
            </span>
          </div>

          {/* Bid Count */}
          {auction.bids && auction.bids.length > 0 && (
            <div className="text-xs text-muted-foreground">
              {auction.bids.length} bid{auction.bids.length !== 1 ? 's' : ''} placed
            </div>
          )}
        </div>
      </CardContent>

      <CardFooter className="pt-3">
        <Button asChild className="w-full" disabled={isExpired}>
          <Link to={`/auction/${auction.id}`}>
            {isExpired ? 'View Details' : 'View & Bid'}
          </Link>
        </Button>
      </CardFooter>
    </Card>
  );
};

export default AuctionCard;

