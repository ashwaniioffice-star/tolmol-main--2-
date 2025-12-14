import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  ArrowRight, 
  Users, 
  TrendingDown, 
  Shield, 
  Clock,
  Star,
  CheckCircle
} from 'lucide-react';
import AuctionList from '../components/auction/AuctionList';
import SearchAndFilter from '../components/common/SearchAndFilter';
import { useAuction } from '../contexts/AuctionContext';
import { formatCurrency } from '../utils/helpers';

const HomePage = () => {
  const { filteredAuctions, isLoading, error } = useAuction();

  // Get featured auctions (hot deals and ending soon)
  const featuredAuctions = filteredAuctions
    .filter(auction => auction.is_hot_deal || auction.is_active)
    .slice(0, 6);

  const stats = [
    {
      icon: Users,
      label: 'Active Users',
      value: '10,000+',
      description: 'Service providers and customers'
    },
    {
      icon: TrendingDown,
      label: 'Average Savings',
      value: '30%',
      description: 'Compared to market rates'
    },
    {
      icon: Shield,
      label: 'Verified Services',
      value: '95%',
      description: 'Quality guaranteed'
    },
    {
      icon: Clock,
      label: 'Quick Response',
      value: '< 2 hrs',
      description: 'Average bid response time'
    }
  ];

  const features = [
    {
      icon: TrendingDown,
      title: 'Reverse Auction System',
      description: 'Service providers compete with lower bids, ensuring you get the best price for quality services.'
    },
    {
      icon: Shield,
      title: 'Verified Providers',
      description: 'All service providers are verified and rated by previous customers for your peace of mind.'
    },
    {
      icon: Users,
      title: 'Wide Network',
      description: 'Access thousands of service providers across India for all your service needs.'
    },
    {
      icon: Star,
      title: 'Quality Assurance',
      description: 'Rating and review system ensures high-quality service delivery every time.'
    }
  ];

  const categories = [
    { name: 'Home Repair', icon: '🔧', count: '500+' },
    { name: 'Cleaning', icon: '🧹', count: '300+' },
    { name: 'Tutoring', icon: '📚', count: '200+' },
    { name: 'Design', icon: '🎨', count: '150+' },
    { name: 'Tech Support', icon: '💻', count: '100+' },
    { name: 'Beauty', icon: '💄', count: '80+' }
  ];

  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-primary/10 via-background to-secondary/10 py-16">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center space-y-6">
            <Badge variant="secondary" className="mb-4">
              India's #1 Service Auction Platform
            </Badge>
            <h1 className="text-4xl md:text-6xl font-bold tracking-tight">
              Get the Best Deal on
              <span className="text-primary"> Any Service</span>
            </h1>
            <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
              Post your service requirement and let verified providers compete with their best offers. 
              Save money while getting quality service.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button size="lg" asChild>
                <Link to="/register">
                  Get Started Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
              <Button variant="outline" size="lg" asChild>
                <Link to="/how-it-works">
                  How It Works
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="container mx-auto px-4">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <Card key={index} className="text-center">
              <CardContent className="pt-6">
                <stat.icon className="h-8 w-8 mx-auto mb-2 text-primary" />
                <div className="text-2xl font-bold">{stat.value}</div>
                <div className="text-sm font-medium">{stat.label}</div>
                <div className="text-xs text-muted-foreground">{stat.description}</div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Categories Section */}
      <section className="container mx-auto px-4">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold mb-4">Popular Categories</h2>
          <p className="text-muted-foreground">
            Browse services by category and find the perfect provider for your needs
          </p>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {categories.map((category, index) => (
            <Card key={index} className="hover:shadow-lg transition-shadow cursor-pointer">
              <CardContent className="pt-6 text-center">
                <div className="text-3xl mb-2">{category.icon}</div>
                <div className="font-medium">{category.name}</div>
                <div className="text-sm text-muted-foreground">{category.count} services</div>
              </CardContent>
            </Card>
          ))}
        </div>
      </section>

      {/* Featured Auctions Section */}
      <section className="container mx-auto px-4">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h2 className="text-3xl font-bold mb-2">Featured Auctions</h2>
            <p className="text-muted-foreground">
              Hot deals and ending soon - don't miss out on these opportunities
            </p>
          </div>
          <Button variant="outline" asChild>
            <Link to="/auctions">
              View All Auctions
              <ArrowRight className="ml-2 h-4 w-4" />
            </Link>
          </Button>
        </div>
        
        <SearchAndFilter />
        
        <div className="mt-8">
          <AuctionList 
            auctions={featuredAuctions} 
            isLoading={isLoading} 
            error={error} 
          />
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-muted/50 py-16">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold mb-4">Why Choose Bid Bazaar?</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Our platform revolutionizes how you find and hire service providers, 
              ensuring quality, affordability, and convenience.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {features.map((feature, index) => (
              <Card key={index}>
                <CardHeader>
                  <feature.icon className="h-8 w-8 text-primary mb-2" />
                  <CardTitle className="text-lg">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-muted-foreground">{feature.description}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-3xl font-bold mb-4">How It Works</h2>
          <p className="text-muted-foreground">
            Simple steps to get the best service at the best price
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
              <span className="text-2xl font-bold text-primary">1</span>
            </div>
            <h3 className="text-xl font-semibold">Post Your Requirement</h3>
            <p className="text-muted-foreground">
              Describe the service you need with details about location, timeline, and budget.
            </p>
          </div>
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
              <span className="text-2xl font-bold text-primary">2</span>
            </div>
            <h3 className="text-xl font-semibold">Receive Competitive Bids</h3>
            <p className="text-muted-foreground">
              Verified service providers compete by offering their best prices for your project.
            </p>
          </div>
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mx-auto">
              <span className="text-2xl font-bold text-primary">3</span>
            </div>
            <h3 className="text-xl font-semibold">Choose & Get Service</h3>
            <p className="text-muted-foreground">
              Select the best offer and get your service completed by a verified professional.
            </p>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-primary text-primary-foreground py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-4">Ready to Save on Your Next Service?</h2>
          <p className="text-xl mb-8 opacity-90">
            Join thousands of satisfied customers who save money with Bid Bazaar
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button size="lg" variant="secondary" asChild>
              <Link to="/register">
                Start Saving Today
                <ArrowRight className="ml-2 h-5 w-5" />
              </Link>
            </Button>
            <Button size="lg" variant="outline" className="border-primary-foreground text-primary-foreground hover:bg-primary-foreground hover:text-primary" asChild>
              <Link to="/register?provider=true">
                Join as Service Provider
              </Link>
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;

