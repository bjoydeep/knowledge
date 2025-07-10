graph TD
    subgraph Hub Cluster
        A[Search-v2-operator] --> B(Search-indexer)
        A --> C(Search-API)
        A --> D(PostgreSQL 16 Database)
        B -- Writes Data To --> D
        C -- Reads Data From --> D
        
        %% Storage Dependencies
        D -- Persists Data To --> D_PVC[PostgreSQL PVC]
        D_PVC -- Uses Storage Class --> STORAGE[Storage Class]
        
        %% Server Foundation Dependencies
        A -- Uses --> SF_PROXY[Server Foundation<br/>ocm-proxyserver]
        SF_PROXY -- Provides Secure Tunnel --> MANAGED_COMM[Managed Cluster Communication]
        
        %% Add-on Framework Dependencies
        A -- Deploys via Add-on Framework --> ADDON_FRAMEWORK[Add-on Framework]
        ADDON_FRAMEWORK -- Manages --> ADDON_CR[ManagedClusterAddOn CR]
        
        %% Certificate Dependencies
        A -- Uses Certificates --> CERT_CA[OCP Service CA]
        CERT_CA -- Provides --> SEARCH_CERTS[Search Certificates<br/>search-postgres Secret<br/>search-indexer ConfigMap<br/>search-ca-crt ConfigMap]
        
        %% RBAC Dependencies
        A -- Requires --> RBAC_ROLES[RBAC Roles & Permissions]
        RBAC_ROLES -- Includes --> SERVICE_ACCOUNTS[Service Accounts]
        RBAC_ROLES -- Includes --> CLUSTER_ROLES[Cluster Roles]
        
        %% Client Dependencies
        E[Clients for Querying and Interaction] -- Queries --> C
        E -- includes --> F(UI - ACM Console)
        E -- includes --> G(OCM Application)
        E -- includes --> H(CLI)
        E -- includes --> I(Automation Tools)
        E -- includes --> J(AI Processor)
        
        %% Authentication Dependencies
        C -- Uses --> AUTH_MECH[Authentication Mechanisms]
        AUTH_MECH -- Includes --> TOKEN_REVIEWS[Token Reviews]
        AUTH_MECH -- Includes --> ACCESS_REVIEWS[Subject Access Reviews]
        AUTH_MECH -- Includes --> IMPERSONATION[User Impersonation]
    end

    subgraph Managed Clusters
        K[Search-collector Add-on/Agent] --> L[Kubernetes API & Other Sources]
        K -- Sends Data To --> B
        
        %% Add-on Framework on Managed Cluster
        ADDON_FRAMEWORK -- Deploys --> K
        K -- Registers with --> ADDON_FRAMEWORK
        
        %% Managed Cluster RBAC
        K -- Uses --> MC_RBAC[Managed Cluster RBAC]
        MC_RBAC -- Based on --> USER_ACCESS[User Access Permissions]
        
        %% Data Collection Dependencies
        L -- Collects From --> K8S_RESOURCES[Kubernetes Resources]
        K8S_RESOURCES -- Includes --> SECRETS[Secrets Metadata]
        K8S_RESOURCES -- Includes --> ALL_RESOURCES[All K8s Resources]
    end

    %% External Dependencies
    subgraph External Systems
        EXTERNAL_CLIENTS[External Clients] -- Access via --> C
        EXTERNAL_CLIENTS -- Use --> API_AUTH[API Authentication]
    end

    %% Data Flow Dependencies
    A -- Deploys & Manages --> K
    L -- Collects Data From --> K
    
    %% Security Dependencies
    SF_PROXY -- Provides TLS --> SECURE_COMM[Secure Communication]
    SECURE_COMM -- Encrypts --> DATA_FLOW[Data Flow]
    
    %% Logging Dependencies
    A -- Logs To --> LOGS[Pod Logs]
    C -- Logs To --> LOGS
    D -- Logs To --> LOGS
    LOGS -- Can Forward To --> SPLUNK[Splunk Universal Forwarder]

    %% Styling
    classDef hub fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef managed fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef external fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef storage fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef security fill:#fce4ec,stroke:#880e4f,stroke-width:2px

    class A,B,C,D,E,F,G,H,I,J hub
    class K,L managed
    class EXTERNAL_CLIENTS,EXTERNAL_CLIENTS external
    class D_PVC,STORAGE storage
    class SF_PROXY,CERT_CA,SEARCH_CERTS,RBAC_ROLES,AUTH_MECH security

**Explanation of Search V2 Dependencies:**

The Search V2 component in ACM has comprehensive dependencies across multiple layers:

**I. Core Search Components (Hub Cluster)**
- **Search-v2-operator**: Central operator that deploys and manages all search components
- **Search-indexer**: Receives data from collectors and writes to PostgreSQL database
- **Search-API**: Provides GraphQL API for querying data from PostgreSQL
- **PostgreSQL 16 Database**: Stores all collected resource data with optional PVC persistence

**II. Server Foundation Dependencies**
- **ocm-proxyserver**: Provides secure tunnel communication between managed clusters and hub
- **Add-on Framework**: Manages deployment of search-collector on managed clusters via ManagedClusterAddOn CRs

**III. Security & Authentication Dependencies**
- **OCP Service CA**: Manages certificates for all search components
- **RBAC System**: Provides role-based access control for search operations
- **Authentication Mechanisms**: Token reviews, subject access reviews, and user impersonation

**IV. Storage Dependencies**
- **PostgreSQL PVC**: Optional persistent storage for database data
- **Storage Class**: Cluster-defined storage class for PVC provisioning

**V. Managed Cluster Dependencies**
- **Search-collector Add-on**: Deployed on each managed cluster to collect Kubernetes resource data
- **Kubernetes API**: Source of all resource data collected by search-collector
- **Managed Cluster RBAC**: Controls what data users can access based on their permissions

**VI. External Client Dependencies**
- **ACM Console**: Primary UI for search functionality
- **OCM Application**: Application lifecycle integration
- **CLI Tools**: Command-line access to search data
- **Automation Tools**: API-based automation and integration
- **AI Processor**: AI/ML integration for search data analysis

**VII. Data Flow Dependencies**
- **Secure Communication**: TLS-encrypted data flow between components
- **Logging**: Comprehensive logging for security and operational monitoring
- **Splunk Integration**: Optional forwarding of logs to external monitoring systems

This dependency mapping shows that Search V2 is deeply integrated with ACM's core infrastructure, requiring coordination with Server Foundation, add-on framework, security systems, and external clients to provide comprehensive multi-cluster resource search capabilities.