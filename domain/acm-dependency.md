# ACM Comprehensive Dependency Graph

This document provides a unified view of all Red Hat Advanced Cluster Management (ACM) component dependencies across all pillars, showing the complete architecture and inter-component relationships.

## Overview

ACM consists of five main pillars that work together to provide comprehensive cluster management:
- **Server Foundation**: Core infrastructure and communication
- **Cluster Lifecycle**: Cluster provisioning, import, and management
- **Application Lifecycle**: Application deployment and GitOps
- **Governance, Risk & Compliance (GRC)**: Policy management and enforcement
- **Observability**: Metrics, logging, and monitoring
- **Search**: Resource discovery and indexing

## Unified Dependency Diagram

```mermaid
graph TD
    %% External Systems
    subgraph External["External Systems & Cloud Providers"]
        GitHub[GitHub/Git Repositories]
        Ansible[Ansible Tower]
        ArgoCD[Argo CD]
        Insights[Red Hat Insights]
        Helm[Helm Repositories]
        ObjectStore[Object Stores<br/>S3, MinIO, etc.]
        CloudProviders[Cloud Providers<br/>AWS, Azure, GCP, etc.]
        BareMetal[Bare Metal Servers]
        ThirdPartyObs[Third-Party Observability]
        ExternalAlerts[External Alerting Systems]
        ExternalLogs[External Log Sources]
        ExternalTraces[External Trace Sources]
    end

    %% Server Foundation Layer
    subgraph Foundation["Server Foundation Layer"]
        ClusterManager[cluster-manager<br/>Central Hub Management]
        Klusterlet[klusterlet<br/>Managed Cluster Agent]
        ProxyServer[ocm-proxyserver<br/>API Aggregation]
        ClusterProxy[cluster-proxy-addon<br/>Cluster Communication]
        RegistrationController[Registration Controller]
        AddOnManager[AddOn Manager]
        ManifestWorkCRs[ManifestWork CRs]
    end

    %% Hub Cluster Management Plane
    subgraph Hub["Hub Cluster Management Plane"]
        User[User / Admin] --> Console[ACM Console]
        
        %% Cluster Lifecycle Components
        subgraph CLC["Cluster Lifecycle"]
            ClusterDeployment[ClusterDeployment CR]
            ManagedCluster[ManagedCluster CR]
            ClusterAddOnConfig[Cluster Add-on Config CR]
            ManagedClusterImportController[Managed Cluster Import Controller]
            KlusterletOperator[Klusterlet Operator]
            KlusterletCR[Klusterlet CR]
            ManagedClusterAddOn[ManagedClusterAddOn CR]
            AddOnControllers[AddOn Specific Controllers]
            ClusterSet[ClusterSet]
            Placement[Placement]
            
            %% Cluster Provisioning Engines
            HiveOperator[Hive Operator]
            HiveClusterDeployment[ClusterDeployment CR Hive]
            CAPIControllers[CAPI Core & Provider Controllers]
            HypershiftAddonManager[Hypershift Add-on Manager]
            HostedCluster[HostedCluster CR]
            NodePool[NodePool CR]
            SiteConfigOperator[SiteConfig Operator]
            InstallationManifests[Installation Manifests]
            ImageBasedInstallOperator[Image Based Install Operator IBIO]
            ConfigISO[Configuration ISO]
            ClusterBaremetalOperator[Cluster Baremetal Operator BMO]
            InfrastructureOperator[Infrastructure Operator CIM]
            AssistedService[Assisted Service]
        end

        %% Application Lifecycle Components
        subgraph ALC["Application Lifecycle"]
            ApplicationSet[ApplicationSet]
            GitOpsCluster[GitOpsCluster]
            ADT[AddOnTemplate]
            ADD[AddOnDeploymentConfig]
            CMA[ClusterManagementAddOn]
            MSA[ManagedServiceAccount]
            GCHC[gitopscluster-controller]
            
            %% Backend Components
            APP_OP[multicloud-operators-application]
            CHANNEL_OP[multicloud-operators-channel]
            SUB_OP[multicloud-operators-subscription]
            PLACEMENT_OP[multicloud-operators-placementrule]
            INTEGRATIONS_OP[multicloud-integrations]
            SUB_REPORT_OP[multicloud-operators-subscription-report]
            CLUSTER_PERM_OP[cluster-permission]
            
            %% Custom Resources
            ACM_APP[ACM Application CR]
            ACM_CHANNEL[ACM Channel CR]
            ACM_SUB[ACM Subscription CR]
            ACM_SUB_STATUS[ACM Subscription Status CR]
            ACM_PLACEMENT[ACM Placement Rule CR]
            ACM_SUB_REPORT[ACM Subscription Report CR]
            ACM_CLUSTER_PERM[ACM ClusterPermission CR]
            ACM_GITOPS_CLUSTER[ACM GitOpsCluster CR]
            ACM_HELMRELEASE[ACM HelmRelease CR]
            
            %% External Dependencies
            ANSIBLE_INTEGRATION[Ansible Integration]
            ANSIBLE_TOKEN[Access Token]
            ANSIBLE_JOB[AnsibleJob CR]
        end

        %% GRC Components
        subgraph GRC["Governance, Risk & Compliance"]
            PolicyPropagator[Policy Propagator Controller]
            PolicyCRs[Policy CRs]
            PolicyAutomations[PolicyAutomations]
            PlacementBinding[PlacementBinding]
            GovernancePolicyFramework[Governance Policy Framework]
            Gatekeeper[Gatekeeper]
            
            %% Hub Components
            GRC_ADDON_CONTROLLER[governance-policy-addon-controller]
            POLICY_GENERATOR[Policy Generator Plugin]
            POLICY_COMPLIANCE[Policy Compliance History]
            FINE_GRAINED_RBAC[Fine Grained RBAC Library]
            HUB_TEMPLATES[Hub Templates Processing]
            METRICS_INTEGRATION[Metrics Integration]
            
            %% Custom Resources
            ACM_POLICY[ACM Policy CR]
            ACM_POLICY_AUTO[ACM PolicyAutomation CR]
            ACM_POLICY_COMPLIANCE[ACM Policy Compliance CR]
            ACM_POLICY_REPORT[ACM Policy Report CR]
            ACM_POLICY_SET[ACM Policy Set CR]
            ACM_POLICY_TEMPLATE[ACM Policy Template CR]
            
            %% External Dependencies
            ANSIBLE_TOWER_GRC[Ansible Tower]
            GIT_REPO_GRC[Git Repository]
            HELM_REPO_GRC[Helm Repository]
            OBJECT_STORE_GRC[Object Store]
        end

        %% Search Components
        subgraph Search["Search"]
            SearchV2Operator[Search-v2-operator]
            SearchIndexer[Search-indexer]
            SearchAPI[Search-API]
            PostgreSQL[PostgreSQL 16 Database]
            SearchCollector[Search-collector Add-on/Agent]
            
            %% Storage Dependencies
            D_PVC[PostgreSQL PVC]
            STORAGE[Storage Class]
            
            %% Security Dependencies
            SF_PROXY[Server Foundation<br/>ocm-proxyserver]
            MANAGED_COMM[Managed Cluster Communication]
            ADDON_FRAMEWORK[Add-on Framework]
            OCP_SERVICE_CA[OCP Service CA]
            RBAC_ROLES[RBAC Roles & Permissions]
            AUTH_MECHANISMS[Authentication Mechanisms]
            
            %% Client Integration
            UI_CLIENTS[UI/CLI/Automation Tools]
            AI_PROCESSOR[AI Processor]
        end

        %% Observability Components
        subgraph OBS["Observability"]
            MCOperator[MultiCluster Observability Operator - MCO]
            MCOAddon[MultiCluster Observability Add-on - MCOA]
            Thanos[Thanos Query, API Gateway, Object Storage]
            Grafana[Grafana]
            AlertManager[AlertManager]
            ClusterManagementAddOn[ClusterManagementAddOn CR]
        end

        %% Other Components
        subgraph Other["Other Components"]
            DR4Hub[DR4Hub Operator]
            Velero[Velero]
            StorageSecret[Storage Secret]
            OADPOperator[OADP Operator]
            VolSyncAddonController[VolSync Addon Controller]
            GlobalHubOperator[Multicluster Global Hub Operator]
            MGHManager[Multicluster Global Hub Manager]
        end
    end

    %% Managed Cluster Workload Plane
    subgraph Managed["Managed Cluster Workload Plane"]
        %% Cluster Lifecycle on Managed
        KlusterletAgent[Klusterlet Agent]
        AddOnAgents[Generic AddOn Agents]
        
        %% Application Lifecycle on Managed
        GAC[gitops-addon Controller]
        OGO[OpenShift GitOps Operator]
        ARGOCD1[ArgoCD Instance]
        TC1[Target Cluster Resources<br/>Deployments, Pods, Secrets]
        STC[spoke-token-controller]
        
        %% Missing Managed Cluster Components
        SUB_OP_MC[multicloud-operators-subscription<br/>on Managed Cluster]
        ACM_SUB_STATUS_MC[ACM Subscription Status CR<br/>on Managed Cluster]
        HELM_RELEASE_OP[multicloud-operators-subscription-release<br/>helmrelease]
        PARENT_SUB_MC[Parent Subscription]
        RBAC_RESOURCES_MC[RBAC Resources on Managed Cluster]
        ROLES[Roles]
        ROLEBINDINGS[RoleBindings]
        CLUSTERROLES[ClusterRoles]
        CLUSTERROLEBINDINGS[ClusterRoleBindings]
        
        %% GRC on Managed
        CERT_POLICY_CONTROLLER[cert-policy-controller]
        CONFIG_POLICY_CONTROLLER[config-policy-controller]
        OPERATOR_POLICY_CONTROLLER[operator-policy-controller]
        IAM_POLICY_CONTROLLER[iam-policy-controller]
        SECURITY_POLICY_CONTROLLER[security-policy-controller]
        CERT_POLICY_CR[cert-policy-controller CR]
        CONFIG_POLICY_CR[config-policy-controller CR]
        OPERATOR_POLICY_CR[operator-policy-controller CR]
        IAM_POLICY_CR[iam-policy-controller CR]
        SECURITY_POLICY_CR[security-policy-controller CR]
        
        %% Search on Managed
        SEARCH_COLLECTOR_MC[Search-collector on Managed Cluster]
        KUBERNETES_API[Kubernetes API]
        SEARCH_API_MC[Search API on Managed Cluster]
        
        %% Observability on Managed
        Prometheus[Prometheus]
        MetricsCollector[Metrics Collector]
        ClusterLoggingOperator[OpenShift Logging Operator]
        OpenTelemetryOperator[OpenTelemetry Operator]
        VolSyncOperatorManaged[VolSync Operator]
        PersistentVolumes[Persistent Volumes]
        SubmarinerOperatorManaged[Submariner Operator]
        SubmarinerGateway[Submariner Gateway]
        OtherManagedClusters[Other Managed Clusters]
        
        %% Monitoring Components
        Exporters[Exporters]
        ClusterMonitoringOperator[Cluster Monitoring Operator OCP]
        EndpointOperator[Endpoint Operator]
    end

    %% Cross-Pillar Dependencies
    subgraph CrossPillar["Cross-Pillar Dependencies"]
        SEARCH[Search API]
        SERVER_FOUNDATION[Server Foundation]
        CONSOLE[Console/UI]
    end

    %% Data Flow Dependencies
    subgraph DataFlow["Data Flow Dependencies"]
        MANIFESTWORK[ManifestWork]
        CHANNEL_CERTS[Channel Certificates]
        SUB_CERTS[Subscription Certificates]
        ARGOCD_CERTS[ArgoCD Certificates]
        CHANNEL_WEBHOOK[Channel Validating Webhook]
        APP_WEBHOOK[Application Validating Webhook]
    end

    %% Connections - Foundation Layer
    Foundation -.->|ManifestWork| Managed
    
    %% Connections - Cluster Lifecycle
    Console --> ClusterDeployment
    Console --> ManagedCluster
    Console --> ClusterAddOnConfig
    ManagedCluster -- Reflects status from --> KlusterletAgent
    ManagedClusterImportController -- Deploys --> KlusterletOperator
    ManagedClusterImportController -- Creates --> KlusterletCR
    KlusterletAgent -- Registers with --> RegistrationController
    AddOnManager -- Creates --> ManagedClusterAddOn
    ManagedClusterAddOn -- Reconciled by --> AddOnControllers
    AddOnControllers -- Generates manifests for --> ManifestWorkCRs
    ClusterSet -- Groups for --> Placement
    
    %% Cluster Provisioning
    ClusterDeployment --> HiveOperator
    HiveOperator -- Creates/Manages --> HiveClusterDeployment
    ClusterDeployment --> CAPIControllers
    ClusterDeployment --> HypershiftAddonManager
    HypershiftAddonManager -- Manages --> HostedCluster
    HostedCluster --> NodePool
    SiteConfigOperator -- Renders templates for --> InstallationManifests
    InstallationManifests -- Contains --> HiveClusterDeployment
    User -- Provides manifests to --> SiteConfigOperator
    ImageBasedInstallOperator -- Uses OpenShift Installer for --> ConfigISO
    ImageBasedInstallOperator -- Works with --> ClusterBaremetalOperator
    InfrastructureOperator -- Uses --> AssistedService
    AssistedService -- Manages hosts for --> ClusterBaremetalOperator
    
    %% Connections - Application Lifecycle
    User --> ApplicationSet
    ApplicationSet --> Placement
    Placement --> ClusterSet
    ApplicationSet --> GitOpsCluster
    
    %% Backend Components
    APP_OP -- Manages --> ACM_APP
    APP_OP -- Collects Subscriptions --> ALL_SUBS[All Involved Subscriptions]
    APP_OP -- Imports Cluster Secrets --> ARGOCD_NAMESPACE[ArgoCD Server Namespace]
    CHANNEL_OP -- Connects to --> GIT_REPO[Git Repository]
    CHANNEL_OP -- Connects to --> HELM_REPO[Helm Repository]
    CHANNEL_OP -- Connects to --> OBJECT_STORE[Object Store]
    CHANNEL_OP -- Creates --> ACM_CHANNEL
    SUB_OP -- Creates --> PARENT_SUB[Parent Subscription Deployable]
    SUB_OP -- Manages --> ACM_SUB
    SUB_OP -- Reports Status --> ACM_SUB_STATUS
    PLACEMENT_OP -- Generates --> TARGET_CLUSTERS[Target Managed Clusters List]
    PLACEMENT_OP -- Creates --> ACM_PLACEMENT
    INTEGRATIONS_OP -- Creates --> MANIFESTWORK
    INTEGRATIONS_OP -- Propagates --> ARGOCD_APPS[ArgoCD Applications to Managed Clusters]
    INTEGRATIONS_OP -- Queries --> SEARCH_API
    INTEGRATIONS_OP -- Builds --> APP_SET_REPORT[Application Set Report]
    SUB_REPORT_OP -- Aggregates --> CLUSTER_REPORTS[Cluster Level Reports]
    SUB_REPORT_OP -- Creates --> APP_REPORTS[App Level Reports]
    SUB_REPORT_OP -- Manages --> ACM_SUB_REPORT
    CLUSTER_PERM_OP -- Creates --> RBAC_MANIFESTWORK[RBAC ManifestWork]
    CLUSTER_PERM_OP -- Distributes --> RBAC_RESOURCES[RBAC Resources]
    CLUSTER_PERM_OP -- Manages --> ACM_CLUSTER_PERM
    
    %% Add-on Framework
    User -- Configures --> ADT
    User -- Configures --> ADD
    ADT --> CMA
    ADD --> CMA
    CMA -- Orchestrates Deployment --> GAC
    CMA -- Orchestrates Deployment --> OGO
    
    %% Managed Service Account
    GCHC -- Watches --> MSA
    MSA -- Creates Short-Lived Tokens --> STC
    
    %% GitOpsCluster
    GitOpsCluster -- Configures/Integrates with --> ARGOCD_HUB[ArgoCD Server on Hub]
    GitOpsCluster -- Imports Cluster Secrets --> ARGOCD_NAMESPACE
    GitOpsCluster -- Manages --> ACM_GITOPS_CLUSTER
    
    %% External Dependencies
    GitOpsCluster -- Pulls Manifests --> GitHub
    GitOpsCluster -- Pulls Manifests --> Helm
    GitOpsCluster -- Pulls Manifests --> ObjectStore
    
    %% Ansible Integration
    ANSIBLE_INTEGRATION -- Connects to --> Ansible
    ANSIBLE_INTEGRATION -- Uses --> ANSIBLE_TOKEN
    ANSIBLE_INTEGRATION -- Creates --> ANSIBLE_JOB
    
    %% Connections - GRC
    PolicyPropagator -- Watches --> PolicyCRs
    PolicyPropagator -- Handles --> PolicyAutomations
    PolicyPropagator -- Resolves --> HUB_TEMPLATES
    PolicyCRs --> PlacementBinding
    PlacementBinding --> Placement
    GovernancePolicyFramework --> Gatekeeper
    
    %% GRC Hub Components
    GRC_ADDON_CONTROLLER -- Creates & Configures --> H[Policy Components on Managed Clusters]
    GRC_ADDON_CONTROLLER -- Uses Add-on Framework --> ADDON_FRAMEWORK
    POLICY_GENERATOR -- Integrates with --> APP_OP
    POLICY_COMPLIANCE -- Uses --> PostgreSQL
    POLICY_COMPLIANCE -- Provides --> HTTP_API[HTTP API]
    FINE_GRAINED_RBAC -- Integrates with --> OBS
    HUB_TEMPLATES -- Uses --> ENCRYPTION[Encryption]
    HUB_TEMPLATES -- Manages --> METADATA[Metadata]
    METRICS_INTEGRATION -- Uses --> OPENSHIFT_METRICS[OpenShift Metrics]
    METRICS_INTEGRATION -- Uses --> ALERT_MANAGER[Alert Manager]
    
    %% GRC Custom Resources
    PolicyCRs -- Creates --> ACM_POLICY
    PolicyAutomations -- Creates --> ACM_POLICY_AUTO
    POLICY_COMPLIANCE -- Creates --> ACM_POLICY_COMPLIANCE
    POLICY_COMPLIANCE -- Creates --> ACM_POLICY_REPORT
    PolicyCRs -- Groups into --> ACM_POLICY_SET
    PolicyCRs -- Uses --> ACM_POLICY_TEMPLATE
    
    %% GRC External Dependencies
    ANSIBLE_TOWER_GRC -- Receives Jobs from --> Ansible
    GIT_REPO_GRC -- Stores Policies --> GitHub
    HELM_REPO_GRC -- Stores Policy Charts --> Helm
    OBJECT_STORE_GRC -- Stores Policy Artifacts --> ObjectStore
    
    %% Connections - Search
    SearchV2Operator --> SearchIndexer
    SearchV2Operator --> SearchAPI
    SearchV2Operator --> PostgreSQL
    SearchIndexer -- Writes Data To --> PostgreSQL
    SearchAPI -- Reads Data From --> PostgreSQL
    SearchV2Operator -- Deploys & Manages --> SearchCollector
    
    %% Search Storage Dependencies
    PostgreSQL -- Persists Data To --> D_PVC
    D_PVC -- Uses Storage Class --> STORAGE
    
    %% Search Security Dependencies
    SearchV2Operator -- Uses --> SF_PROXY
    SF_PROXY -- Provides Secure Tunnel --> MANAGED_COMM
    SearchV2Operator -- Uses --> ADDON_FRAMEWORK
    SearchV2Operator -- Uses --> OCP_SERVICE_CA
    SearchV2Operator -- Uses --> RBAC_ROLES
    SearchV2Operator -- Uses --> AUTH_MECHANISMS
    
    %% Search Client Integration
    UI_CLIENTS -- Queries --> SearchAPI
    AI_PROCESSOR -- Queries --> SearchAPI
    
    %% Connections - Observability
    User --- MCOperator
    User -- Defines Policies/CRs --> MCOAddon
    User -- Defines Placement --> ClusterManagementAddOn
    MCOperator -- Deploys/Manages --> Thanos
    MCOperator -- Deploys/Manages --> Grafana
    MCOperator -- Deploys/Manages --> AlertManager
    MCOAddon -- Distributes CRs --> ClusterLoggingOperator
    MCOAddon -- Distributes CRs --> OpenTelemetryOperator
    Thanos -- Metrics Data --> Grafana
    Thanos -- Alerts --> AlertManager
    AlertManager -- Forwards Alerts --> ExternalAlerts
    
    %% Search Integration in Observability
    SearchIndexer --> PostgreSQL
    SearchAPI --> PostgreSQL
    UI_CLIENTS --> SearchAPI
    
    %% Managed Cluster Components
    KlusterletOperator -- Deploys --> KlusterletAgent
    KlusterletAgent -- Pulls & Applies --> ManifestWorkCRs
    KlusterletAgent -- Installs/Configures --> AddOnAgents
    
    %% Application Lifecycle on Managed
    MCA1[ManagedClusterAddOn] -- Deploys --> GAC
    MCA1 -- Deploys --> OGO
    GAC --> OGO
    OGO -- Manages --> ARGOCD1
    ARGOCD1 -- Deploys Applications --> TC1
    STC -- Connects Securely --> ARGOCD1
    
    %% Missing Managed Cluster Components
    SUB_OP_MC -- Deploys Resources from --> GIT_REPO
    SUB_OP_MC -- Deploys Resources from --> OBJECT_STORE
    SUB_OP_MC -- Manages --> ACM_SUB_STATUS_MC
    HELM_RELEASE_OP -- Deploys --> PARENT_SUB_MC
    HELM_RELEASE_OP -- Deploys Resources from --> HELM_REPO
    HELM_RELEASE_OP -- Manages --> ACM_HELMRELEASE
    RBAC_RESOURCES_MC -- Includes --> ROLES
    RBAC_RESOURCES_MC -- Includes --> ROLEBINDINGS
    RBAC_RESOURCES_MC -- Includes --> CLUSTERROLES
    RBAC_RESOURCES_MC -- Includes --> CLUSTERROLEBINDINGS
    
    %% GRC on Managed
    CERT_POLICY_CONTROLLER -- Manages --> CERT_POLICY_CR
    CONFIG_POLICY_CONTROLLER -- Manages --> CONFIG_POLICY_CR
    OPERATOR_POLICY_CONTROLLER -- Manages --> OPERATOR_POLICY_CR
    IAM_POLICY_CONTROLLER -- Manages --> IAM_POLICY_CR
    SECURITY_POLICY_CONTROLLER -- Manages --> SECURITY_POLICY_CR
    
    %% Search on Managed
    SEARCH_COLLECTOR_MC -- Collects K8s Data --> KUBERNETES_API
    SEARCH_COLLECTOR_MC -- Sends Data to --> SearchIndexer
    SEARCH_COLLECTOR_MC -- Queries --> SEARCH_API_MC
    
    %% Observability on Managed
    Prometheus --- Exporters
    Prometheus --- ClusterMonitoringOperator
    EndpointOperator --> MetricsCollector
    Prometheus --> MetricsCollector
    MetricsCollector -- Sharded Forwarding --> Thanos
    ClusterLoggingOperator --> ExternalLogs
    OpenTelemetryOperator --> ExternalTraces
    SearchCollector -- Collects K8s Data --> SearchIndexer
    
    %% Other Components on Managed
    AddOnAgents --> OpenShiftGitOpsOperatorManaged[OpenShift GitOps Operator]
    OpenShiftGitOpsOperatorManaged --> ArgoCDInstance[ArgoCD Instance]
    ArgoCDInstance -- Deploys/Manages --> TargetClusterResources[Target Kubernetes Resources]
    SpokeTokenController[spoke-token-controller] -- Securely connects --> ArgoCDInstance
    AddOnAgents --> MetricsCollector
    AddOnAgents --> ClusterLoggingOperator
    AddOnAgents --> OpenTelemetryOperator
    AddOnAgents --> VolSyncOperatorManaged
    VolSyncOperatorManaged -- Replicates --> PersistentVolumes
    AddOnAgents --> GovernancePolicyFramework
    GovernancePolicyFramework --> Gatekeeper
    AddOnAgents --> SubmarinerOperatorManaged
    SubmarinerOperatorManaged --> SubmarinerGateway
    SubmarinerGateway -- Establishes connections --> OtherManagedClusters
    AddOnAgents --> SearchCollector
    
    %% Cross-Pillar Dependencies
    SEARCH -- Queried by --> INTEGRATIONS_OP
    SERVER_FOUNDATION -- Provides Communication --> HUB_MANAGED_COMM
    CONSOLE -- Integrates with --> APP_OP
    CONSOLE -- Integrates with --> CHANNEL_OP
    CONSOLE -- Integrates with --> SUB_OP
    
    %% Data Flow Dependencies
    MANIFESTWORK -- Propagates to --> SUB_OP_MC
    MANIFESTWORK -- Propagates to --> HELM_RELEASE_OP
    MANIFESTWORK -- Propagates to --> RBAC_RESOURCES_MC
    
    %% Certificate Dependencies
    CHANNEL_OP -- Uses Certificates --> CHANNEL_CERTS
    SUB_OP -- Uses Certificates --> SUB_CERTS
    ARGOCD1 -- Uses Certificates --> ARGOCD_CERTS
    
    %% Webhook Dependencies
    CHANNEL_OP -- Uses --> CHANNEL_WEBHOOK
    APP_OP -- Uses --> APP_WEBHOOK
    
    %% External Infrastructure Connections
    ClusterDeployment -- Targets --> CloudProviders
    ClusterDeployment -- Targets --> BareMetal
    CAPIControllers -- Interacts with --> CloudProviders
    HypershiftAddonManager -- Provisions worker nodes in --> CloudProviders
    InfrastructureOperator -- Provisions hosts in --> CloudProviders
    InfrastructureOperator -- Provisions hosts in --> BareMetal
    ImageBasedInstallOperator -- Provisions onto --> BareMetal
    ARGOCD1 -- Pulls manifests from --> GitHub
    ARGOCD1 -- Pulls manifests from --> Helm
    ARGOCD1 -- Pulls manifests from --> ObjectStore
    MCOperator -- Exports to --> ThirdPartyObs
    
    %% Orchestration Dependencies
    MCOAddon -- Orchestrates via ClusterManagementAddOn --> ClusterLoggingOperator
    MCOAddon -- Orchestrates via ClusterManagementAddOn --> OpenTelemetryOperator
    
    %% Styling
    classDef hub fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef managed fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef external fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    classDef foundation fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef crd fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef cross fill:#e8f5e8,stroke:#2e7d32,stroke-width:2px

    class ClusterManager,Klusterlet,ProxyServer,ClusterProxy,RegistrationController,AddOnManager,ManifestWorkCRs foundation
    class Console,ClusterDeployment,ManagedCluster,ClusterAddOnConfig,ManagedClusterImportController,KlusterletOperator,KlusterletCR,ManagedClusterAddOn,AddOnControllers,ClusterSet,Placement,HiveOperator,HiveClusterDeployment,CAPIControllers,HypershiftAddonManager,HostedCluster,NodePool,SiteConfigOperator,InstallationManifests,ImageBasedInstallOperator,ConfigISO,ClusterBaremetalOperator,InfrastructureOperator,AssistedService,ApplicationSet,GitOpsCluster,ADT,ADD,CMA,MSA,GCHC,APP_OP,CHANNEL_OP,SUB_OP,PLACEMENT_OP,INTEGRATIONS_OP,SUB_REPORT_OP,CLUSTER_PERM_OP,PolicyPropagator,PolicyCRs,PolicyAutomations,PlacementBinding,GovernancePolicyFramework,Gatekeeper,GRC_ADDON_CONTROLLER,POLICY_GENERATOR,POLICY_COMPLIANCE,FINE_GRAINED_RBAC,HUB_TEMPLATES,METRICS_INTEGRATION,SearchV2Operator,SearchIndexer,SearchAPI,PostgreSQL,SearchCollector,MCOperator,MCOAddon,Thanos,Grafana,AlertManager,ClusterManagementAddOn,DR4Hub,Velero,StorageSecret,OADPOperator,VolSyncAddonController,GlobalHubOperator,MGHManager hub
    class KlusterletAgent,AddOnAgents,GAC,OGO,ARGOCD1,TC1,STC,SUB_OP_MC,ACM_SUB_STATUS_MC,HELM_RELEASE_OP,PARENT_SUB_MC,RBAC_RESOURCES_MC,ROLES,ROLEBINDINGS,CLUSTERROLES,CLUSTERROLEBINDINGS,CERT_POLICY_CONTROLLER,CONFIG_POLICY_CONTROLLER,OPERATOR_POLICY_CONTROLLER,IAM_POLICY_CONTROLLER,SECURITY_POLICY_CONTROLLER,CERT_POLICY_CR,CONFIG_POLICY_CR,OPERATOR_POLICY_CR,IAM_POLICY_CR,SECURITY_POLICY_CR,SEARCH_COLLECTOR_MC,KUBERNETES_API,SEARCH_API_MC,Prometheus,MetricsCollector,ClusterLoggingOperator,OpenTelemetryOperator,VolSyncOperatorManaged,PersistentVolumes,SubmarinerOperatorManaged,SubmarinerGateway,OtherManagedClusters,Exporters,ClusterMonitoringOperator,EndpointOperator,OpenShiftGitOpsOperatorManaged,ArgoCDInstance,TargetClusterResources,SpokeTokenController managed
    class GitHub,Ansible,ArgoCD,Insights,Helm,ObjectStore,CloudProviders,BareMetal,ThirdPartyObs,ExternalAlerts,ExternalLogs,ExternalTraces external
    class SEARCH,SERVER_FOUNDATION,CONSOLE cross
    class ACM_APP,ACM_CHANNEL,ACM_SUB,ACM_SUB_STATUS,ACM_PLACEMENT,ACM_SUB_REPORT,ACM_CLUSTER_PERM,ACM_GITOPS_CLUSTER,ACM_HELMRELEASE,ACM_POLICY,ACM_POLICY_AUTO,ACM_POLICY_COMPLIANCE,ACM_POLICY_REPORT,ACM_POLICY_SET,ACM_POLICY_TEMPLATE crd
```

## Component Dependencies by Pillar

### **1. Server Foundation Layer**
The core infrastructure that all other components depend on:
- **cluster-manager**: Central hub management
- **klusterlet**: Managed cluster agent
- **ocm-proxyserver**: API aggregation
- **cluster-proxy-addon**: Cluster-to-cluster communication
- **Registration Controller**: Manages cluster registration
- **AddOn Manager**: Orchestrates add-on deployment
- **ManifestWork CRs**: Resource propagation mechanism

### **2. Cluster Lifecycle**
Manages cluster provisioning, import, and lifecycle:
- **Core Components**: Klusterlet, Registration Controller, AddOn Manager
- **Provisioning Engines**: Hive, CAPI, Hypershift, SiteConfig, IBIO, Infrastructure Operator
- **External Dependencies**: Cloud providers, bare metal servers, Git repositories

### **3. Application Lifecycle**
Handles application deployment and GitOps workflows:
- **Backend Operators**: multicloud-operators-application, -channel, -subscription, -placementrule
- **Integration Components**: multicloud-integrations, subscription-report, cluster-permission
- **Add-on Framework**: gitops-addon Controller, OpenShift GitOps Operator
- **External Dependencies**: GitHub, Helm repositories, Object storage, Ansible Tower

### **4. Governance, Risk & Compliance (GRC)**
Manages policies and compliance across clusters:
- **Policy Components**: Policy Propagator, Policy CRs, PolicyAutomations
- **Hub Components**: governance-policy-addon-controller, Policy Generator, Compliance History
- **Managed Cluster Controllers**: cert-policy-controller, config-policy-controller, operator-policy-controller
- **External Dependencies**: Ansible Tower, Git repositories, Helm repositories

### **5. Search**
Provides resource discovery and indexing:
- **Core Components**: Search-v2-operator, Search-indexer, Search-API
- **Storage**: PostgreSQL database with PVC
- **Security**: OCP Service CA, RBAC roles, authentication mechanisms
- **Client Integration**: UI/CLI tools, AI processors

### **6. Observability**
Manages metrics, logging, and monitoring:
- **Hub Components**: MultiCluster Observability Operator, Add-on
- **Storage**: Thanos for metrics, Object storage
- **Visualization**: Grafana, AlertManager
- **Managed Cluster**: Prometheus, Metrics Collector, Logging Operator, OpenTelemetry

## Cross-Pillar Dependencies

### **Integration Points**
1. **Search API**: Used by Application Lifecycle for resource discovery
2. **Server Foundation**: Provides secure communication for all pillars
3. **Console/UI**: Unified interface for all pillar operations
4. **Add-on Framework**: Manages deployment across all pillars
5. **ManifestWork**: Propagates resources from hub to managed clusters

### **External Dependencies**
- **Cloud Providers**: AWS, Azure, GCP for cluster provisioning
- **Git Repositories**: GitHub for application manifests and policies
- **Helm Repositories**: For application and policy charts
- **Object Storage**: S3, MinIO for artifacts and backups
- **Ansible Tower**: For automation workflows
- **Third-party Observability**: External monitoring and alerting systems

This unified dependency graph shows how all ACM pillars work together to provide comprehensive cluster management capabilities, with Server Foundation as the core infrastructure and each pillar adding specialized functionality while maintaining clear separation of concerns. 