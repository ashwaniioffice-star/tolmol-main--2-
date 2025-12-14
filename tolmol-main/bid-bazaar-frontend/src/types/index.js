// Type definitions for Bid Bazaar application

export const USER_TYPES = {
  REGULAR: 'regular',
  SERVICE_PROVIDER: 'service_provider'
};

export const AUCTION_CATEGORIES = [
  { value: 'home_repair', label: 'Home Repair' },
  { value: 'cleaning', label: 'Cleaning' },
  { value: 'tutoring', label: 'Tutoring' },
  { value: 'delivery', label: 'Delivery' },
  { value: 'design', label: 'Design & Creative' },
  { value: 'tech_support', label: 'Tech Support' },
  { value: 'beauty', label: 'Beauty & Wellness' },
  { value: 'automotive', label: 'Automotive' },
  { value: 'other', label: 'Other' }
];

export const LOCATION_TYPES = [
  { value: 'local', label: 'Local Area (10km radius)' },
  { value: 'city', label: 'City Wide (50km radius)' },
  { value: 'state', label: 'State Wide (unlimited)' }
];

export const INDIAN_STATES = [
  { value: 'andhra-pradesh', label: 'Andhra Pradesh' },
  { value: 'arunachal-pradesh', label: 'Arunachal Pradesh' },
  { value: 'assam', label: 'Assam' },
  { value: 'bihar', label: 'Bihar' },
  { value: 'chhattisgarh', label: 'Chhattisgarh' },
  { value: 'goa', label: 'Goa' },
  { value: 'gujarat', label: 'Gujarat' },
  { value: 'haryana', label: 'Haryana' },
  { value: 'himachal-pradesh', label: 'Himachal Pradesh' },
  { value: 'jharkhand', label: 'Jharkhand' },
  { value: 'karnataka', label: 'Karnataka' },
  { value: 'kerala', label: 'Kerala' },
  { value: 'madhya-pradesh', label: 'Madhya Pradesh' },
  { value: 'maharashtra', label: 'Maharashtra' },
  { value: 'manipur', label: 'Manipur' },
  { value: 'meghalaya', label: 'Meghalaya' },
  { value: 'mizoram', label: 'Mizoram' },
  { value: 'nagaland', label: 'Nagaland' },
  { value: 'odisha', label: 'Odisha' },
  { value: 'punjab', label: 'Punjab' },
  { value: 'rajasthan', label: 'Rajasthan' },
  { value: 'sikkim', label: 'Sikkim' },
  { value: 'tamil-nadu', label: 'Tamil Nadu' },
  { value: 'telangana', label: 'Telangana' },
  { value: 'tripura', label: 'Tripura' },
  { value: 'uttar-pradesh', label: 'Uttar Pradesh' },
  { value: 'uttarakhand', label: 'Uttarakhand' },
  { value: 'west-bengal', label: 'West Bengal' },
  { value: 'delhi', label: 'Delhi' },
  { value: 'mumbai', label: 'Mumbai' },
  { value: 'kolkata', label: 'Kolkata' },
  { value: 'chennai', label: 'Chennai' }
];

// Mock data for development
export const MOCK_USER = {
  id: 1,
  username: 'john_doe',
  email: 'john@example.com',
  phone: '+91 9876543210',
  is_service_provider: false,
  created_at: new Date().toISOString()
};

export const MOCK_AUCTIONS = [
  {
    id: 1,
    title: 'House Cleaning Service',
    description: 'Need professional house cleaning for a 3BHK apartment. Deep cleaning required including kitchen and bathrooms.',
    category: 'cleaning',
    location: 'Koramangala, Bangalore',
    starting_bid: 2000,
    current_bid: 1500,
    end_time: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
    is_active: true,
    is_hot_deal: true,
    created_at: new Date().toISOString(),
    creator_id: 2,
    location_type: 'city',
    city: 'Bangalore',
    state: 'karnataka',
    radius_km: 50,
    creator: {
      username: 'cleaning_pro',
      email: 'pro@cleaning.com'
    },
    bids: [
      {
        id: 1,
        amount: 1800,
        created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        bidder: { username: 'bidder1' }
      },
      {
        id: 2,
        amount: 1500,
        created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        bidder: { username: 'bidder2' }
      }
    ]
  },
  {
    id: 2,
    title: 'Math Tutoring for Class 10',
    description: 'Looking for experienced math tutor for CBSE Class 10 student. Need help with algebra and geometry.',
    category: 'tutoring',
    location: 'Sector 18, Noida',
    starting_bid: 1000,
    current_bid: 800,
    end_time: new Date(Date.now() + 48 * 60 * 60 * 1000).toISOString(),
    is_active: true,
    is_hot_deal: false,
    created_at: new Date().toISOString(),
    creator_id: 3,
    location_type: 'local',
    city: 'Noida',
    state: 'uttar-pradesh',
    radius_km: 10,
    creator: {
      username: 'student_parent',
      email: 'parent@example.com'
    },
    bids: [
      {
        id: 3,
        amount: 900,
        created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
        bidder: { username: 'tutor1' }
      },
      {
        id: 4,
        amount: 800,
        created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
        bidder: { username: 'tutor2' }
      }
    ]
  },
  {
    id: 3,
    title: 'Logo Design for Startup',
    description: 'Need a professional logo design for my tech startup. Looking for modern, minimalist design with tech feel.',
    category: 'design',
    location: 'Pune, Maharashtra',
    starting_bid: 5000,
    current_bid: 3500,
    end_time: new Date(Date.now() + 72 * 60 * 60 * 1000).toISOString(),
    is_active: true,
    is_hot_deal: true,
    created_at: new Date().toISOString(),
    creator_id: 4,
    location_type: 'state',
    city: 'Pune',
    state: 'maharashtra',
    radius_km: 500,
    creator: {
      username: 'startup_founder',
      email: 'founder@startup.com'
    },
    bids: [
      {
        id: 5,
        amount: 4000,
        created_at: new Date(Date.now() - 4 * 60 * 60 * 1000).toISOString(),
        bidder: { username: 'designer1' }
      },
      {
        id: 6,
        amount: 3500,
        created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        bidder: { username: 'designer2' }
      }
    ]
  }
];

