# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = [
    "ResearchRetrieveResponse",
    "Profile",
    "ProfileEducation",
    "ProfileEmployment",
    "ProfileHobby",
    "ProfilePersonMetadata",
    "ProfilePersonMetadataCurrentLocation",
    "ProfileProject",
    "ProfileSummary",
    "ProfileWriting",
]


class ProfileEducation(BaseModel):
    degree: Optional[str] = None
    """Degree obtained (e.g., BS, MS, PhD)"""

    description: Optional[str] = None
    """Additional details about the education"""

    end_date: Optional[str] = None
    """End date (YYYY-MM-DD format)"""

    start_date: Optional[str] = None
    """Start date (YYYY-MM-DD format)"""

    university_name: Optional[str] = None
    """Name of the university or institution"""

    urls: Optional[List[str]] = None
    """Related URLs"""


class ProfileEmployment(BaseModel):
    company_name: Optional[str] = None
    """Name of the company"""

    description: Optional[str] = None
    """Description of role and responsibilities"""

    end_date: Optional[str] = None
    """End date (YYYY-MM-DD format), null if current position"""

    job_title: Optional[str] = None
    """Job title or role"""

    start_date: Optional[str] = None
    """Start date (YYYY-MM-DD format)"""

    urls: Optional[List[str]] = None
    """Related URLs (company website, LinkedIn, etc.)"""


class ProfileHobby(BaseModel):
    description: Optional[str] = None
    """Description of the hobby or interest"""

    urls: Optional[List[str]] = None
    """Related URLs (blog, portfolio, etc.)"""


class ProfilePersonMetadataCurrentLocation(BaseModel):
    location: str
    """Location name (e.g., 'Palo Alto, California')"""

    comments: Optional[str] = None
    """Notes or context about the location"""

    urls: Optional[List[str]] = None
    """URLs confirming this location"""


class ProfilePersonMetadata(BaseModel):
    alternate_names: Optional[List[str]] = None
    """List of alternate names, nicknames, or aliases"""

    current_locations: Optional[List[ProfilePersonMetadataCurrentLocation]] = None
    """Current location(s) of the person"""

    full_name: Optional[str] = None
    """Primary full name of the person"""

    profile_urls: Optional[List[str]] = None
    """URLs to online profiles (LinkedIn, Twitter, etc.)"""

    tagline: Optional[str] = None
    """Professional tagline or headline"""


class ProfileProject(BaseModel):
    description: Optional[str] = None
    """Description of the project and achievements"""

    end_date: Optional[str] = None
    """End date (YYYY-MM-DD format)"""

    start_date: Optional[str] = None
    """Start date (YYYY-MM-DD format)"""

    title: Optional[str] = None
    """Title of the project"""

    urls: Optional[List[str]] = None
    """Related URLs (project website, GitHub, etc.)"""


class ProfileSummary(BaseModel):
    text: str
    """Combined summary text"""

    urls: Optional[List[str]] = None
    """Deduplicated URLs supporting the summary"""


class ProfileWriting(BaseModel):
    date: Optional[str] = None
    """Publication date (YYYY-MM-DD format)"""

    description: Optional[str] = None
    """Summary or description of the content"""

    title: Optional[str] = None
    """Title of the writing or publication"""

    urls: Optional[List[str]] = None
    """URLs to the publication"""


class Profile(BaseModel):
    education: Optional[List[ProfileEducation]] = None
    """Education history"""

    employment: Optional[List[ProfileEmployment]] = None
    """Employment history"""

    hobbies: Optional[List[ProfileHobby]] = None
    """Hobbies and personal interests"""

    person_metadata: Optional[ProfilePersonMetadata] = None
    """Metadata about a person"""

    projects: Optional[List[ProfileProject]] = None
    """Projects and achievements"""

    summary: Optional[ProfileSummary] = None
    """Comprehensive summary of the person's profile"""

    writings: Optional[List[ProfileWriting]] = None
    """Writings and publications"""


class ResearchRetrieveResponse(BaseModel):
    id: str
    """Unique identifier for the research job"""

    created_at: str
    """Timestamp when research was created (ISO 8601 format)"""

    query: str
    """Original research query"""

    status: str
    """Status of the research job (RUNNING, COMPLETED, FAILED, FAILED_AMBIGUOUS)"""

    updated_at: str
    """Timestamp when research was last updated (ISO 8601 format)"""

    profile: Optional[Profile] = None
    """Complete profile of a researched person"""
