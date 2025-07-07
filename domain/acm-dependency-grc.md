```mermaid
graph TD
    subgraph Hub Cluster
        User --> A[Define Policy CRs & PolicyAutomations]
        A --> B(Policy Propagator Controller)
        B -- Watches --> C[Placement & PlacementBinding CRs]
        B -- Propagates Policies --> D(Replicated Policy CRs)
        B -- Handles --> E(PolicyAutomations)
        B -- Resolves --> F(Hub Templates)
        G[grc-*-policy-addon-controller-*] -- Creates & Configures --> H[Policy Components on Managed Clusters]
    end

    subgraph Managed Cluster
        D --> I(Governance Policy Framework)
        I -- Copies Policies from Hub --> J[ManagedCluster Namespace]
        I -- Records & Sends Updates --> K[Status Sync Controller]
        K -- Compliance Status --> HubCluster[Hub Cluster]
        I -- Creates Templates --> L[Template Sync Controller]
        L -- Generates --> M[Policy Template CRs]
        M -- Leads to (e.g., Gatekeeper integration) --> N[Gatekeeper Resources]
        I -- If Gatekeeper installed --> O[Gatekeeper Constraint Sync]
        O -- Creates --> N
        P[Other Policy Controllers] -- Enforce Policies --> Q[Configuration & Certificate Policies]
        Q -- Generates --> R[Events for Policy]
    end

    HubCluster -.-> K
    B -.-> D
    G -.-> I
    I --> P
    N --> Q