import React, { useState, useEffect } from 'react';
import { FaSearch, FaShoppingCart, FaUserCircle, FaBars, FaTimes } from 'react-icons/fa';
import { useCart } from '../Cart/CartContext.jsx';
import ThemeSwitch from '../ThemeSwitch/ThemeSwitch.jsx';
import './Navbar.scss';

const Navbar = () => {
  const [input, setInput] = useState("");
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const { cart } = useCart();

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <header>
      <a href="/" className="a-name" rel="internal">NAZWAAAAA</a>

      <div className="nav-search">
        <div className="input-wrapper">
          <FaSearch id="search-icon" />
          <input
            placeholder="Szukaj..."
            value={input}
            onChange={handleInputChange}
          />
        </div>
      </div>

      <div className={`nav-icons ${isMenuOpen ? 'menu-open' : ''}`}>
        <ThemeSwitch />
        <a href="/cart">
          <FaShoppingCart />
          <div className="nav-icons-cart">{cart.length}</div>
        </a>
        <a href="/"><FaUserCircle /></a>
      </div>

      <div className="hamburger-menu" onClick={toggleMenu}>
        <FaBars />
      </div>

      <div className={`mobile-menu ${isMenuOpen ? 'open' : ''}`}>
        <div className="hamburger-menu" onClick={toggleMenu}>
          <FaTimes />
        </div>
        <div className="mobile-menu-icons">
          <ThemeSwitch />
          <a href="/cart" onClick={closeMenu}>
            <FaShoppingCart />
            <div className="nav-icons-cart">{cart.length}</div>
          </a>
          <a href="/" onClick={closeMenu}>
            <FaUserCircle />
          </a>
        </div>
      </div>
    </header>
  );
};

export default Navbar;
