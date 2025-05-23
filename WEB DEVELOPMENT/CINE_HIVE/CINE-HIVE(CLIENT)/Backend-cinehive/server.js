// backend/server.js
const express = require('express');
// const session = require('express-session');
const cloudinary = require('cloudinary').v2;
const dotenv = require('dotenv');
const cors = require('cors');

dotenv.config();
const app = express();

// Middleware to parse body
app.use(express.text());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));


app.use(cors({
  origin:['https://cine-hive-tvk.netlify.app','http://localhost:3000',"https://cine-hive-frontend.onrender.com/"],
  credentials: true,
  allowedHeaders: ['Content-Type', 'Authorization'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS','PATCH']
}));

const cookieParser = require('cookie-parser');
app.use(cookieParser('your-secret-key-here')); 
// app.use(
//   session({
//     secret: "12345",
//     resave: false,
//     saveUninitialized: true,
//     maxAge: 86400000,
//     cookie: { secure: false },
//   })
// );


const authRoutes = require('./routes/auth');
const movieRoutes = require('./routes/movie');
const movieFilterRoutes = require('./routes/movie_filters');
const toggleRoutes = require('./routes/toggle');
const reviewRoutes = require('./routes/review');

app.use('/', authRoutes);
app.use('/', movieRoutes);
app.use('/', movieFilterRoutes);
app.use('/', toggleRoutes);
app.use('/', reviewRoutes);

cloudinary.config({ 
  cloud_name: 'dikdgcqfk', 
  api_key: '546778297874854', 
  api_secret: "SewTlGS-eaxx2AqKdapYBarolxg"
});

app.get('/', (req, res) => {
  res.json({ message: 'Welcome to the Movie Catalog API' });
});

const PORT = process.env.X_ZOHO_CATALYST_LISTEN_PORT || 5003;
app.listen(PORT, () =>
  console.log(`BACKEND running at: http://localhost:${PORT}`)
);
