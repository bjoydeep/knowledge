```mermaid
sequenceDiagram
    participant User/Automation as User
    participant SearchV2Operator as Search-v2-operator
    participant SearchIndexer as Search-indexer
    participant PostgreSQL as PostgreSQL 16
    participant SearchAPI as Search-API
    participant SearchCollector as Search-collector
    participant KubernetesAPI as K8s API

    User->>SearchV2Operator: Deploy/Configure Search Service
    SearchV2Operator->>SearchIndexer: Orchestrates Deployment
    SearchV2Operator->>PostgreSQL: Orchestrates Deployment
    SearchV2Operator->>SearchAPI: Orchestrates Deployment
    SearchV2Operator->>SearchCollector: Manages Add-on Deployment (on each Managed Cluster)

    loop Each Managed Cluster
        SearchCollector->>K8sAPI: Collects Kubernetes Resource Data
        SearchCollector->>SearchIndexer: Forwards Collected Data
    end

    SearchIndexer->>PostgreSQL: Processes and Stores Incoming Data

    User->>SearchAPI: Queries Resource Information (via UI, OCM App, CLI, Automation, AI)
    SearchAPI->>PostgreSQL: Retrieves Requested Data
    PostgreSQL-->>SearchAPI: Returns Data
    SearchAPI-->>User: Returns Query Results