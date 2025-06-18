# YouTube API Service

A Flask-based API service for extracting YouTube video metadata using yt-dlp. Features Redis caching, rate limiting, bandwidth tracking, CORS support, and API key authentication.

## Features

- **Video Metadata Extraction**: Get video data, titles, descriptions, thumbnails, and captions
- **Redis Caching**: Cached video metadata for faster subsequent requests
- **Rate Limiting**: Redis-backed rate limiting (120 requests/minute)
- **Bandwidth Tracking**: Monitor network usage per request
- **API Key Authentication**: Secure endpoint access
- **CORS Support**: Browser-friendly with cross-origin requests
- **Production Ready**: Configured for Railway deployment with Gunicorn

## API Endpoints

### Health Check
```
GET /health
```
Returns service status (no auth required).

### Protected Endpoints
All endpoints require `Authorization` header with valid API key.

```
GET /video-data?url=<youtube_url>
GET /video-id?url=<youtube_url>
GET /title?url=<youtube_url>
GET /description?url=<youtube_url>
GET /thumbnail?url=<youtube_url>
GET /automatic-captions?url=<youtube_url>
```

### Example Usage
```bash
curl -H "Authorization: your-api-key" \
     "https://your-app.railway.app/video-data?url=https://youtube.com/watch?v=VIDEO_ID"
```

## Caching

The service uses Redis to cache video metadata:
- **Cache Key**: `video:{youtube_url}`
- **Cache Duration**: Persistent (no expiration)
- **Cached Data**: Complete video metadata including titles, descriptions, thumbnails, and automatic captions
- **Performance**: Subsequent requests for the same video return instantly from cache

## Environment Variables

Required for deployment:

```env
SECRET_KEY=your-secret-key
REDIS_URL=redis://localhost:6379
API_KEY=your-api-key

# Production proxy settings (optional)
PROXY_USERNAME=username
PROXY_PASSWORD=password
PROXY_PORT=port
```

## Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

3. **Run Redis locally**:
   ```bash
   redis-server
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Deployment

### Railway Deployment

The app is configured with:
- Gunicorn WSGI server (10 workers, 60s timeout)
- Production configuration with proxy support
- Nixpacks buildpack

## Technology Stack

- **Flask**: Web framework
- **yt-dlp**: YouTube data extraction
- **Redis**: Caching and rate limiting storage
- **Flask-CORS**: Cross-origin support
- **Flask-Limiter**: Rate limiting
- **Gunicorn**: WSGI server
- **psutil**: Bandwidth monitoring

## Rate Limits

- 120 requests per minute per IP address
- Configurable via Flask-Limiter
- Backed by Redis for distributed deployments