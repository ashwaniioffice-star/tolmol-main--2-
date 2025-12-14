import React, { createContext, useState, useContext, useEffect } from 'react';
import { fetchAuctions, placeBid } from '../lib/helpers'; // Assuming helpers.js is in lib

const AuctionContext = createContext(null);

export const AuctionProvider = ({ children }) => {
  const [auctions, setAuctions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const getAuctions = async () => {
      try {
        const data = await fetchAuctions();
        setAuctions(data);
      } catch (err) {
        setError(err);
      }
      setLoading(false);
    };
    getAuctions();
  }, []);

  const bid = async (auctionId, amount) => {
    try {
      const updatedAuction = await placeBid(auctionId, amount);
      setAuctions((prevAuctions) =>
        prevAuctions.map((auction) =>
          auction.id === auctionId ? updatedAuction : auction
        )
      );
      return updatedAuction;
    } catch (err) {
      setError(err);
      throw err;
    }
  };

  return (
    <AuctionContext.Provider value={{ auctions, loading, error, bid }}>
      {children}
    </AuctionContext.Provider>
  );
};

export const useAuction = () => useContext(AuctionContext);
