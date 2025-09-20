import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Search, ShoppingCart, Star, Filter, Plus, Minus, X } from 'lucide-react';
import axios from 'axios';

interface Sweet {
  id: number;
  name: string;
  category: string;
  price: number;
  quantity: number;
  description: string;
  image_url?: string;
  created_at: string;
}

interface CartItem {
  sweet: Sweet;
  quantity: number;
}

const Dashboard: React.FC = () => {
  const [sweets, setSweets] = useState<Sweet[]>([]);
  const [filteredSweets, setFilteredSweets] = useState<Sweet[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [priceFilter, setPriceFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const [purchaseLoading, setPurchaseLoading] = useState<number | null>(null);
  const [cart, setCart] = useState<CartItem[]>([]);
  const [showCart, setShowCart] = useState(false);
  
  const { token, user } = useAuth();

  const categories = ['Traditional', 'Bengali', 'Premium', 'South Indian'];
  const priceRanges = [
    { label: 'All Prices', value: '' },
    { label: 'Under ₹150', value: '0-150' },
    { label: '₹150 - ₹250', value: '150-250' },
    { label: 'Above ₹250', value: '250+' }
  ];

  useEffect(() => {
    fetchSweets();
  }, []);

  useEffect(() => {
    filterSweets();
  }, [sweets, searchTerm, categoryFilter, priceFilter]);

  const fetchSweets = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/sweets', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSweets(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Failed to fetch sweets:', error);
      setLoading(false);
    }
  };

  const filterSweets = () => {
    let filtered = sweets;

    if (searchTerm) {
      filtered = filtered.filter(sweet =>
        sweet.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        sweet.description.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (categoryFilter) {
      filtered = filtered.filter(sweet => sweet.category === categoryFilter);
    }

    if (priceFilter) {
      if (priceFilter === '0-150') {
        filtered = filtered.filter(sweet => sweet.price < 150);
      } else if (priceFilter === '150-250') {
        filtered = filtered.filter(sweet => sweet.price >= 150 && sweet.price <= 250);
      } else if (priceFilter === '250+') {
        filtered = filtered.filter(sweet => sweet.price > 250);
      }
    }

    setFilteredSweets(filtered);
  };

  const addToCart = (sweet: Sweet) => {
    setCart(prev => {
      const existing = prev.find(item => item.sweet.id === sweet.id);
      if (existing) {
        return prev.map(item =>
          item.sweet.id === sweet.id
            ? { ...item, quantity: Math.min(item.quantity + 1, sweet.quantity) }
            : item
        );
      } else {
        return [...prev, { sweet, quantity: 1 }];
      }
    });
  };

  const removeFromCart = (sweetId: number) => {
    setCart(prev => prev.filter(item => item.sweet.id !== sweetId));
  };

  const updateCartQuantity = (sweetId: number, newQuantity: number) => {
    if (newQuantity <= 0) {
      removeFromCart(sweetId);
      return;
    }
    
    setCart(prev => prev.map(item =>
      item.sweet.id === sweetId
        ? { ...item, quantity: Math.min(newQuantity, item.sweet.quantity) }
        : item
    ));
  };

  const handlePurchase = async (sweetId: number, quantity: number = 1) => {
    setPurchaseLoading(sweetId);
    try {
      const response = await axios.post(
        `http://localhost:8000/api/sweets/${sweetId}/purchase`,
        { quantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      // Update the sweet in the local state
      setSweets(prev => prev.map(sweet => 
        sweet.id === sweetId 
          ? response.data
          : sweet
      ));
      
      // Remove from cart after purchase
      removeFromCart(sweetId);
      
      alert(`Successfully purchased ${quantity} ${sweets.find(s => s.id === sweetId)?.name}!`);
    } catch (error) {
      console.error('Failed to purchase sweet:', error);
      alert('Failed to purchase. Please try again.');
    } finally {
      setPurchaseLoading(null);
    }
  };

  const purchaseCart = async () => {
    for (const item of cart) {
      await handlePurchase(item.sweet.id, item.quantity);
    }
    setCart([]);
    setShowCart(false);
  };

  const getTotalCartPrice = () => {
    return cart.reduce((total, item) => total + (item.sweet.price * item.quantity), 0);
  };

  const getTotalCartItems = () => {
    return cart.reduce((total, item) => total + item.quantity, 0);
  };

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Loading delicious sweets...</p>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Welcome to Sweet Shop, {user?.username}!</h1>
        <p>Discover the finest collection of Indian sweets</p>
      </div>

      {/* Cart Button */}
      <div className="cart-floating-btn" onClick={() => setShowCart(true)}>
        <ShoppingCart size={24} />
        {getTotalCartItems() > 0 && (
          <span className="cart-badge">{getTotalCartItems()}</span>
        )}
      </div>

      {/* Cart Modal */}
      {showCart && (
        <div className="modal-overlay">
          <div className="modal cart-modal">
            <div className="modal-header">
              <h2>Shopping Cart</h2>
              <button onClick={() => setShowCart(false)} className="close-btn">
                <X size={20} />
              </button>
            </div>
            
            <div className="cart-content">
              {cart.length === 0 ? (
                <div className="empty-cart">
                  <ShoppingCart size={48} />
                  <p>Your cart is empty</p>
                </div>
              ) : (
                <>
                  <div className="cart-items">
                    {cart.map(item => (
                      <div key={item.sweet.id} className="cart-item">
                        <img 
                          src={item.sweet.image_url || 'https://via.placeholder.com/60x60'} 
                          alt={item.sweet.name}
                          className="cart-item-image"
                        />
                        <div className="cart-item-details">
                          <h4>{item.sweet.name}</h4>
                          <p>₹{item.sweet.price} each</p>
                        </div>
                        <div className="cart-item-controls">
                          <button 
                            onClick={() => updateCartQuantity(item.sweet.id, item.quantity - 1)}
                            className="quantity-btn"
                          >
                            <Minus size={16} />
                          </button>
                          <span className="quantity">{item.quantity}</span>
                          <button 
                            onClick={() => updateCartQuantity(item.sweet.id, item.quantity + 1)}
                            className="quantity-btn"
                          >
                            <Plus size={16} />
                          </button>
                          <button 
                            onClick={() => removeFromCart(item.sweet.id)}
                            className="remove-btn"
                          >
                            <X size={16} />
                          </button>
                        </div>
                        <div className="cart-item-total">
                          ₹{item.sweet.price * item.quantity}
                        </div>
                      </div>
                    ))}
                  </div>
                  
                  <div className="cart-summary">
                    <div className="cart-total">
                      <strong>Total: ₹{getTotalCartPrice()}</strong>
                    </div>
                    <button 
                      onClick={purchaseCart}
                      className="checkout-btn"
                      disabled={purchaseLoading !== null}
                    >
                      {purchaseLoading !== null ? 'Processing...' : 'Purchase All'}
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Search and Filters */}
      <div className="filters-section">
        <div className="search-box">
          <Search className="search-icon" />
          <input
            type="text"
            placeholder="Search for sweets..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filters">
          <select
            value={categoryFilter}
            onChange={(e) => setCategoryFilter(e.target.value)}
            className="filter-select"
          >
            <option value="">All Categories</option>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>

          <select
            value={priceFilter}
            onChange={(e) => setPriceFilter(e.target.value)}
            className="filter-select"
          >
            {priceRanges.map(range => (
              <option key={range.value} value={range.value}>{range.label}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Sweet Cards Grid */}
      <div className="sweets-grid">
        {filteredSweets.map(sweet => (
          <div key={sweet.id} className="sweet-card">
            <div className="sweet-image">
              <img 
                src={sweet.image_url || 'https://via.placeholder.com/300x200'} 
                alt={sweet.name}
                onError={(e) => {
                  (e.target as HTMLImageElement).src = 'https://via.placeholder.com/300x200';
                }}
              />
              <div className="sweet-category">{sweet.category}</div>
            </div>
            
            <div className="sweet-content">
              <h3 className="sweet-name">{sweet.name}</h3>
              <p className="sweet-description">{sweet.description}</p>
              
              <div className="sweet-details">
                <div className="sweet-price">₹{sweet.price}</div>
                <div className="sweet-stock">
                  {sweet.quantity > 0 ? (
                    <span className="in-stock">{sweet.quantity} available</span>
                  ) : (
                    <span className="out-of-stock">Out of stock</span>
                  )}
                </div>
              </div>

              <div className="sweet-actions">
                <button
                  onClick={() => addToCart(sweet)}
                  disabled={sweet.quantity === 0}
                  className={`add-to-cart-btn ${sweet.quantity === 0 ? 'disabled' : ''}`}
                >
                  Add to Cart
                </button>
                
                <button
                  onClick={() => handlePurchase(sweet.id)}
                  disabled={sweet.quantity === 0 || purchaseLoading === sweet.id}
                  className={`purchase-btn ${sweet.quantity === 0 ? 'disabled' : ''}`}
                >
                  {purchaseLoading === sweet.id ? (
                    'Purchasing...'
                  ) : sweet.quantity === 0 ? (
                    'Out of Stock'
                  ) : (
                    <>
                      <ShoppingCart size={16} />
                      Buy Now
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredSweets.length === 0 && !loading && (
        <div className="no-results">
          <h3>No sweets found</h3>
          <p>Try adjusting your search or filters</p>
        </div>
      )}
    </div>
  );
};

export default Dashboard;