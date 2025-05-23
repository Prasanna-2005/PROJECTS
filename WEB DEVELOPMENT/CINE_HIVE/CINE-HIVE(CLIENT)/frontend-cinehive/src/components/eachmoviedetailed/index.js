import { useParams, useNavigate } from 'react-router-dom';
import { useEffect, useState } from 'react';
import './index.css';

const Eachmoviedetails = () => {
    const { id } = useParams(); // Get movie ID from URL
    const navigate = useNavigate(); // For navigation
    const [movie, setMovie] = useState(null);
    const [reviews, setReviews] = useState([]);
    const [showReviewForm, setShowReviewForm] = useState(false);
    const [reviewContent, setReviewContent] = useState('');
    const [reviewRating, setReviewRating] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    // Fetch movie details when the component loads
    useEffect(() => {
        const getMovieDetails = async () => {
            try {
                const response = await fetch(`https://cinehive-backend.onrender.com/movie/${id}`, {
                    method: 'GET',
                    credentials: 'include'
                });
               
                const data = await response.json();
                console.log("Fetched Movie Data:", data);
                if (response.ok) {
                    setMovie(data.data.movie);
                }
            } catch (error) {
                console.error('Error fetching movie details:', error);
            }
        };

        getMovieDetails();
    }, [id]);

    // Fetch reviews for the movie
    const fetchReviews = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`https://cinehive-backend.onrender.com/review/${id}`, { credentials: 'include' });
            if (response.status === 401) {
                navigate('/login'); // Redirect if not logged in
                return;
            }
            if (!response.ok) {
                throw new Error('Failed to fetch reviews');
            }
            const data = await response.json();
            setReviews(data);
        } catch (error) {
            console.error('Error fetching reviews:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Handle review form toggle
    const handleReviewButtonClick = async () => {
        if (!showReviewForm) {
            await fetchReviews();
        }
        setShowReviewForm(prev => !prev);
    };

    // Submit a new review
    const submitReview = async () => {
        if (!reviewContent || !reviewRating) {
            alert('Please enter both review content and rating');
            return;
        }

        setIsLoading(true);
        try {
            const response = await fetch(`https://cinehive-backend.onrender.com/review/${id}?rating=${reviewRating}`, {
                method: 'POST',
                credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ content: reviewContent })

            });

            if (response.status === 401) {
                navigate('/login'); // Redirect if not logged in
                return;
            }
            if (!response.ok) {
                alert('Failed to add review');
                return;
            }

            setReviewContent('');
            setReviewRating('');
            fetchReviews(); // Refresh review list
        } catch (error) {
            console.error('Error submitting review:', error);
        } finally {
            setIsLoading(false);
        }
    };

    // Toggle Like with optimistic update
    const toggleLike = async () => {
        // Update state immediately for better UX
        setMovie(prevMovie => {
            if (!prevMovie) return null;
            return { ...prevMovie, isLiked: !prevMovie.isLiked };
        });

        try {
            const response = await fetch(`https://cinehive-backend.onrender.com/movie/toggle-like/${id}`, {
                method: 'GET',
                credentials: 'include'
            });

            if (response.status === 401) {
                // Revert optimistic update on authentication error
                setMovie(prevMovie => {
                    if (!prevMovie) return null;
                    return { ...prevMovie, isLiked: !prevMovie.isLiked };
                });
                navigate('/login'); // Redirect if not logged in
                return;
            }
            if (!response.ok) {
                // Revert optimistic update on other errors
                setMovie(prevMovie => {
                    if (!prevMovie) return null;
                    return { ...prevMovie, isLiked: !prevMovie.isLiked };
                });
                throw new Error('Failed to toggle like');
            }

            // Only log the result, state is already updated optimistically
            const result = await response.json();
            console.log("Updated Like Data:", result);
           
            // For the first fetch only, sync with server state to ensure consistency
            if (result.isLiked !== undefined && movie.isLiked !== result.isLiked) {
                setMovie(prevMovie => {
                    if (!prevMovie) return null;
                    return { ...prevMovie, isLiked: result.isLiked };
                });
            }
        } catch (error) {
            console.error('Error toggling like:', error);
        }
    };

    // Toggle Watchlist with optimistic update
    const toggleWatchlist = async () => {
        // Update state immediately for better UX
        setMovie(prevMovie => {
            if (!prevMovie) return null;
            return { ...prevMovie, isWatchlisted: !prevMovie.isWatchlisted };
        });

        try {
            const response = await fetch(`https://cinehive-backend.onrender.com/movie/toggle-watchlist/${id}`, {
                method: 'GET',
                credentials: 'include'
            });

            if (response.status === 401) {
                // Revert optimistic update on authentication error
                setMovie(prevMovie => {
                    if (!prevMovie) return null;
                    return { ...prevMovie, isWatchlisted: !prevMovie.isWatchlisted };
                });
                navigate('/login'); // Redirect if not logged in
                return;
            }
            if (!response.ok) {
                // Revert optimistic update on other errors
                setMovie(prevMovie => {
                    if (!prevMovie) return null;
                    return { ...prevMovie, isWatchlisted: !prevMovie.isWatchlisted };
                });
                throw new Error('Failed to toggle watchlist');
            }
           
            // Only log the result, state is already updated optimistically
            const result = await response.json();
            console.log("Updated Watchlist Data:", result);
           
            // For the first fetch only, sync with server state to ensure consistency
            if (result.isWatchlisted !== undefined && movie.isWatchlisted !== result.isWatchlisted) {
                setMovie(prevMovie => {
                    if (!prevMovie) return null;
                    return { ...prevMovie, isWatchlisted: result.isWatchlisted };
                });
            }
        } catch (error) {
            console.error('Error toggling watchlist:', error);
        }
    };

    // Handle rating selection
    const handleRatingSelect = (rating) => {
        setReviewRating(rating);
    };

    if (!movie) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="movie-detail-container">
        <div className="theme-banner" style={{ backgroundImage: `url(${movie.themeimageUrl})` }}>
  <button className="glass-back-button" onClick={() => navigate(-1)}>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="28"
      height="28"
      viewBox="0 0 24 24"
      fill="none"
      stroke="white"
      strokeWidth="2.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polyline points="15 18 9 12 15 6" />
    </svg>
  </button>
</div>



            <div className="movie-content">
                <div className="poster-container">
                    <img src={movie.posterimageUrl} alt={movie.title} className="poster-image" />
                </div>
                <div className="movie-info">
                    <h2>{movie.title}</h2>
                    <p><strong>⭐ {movie.average_rating}</strong> • {movie.release_year} • {movie.runtime} min</p>
                    <p>{movie.country} • {movie.language}</p>
                    <p><strong>Genres:</strong> {movie.genres.map(g => g.name).join(", ")}</p>
                    <p className="synopsis">{movie.synopsis}</p>
                   
                    <h3>Cast & Crew</h3>
                    <ul className="cast-list">
                        {movie.castCrew.map((person, index) => (
                            <li key={index}>{person.name} - {person.role}</li>
                        ))}
                    </ul>

                    <div className="actions">
                        <button className={`like-btn ${movie.isLiked ? "liked" : ""}`} onClick={toggleLike}>
                                {movie.isLiked ? (
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="22"
                                        height="22"
                                        viewBox="0 0 24 24"
                                        fill="cyan"
                                        stroke="red"
                                        strokeWidth="1.5"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        style={{ marginRight: "6px" }}
                                    >
                                        <path d="M20.84 4.61c-1.54-1.4-3.97-1.33-5.47.15L12 7.17l-3.37-3.4C7.13 3.28 4.7 3.21 3.16 4.61c-1.65 1.5-1.68 4.09-.07 5.65l8.11 8.33c.29.3.77.3 1.06 0l8.11-8.33c1.61-1.56 1.58-4.15-.07-5.65z" />
                                    </svg>
                                    ) : (
                                    <svg
                                        xmlns="http://www.w3.org/2000/svg"
                                        width="22"
                                        height="22"
                                        viewBox="0 0 24 24"
                                        fill="none"
                                        stroke="currentColor"
                                        strokeWidth="1.5"
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                        style={{ marginRight: "6px" }}
                                    >
                                        <path d="M20.84 4.61c-1.54-1.4-3.97-1.33-5.47.15L12 7.17l-3.37-3.4C7.13 3.28 4.7 3.21 3.16 4.61c-1.65 1.5-1.68 4.09-.07 5.65l8.11 8.33c.29.3.77.3 1.06 0l8.11-8.33c1.61-1.56 1.58-4.15-.07-5.65z" />
                                    </svg>
                                    )}
                        </button>


                        <button className={`watchlist-btn ${movie.isWatchlisted ? "watchlisted" : ""}`} onClick={toggleWatchlist}>
                          <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
  {movie.isWatchlisted ? (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="cyan"
      stroke="dodgerblue"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z" />
    </svg>
  ) : (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M19 21l-7-5-7 5V5a2 2 0 012-2h10a2 2 0 012 2z" />
    </svg>
  )}
 
</span>

                        </button>
                    </div>

                    <button className="review-btn" onClick={handleReviewButtonClick}>
                        {showReviewForm ? "Hide Reviews" : "Reviews & Ratings"}
                    </button>

                    {showReviewForm && (
                        <div className="review-section">
                            <h3>User Reviews</h3>
                            {isLoading ? (
                                <div className="review-loader">Loading reviews...</div>
                            ) : (
                                <div className="reviews-list">
                                    {reviews.length > 0 ? (
                                        <ul className="review-items">
                                            {reviews.map((review) => (
                                                <li key={review.id} className="review-item">
                                                    <div className="review-header">
                                                        <span className="review-username">{review.user.username}</span>
                                                        <span className="review-rating">⭐ {review.rating}/10</span>
                                                    </div>
                                                    <p className="review-content">{review.content}</p>
                                                </li>
                                            ))}
                                        </ul>
                                    ) : (
                                        <p className="no-reviews">No reviews yet. Be the first to share your thoughts!</p>
                                    )}
                                </div>
                            )}

                            <div className="add-review-form">
                                <h4>Add Your Review</h4>
                                <textarea
                                    placeholder="Share your thoughts..."
                                    value={reviewContent}
                                    onChange={(e) => setReviewContent(e.target.value)}
                                ></textarea>
                                
                                <div className="rating-container">
                                    <div className="rating-label">Rating: {reviewRating ? `${reviewRating}/10` : 'Select a rating'}</div>
                                    <div className="rating-input-slider">
                                        <input
                                            type="range"
                                            min="1"
                                            max="10"
                                            value={reviewRating}
                                            onChange={(e) => setReviewRating(e.target.value)}
                                            className="rating-slider"
                                        />
                                    </div>
                                    <div className="rating-values">
                                        {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((num) => (
                                            <span 
                                                key={num} 
                                                className={`rating-value ${parseInt(reviewRating) === num ? 'active' : ''}`}
                                                onClick={() => handleRatingSelect(num)}
                                            >
                                                {num}
                                            </span>
                                        ))}
                                    </div>
                                </div>
                                
                                <button className="submit-review-btn" onClick={submitReview} disabled={isLoading}>
                                    {isLoading ? "Submitting..." : "Submit Review"}
                                </button>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Eachmoviedetails;