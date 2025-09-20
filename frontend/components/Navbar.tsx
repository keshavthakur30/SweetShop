import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { ShoppingBag, User, Shield, LogOut } from 'lucide-react';

const Navbar: React.FC = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          <ShoppingBag className="navbar-icon" />
          <span>Sweet Shop</span>
        </Link>
        
        {isAuthenticated ? (
          <div className="navbar-menu">
            <Link to="/dashboard" className="navbar-link">
              Dashboard
            </Link>
            
            {user?.is_admin && (
              <Link to="/admin" className="navbar-link admin-link">
                <Shield size={16} />
                Admin Panel
              </Link>
            )}
            
            <div className="navbar-user">
              <User size={16} />
              <span>{user?.username}</span>
              <button onClick={handleLogout} className="logout-btn">
                <LogOut size={16} />
              </button>
            </div>
          </div>
        ) : (
          <div className="navbar-menu">
            <Link to="/login" className="navbar-link">
              Login
            </Link>
            <Link to="/register" className="navbar-link register-btn">
              Register
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;