#!/bin/bash

# ORBIT Production Deployment Script
# Automated deployment with zero-downtime and rollback capability

set -e

# Configuration
PROJECT_NAME="orbit"
DOCKER_REGISTRY="your-registry.com"
IMAGE_TAG="${1:-latest}"
ENVIRONMENT="${2:-production}"
BACKUP_RETENTION_DAYS=7

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."
    
    # Check if Docker is installed and running
    if ! command -v docker &> /dev/null; then
        error "Docker is not installed"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        error "Docker daemon is not running"
        exit 1
    fi
    
    # Check if Docker Compose is installed
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if environment file exists
    if [[ ! -f ".env.${ENVIRONMENT}" ]]; then
        error "Environment file .env.${ENVIRONMENT} not found"
        exit 1
    fi
    
    success "Prerequisites check passed"
}

# Create backup
create_backup() {
    log "Creating database backup..."
    
    BACKUP_DIR="./backups/$(date +'%Y-%m-%d_%H-%M-%S')"
    mkdir -p "$BACKUP_DIR"
    
    # Backup database
    docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump \
        -U "${POSTGRES_USER}" \
        -d "${POSTGRES_DB}" \
        --no-owner --no-privileges \
        > "${BACKUP_DIR}/database.sql"
    
    # Backup volumes
    docker run --rm \
        -v orbit_postgres_data:/data \
        -v "$(pwd)/${BACKUP_DIR}:/backup" \
        alpine tar czf /backup/postgres_data.tar.gz -C /data .
    
    docker run --rm \
        -v orbit_redis_data:/data \
        -v "$(pwd)/${BACKUP_DIR}:/backup" \
        alpine tar czf /backup/redis_data.tar.gz -C /data .
    
    docker run --rm \
        -v orbit_n8n_data:/data \
        -v "$(pwd)/${BACKUP_DIR}:/backup" \
        alpine tar czf /backup/n8n_data.tar.gz -C /data .
    
    success "Backup created at ${BACKUP_DIR}"
    echo "$BACKUP_DIR" > .last_backup
}

# Build and push images
build_and_push() {
    log "Building and pushing Docker images..."
    
    # Build the main application image
    docker build -t "${DOCKER_REGISTRY}/${PROJECT_NAME}:${IMAGE_TAG}" .
    
    # Tag as latest if this is a production deployment
    if [[ "$ENVIRONMENT" == "production" ]]; then
        docker tag "${DOCKER_REGISTRY}/${PROJECT_NAME}:${IMAGE_TAG}" \
                   "${DOCKER_REGISTRY}/${PROJECT_NAME}:latest"
    fi
    
    # Push images
    docker push "${DOCKER_REGISTRY}/${PROJECT_NAME}:${IMAGE_TAG}"
    
    if [[ "$ENVIRONMENT" == "production" ]]; then
        docker push "${DOCKER_REGISTRY}/${PROJECT_NAME}:latest"
    fi
    
    success "Images built and pushed successfully"
}

# Deploy application
deploy() {
    log "Deploying ORBIT ${IMAGE_TAG} to ${ENVIRONMENT}..."
    
    # Copy environment file
    cp ".env.${ENVIRONMENT}" .env
    
    # Pull latest images
    docker-compose -f docker-compose.prod.yml pull
    
    # Run database migrations
    log "Running database migrations..."
    docker-compose -f docker-compose.prod.yml run --rm orbit-api \
        python -m alembic upgrade head
    
    # Deploy with zero downtime
    log "Starting new containers..."
    docker-compose -f docker-compose.prod.yml up -d --remove-orphans
    
    # Wait for services to be healthy
    log "Waiting for services to be healthy..."
    sleep 30
    
    # Health check
    if ! curl -f http://localhost/health &> /dev/null; then
        error "Health check failed, rolling back..."
        rollback
        exit 1
    fi
    
    # Clean up old images
    docker image prune -f
    
    success "Deployment completed successfully"
}

# Rollback function
rollback() {
    warning "Rolling back to previous version..."
    
    if [[ -f ".last_backup" ]]; then
        BACKUP_DIR=$(cat .last_backup)
        
        # Stop current containers
        docker-compose -f docker-compose.prod.yml down
        
        # Restore database
        docker-compose -f docker-compose.prod.yml up -d postgres redis
        sleep 10
        
        docker-compose -f docker-compose.prod.yml exec -T postgres psql \
            -U "${POSTGRES_USER}" \
            -d "${POSTGRES_DB}" \
            -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
        
        docker-compose -f docker-compose.prod.yml exec -T postgres psql \
            -U "${POSTGRES_USER}" \
            -d "${POSTGRES_DB}" \
            < "${BACKUP_DIR}/database.sql"
        
        # Restore volumes
        docker run --rm \
            -v orbit_postgres_data:/data \
            -v "$(pwd)/${BACKUP_DIR}:/backup" \
            alpine tar xzf /backup/postgres_data.tar.gz -C /data
        
        # Restart services
        docker-compose -f docker-compose.prod.yml up -d
        
        success "Rollback completed"
    else
        error "No backup found for rollback"
    fi
}

# Clean up old backups
cleanup_backups() {
    log "Cleaning up old backups..."
    
    find ./backups -type d -name "*_*-*-*" -mtime +${BACKUP_RETENTION_DAYS} -exec rm -rf {} \;
    
    success "Old backups cleaned up"
}

# Monitor deployment
monitor() {
    log "Monitoring deployment..."
    
    # Check service status
    docker-compose -f docker-compose.prod.yml ps
    
    # Show logs
    docker-compose -f docker-compose.prod.yml logs --tail=50 orbit-api
    
    # Performance check
    log "Running performance checks..."
    
    # API response time
    RESPONSE_TIME=$(curl -o /dev/null -s -w '%{time_total}' http://localhost/health)
    log "API response time: ${RESPONSE_TIME}s"
    
    # Memory usage
    MEMORY_USAGE=$(docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}" | grep orbit)
    log "Memory usage:\n${MEMORY_USAGE}"
    
    success "Monitoring completed"
}

# Main deployment flow
main() {
    log "Starting ORBIT deployment process..."
    log "Environment: ${ENVIRONMENT}"
    log "Image tag: ${IMAGE_TAG}"
    
    check_prerequisites
    create_backup
    
    # Only build and push if not using existing image
    if [[ "$IMAGE_TAG" != "latest" ]] && [[ "$IMAGE_TAG" != *":"* ]]; then
        build_and_push
    fi
    
    deploy
    cleanup_backups
    monitor
    
    success "ORBIT deployment completed successfully!"
    log "Access your application at: https://your-domain.com"
    log "Monitoring dashboard: https://your-domain.com:3001"
    log "n8n workflows: https://your-domain.com:5678"
}

# Handle script arguments
case "${1:-deploy}" in
    "deploy")
        main
        ;;
    "rollback")
        rollback
        ;;
    "backup")
        create_backup
        ;;
    "monitor")
        monitor
        ;;
    "cleanup")
        cleanup_backups
        ;;
    *)
        echo "Usage: $0 {deploy|rollback|backup|monitor|cleanup} [image_tag] [environment]"
        echo ""
        echo "Commands:"
        echo "  deploy    - Deploy the application (default)"
        echo "  rollback  - Rollback to previous version"
        echo "  backup    - Create backup only"
        echo "  monitor   - Monitor current deployment"
        echo "  cleanup   - Clean up old backups"
        echo ""
        echo "Examples:"
        echo "  $0 deploy v1.2.3 production"
        echo "  $0 rollback"
        echo "  $0 backup"
        exit 1
        ;;
esac