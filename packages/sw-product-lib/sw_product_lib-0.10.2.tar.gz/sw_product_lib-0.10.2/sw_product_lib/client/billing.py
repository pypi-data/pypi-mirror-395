from dataclasses import dataclass
from typing import Optional

from strangeworks_core.platform.gql import API, Operation


approval_request = Operation(
    query="""
        query requestBillingApproval (
            $resource_slug: String!,
            $workspace_member_slug: String!,
            $amount: Float!,
            $currency: Currency!
        )
        {
            requestBillingApproval(
                resourceSlug: $resource_slug,
                workspaceMemberSlug: $workspace_member_slug,
                amount: $amount,
                currency: $currency){
                isApproved
                rejectionMessage
            }
        }
        """,
)

create_tx = Operation(
    query="""
        mutation billingTransactionCreate (
            $resource_slug: String!,
            $job_slug: String!,
            $amount: Float!,
            $unit: Currency!,
            $description: String!,
            $memo: String) {
            billingTransactionCreate(input: {
                resourceSlug: $resource_slug,
                jobSlug: $job_slug,
                amount: $amount,
                unit: $unit,
                description: $description,
                memo: $memo,
            }) {
                billingTransaction {
                    id
                    status
                    amount
                    unit
                    description
                    memo
                }
            }
        }
        """,
)


@dataclass
class BillingTransaction:
    id: str
    amount: float
    unit: str
    status: Optional[str] = None
    description: Optional[str] = None
    memo: Optional[str] = None

    @staticmethod
    def from_dict(res: dict):
        return BillingTransaction(
            id=res["id"],
            amount=res["amount"],
            unit=res["unit"],
            status=res["status"],
            description=res["description"],
            memo=res["memo"],
        )


def request_approval(
    api: API,
    resource_slug: str,
    workspace_member_slug: str,
    amount: float,
    currency: str,
) -> bool:
    """Request approval to execute job.
    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    workspaceMemberSlug: str
        used to map workspace and user.
    amount: float
        numerical amount to indicate cost (negative amount) or credit(positive amount)
    currency: str
        unit for the amount

        Returns
    -------
    : bool
        True if request was approved, False otherwise
    """
    platform_result = api.execute(
        approval_request,
        **locals(),
    )
    return (
        False if not platform_result["requestBillingApproval"]["isApproved"] else True
    )


def create_transaction(
    api: API,
    resource_slug: str,
    job_slug: str,
    amount: float,
    unit: str,
    description: str,
    memo: Optional[str] = None,
) -> BillingTransaction:
    """Create a billing transaction on the platform.

    Parameters
    ----------
    api: API
        provides access to the platform API.
    resource_slug: str
        used as identifier for the resource.
    job_slug: str
        used as identifier for the job.
    amount: float
        numerical amount. can be negative.
    unit: str
        describes the unit for the amount. for example, USD for currency.
    description: str
        a brief description that can be seen by the user.
    memo: str
        a string that should not be seen by the user.

     Returns
    -------
    : BillingTransaction
        The ``BillingTransaction`` object
    """
    platform_result = api.execute(
        op=create_tx,
        **locals(),
    )
    return BillingTransaction.from_dict(
        platform_result["billingTransactionCreate"]["billingTransaction"]
    )
