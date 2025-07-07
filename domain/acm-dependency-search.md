```mermaid
graph TD
    subgraph Hub Cluster
        A[Search-v2-operator] --> B(Search-indexer)
        A --> C(Search-API)
        A --> D(PostgreSQL 16 Database)
        B -- Writes Data To --> D
        C -- Reads Data From --> D
        E[Clients for Querying and Interaction] -- Queries --> C
        E -- includes --> F(UI - ACM Console)
        E -- includes --> G(OCM Application)
        E -- includes --> H(CLI)
        E -- includes --> I(Automation Tools)
        E -- includes --> J(AI Processor)
    end

    subgraph Managed Clusters
        K[Search-collector Add-on/Agent] --> L[Kubernetes API & Other Sources]
        K -- Sends Data To --> B
    end

    A -- Deploys & Manages --> K
    L -- Collects Data From --> K