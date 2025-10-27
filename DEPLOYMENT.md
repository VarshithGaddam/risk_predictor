# Deployment Guide

## Local Development

See README.md for local setup instructions.

## Production Deployment

### Option 1: Vercel (Frontend) + Render (Backend)

#### Backend on Render

1. Create account at https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: healthcare-analytics-api
   - **Root Directory**: backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `gunicorn app:app`
5. Add to requirements.txt: `gunicorn==21.2.0`
6. Add environment variable: `PYTHON_VERSION=3.11.0`
7. Deploy!

#### Frontend on Vercel

1. Create account at https://vercel.com
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: dist
4. Add environment variable:
   - `VITE_API_URL`: Your Render backend URL
5. Deploy!

### Option 2: Railway (Full Stack)

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub repo"
3. Add two services:

**Backend Service:**
- Root Directory: `/backend`
- Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
- Start Command: `gunicorn app:app`
- Add PORT environment variable

**Frontend Service:**
- Root Directory: `/frontend`
- Build Command: `npm install && npm run build`
- Start Command: `npm run preview`
- Add VITE_API_URL pointing to backend service

### Option 3: Docker Deployment

#### Backend Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

#### Frontend Dockerfile
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
    volumes:
      - ./backend/healthcare.db:/app/healthcare.db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    environment:
      - VITE_API_URL=http://localhost:5000
    depends_on:
      - backend
```

## Environment Variables

### Backend
- `FLASK_ENV`: production
- `SECRET_KEY`: Generate a secure random key
- `DATABASE`: Path to SQLite database file

### Frontend
- `VITE_API_URL`: Backend API URL

## Database Persistence

For production, consider:
1. Using PostgreSQL instead of SQLite
2. Setting up automated backups
3. Using a managed database service

## Security Considerations

1. **HTTPS**: Always use HTTPS in production
2. **CORS**: Configure CORS to only allow your frontend domain
3. **API Keys**: Add authentication for API endpoints
4. **Rate Limiting**: Implement rate limiting to prevent abuse
5. **Input Validation**: Validate all user inputs
6. **SQL Injection**: Use parameterized queries (already implemented)

## Performance Optimization

1. **Caching**: Add Redis for caching dashboard metrics
2. **CDN**: Use CDN for frontend static assets
3. **Database Indexing**: Add indexes on frequently queried columns
4. **Compression**: Enable gzip compression
5. **Lazy Loading**: Implement lazy loading for large patient lists

## Monitoring

Consider adding:
- Error tracking (Sentry)
- Performance monitoring (New Relic, DataDog)
- Uptime monitoring (UptimeRobot)
- Log aggregation (Loggly, Papertrail)

## Scaling

For high traffic:
1. Use load balancer for multiple backend instances
2. Implement database connection pooling
3. Use message queue for async tasks
4. Consider microservices architecture
5. Implement caching layer (Redis)

## Backup Strategy

1. Automated daily database backups
2. Store backups in separate location (S3, Google Cloud Storage)
3. Test restore procedures regularly
4. Keep backups for 30 days minimum

## CI/CD Pipeline

Example GitHub Actions workflow:

```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
      
      - name: Deploy to Vercel
        run: |
          npm install -g vercel
          vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

## Health Checks

Implement health check endpoints:
- `/api/health` - Basic health check
- `/api/health/db` - Database connectivity
- `/api/health/ml` - ML model status

## Troubleshooting

Common issues:
1. **CORS errors**: Check CORS configuration in Flask
2. **Database locked**: Use connection pooling
3. **Memory issues**: Increase container memory limits
4. **Slow queries**: Add database indexes
5. **Model loading**: Ensure spaCy model is downloaded
