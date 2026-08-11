from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime

# --------------------------------------------------------------------------------
# PYDANTIC SCHEMAS
# These classes define the exact shape of the data that comes IN to our APIs 
# and goes OUT to the frontend.
# --------------------------------------------------------------------------------

# 1. CITIZEN SUBMITS A COMPLAINT (INCOMING)
class ComplaintCreate(BaseModel):
    description: str = Field(..., min_length=10, description="The citizen's complaint text")
    location: str
    citizen_contact: Optional[str] = None
    image_base64: Optional[str] = None

# 2. STATUS HISTORY ITEM (OUTGOING)
class StatusHistoryResponse(BaseModel):
    old_status: str
    new_status: str
    changed_at: datetime
    changed_by: str

    model_config = {"from_attributes": True}

# 3. COMPLAINT DETAILS (OUTGOING)
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
    assigned_to: Optional[str]
    citizen_contact: Optional[str]
    created_at: datetime
    resolved_at: Optional[datetime]
    
    history: List[StatusHistoryResponse] = []

    model_config = {"from_attributes": True}

# 4. PAGINATED COMPLAINTS LIST (OUTGOING)
class PaginatedComplaints(BaseModel):
    total: int
    complaints: List[ComplaintResponse]

# 5. ADMIN UPDATES STATUS (INCOMING)
class StatusUpdate(BaseModel):
    new_status: str
    changed_by: str
    note: Optional[str] = None # Field Officers might add a note

# 6. ADMIN ASSIGNS COMPLAINT (INCOMING)
class AssignComplaint(BaseModel):
    department: Optional[str] = None
    assigned_to: Optional[str] = None

# 7. USER LOGIN (INCOMING)
class UserLogin(BaseModel):
    username: str
    password: str

# 8. JWT TOKEN RESPONSE (OUTGOING)
class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    department: Optional[str] = None

# 9. USER RESPONSE (OUTGOING)
class UserResponse(BaseModel):
    id: str
    username: str
    role: str
    department: Optional[str] = None
    created_at: datetime
    
    model_config = {"from_attributes": True}

# 10. AUDIT LOG (OUTGOING)
class AuditLogResponse(BaseModel):
    id: str
    timestamp: datetime
    user: str
    role: str
    action: str
    resource: Optional[str] = None
    resource_id: Optional[str] = None
    old_value: Optional[str] = None
    new_value: Optional[str] = None
    
    model_config = {"from_attributes": True}

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
