```mermaid

graph TD
    subgraph Hub Cluster
        User --- A[MultiCluster Observability Operator - MCO ]
        User -- Defines Policies/CRs --> B[MultiCluster Observability Add-on - MCOA]
        User -- Defines Placement --> C[ClusterManagementAddOn CR]

        A -- Deploys/Manages --> D[Thanos Query, API Gateway, Object Storage]
        A -- Deploys/Manages --> E[Grafana]
        A -- Deploys/Manages --> F[AlertManager]

        B -- Distributes CRs --> Spoke1_Logging_Operator[OpenShift Logging Operator]
        B -- Distributes CRs --> Spoke1_OpenTelemetry_Collector[OpenTelemetry Collector]
        B -- Distributes CRs --> SpokeN_Logging_Operator[...]
        B -- Distributes CRs --> SpokeN_OpenTelemetry_Collector[...]

        D -- Metrics Data --> E
        D -- Alerts --> F
        F -- Forwards Alerts --> G[External Systems - Alerts]

        H[Search-indexer] --> I[PostgreSQL 16 - Database]
        J[Search-API] --> I
        K[UI/CLI/Automation/AI Processor] --> J
    end

    subgraph Managed Cluster Spoke 1..N
        L[Prometheus] --- M[Exporters]
        L --- N[Cluster Monitoring Operator OCP]
        O[Endpoint Operator] --> P[Metrics Collector]
        L --> P
        P -- Sharded Forwarding --> D
        Spoke1_Logging_Operator --> G_Logs[External Systems Logs]
        Spoke1_OpenTelemetry_Collector --> G_Traces[External Systems Traces]
        Q[Search-collector] -- Collects K8s Data --> H
    end

    

    B -- Orchestrates via C --> Spoke1_Logging_Operator
    B -- Orchestrates via C --> Spoke1_OpenTelemetry_Collector
    B -- Orchestrates via C --> SpokeN_Logging_Operator
    B -- Orchestrates via C --> SpokeN_OpenTelemetry_Collector

    style A fill:#fff,stroke:#333,stroke-width:2px
    style B fill:#fff,stroke:#333,stroke-width:2px
    style C fill:#fff,stroke:#333,stroke-width:2px
    style D fill:#fff,stroke:#333,stroke-width:2px
    style E fill:#fff,stroke:#333,stroke-width:2px
    style F fill:#fff,stroke:#333,stroke-width:2px
    style L fill:#fff,stroke:#333,stroke-width:2px
    style M fill:#fff,stroke:#333,stroke-width:2px
    style N fill:#fff,stroke:#333,stroke-width:2px
    style O fill:#fff,stroke:#333,stroke-width:2px
    style P fill:#fff,stroke:#333,stroke-width:2px
    style Spoke1_Logging_Operator fill:#fff,stroke:#333,stroke-width:2px
    style Spoke1_OpenTelemetry_Collector fill:#fff,stroke:#333,stroke-width:2px
    style Q fill:#fff,stroke:#333,stroke-width:2px

    linkStyle 0 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 1 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 2 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 3 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 4 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 5 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 6 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 7 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 8 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 9 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 10 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 11 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 12 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 13 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 14 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 15 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 16 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 17 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 18 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 19 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 20 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 21 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 22 stroke:#000,stroke-width:1px,fill:none;
    linkStyle 23 stroke:#000,stroke-width:1px,fill:none;