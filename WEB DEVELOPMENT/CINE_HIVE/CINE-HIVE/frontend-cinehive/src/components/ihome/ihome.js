import { useEffect, useRef, useState } from 'react';
import { Link } from 'react-router-dom';
import './home.css';

const CineHive = () => {
  const canvasRef = useRef(null);
  const logoRef = useRef(null);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    // Dynamic constellation background
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    
    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Create stars
    const starCount = Math.min(Math.floor(window.innerWidth * window.innerHeight / 3000), 200);
    const stars = [];
    
    for (let i = 0; i < starCount; i++) {
      stars.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.5 + 0.5,
        vx: Math.random() * 0.05 - 0.025,
        vy: Math.random() * 0.05 - 0.025,
        opacity: Math.random() * 0.5 + 0.5,
        pulseSpeed: Math.random() * 0.02 + 0.003,
        pulseOffset: Math.random() * Math.PI * 2,
      });
    }
    
    // Create connection lines between stars
    const drawConstellations = (mouseX, mouseY) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw stars
      stars.forEach((star, index) => {
        // Update position
        star.x += star.vx;
        star.y += star.vy;
        
        // Wrap around edges
        if (star.x < 0) star.x = canvas.width;
        if (star.x > canvas.width) star.x = 0;
        if (star.y < 0) star.y = canvas.height;
        if (star.y > canvas.height) star.y = 0;
        
        // Pulsing effect
        const pulse = Math.sin(Date.now() * star.pulseSpeed + star.pulseOffset) * 0.2 + 0.8;
        
        // Mouse influence
        const dx = mouseX - star.x;
        const dy = mouseY - star.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        let starOpacity = star.opacity;
        let starRadius = star.radius;
        
        if (distance < 100) {
          const influence = 1 - distance / 100;
          starOpacity = Math.min(1, star.opacity + influence * 0.5);
          starRadius = star.radius + influence * 2;
        }
        
        // Draw star
        ctx.beginPath();
        ctx.arc(star.x, star.y, starRadius * pulse, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(138, 43, 226, ${starOpacity * pulse})`;
        ctx.fill();
        
        // Draw connections between nearby stars
        stars.forEach((otherStar, otherIndex) => {
          if (index !== otherIndex) {
            const dx = star.x - otherStar.x;
            const dy = star.y - otherStar.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            
            if (distance < 150) {
              ctx.beginPath();
              ctx.moveTo(star.x, star.y);
              ctx.lineTo(otherStar.x, otherStar.y);
              
              const opacity = (1 - distance / 150) * 0.2 * pulse;
              ctx.strokeStyle = `rgba(138, 43, 226, ${opacity})`;
              ctx.lineWidth = 0.5;
              ctx.stroke();
            }
          }
        });
        
        // Draw connections to mouse
        if (distance < 200) {
          ctx.beginPath();
          ctx.moveTo(star.x, star.y);
          ctx.lineTo(mouseX, mouseY);
          
          const opacity = (1 - distance / 200) * 0.3;
          ctx.strokeStyle = `rgba(0, 255, 204, ${opacity})`;
          ctx.lineWidth = 0.8;
          ctx.stroke();
        }
      });
      
      // Draw radial glow around mouse
      const gradient = ctx.createRadialGradient(mouseX, mouseY, 10, mouseX, mouseY, 200);
      gradient.addColorStop(0, 'rgba(138, 43, 226, 0.05)');
      gradient.addColorStop(1, 'rgba(138, 43, 226, 0)');
      
      ctx.beginPath();
      ctx.arc(mouseX, mouseY, 200, 0, Math.PI * 2);
      ctx.fillStyle = gradient;
      ctx.fill();
    };
    
    // Animation loop
    let animationId;
    const animate = () => {
      drawConstellations(mousePosition.x, mousePosition.y);
      animationId = requestAnimationFrame(animate);
    };
    
    animate();
    
    // Logo animation
    const logo = logoRef.current;
    if (logo) {
      const letters = logo.querySelectorAll('span');
      
      const handleLogoHover = (e) => {
        const rect = logo.getBoundingClientRect();
        const centerX = rect.left + rect.width / 2;
        const centerY = rect.top + rect.height / 2;
        
        letters.forEach((letter, i) => {
          const letterRect = letter.getBoundingClientRect();
          const letterX = letterRect.left + letterRect.width / 2;
          
          // Calculate distance from mouse to this letter
          const dx = e.clientX - letterX;
          const dy = e.clientY - letterRect.top;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          // Apply 3D effect based on distance
          const intensity = Math.max(0, 1 - distance / 100);
          const rotateY = (letterX - centerX) / 10;
          
          letter.style.transform = `
            perspective(500px) 
            rotateY(${rotateY}deg) 
            translateY(${-intensity * 5}px) 
            translateZ(${intensity * 20}px)
          `;
          
          // Apply glow effect
          letter.style.textShadow = `
            0 0 ${5 + intensity * 15}px rgba(138, 43, 226, ${0.3 + intensity * 0.7})
          `;
          
          // Modify color based on position
          if (i % 2 === 0) {
            letter.style.color = `rgba(255, 255, 255, ${0.8 + intensity * 0.2})`;
          } else {
            letter.style.color = `rgba(0, 255, 204, ${0.8 + intensity * 0.2})`;
          }
        });
      };
      
      logo.addEventListener('mousemove', handleLogoHover);
      logo.addEventListener('mouseleave', () => {
        letters.forEach((letter, i) => {
          letter.style.transform = 'perspective(500px) rotateY(0) translateY(0) translateZ(0)';
          letter.style.textShadow = i % 2 === 0 ? 
            '0 0 10px rgba(138, 43, 226, 0.5)' : 
            '0 0 10px rgba(0, 255, 204, 0.5)';
          letter.style.color = i % 2 === 0 ? 'rgb(255, 255, 255)' : 'rgb(0, 255, 204)';
        });
      });
    }
    
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    const letters = logo.querySelectorAll('span');
      
    const handleLogoHover = (e) => {
      const rect = logo.getBoundingClientRect();
      const centerX = rect.left + rect.width / 2;
      const centerY = rect.top + rect.height / 2;
      
      letters.forEach((letter, i) => {
        const letterRect = letter.getBoundingClientRect();
        const letterX = letterRect.left + letterRect.width / 2;
        
        // Calculate distance from mouse to this letter
        const dx = e.clientX - letterX;
        const dy = e.clientY - letterRect.top;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        // Apply 3D effect based on distance
        const intensity = Math.max(0, 1 - distance / 100);
        const rotateY = (letterX - centerX) / 10;
        
        letter.style.transform = `
          perspective(500px) 
          rotateY(${rotateY}deg) 
          translateY(${-intensity * 5}px) 
          translateZ(${intensity * 20}px)
        `;
        
        // Apply glow effect
        letter.style.textShadow = `
          0 0 ${5 + intensity * 15}px rgba(138, 43, 226, ${0.3 + intensity * 0.7})
        `;
        
        // Modify color based on position
        if (i % 2 === 0) {
          letter.style.color = `rgba(255, 255, 255, ${0.8 + intensity * 0.2})`;
        } else {
          letter.style.color = `rgba(0, 255, 204, ${0.8 + intensity * 0.2})`;
        }
      });
    };
    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener('resize', resizeCanvas);
      window.removeEventListener('mousemove', handleMouseMove);
      if (logo) {
        logo.removeEventListener('mousemove', handleLogoHover);
      }
    };
  }, [mousePosition]);

  // Parallax effect on content
  useEffect(() => {
    const handleMouseMove = (e) => {
      const authContent = document.querySelector('.auth-content');
      if (authContent) {
        const xValue = (e.clientX - window.innerWidth / 2) / 25;
        const yValue = (e.clientY - window.innerHeight / 2) / 25;
        authContent.style.transform = `translate(${xValue}px, ${yValue}px)`;
      }
    };
    
    window.addEventListener('mousemove', handleMouseMove);
    
    return () => {
      window.removeEventListener('mousemove', handleMouseMove);
    };
  }, []);

  return (
    <div className="cinehive-container">
      <canvas ref={canvasRef} className="dynamic-bg"></canvas>
      
      {/* Animated background layers */}
      <div className="bg-layer layer-1"></div>
      <div className="bg-layer layer-2"></div>
      <div className="bg-layer layer-3"></div>
      
      <nav className="cinehive-nav">
        <div ref={logoRef} className="cinehive-logo">
          <span>C</span><span>I</span><span>N</span><span>E</span>
          <span className="divider">-</span>
          <span>H</span><span>I</span><span>V</span><span>E</span>
        </div>
      </nav>

      <main className="cinehive-main">
        <div className="auth-content">
          <h1 className="main-title">
            <span className="text-effect">Enter The Cinematic Universe</span>
          </h1>
          
          <p className="main-subtitle">
            Connect with film enthusiasts and discover your next favorite movie
          </p>
          
          <div className="auth-actions">
            <Link to="/login" className="cine-btn login-btn">
              <span className="btn-text">Access Your Account</span>
              <span className="btn-glow"></span>
            </Link>
            
            <Link to="/signup" className="cine-btn register-btn">
              <span className="btn-text">Create New Account</span>
              <span className="btn-glow"></span>
            </Link>
          </div>
        </div>
      </main>
      
      {/* Floating elements */}
      <div className="floating-elements">
        {Array.from({ length: 5 }).map((_, i) => (
          <div key={i} className={`floating-element elem-${i + 1}`}>
            <div className="element-inner"></div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CineHive;