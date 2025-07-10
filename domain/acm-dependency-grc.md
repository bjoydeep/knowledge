graph TD
    subgraph Hub Cluster
        User --> A[Define Policy CRs & PolicyAutomations]
        A --> B(Policy Propagator Controller)
        B -- Watches --> C[Placement & PlacementBinding CRs]
        B -- Propagates Policies --> D(Replicated Policy CRs)
        B -- Handles --> E(PolicyAutomations)
        B -- Resolves --> F(Hub Templates)
        
        %% Missing Hub Components
        G[governance-policy-addon-controller] -- Creates & Configures --> H[Policy Components on Managed Clusters]
        G -- Uses Add-on Framework --> ADDON_FRAMEWORK[Add-on Framework]
        
        %% Policy Generator Integration
        POLICY_GENERATOR[Policy Generator Plugin] -- Integrates with --> APP_LIFECYCLE[Application Lifecycle<br/>Subscription Controller]
        POLICY_GENERATOR -- Generates Policies from --> GIT_SOURCES[Git Sources<br/>Helm Charts<br/>Kustomize]
        
        %% Policy Compliance History (ACM 2.10, removed 2.13)
        COMPLIANCE_HISTORY[Policy Compliance History] -- Stores Data in --> POSTGRES_DB[PostgreSQL Database]
        COMPLIANCE_HISTORY -- Exposes API via --> HTTP_API[HTTP API Route]
        
        %% Fine Grained RBAC
        FINE_RBAC[Fine Grained RBAC Library] -- Integrates with --> OBSERVABILITY[Observability]
        
        %% Hub Templates Processing
        HUB_TEMPLATES[Hub Templates Processing] -- Encrypts Sensitive Data --> TEMPLATE_ENCRYPTION[Template Encryption]
        HUB_TEMPLATES -- Provides Metadata --> TEMPLATE_METADATA[ManagedCluster Metadata<br/>Policy Metadata]
        
        %% Metrics Integration
        B -- Provides Metrics to --> OPENSHIFT_METRICS[OpenShift Metrics]
        OPENSHIFT_METRICS -- Forwards to --> ALERT_MANAGER[Alert Manager]
        ALERT_MANAGER -- Sends Alerts to --> EXTERNAL_ALERTING[External Alerting Systems]
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
        
        %% Missing Managed Cluster Components
        CERT_POLICY[cert-policy-controller] -- Enforces --> CERT_POLICIES[Certificate Policies]
        CONFIG_POLICY[config-policy-controller] -- Enforces --> CONFIG_POLICIES[Configuration Policies]
        OPERATOR_POLICY[OperatorPolicy Controller] -- Enforces --> OPERATOR_POLICIES[Operator Policies]
        IAM_POLICY[iam-policy-controller] -- Enforces --> IAM_POLICIES[IAM Policies<br/>(Deprecated ACM 2.10)]
        
        %% Gatekeeper Components
        GATEKEEPER_OP[gatekeeper-operator-controller-manager] -- Manages --> GATEKEEPER_CM[gatekeeper-controller-manager]
        GATEKEEPER_CM -- Provides --> GATEKEEPER_WEBHOOK[gatekeeper-webhook-service]
        GATEKEEPER_AUDIT[gatekeeper-audit] -- Audits --> K8S_RESOURCES[Kubernetes Resources]
        
        %% Policy Framework Add-on
        POLICY_FRAMEWORK_ADDON[governance-policy-framework-addon] -- Syncs Policies --> I
        POLICY_FRAMEWORK_ADDON -- Syncs Gatekeeper Objects --> GATEKEEPER_SYNC[Gatekeeper Sync Controller]
        GATEKEEPER_SYNC -- Syncs --> GATEKEEPER_CONSTRAINTS[Gatekeeper Constraints<br/>ConstraintTemplates]
        
        %% Standalone Hub Templating
        STANDALONE_TEMPLATING[governance-standalone-hub-templating] -- Allows Direct Access --> HUB_ACCESS[Hub Cluster Access]
        HUB_ACCESS -- Caches Data in --> CACHE_SECRETS[Secrets Cache]
        
        %% Diff Logging
        DIFF_LOGGING[Policy Diff Logging] -- Logs NonCompliant Details --> POLICY_LOGS[Policy Logs]
        
        %% Managed Cluster Metrics
        MANAGED_METRICS[Managed Cluster Metrics] -- Reports Policy Status --> OPENSHIFT_METRICS
    end

    %% External Dependencies
    subgraph External Systems
        GIT_REPO[GitHub Repository] -- Stores Policies --> POLICY_GENERATOR
        ANSIBLE_TOWER[Ansible Tower] -- Receives Jobs from --> E
        COMMUNITY_POLICIES[Community Policy Repositories<br/>Sysdig Secure<br/>GitHub Auth] -- Provides Policies --> A
        KUSTOMIZE[Kustomize] -- Processes Templates --> POLICY_GENERATOR
        EXTERNAL_ALERTING[External Alerting Systems] -- Receives Alerts from --> ALERT_MANAGER
    end

    %% Cross-Pillar Dependencies
    subgraph Other ACM Pillars
        APP_LIFECYCLE[Application Lifecycle<br/>Subscription Controller] -- Integrates with --> POLICY_GENERATOR
        OBSERVABILITY[Observability] -- Integrates with --> FINE_RBAC
        SERVER_FOUNDATION[Server Foundation] -- Provides Communication --> HUB_MANAGED_COMM[Hub-Managed Cluster Communication]
    end

    %% Data Flow Dependencies
    HubCluster -.-> K
    B -.-> D
    G -.-> I
    I --> P[Other Policy Controllers]
    N --> Q[Configuration & Certificate Policies]
    Q -- Generates --> R[Events for Policy]
    
    %% Add-on Framework Dependencies
    ADDON_FRAMEWORK -- Deploys --> POLICY_FRAMEWORK_ADDON
    ADDON_FRAMEWORK -- Manages --> MANAGEDCLUSTER_ADDON[ManagedClusterAddOn CRs]
    
    %% Template Processing Dependencies
    F -- Uses Encryption Key --> TEMPLATE_ENCRYPTION
    TEMPLATE_ENCRYPTION -- Copied to Managed Cluster --> SPEC_SYNC[Spec-Sync Controller]
    
    %% Security Dependencies
    GATEKEEPER_WEBHOOK -- Uses TLS Certificate --> GATEKEEPER_CERTS[Gatekeeper Certificates]
    GATEKEEPER_CERTS -- Generated by --> GATEKEEPER_CERT_CONTROLLER[Gatekeeper Certificate Controller]
    
    %% Styling
    classDef hub fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef managed fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef external fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef other fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef deprecated fill:#ffebee,stroke:#c62828,stroke-width:2px

    class A,B,C,D,E,F,G,POLICY_GENERATOR,COMPLIANCE_HISTORY,FINE_RBAC,HUB_TEMPLATES hub
    class I,J,K,L,M,N,O,CERT_POLICY,CONFIG_POLICY,OPERATOR_POLICY,GATEKEEPER_OP,GATEKEEPER_CM,GATEKEEPER_AUDIT,POLICY_FRAMEWORK_ADDON managed
    class GIT_REPO,ANSIBLE_TOWER,COMMUNITY_POLICIES,KUSTOMIZE,EXTERNAL_ALERTING external
    class APP_LIFECYCLE,OBSERVABILITY,SERVER_FOUNDATION other
    class IAM_POLICY deprecated

**Explanation of GRC Dependencies:**

The Governance, Risk & Compliance (GRC) component in ACM has comprehensive dependencies across multiple layers:

**I. Hub Cluster Components**
- **Policy Propagator Controller**: Central component that syncs policies between user namespaces and managed cluster namespaces
- **governance-policy-addon-controller**: Controller leveraging the add-on framework to deploy GRC controllers to managed clusters
- **Policy Generator**: Community plugin that integrates with Application Lifecycle subscription controller to generate policies from various sources
- **Policy Compliance History**: Stores detailed compliance data in PostgreSQL database (ACM 2.10, removed 2.13)
- **Fine Grained RBAC**: Library for fine-grained access control, integrated with Observability
- **Hub Templates Processing**: Handles template processing with encryption for sensitive data

**II. Managed Cluster Components**
- **Governance Policy Framework**: Core framework that copies policies from hub and manages policy enforcement
- **Policy Controllers**: 
  - **cert-policy-controller**: Enforces certificate policies
  - **config-policy-controller**: Enforces configuration policies and operator policies
  - **iam-policy-controller**: Enforces IAM policies (deprecated ACM 2.10)
- **Gatekeeper Components**:
  - **gatekeeper-operator-controller-manager**: Manages Gatekeeper deployment
  - **gatekeeper-controller-manager**: Core Gatekeeper controller
  - **gatekeeper-audit**: Audits Kubernetes resources
  - **gatekeeper-webhook-service**: Admission webhook service
- **Policy Framework Add-on**: Syncs policies and Gatekeeper objects between hub and managed clusters
- **Standalone Hub Templating**: Allows direct hub access for template resolution (ACM 2.13)

**III. External Dependencies**
- **GitHub Repository**: Stores policies and policy templates
- **Ansible Tower**: Receives automation jobs for policy remediation
- **Community Policy Repositories**: External policy sources (Sysdig Secure, GitHub Auth)
- **Kustomize**: Template processing for policy generation
- **External Alerting Systems**: Receives policy compliance alerts

**IV. Cross-Pillar Dependencies**
- **Application Lifecycle**: Integration through subscription controller for policy distribution
- **Observability**: Integration for fine-grained RBAC and metrics
- **Server Foundation**: Provides secure communication between hub and managed clusters

**V. Data Flow Dependencies**
- **Add-on Framework**: Manages deployment and lifecycle of GRC components on managed clusters
- **Template Processing**: Hub templates with encryption, managed cluster templates
- **Metrics Integration**: Policy status metrics provided to OpenShift and external systems
- **Security Dependencies**: TLS certificates for Gatekeeper webhook, template encryption keys

**VI. Advanced Features**
- **Policy Diff Logging**: Logs non-compliant policy details (user opt-in)
- **Template Encryption**: Protects sensitive data in policy templates
- **Standalone Hub Access**: Direct hub access for template resolution on managed clusters
- **Community Policy Integration**: Support for external policy repositories

This dependency mapping shows that GRC is deeply integrated with ACM's core infrastructure, requiring coordination with Application Lifecycle, Observability, Server Foundation, and external systems to provide comprehensive policy governance across the cluster fleet.