const db = require('../config/db.config');
const bcrypt = require('bcrypt');

exports.register = async (req, res) => {
    try {
      const { email, username, password } = req.body;
  
      if (!username || !email || !password) {
        return res.status(400).json({ message: 'All fields are required' });
      }
  
      // Check if user exists
      const [existingUsers] = await db.query(
        'SELECT * FROM users WHERE email = ?',
        [email]
      );
      console.log(existingUsers);
      if (existingUsers.length > 0) {
        return res.status(400).json({ message: 'Username or email already exists' });
      }
  
      // Hash password
      const salt = await bcrypt.genSalt(10);
      const hashedPassword = await bcrypt.hash(password, salt);
  
      let role = 'user';
      const [result] = await db.query(
        'INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)',
        [username, email, hashedPassword, role]
      );
  
      if (result.affectedRows === 1) {
        return res.status(201).json({ 
          message: 'User registered successfully', 
          role: role 
        });
      } else {
        return res.status(500).json({ message: 'Failed to register user' });
      }
  
    } catch (error) {
      console.error(error);
      return res.status(500).json({ message: 'Server error' });
    }
  };
  





exports.login = async (req, res) => {
  try {
  
    const { email, password } = req.body;
   
    const [users] = await db.query(
      'SELECT * FROM users WHERE email = ?',
      [email]
    );

    if (users.length === 0) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }

    const user = users[0];

    // Verify password
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }
    
    // Store user info in session
    // req.session.user = {
    //   id: user.id,
    //   username: user.username,
    //   email: user.email,
    //   role: user.role
    // };
    // req.session.isLoggedIn = true;

    res.cookie('user_id', user.id, {
      httpOnly: true,    // Prevents JavaScript access
      secure: true,      // Only sent over HTTPS
      sameSite: 'none',  // Required for cross-site cookies
      signed: true,      // Encrypts the cookie value
      maxAge: 24 * 60 * 60 * 1000, // 24 hours
    });


    return res.status(200).json({
      message: 'Login successful',
      user: {
        id: user.id,
        username: user.username,
        email: user.email,
        role: user.role
      }
    });
  } catch (error) {
    console.error(error);
    return res.status(500).json({ message: 'Server error' });
  }
};




exports.logout = (req, res) => {
  req.session.destroy((err) => {
    if (err) {
      return res.status(500).json({ message: 'Failed to logout' });
    }
        return res.status(200).json({ message: 'Logged out successfully' });
  });
};




exports.getProfile = async (req, res) => {
  try {
    
    const [users] = await db.query(
      'SELECT id, username, email,role FROM users WHERE id = ?', 
      [req.signedCookies.user_id]
    );
    
    if (users.length === 0) {
      return res.status(404).json({ message: 'User not found' });
    }
    
    return res.status(200).json(users[0]);
  } catch (error) {
    console.error(error);
    return res.status(500).json({ message: 'Server error' });
  }
};


