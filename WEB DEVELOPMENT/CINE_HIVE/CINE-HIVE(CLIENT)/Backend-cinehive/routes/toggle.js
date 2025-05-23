const express = require('express');
const router = express.Router();
const toggleController = require('../controllers/toggle');

router.get('/movie/toggle-like/:movie_id', toggleController.toggleLike);
router.get('/movie/toggle-watchlist/:movie_id', toggleController.toggleWatchlist);

module.exports = router;