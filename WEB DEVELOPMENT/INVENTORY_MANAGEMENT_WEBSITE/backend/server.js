const express = require('express');
const multer = require('multer');
const path = require('path');
const fs = require('fs');

const { MongoClient } = require('mongodb');
const { ObjectId } = require('mongodb');

const app = express();
const DEFAULT_IMAGE_PATH = path.join(__dirname, 'public/img/image.png');
const upload = multer({ storage: multer.memoryStorage() }); // Store in memory for processing

app.use('/static',express.static('public'));    //sets a static directory in server root
app.set('view engine','ejs')
app.set('views','./views')
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const url = 'mongodb://127.0.0.1:27017'; // Use 127.0.0.1 instead of localhost
const client = new MongoClient(url);



async function run() {
  try {
    await client.connect();
    const database = client.db('inventory');
    const products = database.collection('products');

    app.get('/', (req, res) => {
      res.send('Backend is working!');
    });

 

    app.post('/product', upload.single('image'), async (req, res) => {
      const val = req.body
      let imageBuffer;
      let imageType;
      try {
          if (req.file) {
              // Use uploaded image
              imageBuffer = req.file.buffer;
              imageType = req.file.mimetype;
          } else {
              // Use default image
              imageBuffer = fs.readFileSync(DEFAULT_IMAGE_PATH); // Read the default image file
              imageType = 'image/png'; // Update based on your default image type
          }
  
          // Construct a product document
          const product = {
              ...val,
              image: imageBuffer,
              imageType,
          };
          const result = await products.insertOne(product); // Insert into MongoDB
          product.image = product.image.toString('base64'); // Convert image buffer to base64 string
          res.send(product);
      } catch (err) {
          console.error(err);
          res.status(500).send({ error: 'Failed to upload product' });
      }
    });
  


    // Delete product (including image if stored in filesystem)
    app.delete('/product/:id', async (req, res) => {
        const id = req.params.id;
        try {
           
            if (!ObjectId.isValid(id)) {
                return res.status(400).send({ error: 'Invalid product ID format' });
            }

            const product = await products.findOne({ _id: new ObjectId(id) });
            if (!product) {
                return res.status(404).send({ error: 'Product not found' });
            }
            const result = await products.deleteOne({ _id: new ObjectId(id) });
            
            if (result.deletedCount === 0) {
                return res.status(404).send({ error: 'Product not found' });
            }

            res.status(200).send({ message: 'Product deleted successfully' });
        } catch (err) {
            console.error(err);
            res.status(500).send({ error: 'Failed to delete product' });
        }
    });

      app.get('/product/:id', async (req, res) => {
          const id = req.params.id;
          try {
              if (!ObjectId.isValid(id)) {
                  return res.status(400).send({ error: 'Invalid product ID format' });
              }
              const product = await products.findOne({ _id: new ObjectId(id) });
              if (!product) {
                  return res.status(404).send({ error: 'Product not found' });
              }
              if (product.image) {
                  // Convert image buffer to base64 string
                  product.image = product.image.toString('base64');
              }
              res.send(product);
          } catch (err) {
              console.error(err);
              res.status(500).send({ error: 'Failed to get product' });
          }
      });
  

      app.get('/products', async (req, res) => {
        const query = req.query.q || ''; // Get the search query
        try {
          const productList = await products.find({ 
            $or: [
              { name: { $regex: query, $options: 'i' } },
              { description: { $regex: query, $options: 'i' } },
              { model: { $regex: query, $options: 'i' } }
            ]
          }).toArray();
      
          const productsWithImages = productList.map(product => {
            if (product.image) {
              // Convert image buffer to base64 string
              product.image = product.image.toString('base64');
            }
            return product;
          });
      
          res.status(200).send(productsWithImages);  // Send the product list with base64 images
        } catch (err) {
          console.error(err);
          res.status(500).send({ error: 'Failed to get products' });
        }
      });
      
    
      
      app.put('/product/:id', upload.single('image'), async (req, res) => {
        const id = req.params.id;
        const updatedProduct = req.body;  
        let imageBuffer;
        let imageType;
        try {
            if (!ObjectId.isValid(id)) {
                return res.status(400).send({ error: 'Invalid product ID format' });
            }
            if (req.file) {
                imageBuffer = req.file.buffer;
                imageType = req.file.mimetype;
            } else {
                const existingProduct = await products.findOne({ _id: new ObjectId(id) });
                if (!existingProduct) {
                    return res.status(404).send({ error: 'Product not found' });
                }
                imageBuffer = existingProduct.image;  // Retain the old image
                imageType = existingProduct.imageType;  // Retain the old image type
            }
            const updateDoc = {
                ...updatedProduct,  // Include all other fields in the update
                image: imageBuffer,  // Update the image if new image is provided
                imageType,  // Update the image type if new image is provided
            };
            const result = await products.updateOne(
                { _id: new ObjectId(id) },
                { $set: updateDoc }
            );
            if (result.modifiedCount === 0) {
                return res.status(404).send({ error: 'Product not found or no changes made' });
            }
            res.send({ message:`${result.modifiedCount}` });
        } catch (err) {
            console.error(err);
            res.status(500).send({ error: 'Failed to update product' });
        }
    });

    const PORT =5000;
    app.listen(PORT, () => console.log(`Connected to MongoDB! and Server running on port ${PORT}`));
  } catch (err) {
    console.error(err);
  }
}

run().catch(console.dir);
