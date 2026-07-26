const express = require('express');
const path = require('path');
const dotenv = require('dotenv');
const compression = require('compression');

// Load environment variables from .env file
dotenv.config();

const app = express();
const PORT = process.env.PORT || 3000;
const API_URL = process.env.API_URL || 'http://localhost:8000';

// Enable GZip compression for all responses
app.use(compression());

// Serve dynamic environment configuration for browser runtime
app.get('/env.js', (req, res) => {
  res.setHeader('Content-Type', 'application/javascript');
  res.setHeader('Cache-Control', 'no-cache');
  res.send(`window.APP_CONFIG = Object.freeze({ API_URL: "${process.env.API_URL || 'http://localhost:8000'}" });`);
});

// Serve static assets from frontend directory with HTTP caching
app.use('/css', express.static(path.join(__dirname, 'css')));
app.use('/js', express.static(path.join(__dirname, 'js')));
app.use(express.static(__dirname, {
  maxAge: '1d',
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.html')) {
      res.setHeader('Cache-Control', 'no-cache');
    }
  }
}));

// Route handlers for landing page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'html', 'index.html'));
});
app.get('/index.html', (req, res) => {
  res.sendFile(path.join(__dirname, 'html', 'index.html'));
});

// Clean route navigation to HTML pages with and without .html extension
const pages = ['login', 'admin', 'ngo', 'restaurant', 'student', 'volunteer'];
pages.forEach(page => {
  const handler = (req, res) => res.sendFile(path.join(__dirname, 'html', `${page}.html`));
  app.get(`/${page}`, handler);
  app.get(`/${page}.html`, handler);
  app.get(`/html/${page}.html`, handler);
});

// Catch-all fallback handler
app.use((req, res) => {
  res.sendFile(path.join(__dirname, 'html', 'index.html'));
});

if (require.main === module) {
  app.listen(PORT, () => {
    console.log(`==========================================`);
    console.log(`🚀 FoodShare Optimized Frontend Server Running!`);
    console.log(`🌐 Server URL : http://localhost:${PORT}`);
    console.log(`🔗 Backend API: ${API_URL}`);
    console.log(`⚡ GZip Compression & Caching: ACTIVE`);
    console.log(`==========================================`);
  });
}

module.exports = app;
