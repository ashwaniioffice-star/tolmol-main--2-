import React from 'react';
import { Link } from 'react-router-dom';
import { Gavel, Mail, Phone, MapPin } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-muted/50 border-t">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Brand Section */}
          <div className="space-y-4">
            <div className="flex items-center space-x-2">
              <div className="flex items-center justify-center w-8 h-8 bg-primary rounded-lg">
                <Gavel className="h-5 w-5 text-primary-foreground" />
              </div>
              <span className="text-xl font-bold">Bid Bazaar</span>
            </div>
            <p className="text-sm text-muted-foreground">
              India's premier reverse auction platform for services. 
              Connect with service providers and get the best deals.
            </p>
            <div className="flex space-x-4">
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <MapPin className="h-4 w-4" />
                <span>All over India</span>
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold">Quick Links</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/" className="text-muted-foreground hover:text-foreground transition-colors">
                  Browse Auctions
                </Link>
              </li>
              <li>
                <Link to="/how-it-works" className="text-muted-foreground hover:text-foreground transition-colors">
                  How It Works
                </Link>
              </li>
              <li>
                <Link to="/categories" className="text-muted-foreground hover:text-foreground transition-colors">
                  Categories
                </Link>
              </li>
              <li>
                <Link to="/register" className="text-muted-foreground hover:text-foreground transition-colors">
                  Join as Service Provider
                </Link>
              </li>
            </ul>
          </div>

          {/* Categories */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold">Popular Categories</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/category/home-repair" className="text-muted-foreground hover:text-foreground transition-colors">
                  Home Repair
                </Link>
              </li>
              <li>
                <Link to="/category/cleaning" className="text-muted-foreground hover:text-foreground transition-colors">
                  Cleaning Services
                </Link>
              </li>
              <li>
                <Link to="/category/tutoring" className="text-muted-foreground hover:text-foreground transition-colors">
                  Tutoring
                </Link>
              </li>
              <li>
                <Link to="/category/design" className="text-muted-foreground hover:text-foreground transition-colors">
                  Design & Creative
                </Link>
              </li>
              <li>
                <Link to="/category/tech-support" className="text-muted-foreground hover:text-foreground transition-colors">
                  Tech Support
                </Link>
              </li>
            </ul>
          </div>

          {/* Support */}
          <div className="space-y-4">
            <h3 className="text-sm font-semibold">Support</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <Link to="/help" className="text-muted-foreground hover:text-foreground transition-colors">
                  Help Center
                </Link>
              </li>
              <li>
                <Link to="/safety" className="text-muted-foreground hover:text-foreground transition-colors">
                  Safety Guidelines
                </Link>
              </li>
              <li>
                <Link to="/terms" className="text-muted-foreground hover:text-foreground transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link to="/privacy" className="text-muted-foreground hover:text-foreground transition-colors">
                  Privacy Policy
                </Link>
              </li>
            </ul>
            <div className="space-y-2">
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Mail className="h-4 w-4" />
                <span>support@bidbazaar.com</span>
              </div>
              <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                <Phone className="h-4 w-4" />
                <span>+91 1800-123-4567</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Section */}
        <div className="mt-12 pt-8 border-t border-border">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="text-sm text-muted-foreground">
              © 2024 Bid Bazaar. All rights reserved.
            </div>
            <div className="flex space-x-6 text-sm">
              <Link to="/terms" className="text-muted-foreground hover:text-foreground transition-colors">
                Terms
              </Link>
              <Link to="/privacy" className="text-muted-foreground hover:text-foreground transition-colors">
                Privacy
              </Link>
              <Link to="/cookies" className="text-muted-foreground hover:text-foreground transition-colors">
                Cookies
              </Link>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;

