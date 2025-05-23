const db = require("../config/db.config");



const reviewController = {
  getReviewsByMovieId: async (req, res) => {
    const movieId = req.params.movieId;
    if (isNaN(movieId)) {
      return res.status(400).json({ message: "Invalid movie ID" });
    }
    const [movies] = await db.query("SELECT id FROM movies WHERE id = ?", [
      movieId,
    ]);

    if (movies.length === 0) {
      return res.status(404).json({ message: "Movie not found" });
    }

    // get reviews from the table
    const [reviews] = await db.query(
      "select r.id, r.movie_id, r.content, r.rating, r.likes_count,r.dislikes_count,u.id as user_id, u.username, u.email from reviews r join users u on r.user_id=u.id where r.movie_id=?",
      [movieId]
    );

    let reviewResponse = [];
    for (let review of reviews) {
      let resp = {
        id: review.id,
        content: review.content,
        rating: review.rating,
        movie_id: review.movie_id,
        likes_count: review.likes_count,
        dislikes_count: review.dislikes_count,
        user: {
          id: review.user_id,
          username: review.username
        },
      };

      reviewResponse.push(resp);
    }

    return res.json(reviewResponse);
  },




  addOrUpdateReview: async (req, res) => {
    const userId = req.signedCookies.user_id;
const movieId = req.params.movieId;

// Check if the movie exists
const [movies] = await db.query("SELECT id FROM movies WHERE id = ?", [movieId]);

if (movies.length === 0) {
  return res.status(404).json({ message: "Movie not found" });
}

// Parse content and rating from JSON body
const { content } = req.body;
const rating = req.query.rating;

if (!content || typeof rating === 'undefined') {
  return res.status(400).json({ message: content+rating });
}

const numericRating = parseFloat(rating);

    // Update average rating and rating count
    await db.query(
      `UPDATE movies 
      SET average_rating = (average_rating * rating_count + ?) / (rating_count + 1), 
      rating_count = rating_count + 1 
      WHERE id = ?`,
      [numericRating, movieId]
    );

    // Insert new review
    try {
      const [result] = await db.query(
        "INSERT INTO reviews(movie_id, user_id, content, rating) VALUES (?, ?, ?, ?)",
        [movieId, userId, content, numericRating]
      );

      if (result.affectedRows === 1) {
        return res.status(201).json({
          message: "Review added successfully",
        });
      } else {
        return res.status(500).json({ message: "Failed to add review" });
      }
    } catch (error) {
      console.error(error);
      return res.status(500).json({ message: "Server error" });
    }
},
  






  deleteReview: async (req, res) => {
    const movieId = req.params.movieId;
    const reviewId = req.params.reviewId;
    const userId  = req.signedCookies.user_id;

    // check if the movie exists and review exists
    const [movies] = await db.query("SELECT id FROM movies WHERE id = ?", [
      movieId,
    ]);
    if (movies.length === 0) {
      return res.status(404).json({ message: "Movie not found" });
    }    
    const [reviews] = await db.query("SELECT id FROM reviews WHERE id = ?", [
      reviewId,
    ]);

    if (reviews.length === 0) {
      return res.status(404).json({ message: "Review not found" });
    }

  
    // check if the user is the author of the review
    const [review] = await db.query(
      "SELECT user_id FROM reviews WHERE id = ?",
      [reviewId]
    );

    if (review[0].user_id !== userId) {
      return res
        .status(403)
        .json({ message: "Forbidden, cannot delete other users' reviews" });
    }

    // update the rating_count and the average_rating in the movies table
    const [ratings] = await db.query(
      "SELECT rating FROM reviews WHERE movie_id = ?",
      [movieId]
    );
 
    const ratingCount = ratings.length;
    const totalRating = ratings.reduce((acc, curr) => acc + curr.rating, 0);
    const averageRating = totalRating / ratingCount;

      // delete the review
      await db.query("DELETE FROM reviews WHERE id = ?", [reviewId]);

    await db.query(
      "UPDATE movies SET rating_count = ?, average_rating = ? WHERE id = ?",
      [ratingCount, averageRating, movieId]
    );

    return res.status(200).json({ message: "Review deleted successfully" });
  },
};
module.exports = reviewController;

