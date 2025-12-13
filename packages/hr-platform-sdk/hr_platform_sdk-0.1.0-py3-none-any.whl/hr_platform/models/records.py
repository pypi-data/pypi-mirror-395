"""HR Record models.

Pydantic models for HR records and their nested components.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from hr_platform.models.enums import Entity, RecordStatus


class Workforce(BaseModel):
    """Workforce composition data.

    Tracks headcount by gender and age bracket for both
    blue collar and white collar employees.
    """

    model_config = ConfigDict(populate_by_name=True)

    # Blue Collar
    bc_male: int = Field(default=0, ge=0, description="Male blue collar employees")
    bc_female: int = Field(default=0, ge=0, description="Female blue collar employees")
    bc_age_under_20: int = Field(default=0, ge=0, alias="bc_age_under_20")
    bc_age_20_29: int = Field(default=0, ge=0)
    bc_age_30_39: int = Field(default=0, ge=0)
    bc_age_40_49: int = Field(default=0, ge=0)
    bc_age_50_59: int = Field(default=0, ge=0)
    bc_age_60_plus: int = Field(default=0, ge=0)
    bc_ausgesteuert: int = Field(
        default=0, ge=0, description="Long-term sick (out of payroll)"
    )

    # White Collar
    wc_male: int = Field(default=0, ge=0, description="Male white collar employees")
    wc_female: int = Field(
        default=0, ge=0, description="Female white collar employees"
    )
    wc_age_under_20: int = Field(default=0, ge=0)
    wc_age_20_29: int = Field(default=0, ge=0)
    wc_age_30_39: int = Field(default=0, ge=0)
    wc_age_40_49: int = Field(default=0, ge=0)
    wc_age_50_59: int = Field(default=0, ge=0)
    wc_age_60_plus: int = Field(default=0, ge=0)
    wc_ausgesteuert: int = Field(
        default=0, ge=0, description="Long-term sick (out of payroll)"
    )
    wc_overhead: int = Field(default=0, ge=0, description="Overhead/shared services")

    @property
    def blue_collar_total(self) -> int:
        """Total blue collar headcount."""
        return self.bc_male + self.bc_female

    @property
    def white_collar_total(self) -> int:
        """Total white collar headcount."""
        return self.wc_male + self.wc_female

    @property
    def total_headcount(self) -> int:
        """Total headcount across all collar types."""
        return self.blue_collar_total + self.white_collar_total


class Capacity(BaseModel):
    """Capacity and FTE data.

    Full-time equivalents and hours worked including
    external workers and overtime.
    """

    model_config = ConfigDict(populate_by_name=True)

    fte_blue_collar: float = Field(
        default=0.0, ge=0, description="Blue collar FTE from payroll"
    )
    fte_white_collar: float = Field(
        default=0.0, ge=0, description="White collar FTE from payroll"
    )
    fte_overhead: float = Field(
        default=0.0, ge=0, description="Overhead/shared services FTE"
    )
    external_hours_blue: float = Field(
        default=0.0, ge=0, description="Blue collar temp worker hours"
    )
    external_hours_white: float = Field(
        default=0.0, ge=0, description="White collar temp worker hours"
    )
    overtime_hours_blue: float = Field(
        default=0.0, ge=0, description="Blue collar overtime hours"
    )
    overtime_hours_white: float = Field(
        default=0.0, ge=0, description="White collar overtime hours"
    )

    @property
    def total_internal_fte(self) -> float:
        """Total internal FTE."""
        return self.fte_blue_collar + self.fte_white_collar + self.fte_overhead

    @property
    def total_external_fte(self) -> float:
        """Total external FTE (hours / 173)."""
        return (self.external_hours_blue + self.external_hours_white) / 173


class Absences(BaseModel):
    """Absence data.

    Sick days, vacation, and various leave types.
    """

    model_config = ConfigDict(populate_by_name=True)

    sick_days_blue: int = Field(
        default=0, ge=0, description="Blue collar sick leave days"
    )
    sick_days_white: int = Field(
        default=0, ge=0, description="White collar sick leave days"
    )
    long_term_sick_fte: float = Field(
        default=0.0, ge=0, description="Long-term sick employees (FTE)"
    )
    vacation_hours_blue: float = Field(
        default=0.0, ge=0, description="Blue collar vacation hours taken"
    )
    vacation_hours_white: float = Field(
        default=0.0, ge=0, description="White collar vacation hours taken"
    )
    maternity_fte: float = Field(
        default=0.0, ge=0, description="Employees on maternity leave (FTE)"
    )
    parental_fte: float = Field(
        default=0.0, ge=0, description="Employees on parental leave (FTE)"
    )

    @property
    def total_sick_days(self) -> int:
        """Total sick days."""
        return self.sick_days_blue + self.sick_days_white


class Turnover(BaseModel):
    """Employee turnover data.

    Voluntary and involuntary departures by collar type.
    """

    model_config = ConfigDict(populate_by_name=True)

    voluntary_bc: int = Field(
        default=0, ge=0, description="Blue collar voluntary departures"
    )
    voluntary_wc: int = Field(
        default=0, ge=0, description="White collar voluntary departures"
    )
    involuntary_bc: int = Field(
        default=0, ge=0, description="Blue collar involuntary departures"
    )
    involuntary_wc: int = Field(
        default=0, ge=0, description="White collar involuntary departures"
    )

    @property
    def total_voluntary(self) -> int:
        """Total voluntary departures."""
        return self.voluntary_bc + self.voluntary_wc

    @property
    def total_involuntary(self) -> int:
        """Total involuntary departures."""
        return self.involuntary_bc + self.involuntary_wc

    @property
    def total_departures(self) -> int:
        """Total departures."""
        return self.total_voluntary + self.total_involuntary


class Performance(BaseModel):
    """Performance review data."""

    model_config = ConfigDict(populate_by_name=True)

    year_reviews_blue: int = Field(
        default=0, ge=0, description="Blue collar annual reviews completed"
    )
    year_reviews_white: int = Field(
        default=0, ge=0, description="White collar annual reviews completed"
    )

    @property
    def total_reviews(self) -> int:
        """Total reviews completed."""
        return self.year_reviews_blue + self.year_reviews_white


class Financials(BaseModel):
    """Financial data.

    Personnel costs including wages, salaries, and temp costs.
    """

    model_config = ConfigDict(populate_by_name=True)

    wages: float = Field(default=0.0, ge=0, description="Blue collar wages (EUR)")
    salaries: float = Field(default=0.0, ge=0, description="White collar salaries (EUR)")
    salaries_overhead: float = Field(
        default=0.0, ge=0, description="Overhead salaries (EUR)"
    )
    temp_wages: float = Field(
        default=0.0, ge=0, description="Temporary/external worker costs (EUR)"
    )

    @property
    def total_costs(self) -> float:
        """Total personnel costs."""
        return self.wages + self.salaries + self.salaries_overhead + self.temp_wages


class HRRecord(BaseModel):
    """Base HR record without nested data.

    Contains the core record metadata and workflow information.
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(description="Unique record identifier (UUID)")
    entity: Entity = Field(description="Organizational entity code")
    year: int = Field(ge=2020, le=2100, description="Reporting year")
    month: int = Field(ge=1, le=12, description="Reporting month")
    working_days: int = Field(default=21, ge=0, le=31, description="Workable days")
    status: RecordStatus = Field(
        default=RecordStatus.DRAFT, description="Workflow status"
    )

    # Workflow tracking
    submitted_by: str | None = Field(
        default=None, description="User ID who submitted"
    )
    submitted_at: str | None = Field(
        default=None, description="Submission timestamp"
    )
    approved_by: str | None = Field(
        default=None, description="User ID who approved/rejected"
    )
    approved_at: str | None = Field(
        default=None, description="Approval/rejection timestamp"
    )
    rejected_reason: str | None = Field(
        default=None, description="Rejection reason if rejected"
    )

    # Timestamps
    created_at: str = Field(description="Record creation timestamp")
    updated_at: str = Field(description="Last modification timestamp")


class FullHRRecord(HRRecord):
    """Complete HR record with all nested data.

    Extends HRRecord with workforce, capacity, absences,
    turnover, performance, and financial data.
    """

    workforce: Workforce | None = Field(default=None)
    capacity: Capacity | None = Field(default=None)
    absences: Absences | None = Field(default=None)
    turnover: Turnover | None = Field(default=None)
    performance: Performance | None = Field(default=None)
    financials: Financials | None = Field(default=None)


class CreateRecordRequest(BaseModel):
    """Request body for creating a new HR record."""

    model_config = ConfigDict(populate_by_name=True)

    entity: Entity = Field(description="Organizational entity code")
    year: int = Field(ge=2020, le=2100, description="Reporting year")
    month: int = Field(ge=1, le=12, description="Reporting month")
    working_days: int = Field(default=21, ge=0, le=31, description="Workable days")

    workforce: Workforce | None = Field(default=None)
    capacity: Capacity | None = Field(default=None)
    absences: Absences | None = Field(default=None)
    turnover: Turnover | None = Field(default=None)
    performance: Performance | None = Field(default=None)
    financials: Financials | None = Field(default=None)


class UpdateRecordRequest(BaseModel):
    """Request body for updating an HR record."""

    model_config = ConfigDict(populate_by_name=True)

    entity: Entity = Field(description="Organizational entity code")
    year: int = Field(ge=2020, le=2100, description="Reporting year")
    month: int = Field(ge=1, le=12, description="Reporting month")
    working_days: int = Field(default=21, ge=0, le=31, description="Workable days")

    workforce: Workforce | None = Field(default=None)
    capacity: Capacity | None = Field(default=None)
    absences: Absences | None = Field(default=None)
    turnover: Turnover | None = Field(default=None)
    performance: Performance | None = Field(default=None)
    financials: Financials | None = Field(default=None)


class RejectRecordRequest(BaseModel):
    """Request body for rejecting a record."""

    reason: str = Field(min_length=1, description="Rejection reason")


class RecordCreatedResponse(BaseModel):
    """Response from creating a record."""

    id: str = Field(description="Created record ID")
    message: str = Field(default="Record created successfully")


class RecordUpdatedResponse(BaseModel):
    """Response from updating a record."""

    id: str = Field(description="Updated record ID")
    message: str = Field(default="Record updated successfully")


class RecordDeletedResponse(BaseModel):
    """Response from deleting a record."""

    message: str = Field(default="Record deleted successfully")


class WorkflowResponse(BaseModel):
    """Response from workflow actions (submit, approve, reject)."""

    message: str = Field(description="Success message")
