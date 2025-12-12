# Deployment

Learn how to deploy Ceylon AI agents to production environments.

## Deployment Options

Ceylon AI agents can be deployed in various ways depending on your infrastructure and requirements:

### Serverless Deployment

- **[Modal.com](modal.md)** - Recommended for most use cases
  - Zero infrastructure management
  - Automatic scaling
  - Pay-per-use pricing
  - Built-in Ollama support

### Container Deployment

- **Docker** - Package your agent in a container
- **Kubernetes** - Orchestrate multiple agents
- **Cloud Run** - Google Cloud's container platform
- **AWS Lambda** - Amazon's serverless compute

### Traditional Deployment

- **Virtual Machines** - Full control over environment
- **Dedicated Servers** - Maximum performance
- **On-Premises** - Complete data sovereignty

## Choosing a Deployment Method

| Method         | Best For                                  | Complexity         | Cost        |
| -------------- | ----------------------------------------- | ------------------ | ----------- |
| **Modal.com**  | Quick deployments, prototypes, production | ⭐ Low             | 💰 Variable |
| **Docker**     | Consistent environments, portability      | ⭐⭐ Medium        | 💰💰 Fixed  |
| **Kubernetes** | Large scale, high availability            | ⭐⭐⭐⭐ High      | 💰💰💰 High |
| **VM/Server**  | Full control, custom requirements         | ⭐⭐⭐ Medium-High | 💰💰 Fixed  |

## Getting Started

### Quick Start: Modal.com

For the fastest path to production, we recommend Modal.com:

1. **Install Modal**:

   ```bash
   pip install modal
   ```

2. **Authenticate**:

   ```bash
   modal setup
   ```

3. **Deploy**:
   ```bash
   modal deploy my_agent.py
   ```

See the [Modal.com Guide](modal.md) for detailed instructions.

### Docker Deployment

Package your agent in a container:

```dockerfile
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y python3.12 curl
RUN curl -fsSL https://ollama.ai/install.sh | sh
RUN pip install ceylonai-next
COPY my_agent.py /app/
CMD ["python3", "/app/my_agent.py"]
```

## Production Considerations

### Security

- Use environment variables for sensitive configuration
- Implement authentication for web endpoints
- Keep dependencies updated
- Use HTTPS for all external communication

### Monitoring

- Log all agent interactions
- Track performance metrics
- Set up alerting for errors
- Monitor resource usage

### Scaling

- Use horizontal scaling for high traffic
  -implement rate limiting
- Cache frequent queries
- Consider load balancing

### Cost Optimization

- Choose appropriate model sizes
- Use persistent storage for models
- Set realistic timeouts
- Monitor and optimize resource usage

## Deployment Guides

- **[Modal.com Deployment](modal.md)** - Step-by-step guide for serverless deployment

## Coming Soon

- Docker Deployment Guide
- Kubernetes Deployment Guide
- AWS Lambda Deployment Guide
- Google Cloud Run Deployment Guide

## Need Help?

- Check the [Modal.com Guide](modal.md) for detailed instructions
- Visit our [GitHub repository](https://github.com/ceylonai/next-processor)
- Join our community discussions
