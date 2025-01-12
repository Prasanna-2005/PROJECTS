import React, { useState } from 'react';
import axios from 'axios';

const DeleteProduct = ({ onDelete }) => {
  const [productId, setProductId] = useState('');
  const [success, setSuccess] = useState(false);

  const handleChange = (e) => {
    setProductId(e.target.value);
  };

  const handleDelete = async (e) => {
    e.preventDefault();
    try {
      await axios.delete(`/product/${productId}`);
      onDelete(productId);
      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000); // Show success message for 3 seconds
      setProductId('');
    } catch (error) {
      console.error('Error deleting product:', error);
    }
  };

  return (
    <div className="delete-product flex flex-col items-center m-5">
      {success && <div className="success-message text-green-500 font-bold mb-4">Product deleted successfully!</div>}
      <form onSubmit={handleDelete} style={{ display: success ? 'none' : 'block' }} className="flex flex-col">
        <div className="mb-4">
          <label>Product ID:</label>
          <input type="text" value={productId} onChange={handleChange} placeholder="Enter Product ID to delete" className="p-2 border rounded w-full" />
        </div>
        <button type="submit" className="px-4 py-2 bg-red-500 text-white rounded">Delete Product</button>
      </form>
    </div>
  );
};

export default DeleteProduct;
