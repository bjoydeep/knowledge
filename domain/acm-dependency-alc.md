```mermaid

graph TD
    subgraph Hub Cluster
        User --> A[ApplicationSet]
        A --> B[Placement]
        B --> C[ClusterSet]
        A --> D[GitOpsCluster]

        User -- Configures --> ADT[AddOnTemplate]
        User -- Configures --> ADD[AddOnDeploymentConfig]
        ADT --> CMA[ClusterManagementAddOn]
        ADD --> CMA

        CMA -- Orchestrates Deployment --> GAC[gitops-addon Controller on Spoke]
        CMA -- Orchestrates Deployment --> OGO[OpenShift GitOps Operator on Spoke]

        GCHC[gitopscluster-controller] -- Watches --> MSA[ManagedServiceAccount]
        MSA -- Creates Short-Lived Tokens --> STC[spoke-token-controller on Spoke]

    end

    subgraph Managed Cluster Spoke 1..N
        MCA1[ManagedClusterAddOn] -- Deploys --> GAC
        MCA1 -- Deploys --> OGO

        GAC --> OGO
        OGO -- Manages --> ARGOCD1[ArgoCD Instance]
        ARGOCD1 -- Deploys Applications --> TC1[Target Cluster Resources e.g. Deployments Pods Secrets]
        STC -- Connects Securely --> ARGOCD1
    end

    

    subgraph External Sources
        D -- Pulls Manifests --> GR[Git Repository]
        D -- Pulls Manifests --> HR[Helm Repository]
        D -- Pulls Manifests --> OS[Object Storage]
    end


    D -- Configures/Integrates with --> ARGOCD1
  

    