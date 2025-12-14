const API_BASE_URL = 
  import.meta.env.VITE_API_BASE_URL || "http://localhost:5000/api";

export const loginUser = async (credentials) => {
  const response = await fetch(`${API_BASE_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(credentials),
  });
  if (!response.ok) {
    throw new Error("Login failed");
  }
  return response.json();
};

export const registerUser = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/register`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(userData),
  });
  if (!response.ok) {
    throw new Error("Registration failed");
  }
  return response.json();
};

export const logoutUser = () => {
  // In a real application, you might want to invalidate the token on the server
  console.log("User logged out");
};

export const fetchAuctions = async () => {
  const response = await fetch(`${API_BASE_URL}/auctions`);
  if (!response.ok) {
    throw new Error("Failed to fetch auctions");
  }
  return response.json();
};

export const placeBid = async (auctionId, amount) => {
  const response = await fetch(`${API_BASE_URL}/auctions/${auctionId}/bid`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
    body: JSON.stringify({ amount }),
  });
  if (!response.ok) {
    throw new Error("Failed to place bid");
  }
  return response.json();
};