from datetime import datetime

from pydantic import Field

from .agent import Agent
from .contract import Contract
from .entity import Entity
from .file import File
from .group import Group
from .meta_array import MetaArray
from .organization import Organization
from .organization_account import OrganizationAccount
from .project import Project
from .purchaseorder_position import PurchaseOrderPosition
from .rate import Rate
from .state import State
from .store import Store


class PurchaseOrder(Entity):
    id: str = Field(alias="id")
    account_id: str | None = Field(None, alias="accountId")
    agent: Agent | None = Field(None, alias="agent")
    agent_account: str | None = Field(None, alias="agentAccount")
    applicable: bool | None = Field(None, alias="applicable")
    attributes: list[dict] | None = Field(None, alias="attributes")
    code: str | None = Field(None, alias="code")
    contract: Contract | None = Field(None, alias="contract")
    created: datetime | None = Field(None, alias="created")
    deleted: datetime | None = Field(None, alias="deleted")
    delivery_planned_moment: datetime | None = Field(
        None, alias="deliveryPlannedMoment"
    )
    description: str | None = Field(None, alias="description")
    external_code: str | None = Field(None, alias="externalCode")
    files: File | list[File] | None = Field(None, alias="files")
    group: Group | None = Field(None, alias="group")
    invoiced_sum: float | None = Field(None, alias="invoicedSum")
    moment: datetime | None = Field(None, alias="moment")
    name: str | None = Field(None, alias="name")
    organization: Organization | None = Field(None, alias="organization")
    organization_account: OrganizationAccount | None = Field(
        None, alias="organizationAccount"
    )
    owner: Agent | None = Field(None, alias="owner")
    payed_sum: float | None = Field(None, alias="payedSum")
    positions: PurchaseOrderPosition | MetaArray[PurchaseOrderPosition] | None = Field(
        None, alias="positions"
    )
    printed: bool | None = Field(None, alias="printed")
    project: Project | None = Field(None, alias="project")
    published: bool | None = Field(None, alias="published")
    rate: Rate | None = Field(None, alias="rate")
    shared: bool | None = Field(None, alias="shared")
    shipped_sum: float | None = Field(None, alias="shippedSum")
    state: State | None = Field(None, alias="state")
    store: Store | None = Field(None, alias="store")
    sum: float | None = Field(None, alias="sum")
    sync_id: str | None = Field(None, alias="syncId")
    updated: datetime | None = Field(None, alias="updated")
    vat_enabled: bool | None = Field(None, alias="vatEnabled")
    vat_included: bool | None = Field(None, alias="vatIncluded")
    vat_sum: float | None = Field(None, alias="vatSum")
    wait_sum: float | None = Field(None, alias="waitSum")
