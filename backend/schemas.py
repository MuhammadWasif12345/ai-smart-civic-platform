from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --------------------------------------------------------------------------------
# PYDANTIC SCHEMAS
# These classes define the exact shape of the data that comes IN to our APIs 
# and goes OUT to the frontend. They automatically validate the data (e.g., 
# making sure a required field isn't missing) and convert it to JSON.
# --------------------------------------------------------------------------------

# 1. CITIZEN SUBMITS A COMPLAINT (INCOMING)
class ComplaintCreate(BaseModel):
    # The citizen's description of the problem. It must be at least 10 characters long,
    # as defined in our error handling requirements, to ensure there's enough detail.
    description: str = Field(..., min_length=10, description="The citizen's complaint text")
    
    # Where the problem is located.
    location: str
    
    # Optional contact info for the citizen to receive updates.
    citizen_contact: Optional[str] = None
    
    # Optional image uploaded by the citizen
    image_base64: Optional[str] = None
    
    # We do NOT include AI fields (category, priority) here because the citizen
    # doesn't provide them — our backend generates those after submission.

# 2. STATUS HISTORY ITEM (OUTGOING)
class StatusHistoryResponse(BaseModel):
    # Represents a single change in the complaint's history
    old_status: str
    new_status: str
    changed_at: datetime
    changed_by: str

    # ConfigDict(from_attributes=True) is the modern Pydantic v2 equivalent of orm_mode=True.
    # It tells Pydantic to read data directly from our SQLAlchemy database objects.
    model_config = {"from_attributes": True}

# 3. COMPLAINT DETAILS (OUTGOING)
# This is what the API sends back to the frontend (citizen tracking or admin dashboard)
class ComplaintResponse(BaseModel):
    complaint_id: str
    description: str
    category: str
    priority: str
    ai_summary: Optional[str]
    ai_confidence: Optional[float]
    location: str
    image_path: Optional[str]
    status: str
    assigned_department: Optional[str]
    citizen_contact: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    # A list of history records, letting the frontend build a timeline of events
    history: List[StatusHistoryResponse] = []

    model_config = {"from_attributes": True}

# 4. PAGINATED COMPLAINTS LIST (OUTGOING)
# Used by the admin dashboard table to show many complaints at once
class PaginatedComplaints(BaseModel):
    total: int
    complaints: List[ComplaintResponse]

# 5. ADMIN UPDATES STATUS (INCOMING)
class StatusUpdate(BaseModel):
    # The new state to transition the complaint into (e.g., "In Progress")
    new_status: str
    
    # Who is making the change (used for the audit log)
    changed_by: str

# 6. ADMIN ASSIGNS DEPARTMENT (INCOMING)
class AssignDepartment(BaseModel):
    # The name of the department taking over (e.g., "Water Department")
    department: str

# 7. ADMIN LOGIN (INCOMING)
class AdminLogin(BaseModel):
    username: str
    password: str

# 8. JWT TOKEN RESPONSE (OUTGOING)
class Token(BaseModel):
    # The actual encrypted JWT string
    access_token: str
    
    # Always "bearer" for standard JWT flows
    token_type: str

# --------------------------------------------------------------------------------
# ANALYTICS RESPONSES
# --------------------------------------------------------------------------------

class ResolutionTimeStats(BaseModel):
    mean_hours: float
    median_hours: float
    mode_hours: float
    std_dev_hours: float
    variance: float
    min_hours: float
    max_hours: float
    range_hours: float
    q1_hours: float
    q3_hours: float
    iqr_hours: float
    # A plain-English explanation of what these numbers mean
    interpretation: str

class CategoryDistribution(BaseModel):
    category: str
    count: int
    percentage: float

class PriorityDistribution(BaseModel):
    priority: str
    count: int

class TrendData(BaseModel):
    date: str
    count: int

class AnalyticsOverview(BaseModel):
    total_complaints: int
    open_complaints: int
    critical_priority: int
    resolved_this_week: int

# --------------------------------------------------------------------------------
# CHATBOT SCHEMAS
# --------------------------------------------------------------------------------

class ChatMessage(BaseModel):
    role: str # "user" or "model"
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class ChatResponse(BaseModel):
    reply: str

