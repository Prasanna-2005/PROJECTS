import React, { useState } from 'react';
import AddProduct from './components/AddProduct';
import UpdateProduct from './components/UpdateProduct';
import DeleteProduct from './components/DeleteProduct';
import SearchBar from './components/SearchBar';
import ProductList from './components/ProductList';
import ProductItem from './components/ProductItem';

const App = () => {
  const [products, setProducts] = useState([]);
  const [productIdToUpdate, setProductIdToUpdate] = useState('');
  const [showForm, setShowForm] = useState(null);
  const [singleProduct, setSingleProduct] = useState(null);
  const [show, setShow] = useState(null);

  const handleProductAdded = (newProduct) => {
    setSingleProduct(newProduct);
    setShowForm(null);
    setShow(false);
  };

  const handleProductUpdated = (updatedProduct) => {
    setSingleProduct(updatedProduct);
    setProducts(products.map(product => product._id === updatedProduct._id ? updatedProduct : product));
    setShowForm(null);
    setShow(false);
  };

  const handleProductDeleted = (deletedProductId) => {
    setProducts(products.filter(product => product._id !== deletedProductId));
    setShowForm(null);
    alert(`${deletedProductId} deleted`);
  };

  const handleSearchResults = (results) => {
    setProducts(results);
    setShowForm(null);
    setSingleProduct(null);
    setShow(true);
  };

  return (
    <div className="app flex flex-col items-center p-6 font-sans bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 min-h-screen text-white">
  <h1 className="text-4xl font-extrabold mb-6">Inventory Management System</h1>

  {/* Search Bar */}
  <div className="w-full max-w-2xl mb-6">
    <SearchBar onSearchResults={handleSearchResults} />
  </div>

  {/* Action Buttons */}
  <div className="flex flex-wrap justify-center space-x-4 mb-8">
    <button
      onClick={() => {
        setShowForm("add");
        setShow(false);
        setSingleProduct(null);
      }}
      className="px-6 py-3 bg-green-600 hover:bg-green-700 text-white font-medium rounded-lg shadow-md transition-transform transform hover:scale-105"
    >
      Add Product
    </button>
    <button
      onClick={() => {
        setShowForm("update");
        setShow(false);
        setSingleProduct(null);
      }}
      className="px-6 py-3 bg-yellow-500 hover:bg-yellow-600 text-white font-medium rounded-lg shadow-md transition-transform transform hover:scale-105"
    >
      Update Product
    </button>
    <button
      onClick={() => {
        setShowForm("delete");
        setShow(false);
        setSingleProduct(null);
      }}
      className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white font-medium rounded-lg shadow-md transition-transform transform hover:scale-105"
    >
      Delete Product
    </button>
  </div>

  {/* Conditional Forms */}
  <div className="w-full max-w-3xl">
    {showForm === "add" &&<AddProduct onProductAdded={handleProductAdded} />}

    {showForm === "update" && (
  <div className="update-product bg-white p-6 rounded-lg shadow-md text-black max-w-md mx-auto">
    <h2 className="text-xl font-bold mb-4 text-center text-indigo-600">Update Product</h2>
    <label className="block mb-2 text-sm font-medium">Update Product ID:</label>
    <input
      type="text"
      value={productIdToUpdate}
      onChange={(e) => setProductIdToUpdate(e.target.value)}
      className="w-full border border-gray-300 rounded px-3 py-2 mb-4"
      placeholder="Enter Product ID"
    />
    <UpdateProduct productId={productIdToUpdate} onUpdate={handleProductUpdated} />
  </div>
)}

    {showForm === "delete" && <DeleteProduct onDelete={handleProductDeleted} />}
  </div>

  {/* Product Display */}
  <div className="w-full max-w-4xl mt-8">
    {singleProduct ? (
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <ProductItem product={singleProduct} />
      </div>
    ) : (
      show && (
        <div className="bg-white p-6 rounded-lg shadow-lg">
          <ProductList products={products} />
        </div>
      )
    )}
  </div>
</div>)};
export default App;
