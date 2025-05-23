const express = require('express');
const router = express.Router();
const MovieFilterController = require('../controllers/movie_filters');


router.get('/movies/latest', MovieFilterController.getLatestMovies);
router.get('/movies/top-rated', MovieFilterController.getTopRatedMovies);
router.get('/movies/lang', MovieFilterController.getMoviesByLanguage); // Uses query parameter `?language=`
router.get('/movies/genre',MovieFilterController.getMoviesByGenre); // Uses query parameter `?genre=`
router.get('/movies/liked',MovieFilterController.getLikedMovies); // Uses query parameter `?user_id=`
router.get('/movies/watchlists',MovieFilterController.getWatchlistedMovies); // Uses query parameter `?user_id=`


module.exports = router;