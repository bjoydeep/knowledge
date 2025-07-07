# acm dependency graph

```mermaid

graph TB
    %% External Services
    subgraph External["External Services & Cloud Providers"]
        GitHub[GitHub/Git Repositories]
        Ansible[Ansible Tower]
        ArgoCD[Argo CD]
        Insights[Red Hat Insights]
        Helm[Helm Repositories]
        ObjectStore[Object Stores<br/>S3, MinIO, etc.]
        CloudProviders[Cloud Providers<br/>AWS, Azure, GCP, etc.]
    end

    %% Foundation Layer
    subgraph Foundation["Foundation Layer (Server Foundation)"]
        ClusterManager[cluster-manager<br/>Central Hub Management]
        Klusterlet[klusterlet<br/>Managed Cluster Agent]
        ProxyServer[ocm-proxyserver<br/>API Aggregation]
        ClusterProxy[cluster-proxy-addon<br/>Cluster Communication]
    end

    %% Management Layer
    subgraph Management["Management Layer"]
        subgraph Console["Console & UI"]
            ConsoleUI[console<br/>RHACM UI Plugin]
            ConsoleMCE[console-mce<br/>MCE UI Plugin]
            CLIDownload[acm-cli<br/>CLI Download]
        end
        
        subgraph Search["Search"]
            SearchCollector[search-collector<br/>Data Collection]
            SearchAggregator[search-aggregator<br/>Data Aggregation]
            SearchAPI[search-api<br/>Search API]
            SearchDB[search-redisgraph<br/>Graph Database]
        end
    end

    %% Application & Policy Layer
    subgraph AppPolicy["Application & Policy Layer"]
        subgraph AppLifecycle["Application Lifecycle"]
            AppOperator[multicloud-operators-application<br/>Application Management]
            ChannelOperator[multicloud-operators-channel<br/>Repository Management]
            SubscriptionOperator[multicloud-operators-subscription<br/>Deployment Management]
            Integrations[multicloud-integrations<br/>External Integrations]
        end
        
        subgraph GRC["Governance, Risk & Compliance"]
            PolicyPropagator[governance-policy-propagator<br/>Policy Distribution]
            PolicyAddon[governance-policy-addon-controller<br/>Addon Management]
            CertPolicy[cert-policy-controller<br/>Certificate Policies]
            ConfigPolicy[config-policy-controller<br/>Configuration Policies]
            Gatekeeper[gatekeeper-operator<br/>OPA Gatekeeper]
        end
    end

    %% Observability Layer
    subgraph Observability["Observability Layer"]
        ObsOperator[multicluster-observability-operator<br/>Central Operator]
        Thanos[observability-thanos-*<br/>Metrics Storage/Query]
        Grafana[observability-grafana<br/>Visualization]
        AlertManager[observability-alertmanager<br/>Alerting]
        EndpointObs[endpoint-observability-operator<br/>Managed Cluster Agent]
    end

    %% Specialized Components
    subgraph Specialized["Specialized Components"]
        HyperShift[hypershift-addon-operator<br/>Hosted Control Planes]
        Submariner[submariner-operator<br/>Cross-Cluster Networking]
        DR4Hub[cluster-backup-controller<br/>Disaster Recovery]
    end

    %% Managed Clusters
    subgraph ManagedClusters["Managed Clusters"]
        MC1[Managed Cluster 1]
        MC2[Managed Cluster 2]
        MC3[Managed Cluster N]
    end

    %% External Dependencies
    GitHub --> AppLifecycle
    GitHub --> GRC
    Ansible --> Console
    Ansible --> AppLifecycle
    Ansible --> GRC
    ArgoCD --> AppLifecycle
    Insights --> Console
    Helm --> AppLifecycle
    ObjectStore --> AppLifecycle
    ObjectStore --> Observability
    ObjectStore --> DR4Hub
    CloudProviders --> HyperShift
    CloudProviders --> Submariner

    %% Foundation Dependencies (All components depend on Server Foundation)
    Foundation --> Management
    Foundation --> AppPolicy
    Foundation --> Observability
    Foundation --> Specialized

    %% Search Dependencies (Most components use Search)
    Search --> Console
    Search --> AppLifecycle
    Search --> GRC
    Search --> Observability
    Search --> Specialized

    %% Console Dependencies (Console integrates with most components)
    Console --> AppLifecycle
    Console --> GRC
    Console --> Observability
    Console --> Specialized

    %% App Lifecycle Dependencies
    AppLifecycle --> GRC

    %% Managed Cluster Connections
    Foundation -. ManifestWork .-> ManagedClusters
    Search -. Data Collection .-> ManagedClusters
    Observability -. Data Collection .-> ManagedClusters
    GRC -. Policy Distribution .-> ManagedClusters
    AppLifecycle -. Application Deployment .-> ManagedClusters


    %% Internal Component Relationships
    SearchCollector --> SearchAggregator
    SearchAggregator --> SearchAPI
    SearchAPI --> SearchDB
    
    AppOperator --> ChannelOperator
    AppOperator --> SubscriptionOperator
    SubscriptionOperator --> Integrations
    
    PolicyPropagator --> PolicyAddon
    PolicyAddon --> CertPolicy
    PolicyAddon --> ConfigPolicy
    ConfigPolicy --> Gatekeeper
    
    ObsOperator --> Thanos
    Thanos --> Grafana
    Thanos --> AlertManager
    EndpointObs --> ObsOperator

    %% Styling
    style Foundation fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style Management fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    style AppPolicy fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    style Observability fill:#fff3e0,stroke:#e65100,stroke-width:2px
    style Specialized fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    style External fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    style ManagedClusters fill:#fafafa,stroke:#424242,stroke-width:1px

    

      