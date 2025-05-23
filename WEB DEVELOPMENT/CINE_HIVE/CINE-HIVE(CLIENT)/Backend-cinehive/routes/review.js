const express = require("express");
const router = express.Router();
const authController = require("../controllers/auth");
const ReviewController = require("../controllers/review"); 

router.get(
  '/review/:movieId',ReviewController.getReviewsByMovieId
);

router.post(
  '/review/:movieId/',ReviewController.addOrUpdateReview 
);

router.delete(
  "/review/:movieId/:reviewId",ReviewController.deleteReview
);

module.exports = router;

