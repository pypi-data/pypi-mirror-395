#!/usr/bin/env python3
"""
AnalyticsService - Thread-safe analytics and statistics service.

Provides comprehensive analytics functions for survey data including
response rates, participation metrics, organization status tracking,
and activity monitoring.
"""

import threading
from datetime import datetime
from typing import Any, Dict, List, Optional

from src.extractors.sheets_reader import SheetsReader


class AnalyticsService:
    """
    Thread-safe analytics service for survey data.

    Provides analytics, statistics, and reporting metrics for survey responses
    across multiple stakeholder types (Intake, CEO, Tech, Staff).
    """

    def __init__(self, data_service):
        """
        Initialize analytics service with data dependency.

        Args:
            data_service: DataService instance for accessing sheet data
        """
        self._data_service = data_service
        self._lock = threading.RLock()  # Use RLock for reentrant lock support

    def get_response_rates(self) -> Dict[str, Any]:
        """
        Calculate response rates using the master organization list.

        Maps organizations from OrgMaster (using 'Organization' field) to
        Intake data (using 'Organization Name:' field) to calculate
        outreach vs response rates.

        Returns:
            Dictionary with response rate metrics and org-level details
        """
        with self._lock:
            org_master = self._data_service.get_tab_data("OrgMaster")
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Get all organizations from master list
            master_orgs = {
                row.get("Organization", "").strip()
                for row in org_master
                if row.get("Organization", "").strip()
            }

            # Get organizations that responded to intake
            intake_orgs = {
                row.get("Organization Name:", "").strip()
                for row in intake_data
                if row.get("Organization Name:", "").strip()
            }

            # Get organizations with CEO responses
            ceo_orgs = {
                row.get("CEO Organization", "").strip()
                for row in ceo_data
                if row.get("CEO Organization", "").strip()
            }

            # Get organizations with Tech responses
            tech_orgs = {
                row.get("Organization", "").strip()
                for row in tech_data
                if row.get("Organization", "").strip()
            }

            # Get organizations with Staff responses
            staff_orgs = {
                row.get("Organization", "").strip()
                for row in staff_data
                if row.get("Organization", "").strip()
            }

            # Calculate metrics
            total_outreach = len(master_orgs)
            total_responded = len(intake_orgs)
            intake_response_rate = (
                (total_responded / total_outreach * 100) if total_outreach > 0 else 0
            )

            # Survey completion metrics
            ceo_responses = len(ceo_orgs)
            tech_responses = len(tech_orgs)
            staff_responses = len(staff_orgs)

            return {
                "total_outreach": total_outreach,
                "total_responded": total_responded,
                "not_responded": total_outreach - total_responded,
                "intake_response_rate": round(intake_response_rate, 1),
                "ceo_responses": ceo_responses,
                "tech_responses": tech_responses,
                "staff_responses": staff_responses,
                "master_orgs": sorted(master_orgs),
                "responded_orgs": sorted(intake_orgs),
                "not_responded_orgs": sorted(master_orgs - intake_orgs),
            }

    def get_participation_overview(self) -> Dict[str, Any]:
        """
        Get aggregate participation metrics for dashboard.

        Returns:
            Dictionary with participation statistics across survey types
        """
        with self._lock:
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Extract unique organizations from each tab
            intake_orgs = {
                row.get("Organization Name:", "").strip()
                for row in intake_data
                if row.get("Organization Name:", "").strip()
            }

            ceo_orgs = {
                row.get("CEO Organization", "").strip()
                for row in ceo_data
                if row.get("CEO Organization", "").strip()
            }

            tech_orgs = {
                row.get("Organization", "").strip()
                for row in tech_data
                if row.get("Organization", "").strip()
            }

            staff_orgs = {
                row.get("Organization", "").strip()
                for row in staff_data
                if row.get("Organization", "").strip()
            }

            # Calculate metrics
            total_orgs = len(intake_orgs)
            ceo_complete = len(intake_orgs & ceo_orgs)
            tech_complete = len(intake_orgs & tech_orgs)
            staff_complete = len(intake_orgs & staff_orgs)
            fully_complete = len(intake_orgs & ceo_orgs & tech_orgs & staff_orgs)
            not_started = len(intake_orgs - ceo_orgs)

            return {
                "total_organizations": total_orgs,
                "ceo_complete": ceo_complete,
                "tech_complete": tech_complete,
                "staff_complete": staff_complete,
                "fully_complete": fully_complete,
                "not_started": not_started,
                "ceo_percent": round(100.0 * ceo_complete / total_orgs, 1) if total_orgs > 0 else 0,
                "tech_percent": (
                    round(100.0 * tech_complete / total_orgs, 1) if total_orgs > 0 else 0
                ),
                "staff_percent": (
                    round(100.0 * staff_complete / total_orgs, 1) if total_orgs > 0 else 0
                ),
                "fully_percent": (
                    round(100.0 * fully_complete / total_orgs, 1) if total_orgs > 0 else 0
                ),
            }

    def get_organizations_status(self) -> List[Dict[str, Any]]:
        """
        Get per-organization completion status, sorted by most recent activity.

        Returns:
            List of organization status dictionaries with completion details
        """
        with self._lock:
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Create lookup dictionaries with dates for each survey type
            ceo_orgs_dates = {}
            for row in ceo_data:
                org_name = row.get("CEO Organization", "").strip()
                if org_name:
                    ceo_orgs_dates[org_name] = row.get("Date", "")

            tech_orgs_dates = {}
            for row in tech_data:
                org_name = row.get("Organization", "").strip()
                if org_name:
                    tech_orgs_dates[org_name] = row.get("Date", "")

            staff_orgs_dates = {}
            for row in staff_data:
                org_name = row.get("Organization", "").strip()
                if org_name:
                    staff_orgs_dates[org_name] = row.get("Date", "")

            # Build organization status list with most recent activity
            organizations = []
            for row in intake_data:
                org_name = row.get("Organization Name:", "").strip()
                if not org_name:
                    continue

                intake_date = row.get("Date", "")

                has_ceo = org_name in ceo_orgs_dates
                has_tech = org_name in tech_orgs_dates
                has_staff = org_name in staff_orgs_dates

                # Determine overall status
                if has_ceo and has_tech and has_staff:
                    overall_status = "complete"
                elif has_ceo:
                    overall_status = "in_progress"
                else:
                    overall_status = "not_started"

                # Find most recent activity across all surveys
                all_dates = [intake_date]
                if has_ceo:
                    all_dates.append(ceo_orgs_dates[org_name])
                if has_tech:
                    all_dates.append(tech_orgs_dates[org_name])
                if has_staff:
                    all_dates.append(staff_orgs_dates[org_name])

                # Get max date (most recent activity)
                most_recent_activity = max(all_dates) if all_dates else ""

                # Calculate completion percentage
                completed_surveys = sum([has_ceo, has_tech, has_staff])
                completion_pct = int((completed_surveys / 3) * 100)

                organizations.append(
                    {
                        "organization": org_name,
                        "intake_date": intake_date[:10] if intake_date else "",
                        "ceo_status": "complete" if has_ceo else "pending",
                        "tech_status": "complete" if has_tech else "pending",
                        "staff_status": "complete" if has_staff else "pending",
                        "overall_status": overall_status,
                        "last_activity": most_recent_activity,
                        "completed_surveys": completed_surveys,
                        "completion_pct": completion_pct,
                    }
                )

            # Sort by most recent activity descending (return ALL organizations)
            organizations.sort(key=lambda x: x["last_activity"], reverse=True)
            return organizations

    def get_latest_activity(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent submission activity across all tabs.

        Args:
            limit: Maximum number of activities to return (default: 10)

        Returns:
            List of recent activity dictionaries
        """
        with self._lock:
            activities = []

            # Intake activities
            intake_data = self._data_service.get_tab_data("Intake")
            for row in intake_data:
                org_name = row.get("Organization Name:", "").strip()
                date = row.get("Date", "")
                if org_name and date:
                    activities.append(
                        {
                            "organization": org_name,
                            "activity_type": "Intake",
                            "timestamp": date[:16] if len(date) >= 16 else date,
                            "activity_description": "Intake form completed",
                        }
                    )

            # CEO activities
            ceo_data = self._data_service.get_tab_data("CEO")
            for row in ceo_data:
                org_name = row.get("CEO Organization", "").strip()
                date = row.get("Date", "")
                name = row.get("Name", "")
                if org_name and date:
                    activities.append(
                        {
                            "organization": org_name,
                            "activity_type": "CEO",
                            "timestamp": date[:16] if len(date) >= 16 else date,
                            "activity_description": (
                                f"CEO survey completed by {name}"
                                if name
                                else "CEO survey completed"
                            ),
                        }
                    )

            # Tech activities
            tech_data = self._data_service.get_tab_data("Tech")
            for row in tech_data:
                org_name = row.get("Organization", "").strip()
                date = row.get("Date", "")
                name = row.get("Name", "")
                if org_name and date:
                    activities.append(
                        {
                            "organization": org_name,
                            "activity_type": "Tech",
                            "timestamp": date[:16] if len(date) >= 16 else date,
                            "activity_description": (
                                f"Tech survey completed by {name}"
                                if name
                                else "Tech survey completed"
                            ),
                        }
                    )

            # Staff activities
            staff_data = self._data_service.get_tab_data("Staff")
            for row in staff_data:
                org_name = row.get("Organization", "").strip()
                date = row.get("Date", "")
                name = row.get("Name", "")
                if org_name and date:
                    activities.append(
                        {
                            "organization": org_name,
                            "activity_type": "Staff",
                            "timestamp": date[:16] if len(date) >= 16 else date,
                            "activity_description": (
                                f"Staff survey completed by {name}"
                                if name
                                else "Staff survey completed"
                            ),
                        }
                    )

            # Sort by timestamp descending and limit
            activities.sort(key=lambda x: x["timestamp"], reverse=True)
            return activities[:limit]

    def get_funnel_data(self) -> Dict[str, Any]:
        """
        Get participation funnel numbers.

        Returns:
            Dictionary with funnel metrics (intake → CEO → Tech → Staff)
        """
        with self._lock:
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Count unique organizations
            intake_count = len(
                {
                    row.get("Organization Name:", "").strip()
                    for row in intake_data
                    if row.get("Organization Name:", "").strip()
                }
            )

            ceo_count = len(
                {
                    row.get("CEO Organization", "").strip()
                    for row in ceo_data
                    if row.get("CEO Organization", "").strip()
                }
            )

            tech_count = len(
                {
                    row.get("Organization", "").strip()
                    for row in tech_data
                    if row.get("Organization", "").strip()
                }
            )

            staff_count = len(
                {
                    row.get("Organization", "").strip()
                    for row in staff_data
                    if row.get("Organization", "").strip()
                }
            )

            return {
                "intake": intake_count,
                "ceo": ceo_count,
                "tech": tech_count,
                "staf": staff_count,
                "ceo_percent": (
                    round(100.0 * ceo_count / intake_count, 1) if intake_count > 0 else 0
                ),
                "tech_percent": (
                    round(100.0 * tech_count / intake_count, 1) if intake_count > 0 else 0
                ),
                "staff_percent": (
                    round(100.0 * staff_count / intake_count, 1) if intake_count > 0 else 0
                ),
            }

    def get_stats(self) -> Dict[str, Any]:
        """
        Get basic statistics about loaded data including response rates.

        Returns:
            Dictionary with tab statistics and metadata
        """
        with self._lock:
            all_data = self._data_service.get_all_data()
            metadata = all_data.get("_metadata", {})

            tabs_stats = []
            for tab_name in SheetsReader.TABS.keys():
                row_count = self._data_service.get_row_count(tab_name)
                tabs_stats.append(
                    {
                        "tab_name": tab_name,
                        "row_count": row_count,
                        "last_extract": metadata.get("last_fetch", ""),
                    }
                )

            # Include response rates from master list
            try:
                response_rates = self.get_response_rates()
            except Exception as e:
                print(f"Error calculating response rates: {e}")
                response_rates = None

            stats = {
                "tabs": tabs_stats,
                "total_rows": metadata.get("total_rows", 0),
                "last_fetch": metadata.get("last_fetch", ""),
                "spreadsheet_id": metadata.get("spreadsheet_id", ""),
            }

            if response_rates:
                stats["response_rates"] = response_rates

            return stats

    def get_organizations_summary(self) -> List[Dict[str, Any]]:
        """
        Get detailed organization data from master list with intake information.

        Shows ALL organizations from OrgMaster list with their response status.

        Email Resolution:
        - Uses email from Intake sheet if organization has responded
        - Falls back to email from OrgMaster sheet if organization hasn't responded
        - Provides maximum email coverage for all organizations

        Returns:
            List of organization summary dictionaries
        """
        with self._lock:
            org_master = self._data_service.get_tab_data("OrgMaster")
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Create lookup dictionaries for intake data
            intake_lookup = {}
            for row in intake_data:
                org_name = row.get("Organization Name:", "").strip()
                if org_name:
                    intake_lookup[org_name] = row

            # Create lookup sets for survey responses
            ceo_orgs = {
                row.get("CEO Organization", "").strip()
                for row in ceo_data
                if row.get("CEO Organization", "").strip()
            }
            tech_orgs = {
                row.get("Organization", "").strip()
                for row in tech_data
                if row.get("Organization", "").strip()
            }
            staff_orgs = {
                row.get("Organization", "").strip()
                for row in staff_data
                if row.get("Organization", "").strip()
            }

            organizations = []

            # Iterate through ALL organizations in master list
            for row in org_master:
                org_name = row.get("Organization", "").strip()
                if not org_name:
                    continue

                # Check if this org submitted intake
                intake_record = intake_lookup.get(org_name)
                has_intake = intake_record is not None

                # Check survey completions
                has_ceo = org_name in ceo_orgs
                has_tech = org_name in tech_orgs
                has_staff = org_name in staff_orgs

                # Determine overall status
                if not has_intake:
                    status = "No Response"
                elif has_ceo and has_tech and has_staff:
                    status = "Complete"
                elif has_ceo or has_tech or has_staff:
                    status = "In Progress"
                else:
                    status = "Intake Only"

                # Determine email: use intake email if available, otherwise use OrgMaster email
                email = ""
                if intake_record and intake_record.get("Email", "").strip():
                    email = intake_record.get("Email", "").strip()
                else:
                    # Use email from OrgMaster for organizations that haven't responded
                    email = row.get("Email", "").strip()

                organizations.append(
                    {
                        "organization": org_name,
                        "email": email,
                        "submitted_date": (
                            self._format_date(intake_record.get("Date", ""))
                            if intake_record
                            else "Not Submitted"
                        ),
                        "status": status,
                        "has_intake": has_intake,
                        "ceo_complete": has_ceo,
                        "tech_complete": has_tech,
                        "staff_complete": has_staff,
                    }
                )

            # Sort: Responded first (by date), then not responded (alphabetically)
            organizations.sort(
                key=lambda x: (
                    not x["has_intake"],  # Not responded goes to bottom
                    (
                        x["submitted_date"] if x["has_intake"] else x["organization"]
                    ),  # Date for responded, name for not
                )
            )

            return organizations

    def get_complete_organizations(self) -> List[Dict[str, Any]]:
        """
        Get organizations that have completed all surveys.

        Returns:
            List of organization dictionaries with completion dates
        """
        with self._lock:
            intake_data = self._data_service.get_tab_data("Intake")
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Create lookup dictionaries with dates
            ceo_dates = {
                row.get("CEO Organization", "").strip(): self._format_date(row.get("Date", ""))
                for row in ceo_data
                if row.get("CEO Organization", "").strip()
            }
            tech_dates = {
                row.get("Organization", "").strip(): self._format_date(row.get("Date", ""))
                for row in tech_data
                if row.get("Organization", "").strip()
            }
            staff_dates = {
                row.get("Organization", "").strip(): self._format_date(row.get("Date", ""))
                for row in staff_data
                if row.get("Organization", "").strip()
            }

            complete_orgs = []
            for row in intake_data:
                org_name = row.get("Organization Name:", "").strip()
                if not org_name:
                    continue

                # Check if all surveys are complete
                if org_name in ceo_dates and org_name in tech_dates and org_name in staff_dates:
                    complete_orgs.append(
                        {
                            "organization": org_name,
                            "intake_date": self._format_date(row.get("Date", "")),
                            "ceo_date": ceo_dates[org_name],
                            "tech_date": tech_dates[org_name],
                            "staff_date": staff_dates[org_name],
                        }
                    )

            # Sort by organization name
            complete_orgs.sort(key=lambda x: x["organization"])
            return complete_orgs

    def get_organization_detail(self, org_name: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed organization information for organization detail page.

        Args:
            org_name: Name of the organization

        Returns:
            Dictionary with organization detail data including:
            - intake_record: Full intake record dict or None
            - completion_pct: Completion percentage (0-100)
            - completed_surveys: Number of completed surveys (0-3)
            - total_surveys: Total expected surveys (always 3)
            - contacts: List of contact dicts with survey status

            Returns None if organization not found.
        """
        with self._lock:
            # Get intake record for organization
            intake_data = self._data_service.get_tab_data("Intake")
            intake_record = next(
                (r for r in intake_data if r.get("Organization Name:") == org_name), None
            )

            # If no intake record, organization doesn't exist
            if not intake_record:
                return None

            # Get survey data for completion calculation
            ceo_data = self._data_service.get_tab_data("CEO")
            tech_data = self._data_service.get_tab_data("Tech")
            staff_data = self._data_service.get_tab_data("Staff")

            # Check survey completion status
            ceo_complete = any(r.get("CEO Organization") == org_name for r in ceo_data)
            tech_complete = any(r.get("Organization") == org_name for r in tech_data)
            staff_complete = any(r.get("Organization") == org_name for r in staff_data)

            # Calculate completion metrics
            completed_surveys = sum([ceo_complete, tech_complete, staff_complete])
            total_surveys = 3
            completion_pct = int((completed_surveys / total_surveys) * 100)

            # Build contacts list from intake record
            contacts = []

            # CEO contact
            ceo_email = intake_record.get("Email Address")
            if ceo_email:
                contacts.append(
                    {
                        "type": "CEO",
                        "role": "CEO",
                        "email": ceo_email,
                        "name": intake_record.get("First Name", "")
                        + " "
                        + intake_record.get("Last Name", ""),
                        "has_survey": ceo_complete,
                    }
                )

            # Tech Lead contact
            tech_email = intake_record.get("Tech Lead Email")
            if tech_email:
                contacts.append(
                    {
                        "type": "Tech Lead",
                        "role": "Technology Lead",
                        "email": tech_email,
                        "name": intake_record.get("Tech Lead Name", "Tech Lead"),
                        "has_survey": tech_complete,
                    }
                )

            # Staff contacts
            staff_email = intake_record.get("Staff Email")
            if staff_email:
                contacts.append(
                    {
                        "type": "Staff",
                        "role": "Staff Member",
                        "email": staff_email,
                        "name": intake_record.get("Staff Name", "Staff"),
                        "has_survey": staff_complete,
                    }
                )

            return {
                "intake_record": intake_record,
                "completion_pct": completion_pct,
                "completed_surveys": completed_surveys,
                "total_surveys": total_surveys,
                "contacts": contacts,
            }

    def get_ceo_summary(self) -> List[Dict[str, Any]]:
        """
        Get detailed CEO survey responses.

        Returns:
            List of CEO response dictionaries with organization, contact info, and key fields
        """
        with self._lock:
            ceo_data = self._data_service.get_tab_data("CEO")

            responses = []
            for row in ceo_data:
                org_name = row.get("CEO Organization", "").strip()
                if not org_name:
                    continue

                # Extract key fields from CEO survey
                name = row.get("Name", "")
                email = row.get("Email", "")
                date = self._format_date(row.get("Date", ""))

                # Get some key responses (adjust field names based on actual data)
                vision = self._truncate_text(row.get("C-1", "") or row.get("Vision", ""), 150)
                challenges = self._truncate_text(
                    row.get("C-2", "") or row.get("Challenges", ""), 150
                )

                responses.append(
                    {
                        "organization": org_name,
                        "name": name,
                        "email": email,
                        "submitted_date": date,
                        "vision": vision,
                        "challenges": challenges,
                    }
                )

            # Sort by date descending
            responses.sort(key=lambda x: x["submitted_date"], reverse=True)
            return responses

    def get_tech_summary(self) -> List[Dict[str, Any]]:
        """
        Get detailed Tech Lead survey responses.

        Returns:
            List of Tech Lead response dictionaries with organization, contact info, and key fields
        """
        with self._lock:
            tech_data = self._data_service.get_tab_data("Tech")

            responses = []
            for row in tech_data:
                org_name = row.get("Organization", "").strip()
                if not org_name:
                    continue

                name = row.get("Name", "")
                email = row.get("Email", "")
                date = self._format_date(row.get("Date", ""))

                # Get key infrastructure responses
                infrastructure = self._truncate_text(
                    row.get("TL-1", "") or row.get("Infrastructure", ""), 150
                )
                tools = self._truncate_text(row.get("TL-2", "") or row.get("Tools", ""), 150)

                responses.append(
                    {
                        "organization": org_name,
                        "name": name,
                        "email": email,
                        "submitted_date": date,
                        "infrastructure": infrastructure,
                        "tools": tools,
                    }
                )

            # Sort by date descending
            responses.sort(key=lambda x: x["submitted_date"], reverse=True)
            return responses

    def get_staff_summary(self) -> List[Dict[str, Any]]:
        """
        Get detailed Staff survey responses.

        Returns:
            List of Staff response dictionaries with organization, contact info, and key fields
        """
        with self._lock:
            staff_data = self._data_service.get_tab_data("Staff")

            responses = []
            for row in staff_data:
                org_name = row.get("Organization", "").strip()
                if not org_name:
                    continue

                name = row.get("Name", "")
                email = row.get("Email", "")
                date = self._format_date(row.get("Date", ""))

                # Get key usage responses
                usage = self._truncate_text(row.get("S-1", "") or row.get("Usage", ""), 150)
                satisfaction = self._truncate_text(
                    row.get("S-2", "") or row.get("Satisfaction", ""), 150
                )

                responses.append(
                    {
                        "organization": org_name,
                        "name": name,
                        "email": email,
                        "submitted_date": date,
                        "usage": usage,
                        "satisfaction": satisfaction,
                    }
                )

            # Sort by date descending
            responses.sort(key=lambda x: x["submitted_date"], reverse=True)
            return responses

    def _format_date(self, date_str: str) -> str:
        """
        Format date string to human-readable format.

        Args:
            date_str: ISO date string or similar

        Returns:
            Formatted date string or 'N/A'
        """
        if not date_str:
            return "N/A"
        try:
            # Try parsing ISO format
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            return dt.strftime("%b %d, %Y")
        except Exception:
            # Return first 10 characters if format is unknown
            return date_str[:10] if len(date_str) >= 10 else date_str

    def _truncate_text(self, text: str, max_length: int = 100) -> str:
        """
        Truncate long text with ellipsis.

        Args:
            text: Text to truncate
            max_length: Maximum length before truncation

        Returns:
            Truncated text with ellipsis if longer than max_length
        """
        if not text:
            return ""
        text = str(text).strip()
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."


# Global singleton instance
_analytics_service_instance = None
_analytics_service_lock = threading.RLock()


def get_analytics_service(data_service=None):
    """
    Get the global AnalyticsService instance (thread-safe singleton).

    Args:
        data_service: DataService instance (required for first call)

    Returns:
        AnalyticsService instance

    Raises:
        ValueError: If data_service not provided on first call
    """
    global _analytics_service_instance

    if _analytics_service_instance is None:
        with _analytics_service_lock:
            if _analytics_service_instance is None:
                if data_service is None:
                    raise ValueError("data_service required for first initialization")
                _analytics_service_instance = AnalyticsService(data_service)

    return _analytics_service_instance


def reset_analytics_service() -> None:
    """
    Reset the global AnalyticsService singleton.

    This function is useful for testing to ensure a fresh instance
    is created for each test that needs it.

    Note:
        This should only be used in test environments.
    """
    global _analytics_service_instance
    with _analytics_service_lock:
        _analytics_service_instance = None
