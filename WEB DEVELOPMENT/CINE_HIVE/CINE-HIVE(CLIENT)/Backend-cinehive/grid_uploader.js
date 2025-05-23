const path = require('path');
const cloudinary = require('cloudinary').v2;


cloudinary.config({ 
    cloud_name: 'dikdgcqfk', 
    api_key: '546778297874854', 
    api_secret: "SewTlGS-eaxx2AqKdapYBarolxg"
  });

// Upload Function
async function uploadImageFromDir(fileName) {
  const localFilePath = path.join(__dirname, '/uploads/grid_images', fileName); // e.g., grid_images/1.jpg

  try {
    const result = await cloudinary.uploader.upload(localFilePath, {
      folder: 'grid_images',                        
      public_id: path.parse(fileName).name,         
      overwrite: true,                             
      use_filename: true,                           
      unique_filename: false,                      
      resource_type: 'image'                        
    });

    console.log('Uploaded:', result.secure_url);
    return result.secure_url;
  } catch (err) {
    console.error('Upload failed:', err);
    return null;
  }
}


uploadImageFromDir('31.jpg');


