```mermaid

sequenceDiagram
    actor User
    participant ACMConsole as ACM Console

    box Hub Cluster
        participant HubController as "Hub Controller"
        participant ClusterImportController as "Cluster Import Controller"
        participant AddonManager as "Add-on Manager"
        participant AddonSpecificControllers as "Add-on Specific Controllers"
        participant RegistrationController as "Registration Controller"
    end

    box Managed Cluster
        participant KlusterletOperator as "Klusterlet Operator"
        participant KlusterletAgent as "Klusterlet Agent"
        participant AddonAgent as "Add-on Agent"
    end

    %% Cluster Creation and Import Workflow
    User->>ACMConsole: Initiates **Cluster Creation** [1]
    activate ACMConsole

    ACMConsole->>HubController: Creates **ClusterDeployment, ManagedCluster, & ClusterAddonConfig CRs** (on Hub Cluster) [1]
    deactivate ACMConsole
    activate HubController

    HubController->>Managed Cluster: **Provisions New Cluster** [1]
    deactivate HubController

    Managed Cluster-->>ClusterImportController: Cluster Provisioning Complete (Hub Cluster's **ClusterDeployment CR** updated with admin kubeconfig) [1]
    activate ClusterImportController

    ClusterImportController->>Managed Cluster: Deploys **Klusterlet Operator** (to Managed Cluster using kubeconfig) [2]
    deactivate ClusterImportController
    activate KlusterletOperator

    KlusterletOperator->>Managed Cluster: Creates **Cluster CR** (on Managed Cluster) [2]
    KlusterletOperator->>KlusterletAgent: Deploys **Klusterlet Agent** [2]
    deactivate KlusterletOperator
    activate KlusterletAgent

    KlusterletAgent->>RegistrationController: **Registers Managed Cluster** with Hub Cluster [2]
    activate RegistrationController
    RegistrationController-->>KlusterletAgent: Registration Acknowledged
    deactivate RegistrationController

    loop Continuous Status Updates
        KlusterletAgent->>HubController: Updates **ManagedCluster CR** & **Cluster List CRs** Status (on Hub Cluster) [2]
    end

    %% Add-on Management Workflow
    opt Add-on Management Flow
        AddonManager->>AddonSpecificControllers: Creates **ManagedClusterAddon CR** (on Hub Cluster) [2]
        activate AddonSpecificControllers
        AddonSpecificControllers->>Managed Cluster: Reconciles **ManagedClusterAddon CRs** & Generates **Manifest Works** (for Add-on Agent deployment) [2]
        deactivate AddonSpecificControllers

        KlusterletAgent->>Managed Cluster: **Pulls Manifest Works** [2]
        KlusterletAgent->>AddonAgent: Applies Manifest Works (Installs **Add-on Agent**) [2]
        activate AddonAgent

        AddonAgent->>KlusterletAgent: Creates **Add-on List** (on Managed Cluster) [2]
        KlusterletAgent->>AddonAgent: Reads **Add-on List CRs** [2]
        KlusterletAgent->>AddonManager: Updates **ManagedClusterAddon CR Status** (on Hub Cluster) [2]
        deactivate AddonAgent
    end