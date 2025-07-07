# ACM Component Dependency Graph

## Overview
This document provides a comprehensive dependency graph for Red Hat Advanced Cluster Management (ACM) based on analysis of the threat model questionnaires and Threat Dragon diagrams.

## Core Architecture Layers

### 1. Foundation Layer (Server Foundation)
**Core Components:**
- `cluster-manager` - Central hub management
- `klusterlet` - Managed cluster agent
- `ocm-proxyserver` - API aggregation
- `cluster-proxy-addon` - Cluster-to-cluster communication

**Dependencies:**
- **Internal**: All other ACM components depend on Server Foundation
- **External**: None (foundation layer)

### 2. Management Layer

#### Console & User Interface
**Components:**
- `console` - RHACM UI plugin
- `console-mce` - MCE UI plugin  
- `acm-cli` - CLI download service

**Dependencies:**
- **Internal**: 
  - Server Foundation (for cluster management)
  - Search (for resource discovery)
  - App Lifecycle (for application management)
  - GRC (for policy management)
  - Observability (for metrics/insights)
- **External**:
  - GitHub (for repository access)
  - Ansible Tower (for automation)
  - Red Hat Insights (for cluster insights)

#### Search
**Components:**
- `search-collector` - Data collection
- `search-aggregator` - Data aggregation
- `search-api` - Search API
- `search-redisgraph` - Graph database

**Dependencies:**
- **Internal**:
  - Server Foundation (for cluster communication via proxy)
  - All managed clusters (for data collection)
- **External**: None

### 3. Application & Policy Layer

#### Application Lifecycle
**Components:**
- `multicloud-operators-application` - Application management
- `multicloud-operators-channel` - Repository management
- `multicloud-operators-subscription` - Deployment management
- `multicloud-integrations` - External integrations

**Dependencies:**
- **Internal**:
  - Server Foundation (for cluster management)
  - Search (for resource discovery)
- **External**:
  - GitHub/Git repositories
  - Helm repositories
  - Object stores (MinIO, AWS S3)
  - Ansible Tower
  - Argo CD

#### Governance, Risk & Compliance (GRC)
**Components:**
- `governance-policy-propagator` - Policy distribution
- `governance-policy-addon-controller` - Addon management
- `cert-policy-controller` - Certificate policies
- `config-policy-controller` - Configuration policies
- `gatekeeper-operator` - OPA Gatekeeper integration

**Dependencies:**
- **Internal**:
  - Server Foundation (for cluster communication)
  - App Lifecycle (for GitOps integration)
- **External**:
  - GitHub (for policy repositories)
  - Ansible Tower (for remediation)
  - Community policy repositories

### 4. Observability Layer

#### Observability
**Components:**
- `multicluster-observability-operator` - Central operator
- `observability-thanos-*` - Metrics storage/query
- `observability-grafana` - Visualization
- `observability-alertmanager` - Alerting
- `endpoint-observability-operator` - Managed cluster agent

**Dependencies:**
- **Internal**:
  - Server Foundation (for cluster communication)
  - All managed clusters (for metrics collection)
- **External**:
  - Object stores (for metrics storage)
  - Remote write endpoints (Kafka, Victoria, etc.)

### 5. Specialized Components

#### HyperShift
**Components:**
- `hypershift-addon-operator` - Addon management
- `hypershift-operator` - Hosted control plane management

**Dependencies:**
- **Internal**:
  - Server Foundation (for cluster management)
- **External**:
  - Cloud providers (AWS, Azure, GCP)
  - S3 buckets (for etcd backups)

#### Submariner
**Components:**
- `submariner-operator` - Network connectivity
- `submariner-gateway` - Cross-cluster networking

**Dependencies:**
- **Internal**:
  - Server Foundation (for cluster discovery)
- **External**:
  - Cloud providers (for network configuration)

#### Disaster Recovery (DR4Hub)
**Components:**
- `cluster-backup-controller` - Backup management
- `volsync` - Data synchronization

**Dependencies:**
- **Internal**:
  - Server Foundation (for cluster access)
- **External**:
  - Object stores (for backup storage)
  - S3-compatible storage

## External Dependencies Summary

### Cloud Providers
- **AWS**: S3, EKS, IAM, VPC
- **Azure**: Blob Storage, AKS, Managed Identity
- **GCP**: Cloud Storage, GKE, IAM
- **OpenStack**: Swift, Keystone
- **VMware**: vSphere, vCenter

### External Services
- **GitHub/Git**: Repository access, policy storage
- **Ansible Tower**: Automation and remediation
- **Argo CD**: GitOps workflows
- **Red Hat Insights**: Cluster insights and recommendations
- **Helm Repositories**: Chart distribution
- **Object Stores**: Metrics, backups, application artifacts

### Security & Authentication
- **OCP Service CA**: Certificate management
- **OpenShift OAuth**: Authentication
- **mTLS**: Inter-cluster communication
- **RBAC**: Access control

## Data Flow Patterns

### Hub-to-Managed Cluster Communication
1. **Server Foundation** provides the base communication layer
2. **Cluster Proxy** enables secure tunnel connections
3. **ManifestWork** distributes resources to managed clusters
4. **Addon Framework** manages component deployment

### External Data Collection
1. **Search** collects resource data from all clusters
2. **Observability** collects metrics and logs
3. **GRC** collects policy compliance data
4. **App Lifecycle** manages application state

### User Interface Integration
1. **Console** provides unified UI access
2. **Search API** enables resource discovery
3. **Observability** provides metrics visualization
4. **GRC** provides policy management interface

## Security Considerations

### Certificate Management
- **Hub Cluster**: Self-signed CA for internal services
- **Managed Clusters**: Client certificates for hub communication
- **External Services**: TLS certificates for secure connections

### Data Encryption
- **In Transit**: TLS/mTLS for all communications
- **At Rest**: Storage-level encryption (OCP managed)
- **Secrets**: Kubernetes secret encryption

### Access Control
- **RBAC**: Kubernetes-native role-based access
- **Service Accounts**: Component-specific permissions
- **Network Policies**: Cluster-to-cluster communication control

## Dependency Matrix

| Component | Server Foundation | Search | Console | App Lifecycle | GRC | Observability | HyperShift | Submariner | DR4Hub |
|-----------|------------------|--------|---------|---------------|-----|---------------|------------|------------|--------|
| Server Foundation | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Search | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Console | ✓ | ✓ | - | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| App Lifecycle | ✓ | ✓ | ✓ | - | ✓ | - | - | - | - |
| GRC | ✓ | ✓ | ✓ | ✓ | - | - | - | - | - |
| Observability | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| HyperShift | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| Submariner | ✓ | ✓ | ✓ | - | - | - | - | - | - |
| DR4Hub | ✓ | ✓ | ✓ | - | - | - | - | - | - |

**Legend:**
- `-` = No direct dependency
- `✓` = Direct dependency exists

## Key Insights

1. **Server Foundation is the Core**: All components depend on Server Foundation for basic cluster management and communication.

2. **Search is Central**: Most components use Search for resource discovery and management.

3. **Console Provides Unified Access**: The console integrates with most components to provide a unified user experience.

4. **External Dependencies are Significant**: ACM heavily relies on external services for GitOps, automation, and storage.

5. **Security is Multi-Layered**: Certificate management, encryption, and access control are implemented at multiple levels.

6. **Data Flow is Bidirectional**: Components both collect data from and distribute data to managed clusters and external services.

This dependency graph shows that ACM is a complex, interconnected system where components work together to provide comprehensive multi-cluster management capabilities while maintaining security and scalability. 