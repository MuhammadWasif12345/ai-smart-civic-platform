from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import AnalyticsOverview, CategoryDistribution, PriorityDistribution, ResolutionTimeStats
from ..services.statistics_service import StatisticsEngine
from .auth import get_current_admin

# --------------------------------------------------------------------------------
# ANALYTICS ROUTER
# These endpoints provide the data needed to draw the charts and display the statistics
# on the admin dashboard. This is the core of the Batch 4 project requirement.
# Every endpoint requires an admin login.
# --------------------------------------------------------------------------------

router = APIRouter()

@router.get("/overview", response_model=AnalyticsOverview, dependencies=[Depends(get_current_admin)])
def get_overview(db: Session = Depends(get_db)):
    """
    Returns the top-level numbers for the dashboard's summary cards.
    """
    return StatisticsEngine.get_overview_stats(db)

@router.get("/distribution/category", response_model=List[CategoryDistribution], dependencies=[Depends(get_current_admin)])
def get_category_distribution(db: Session = Depends(get_db)):
    """
    Returns data for a pie/donut chart showing how many complaints fall into each category.
    """
    return StatisticsEngine.get_category_distribution(db)

@router.get("/distribution/priority", response_model=List[PriorityDistribution], dependencies=[Depends(get_current_admin)])
def get_priority_distribution(db: Session = Depends(get_db)):
    """
    Returns data for a bar chart showing the breakdown of priorities.
    """
    return StatisticsEngine.get_priority_distribution(db)

@router.get("/resolution-time", response_model=ResolutionTimeStats, dependencies=[Depends(get_current_admin)])
def get_resolution_time(db: Session = Depends(get_db)):
    """
    The main Batch 4 statistics endpoint. Returns central tendency (mean, median), 
    spread (variance, std dev), and quartiles for resolution times, along with 
    a plain-English interpretation.
    """
    return StatisticsEngine.get_resolution_time_stats(db)

@router.get("/public")
def get_public_analytics(db: Session = Depends(get_db)):
    """
    Publicly accessible endpoint for the homepage.
    Aggregates data safely for public display on the dynamic charts.
    """
    return {
        "categories": StatisticsEngine.get_category_distribution(db),
        "priorities": StatisticsEngine.get_priority_distribution(db),
        "resolution": StatisticsEngine.get_resolution_time_stats(db)
    }

