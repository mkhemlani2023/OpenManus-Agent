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



## 🚀 Backend Deployment

Now that your frontend is deployed on Netlify, you need to deploy the backend API to a separate hosting provider. This will allow your Netlify frontend to communicate with a live backend.

### 1. Push Backend Code to GitHub

First, create a new, empty public GitHub repository (e.g., `openmanus-backend`) and push the contents of the `/home/ubuntu/openmanus-backend-production/` directory to it. This directory contains:

- `app.py`: The main Flask application
- `requirements.txt`: Python dependencies
- `Procfile`: For Heroku deployment
- `.env.example`: Example environment variables
- `README.md`: Backend-specific documentation

### 2. Choose a Backend Hosting Provider

Here are some recommended options:

#### Option A: Railway (Recommended for ease of use and free tier)

1.  **Sign up/Log in to Railway:** Go to [https://railway.app/](https://railway.app/) and sign up or log in.
2.  **Create a new project:** Click on "New Project" and select "Deploy from GitHub Repo".
3.  **Connect your repository:** Select the GitHub repository where you pushed the backend code (e.g., `mkhemlani2023/openmanus-backend`).
4.  **Configure Environment Variables:**
    *   Railway will automatically detect your `Procfile` and `requirements.txt`.
    *   You **MUST** set the `SECRET_KEY` environment variable to a strong, random string. This is crucial for security.
    *   Optionally, set `DATABASE_URL` if you want to use a PostgreSQL database instead of SQLite (e.g., `postgresql://user:password@host:port/database`). If not set, SQLite will be used by default.
    *   Ensure `PORT` is set to `5000` (or the port your Flask app listens on).
5.  **Deploy:** Railway will automatically build and deploy your application. Once deployed, Railway will provide you with a public URL for your backend (e.g., `https://your-backend-url.up.railway.app`).

#### Option B: Heroku

1.  **Sign up/Log in to Heroku:** Go to [https://www.heroku.com/](https://www.heroku.com/) and sign up or log in.
2.  **Create a new app:** Click on "New" -> "Create new app".
3.  **Connect to GitHub:** Connect your Heroku app to the GitHub repository where your backend code is located.
4.  **Configure Buildpacks:** Add `heroku/python` buildpack.
5.  **Configure Environment Variables:** Set `SECRET_KEY` and optionally `DATABASE_URL`.
6.  **Deploy:** Deploy your app from the connected GitHub branch.

#### Option C: Render

1.  **Sign up/Log in to Render:** Go to [https://render.com/](https://render.com/) and sign up or log in.
2.  **New Web Service:** Create a new web service and connect your GitHub repository.
3.  **Configure Build and Start Commands:**
    *   **Build Command:** `pip install -r requirements.txt`
    *   **Start Command:** `gunicorn app:app`
4.  **Configure Environment Variables:** Set `SECRET_KEY` and optionally `DATABASE_URL`.
5.  **Deploy:** Deploy your web service.

### 3. Update Frontend API URL

Once your backend is deployed and you have its public URL, you need to update your Netlify frontend to point to this new URL.

1.  **Go to your Netlify site settings:** In your Netlify dashboard, navigate to your `openmanusagent.netlify.app` site.
2.  **Environment Variables:** Go to "Site settings" -> "Build & deploy" -> "Environment variables".
3.  **Add/Edit `VITE_API_URL`:** Add a new environment variable named `VITE_API_URL` and set its value to the public URL of your deployed backend (e.g., `https://your-backend-url.up.railway.app`).
4.  **Trigger a redeploy:** After saving the environment variable, trigger a redeploy of your Netlify site. This will rebuild your frontend with the correct backend API URL.

After these steps, your Netlify frontend should be able to communicate with your deployed backend, and the chat functionality with persistent storage will work correctly.

