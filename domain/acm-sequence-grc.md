```mermaid

sequenceDiagram
    participant User
    participant PolicyPropagatorController as PPC
    participant PlacementAndBindingCRs as P&BCRs
    participant grcPolicyAddonController as GPAC
    participant ReplicatedPolicyCRs as RPCs
    participant GovernancePolicyFramework as GPF
    participant StatusSyncController as SSC
    participant TemplateSyncController as TSC
    participant PolicyTemplateCRs as PTCRs
    participant GatekeeperConstraintSync as GCS
    participant OtherPolicyControllers as OPC
    participant ManagedCluster as MC

    User->>PPC: Defines Root Policy CRs & PolicyAutomations
    PPC->>PPC: Watches Root Policy CRs
    PPC->>P&BCRs: Leverages Placement & PlacementBinding CRs
    PPC->>RPCs: Propagates Policies to Designated Managed Cluster Namespaces
    PPC->>PPC: Handles PolicyAutomations & Resolves Hub Templates
    GPAC->>MC: Creates & Configures Policy Components

    RPCs->>GPF: Propagated Policies Arrive
    GPF->>GPF: Copies Policies to ManagedCluster Namespace
    GPF->>SSC: (via Status Sync) Records Compliance Events
    SSC-->>User: Sends Compliance Status Updates (to Hub Cluster)
    GPF->>TSC: (via Template Sync) Creates Templates for Config Policies
    TSC->>PTCRs: Generates Policy Template CRs
    PTCRs->>MC: Leads to (e.g., Gatekeeper Resources)

    alt Gatekeeper Installed
        GPF->>GCS: Triggers Gatekeeper Constraint Sync
        GCS->>MC: Creates Gatekeeper Policy Resources for Admission Control
    end

    OPC->>MC: Enforces Configuration & Certificate Policies
    MC-->>MC: Generates Events for Policy Compliance/Enforcement