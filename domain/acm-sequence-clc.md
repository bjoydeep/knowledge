```mermaid

sequenceDiagram
    actor User
    participant ACMConsole as ACM Console

    box Hub Cluster
        participant HiveController as "Hive Controller"
        participant ClusterImportController as "Cluster Import Controller"
        participant RegistrationController as "Registration Controller"
        participant AddonManager as "Add-on Manager"
        participant AddonSpecificControllers as "Add-on Specific Controllers"
    end

    box Managed Cluster
        participant KlusterletOperator as "Klusterlet Operator"
        participant KlusterletAgent as "Klusterlet Agent"
        participant AddonAgent as "Add-on Agent"
    end

    %% Cluster Creation and Import Workflow
    User->>ACMConsole: Initiates **Cluster Creation** [1]
    activate ACMConsole

    ACMConsole->>HubCluster: Creates **ClusterDeployment, ManagedCluster, & ClusterAddonConfig CRs** (on Hub Cluster) [1]
    Note over ACMConsole,HubCluster: These CRs are then reconciled by respective controllers.
    deactivate ACMConsole

    HubCluster->>HiveController: ClusterDeployment CR created for provisioning
    activate HiveController
    HiveController->>Managed Cluster: **Provisions New Cluster** (via ClusterDeployment) [1-3]
    Note over HiveController: Hive is the dedicated project for IPI cluster deployment. [3]
    deactivate HiveController

    Managed Cluster-->>ClusterImportController: Cluster Provisioning Complete (Hub Cluster's **ClusterDeployment CR** updated with admin kubeconfig) [1]
    activate ClusterImportController
    ClusterImportController->>Managed Cluster: Deploys **Klusterlet Operator** (to Managed Cluster using kubeconfig) [4]
    ClusterImportController->>Managed Cluster: Creates **Klusterlet CR** (on Managed Cluster) [4]
    deactivate ClusterImportController
    activate KlusterletOperator

    KlusterletOperator->>KlusterletAgent: Deploys **Klusterlet Agent** (based on Klusterlet CR) [4]
    deactivate KlusterletOperator
    activate KlusterletAgent

    KlusterletAgent->>RegistrationController: **Registers Managed Cluster** with Hub Cluster [4]
    activate RegistrationController
    RegistrationController-->>HubCluster: Registration Acknowledged (updates **ManagedCluster CR** & **Cluster Lease CR** on Hub) [4-6]
    deactivate RegistrationController

    loop Continuous Status Updates
        KlusterletAgent->>HubCluster: Updates **ManagedCluster CR Status** (on Hub Cluster) [4]
        KlusterletAgent->>HubCluster: Updates **Cluster Lease CR Status** (on Hub Cluster) [4-6]
    end

    %% Add-on Management Workflow (retained for context, as it's a subsequent phase)
    opt Add-on Management Flow
        AddonManager->>HubCluster: Creates **ManagedClusterAddon CR** (on Hub Cluster) [1]
        activate AddonSpecificControllers
        AddonSpecificControllers->>HubCluster: Reconciles **ManagedClusterAddon CRs** & Generates **Manifest Works** (for Add-on Agent deployment) [1]
        deactivate AddonSpecificControllers

        KlusterletAgent->>HubCluster: **Pulls Manifest Works** [1]
        KlusterletAgent->>Managed Cluster: Applies Manifest Works (Installs **Add-on Agent**) [1]
        activate AddonAgent

        AddonAgent->>Managed Cluster: Creates **Add-on Lease CRs** (on Managed Cluster) [1]
        KlusterletAgent->>Managed Cluster: Reads **Add-on Lease CRs** [1]
        KlusterletAgent->>HubCluster: Updates **ManagedClusterAddon CR Status** (on Hub Cluster) [1]
        deactivate AddonAgent
    end