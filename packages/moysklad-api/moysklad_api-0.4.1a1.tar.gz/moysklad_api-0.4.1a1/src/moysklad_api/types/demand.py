from datetime import datetime

from pydantic import Field

from .account import Account
from .agent import Agent
from .attribute import Attribute
from .contract import Contract
from .demand_position import DemandPosition
from .employee import Employee
from .entity import Entity
from .file import File
from .group import Group
from .organization import Organization
from .overhead import Overhead
from .project import Project
from .rate import Rate
from .sales_channel import SalesChannel
from .shipment_address_full import ShipmentAddressFull
from .state import State
from .store import Store


class Demand(Entity):
    account_id: str = Field(..., alias="accountId")
    agent: Agent = Field(..., alias="agent")
    agent_account: Account | None = Field(None, alias="agentAccount")
    applicable: bool = Field(..., alias="applicable")
    attributes: list[Attribute] | None = Field(None, alias="attributes")
    code: str | None = Field(None, alias="code")
    contract: Contract | None = Field(None, alias="contract")
    created: datetime = Field(..., alias="created")
    deleted: datetime | None = Field(None, alias="deleted")
    description: str | None = Field(None, alias="description")
    external_code: str = Field(..., alias="externalCode")
    files: File | None = Field(None, alias="files")
    group: Group = Field(..., alias="group")
    id: str = Field(..., alias="id")
    moment: datetime = Field(..., alias="moment")
    name: str = Field(..., alias="name")
    organization: Organization = Field(..., alias="organization")
    organization_account: Account | None = Field(None, alias="organizationAccount")
    overhead: Overhead | None = Field(None, alias="overhead")
    owner: Employee | None = Field(None, alias="owner")
    payed_sum: float | None = Field(None, alias="payedSum")
    positions: DemandPosition | None = Field(None, alias="positions")
    printed: bool = Field(..., alias="printed")
    project: Project | None = Field(None, alias="project")
    published: bool = Field(..., alias="published")
    rate: Rate = Field(..., alias="rate")
    sales_channel: SalesChannel | None = Field(None, alias="salesChannel")
    shared: bool = Field(..., alias="shared")
    shipment_address: str | None = Field(None, alias="shipmentAddress")
    shipment_address_full: ShipmentAddressFull | None = Field(
        None, alias="shipmentAddressFull"
    )
    state: State | None = Field(None, alias="state")
    store: Store = Field(..., alias="store")
    sum: float = Field(..., alias="sum")
    sync_id: str | None = Field(None, alias="syncId")
    updated: datetime = Field(..., alias="updated")
    vat_enabled: bool = Field(..., alias="vatEnabled")
    vat_included: bool | None = Field(None, alias="vatIncluded")
    vat_sum: float | None = Field(None, alias="vatSum")
