# SCARCITY Framework

**Scarcity-aware Causal Adaptive Resource-efficient Intelligence Training sYstem**

An advanced machine learning framework for online, resource-constrained environments with real-time causal discovery, adaptive resource management, and federated learning capabilities.

---

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- 4GB RAM minimum

### Backend Setup
```bash
cd backend
python -m venv .venv
.venv\Scripts\activate # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend Setup
```bash
cd scarcity-deep-dive
npm install
npm run dev
```

### Access
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- API: http://localhost:8000/api/v2

---

## Complete Documentation

**[→ View Complete Documentation Index](./DOCUMENTATION_INDEX.md)**

### Quick Links
- **[Product Overview](./docs/01-product-overview.md)** - What is SCARCITY?
- **[Architecture](./docs/02-architecture.md)** - System design and structure
- **[Mathematical Foundations](./docs/03-mathematical-foundations.md)** - Theory and math
- **[Core Algorithms](./docs/04-core-algorithms.md)** - Implementation details
- **[Backend Guide](./docs/05-backend-implementation.md)** - Backend deep dive

---

## Key Features

### Multi-Path Inference Engine (MPIE)
Discover causal relationships from streaming data automatically
- Real-time causal graph discovery
- Statistical validation with bootstrap resampling
- Hypergraph representation

### Dynamic Resource Governor (DRG)
Adapt to resource constraints dynamically
- Real-time CPU/memory/GPU monitoring
- PID-based control policies
- Predictive resource forecasting

### Federation Layer
Enable decentralized learning across organizations
- Peer-to-peer model sharing
- Multiple aggregation strategies (FedAvg, Weighted, Adaptive)
- Differential privacy protection

### Meta-Learning Agent
Transfer knowledge across domains and tasks
- Cross-domain optimization
- Prior knowledge extraction
- Adaptive hyperparameter tuning

### 3D Simulation Engine
Visualize and explore causal hypergraphs
- Interactive 3D visualization
- Force-directed graph layout
- Real-time updates

---

## Architecture

```

Frontend (React) 
Dashboard | Engine | Federation | Domains | Visualization 

REST API

Backend (FastAPI) 
API Layer | ScarcityCoreManager | Domain Manager 

Event Bus

Scarcity Core Components 
Runtime Bus | MPIE | DRG | Federation | Meta | Simulation 

```

---

## Project Structure

```
scace4/
backend/ # Python FastAPI backend
app/
api/v2/ # REST API endpoints
core/ # Business logic
main.py # FastAPI app
scripts/ # Utility scripts
tests/ # Test files

scarcity/ # Core ML library
runtime/ # Event bus
engine/ # MPIE orchestrator
governor/ # DRG
federation/ # Federation layer
meta/ # Meta-learning
simulation/ # 3D simulation

scarcity-deep-dive/ # React frontend
src/
pages/ # Page components
components/ # Reusable components
lib/ # API client
package.json

docs/ # Comprehensive documentation
01-product-overview.md
02-architecture.md
03-mathematical-foundations.md
04-core-algorithms.md
05-backend-implementation.md
```

---

## Use Cases

### Healthcare
Federated learning across hospitals without sharing patient data

### Finance
Real-time fraud detection with adaptive resource allocation

### Manufacturing
Predictive maintenance on edge devices with limited compute

### Retail
Multi-domain learning for rapid adaptation to new markets

---

## Technology Stack

### Backend
- **Framework**: FastAPI 0.115.0
- **Language**: Python 3.11+
- **Async**: asyncio
- **Validation**: Pydantic
- **Numerical**: NumPy

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build**: Vite
- **UI**: shadcn/ui
- **State**: TanStack Query

### Core Library
- **Language**: Python
- **Algorithms**: Custom implementations
- **Math**: NumPy, SciPy

---

## Performance

- **Data Ingestion**: 100-500 windows/second
- **Causal Discovery**: 50-200 candidate paths/second
- **API Latency**: < 100ms (p95)
- **Resource Monitoring**: 2 Hz
- **Memory Usage**: 500MB - 2GB
- **CPU**: 2-4 cores recommended

---

## Testing

```bash
# Backend tests
cd backend
pytest tests/

# Frontend tests
cd scarcity-deep-dive
npm test
```

---

## Documentation

### For Developers
1. [Architecture Guide](./docs/02-architecture.md)
2. [Backend Implementation](./docs/05-backend-implementation.md)
3. [API Reference](./docs/07-api-reference.md)

### For Data Scientists
1. [Mathematical Foundations](./docs/03-mathematical-foundations.md)
2. [Core Algorithms](./docs/04-core-algorithms.md)
3. [Data Flow](./docs/08-data-flow.md)

### For DevOps
1. [Deployment Guide](./docs/10-deployment.md)
2. [Configuration](./docs/10-deployment.md#configuration)
3. [Monitoring](./docs/10-deployment.md#monitoring)

---

## Contributing

We welcome contributions! Please see our [Development Guide](./docs/11-development-guide.md) for:
- Code style and conventions
- Git workflow
- Adding new features
- Testing requirements

---

## License

[Add license information here]

---

## Acknowledgments

Built with modern ML research and production best practices.

---

## Support

- **Documentation**: [Complete Documentation Index](./DOCUMENTATION_INDEX.md)
- **Troubleshooting**: [Troubleshooting Guide](./docs/12-troubleshooting.md)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)

---

**Version**: 2.0.0 
**Status**: Production Ready 
**Last Updated**: December 3, 2025
