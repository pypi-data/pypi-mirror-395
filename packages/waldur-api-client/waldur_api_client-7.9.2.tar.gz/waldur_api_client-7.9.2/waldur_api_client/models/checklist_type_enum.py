from enum import Enum


class ChecklistTypeEnum(str, Enum):
    CUSTOMER_ONBOARDING = "customer_onboarding"
    OFFERING_COMPLIANCE = "offering_compliance"
    PROJECT_COMPLIANCE = "project_compliance"
    PROJECT_METADATA = "project_metadata"
    PROPOSAL_COMPLIANCE = "proposal_compliance"

    def __str__(self) -> str:
        return str(self.value)
