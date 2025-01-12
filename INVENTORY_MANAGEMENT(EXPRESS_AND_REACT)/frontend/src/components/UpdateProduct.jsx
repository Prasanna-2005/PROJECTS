import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UpdateProduct = ({ productId, onUpdate }) => {
  const [formData, setFormData] = useState({});
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const response = await axios.get(`/product/${productId}`);
        const product = response.data;
        setFormData({
          name: product.name,
          description: product.description,
          price: product.price,
          discount: product.discount,
          image: null,
        });
      } catch (error) {
        console.error('Error fetching product:', error);
      }
    };

    if (productId) fetchProduct();
  }, [productId]);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    setFormData(prevFormData => ({
      ...prevFormData,
      [name]: files ? files[0] : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();

    Object.keys(formData).forEach((key) => {
      if (formData[key] !== '' && formData[key] !== null) {
        data.append(key, formData[key]);
      }
    });

    try {
      await axios.put(`/product/${productId}`, data);
      const response = await axios.get(`/product/${productId}`);
      onUpdate(response.data);

      setSuccess(true);
      setTimeout(() => setSuccess(false), 3000); // Show success message for 3 seconds
    } catch (error) {
      console.error('Error updating product:', error);
    }
  };

  return (
    <div className="update-product flex flex-col items-center m-5">
      {success && <div className="success-message text-green-500 font-bold mb-4">Product updated successfully!</div>}
      <form onSubmit={handleSubmit} style={{ display: success ? 'none' : 'block' }} className="flex flex-col">
        <div className="mb-4">
          <label>Name:</label>
          <input type="text" name="name" value={formData.name || ''} onChange={handleChange} className="p-2 border rounded w-full" />
        </div>
        <div className="mb-4">
          <label>Description:</label>
          <textarea name="description" value={formData.description || ''} onChange={handleChange} className="p-2 border rounded w-full" />
        </div>
        <div className="mb-4">
          <label>Price:</label>
          <input type="number" name="price" value={formData.price || ''} onChange={handleChange} className="p-2 border rounded w-full" />
        </div>
        <div className="mb-4">
          <label>Discount:</label>
          <input type="number" name="discount" value={formData.discount || ''} onChange={handleChange} className="p-2 border rounded w-full" />
        </div>
        <div className="mb-4">
          <label>Image:</label>
          <input type="file" name="image" onChange={handleChange} className="p-2 border rounded w-full" />
        </div>
        <button type="submit" className="px-4 py-2 bg-yellow-500 text-white rounded">Update Product</button>
      </form>
    </div>
  );
};

export default UpdateProduct;
