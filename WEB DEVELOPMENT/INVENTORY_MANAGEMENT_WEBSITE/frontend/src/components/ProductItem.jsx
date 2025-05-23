const ProductItem = ({ product }) => {
  const { name, description, model, price, discount, image } = product;
  const imageUrl = `data:${product.imageType};base64,${image}`;

  return (
    <div className="border rounded-lg p-4 flex flex-col items-center text-center bg-gray-100">
      <h3 className="text-teal-700 font-bold mb-2">{name}</h3>
      {image && (
        <img
          src={imageUrl}
          alt={name}
          className="w-full max-w-xs h-auto object-contain mb-4"
        />
      )}
      <p className="text-gray-700 mb-1">Description: {description}</p>
      <p className="text-gray-700 mb-1">Price: ${price}</p>
      <p className="text-gray-700">Discount: {discount}%</p>
    </div>
  );
};

export default ProductItem;
