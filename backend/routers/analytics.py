from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import AnalyticsOverview, CategoryDistribution, PriorityDistribution, ResolutionTimeStats
from ..services.statistics_service import StatisticsEngine
from .auth import get_current_user, require_role

# --------------------------------------------------------------------------------
# ANALYTICS ROUTER
# These endpoints provide the data needed to draw the charts and display the statistics
# on the admin dashboard. This is the core of the Batch 4 project requirement.
# Every endpoint requires an admin login.
# --------------------------------------------------------------------------------

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverview, dependencies=[Depends(require_role(["SUPER_ADMIN", "MUNICIPAL_ADMIN", "SUPERVISOR"]))])
def get_overview(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Returns the top-level numbers for the dashboard's summary cards.
    """
    dept = user.department if user.role == "SUPERVISOR" else None
    return StatisticsEngine.get_overview_stats(db, dept)

@router.get("/distribution/category", response_model=List[CategoryDistribution], dependencies=[Depends(require_role(["SUPER_ADMIN", "MUNICIPAL_ADMIN", "SUPERVISOR"]))])
def get_category_distribution(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Returns data for a pie/donut chart showing how many complaints fall into each category.
    """
    dept = user.department if user.role == "SUPERVISOR" else None
    return StatisticsEngine.get_category_distribution(db, dept)

@router.get("/distribution/priority", response_model=List[PriorityDistribution], dependencies=[Depends(require_role(["SUPER_ADMIN", "MUNICIPAL_ADMIN", "SUPERVISOR"]))])
def get_priority_distribution(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    Returns data for a bar chart showing the breakdown of priorities.
    """
    dept = user.department if user.role == "SUPERVISOR" else None
    return StatisticsEngine.get_priority_distribution(db, dept)

@router.get("/resolution-time", response_model=ResolutionTimeStats, dependencies=[Depends(require_role(["SUPER_ADMIN", "MUNICIPAL_ADMIN", "SUPERVISOR"]))])
def get_resolution_time(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """
    The main Batch 4 statistics endpoint. Returns central tendency (mean, median), 
    spread (variance, std dev), and quartiles for resolution times, along with 
    a plain-English interpretation.
    """
    dept = user.department if user.role == "SUPERVISOR" else None
    return StatisticsEngine.get_resolution_time_stats(db, dept)

@router.get("/public")
def get_public_analytics(db: Session = Depends(get_db)):
    """
    Publicly accessible endpoint for the homepage.
    Aggregates data safely for public display on the dynamic charts.
    """
    return {
        "overview": StatisticsEngine.get_overview_stats(db),
        "categories": StatisticsEngine.get_category_distribution(db),
        "priorities": StatisticsEngine.get_priority_distribution(db),
        "resolution": StatisticsEngine.get_resolution_time_stats(db)
    }

