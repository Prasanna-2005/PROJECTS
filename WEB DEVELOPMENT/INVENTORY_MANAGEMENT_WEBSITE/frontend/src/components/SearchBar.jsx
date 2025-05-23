import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = ({ onSearchResults }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleChange = (e) => {
    setSearchTerm(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.get(`/products?q=${searchTerm}`);
      onSearchResults(response.data);
    } catch (error) {
      console.error('Error searching products:', error);
    }
  };

  return (
    <form className="search-bar flex justify-center mb-5" onSubmit={handleSubmit}>
      <input
        type="text"
        value={searchTerm}
        onChange={handleChange}
        placeholder="Search products..."
        className="p-2 border rounded mr-2"
      />
      <button type="submit" className="px-4 py-2 bg-blue-500 text-white rounded">Search/List-all</button>
    </form>
  );
};

export default SearchBar;
