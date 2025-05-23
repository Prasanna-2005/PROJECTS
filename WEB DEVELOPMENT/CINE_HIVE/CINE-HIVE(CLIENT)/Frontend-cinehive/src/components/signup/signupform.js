import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './signup.css';



class SignUpForm extends Component {
  state = {
    username: '',
    password: '',
    confirmPassword: '',
    email: '',
    showSubmitError: false,
    errorMsg: '',
  };

  onChangeUsername = event => this.setState({ username: event.target.value });
  onChangePassword = event => this.setState({ password: event.target.value });
  onChangeConfirmPassword = event => this.setState({ confirmPassword: event.target.value });
  onChangeEmail = event => this.setState({ email: event.target.value });

  submitForm = async event => {
    event.preventDefault();
    const { username, email, password, confirmPassword } = this.state;
    
    if (password !== confirmPassword) {
      this.setState({ showSubmitError: true, errorMsg: 'Passwords do not match' });
      return;
    }
    
    
    try {
     
      const response = await fetch('https://cinehive-backend.onrender.com/register', {
        method: 'POST',
        body: JSON.stringify({
          username: username,
          email: email,
          password: password
        }),
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      
      const data = await response.json();
      console.log(data);
      if (!response.ok) {
        throw new Error(data.message || 'Something went wrong');
      }
      
      alert('Registration successful! You can now log in.');
    } catch (error) {
      this.setState({ showSubmitError: true, errorMsg: error.message });
    }
  };

  render() {
    const { showSubmitError, errorMsg } = this.state;
    return (
       
        
      <div className="signup-container">
  <Link to="/" className="top-left-logo">
    <div className="netflix-logo">CineHive</div>
  </Link>
  
  <div className="signup-form-container">
    <h1 className="signup-title">Sign Up</h1>
    <form className="signup-form" onSubmit={this.submitForm}>
      <div className="form-group">
        <input
          type="text"
          id="username"
          placeholder="Username"
          onChange={this.onChangeUsername}
          className="form-input"
          required
        />
      </div>
      <div className="form-group">
        <input
          type="email"
          id="email"
          placeholder="Email"
          onChange={this.onChangeEmail}
          className="form-input"
          required
        />
      </div>
      <div className="form-group">
        <input
          type="password"
          id="password"
          placeholder="Password"
          onChange={this.onChangePassword}
          className="form-input"
          required
        />
      </div>
      <div className="form-group">
        <input
          type="password"
          id="confirmPassword"
          placeholder="Confirm Password"
          onChange={this.onChangeConfirmPassword}
          className="form-input"
          required
        />
      </div>
      <button type="submit" className="signup-button">
        Sign Up
      </button>
      {showSubmitError && <p className="error-message">*{errorMsg}</p>}
    </form>
    <div className="login-link">
      <p>
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  </div>
</div>
    );
  }
}

export default SignUpForm;