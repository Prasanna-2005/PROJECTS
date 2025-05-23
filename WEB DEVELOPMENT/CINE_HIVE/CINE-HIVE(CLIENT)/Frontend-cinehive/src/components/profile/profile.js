import React, { useEffect, useState } from 'react';
import '../eachmoviegrid/grid.css';
import Eachmovie from '../eachmoviegrid';
import './profile.css';
import { useNavigate } from 'react-router-dom';

const Profile = () => {
    const [profile, setProfile] = useState({});
    const [likedMovies, setLikedMovies] = useState([]);
    const [watchlistMovies, setWatchlistMovies] = useState([]);
    const [isProfileLoading, setIsProfileLoading] = useState(true);
    const [isLikedLoading, setIsLikedLoading] = useState(true);
    const [isWatchlistLoading, setIsWatchlistLoading] = useState(true);

    const navigate = useNavigate();

    useEffect(() => {
        // Fetch profile data
        fetch('https://cinehive-backend.onrender.com/profile', { credentials: 'include' })
            .then(res => res.json())
            .then(data => {
                setProfile(data);
                setIsProfileLoading(false);
            })
            .catch(err => {
                console.error('Error fetching profile:', err);
                setIsProfileLoading(false);
            });
        
        // Fetch user's liked movies
        fetch('https://cinehive-backend.onrender.com/movies/liked', { credentials: 'include' })
            .then(res => res.json())
            .then(data => {
                console.log('Liked movies data:', data.data.movies);
                if (data.data?.movies) {
                    setLikedMovies(
                        data.data.movies.map(movie => ({
                            ...movie,
                            isLiked: true
                        }))
                    );
                }
                setIsLikedLoading(false);
            })
            .catch(err => {
                console.error('Error fetching liked movies:', err);
                setIsLikedLoading(false);
            });
        
        // Fetch user's watchlisted movies
        fetch('https://cinehive-backend.onrender.com/movies/watchlists', { credentials: 'include' })
            .then(res => res.json())
            .then(data => {
                console.log('Watchlist movies data:', data.data.movies);
                if (data.data?.movies) {
                    setWatchlistMovies(
                        data.data.movies.map(movie => ({
                            ...movie,
                            isWatchlisted: true
                        }))
                    );
                }
                setIsWatchlistLoading(false);
            })
            .catch(err => {
                console.error('Error fetching watchlist:', err);
                setIsWatchlistLoading(false);
            });
    }, []);

    // Format movies data for Eachmovie component
    const formatMovieData = (movies) => {
        return movies.map(movie => ({
            id: movie.id || movie.movie_id,
            posterImageUrl: movie.poster_path ? 
                `https://image.tmdb.org/t/p/w500${movie.poster_path}` : 
                (movie.posterImageUrl || '/placeholder-poster.jpg'),
            title: movie.title || movie.name,
            isLiked: movie.isLiked || false,
            isWatchlisted: movie.isWatchlisted || false
        }));
    };

    const isLoading = isProfileLoading || isLikedLoading || isWatchlistLoading;

    if (isLoading) {
        return <div className="loading">Loading...</div>;
    }

    return (
        <div className="profile-container">
            {/* Navbar */}
              <div className="navbar">
                <button onClick={() => navigate(-1)} className="nav-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M15 6l-6 6 6 6" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Back
                    </button>

                    <button onClick={() => navigate('/home')} className="nav-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M3 12l9-9 9 9v8a2 2 0 0 1-2 2h-4a2 2 0 0 1-2-2v-4h-4v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Home
                    </button>

                    <button onClick={() => navigate('/logout')} className="nav-button">
                    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
                        <path d="M16 17l5-5-5-5M21 12H9M13 5v-1a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1" stroke="white" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                    Logout
                    </button>

            </div>
            {/* Profile Header */}
            <div className="profile-header">
  <div className="profile-card">
    <div className="profile-avatar">
    <svg viewBox="0 0 24 24" fill="currentColor" width="48" height="48">
        <path d="M12 12c2.76 0 5-2.24 5-5s-2.24-5-5-5-5 2.24-5 5 2.24 5 5 5zm0 2c-3.33 0-10 1.67-10 5v3h20v-3c0-3.33-6.67-5-10-5z"/>
      </svg>
    </div>
    <div className="profile-details">
      <h2 className="profile-title">Welcome, {profile.username} 👋</h2>
      <p className="profile-email">{profile.email}</p>
    </div>
  </div>
</div>


            {/* Liked Movies Section */}
            <div className="movies-section">
                <h2>Liked Movies</h2>
                {likedMovies.length > 0 ? (
                    <div className="video-grid">
                        {formatMovieData(likedMovies).map(eachmovie => (
                            <Eachmovie details={eachmovie} key={eachmovie.id} />
                        ))}
                    </div>
                ) : (
                    <p className="no-movies">No liked movies found.</p>
                )}
            </div>

            {/* Watchlist Movies Section */}
            <div className="movies-section">
                <h2>My Watchlist</h2>
                {watchlistMovies.length > 0 ? (
                    <div className="video-grid">
                        {formatMovieData(watchlistMovies).map(eachmovie => (
                            <Eachmovie details={eachmovie} key={eachmovie.id} />
                        ))}
                    </div>
                ) : (
                    <p className="no-movies">No watchlisted movies found.</p>
                )}
            </div>
        </div>
        
    );
};

export default Profile;
