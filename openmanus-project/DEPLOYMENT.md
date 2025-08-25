# OpenManus Deployment Guide

This guide covers how to deploy OpenManus to various platforms and set up the complete application stack.

## 🚀 Quick Start Deployment

### Frontend Deployment (Netlify)

The frontend is ready for immediate deployment to Netlify:

1. **Automatic Deployment** (Recommended)
   - The application has been packaged and is ready for Netlify deployment
   - Use the publish button in the UI to deploy instantly
   - The build artifacts are in the `dist/` folder

2. **Manual Deployment**
   ```bash
   # Build the frontend
   npm run build
   
   # Deploy the dist folder to Netlify
   # The _redirects file is already configured for SPA routing
   ```

### Backend Deployment Options

#### Option 1: Railway (Recommended)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

#### Option 2: Heroku
```bash
# Create Procfile (already included)
echo "web: cd api && python main.py" > Procfile

# Deploy to Heroku
heroku create openmanus-backend
git push heroku main
```

#### Option 3: DigitalOcean App Platform
- Upload the `api/` folder
- Set build command: `pip install -r requirements.txt`
- Set run command: `python main.py`

## 🔧 Configuration

### Environment Variables

#### Frontend (.env)
```env
VITE_API_URL=https://your-backend-url.com
```

#### Backend (.env)
```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///production.db
CORS_ORIGINS=https://your-frontend-url.netlify.app
```

### Database Setup

#### SQLite (Default)
- No additional setup required
- Database file created automatically
- Perfect for small to medium applications

#### PostgreSQL (Production)
```bash
# Install psycopg2
pip install psycopg2-binary

# Update DATABASE_URL
export DATABASE_URL=postgresql://user:password@host:port/database
```

## 📁 Project Structure for Deployment

```
openmanus-project/
├── dist/                   # Built frontend (deploy to Netlify)
│   ├── index.html
│   ├── assets/
│   └── _redirects         # SPA routing configuration
├── api/                   # Backend (deploy separately)
│   ├── main.py           # Flask application entry point
│   ├── models/           # Database models
│   ├── routes/           # API routes
│   └── requirements.txt  # Python dependencies
└── src/                  # Frontend source (for development)
```

## 🌐 Domain Configuration

### Custom Domain Setup

#### Netlify
1. Go to Site Settings > Domain Management
2. Add custom domain
3. Configure DNS records:
   ```
   Type: CNAME
   Name: www
   Value: your-site.netlify.app
   ```

#### Backend Domain
1. Configure your backend hosting provider
2. Update CORS settings in Flask app
3. Update frontend API URL

## 🔒 Security Configuration

### Production Security Checklist

#### Frontend
- [ ] Environment variables configured
- [ ] API URLs updated for production
- [ ] HTTPS enforced
- [ ] CSP headers configured

#### Backend
- [ ] Secret key changed from default
- [ ] CORS origins restricted to frontend domain
- [ ] Database credentials secured
- [ ] Input validation enabled
- [ ] Rate limiting configured

### CORS Configuration
```python
# In api/main.py
CORS(app, origins=[
    "https://your-frontend.netlify.app",
    "https://your-custom-domain.com"
])
```

## 📊 Monitoring and Analytics

### Application Monitoring
- **Frontend**: Netlify Analytics (built-in)
- **Backend**: Add logging and monitoring service
- **Database**: Monitor query performance

### Error Tracking
```python
# Add to api/main.py
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
```

## 🔄 CI/CD Pipeline

### GitHub Actions (Optional)
```yaml
# .github/workflows/deploy.yml
name: Deploy to Netlify
on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Node.js
        uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm install
      - run: npm run build
      - name: Deploy to Netlify
        uses: nwtgck/actions-netlify@v1.2
        with:
          publish-dir: './dist'
        env:
          NETLIFY_AUTH_TOKEN: ${{ secrets.NETLIFY_AUTH_TOKEN }}
          NETLIFY_SITE_ID: ${{ secrets.NETLIFY_SITE_ID }}
```

## 🐛 Troubleshooting

### Common Deployment Issues

#### Frontend Issues
1. **404 on page refresh**
   - Ensure `_redirects` file exists in `dist/`
   - Content: `/* /index.html 200`

2. **API connection failed**
   - Check VITE_API_URL environment variable
   - Verify CORS configuration on backend

#### Backend Issues
1. **Database connection failed**
   - Check DATABASE_URL format
   - Ensure database file permissions (SQLite)

2. **CORS errors**
   - Update CORS origins in Flask app
   - Check frontend domain configuration

### Performance Optimization

#### Frontend
- Lazy loading implemented
- Code splitting enabled
- Assets optimized in build process

#### Backend
- Database query optimization
- Response caching (add Redis if needed)
- Connection pooling for production databases

## 📈 Scaling Considerations

### When to Scale

#### Frontend
- Use CDN for global distribution
- Implement service worker for offline functionality
- Add performance monitoring

#### Backend
- Move to PostgreSQL for better performance
- Add Redis for session storage
- Implement horizontal scaling

### Database Scaling
```python
# PostgreSQL configuration for production
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 120,
    'pool_pre_ping': True
}
```

## 🔐 Backup and Recovery

### Database Backup
```bash
# SQLite backup
cp api/database/app.db backup/app_$(date +%Y%m%d).db

# PostgreSQL backup
pg_dump $DATABASE_URL > backup/db_$(date +%Y%m%d).sql
```

### Automated Backups
- Set up daily database backups
- Store backups in cloud storage
- Test recovery procedures regularly

## 📞 Support and Maintenance

### Regular Maintenance Tasks
- [ ] Update dependencies monthly
- [ ] Monitor error logs weekly
- [ ] Review performance metrics
- [ ] Update security configurations

### Getting Help
- Check GitHub Issues for common problems
- Review application logs for error details
- Monitor Netlify and backend hosting dashboards

---

**Deployment Status**: ✅ Ready for production deployment
**Last Updated**: $(date)
**Version**: 1.0.0

