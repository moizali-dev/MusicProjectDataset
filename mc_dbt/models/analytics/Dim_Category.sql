Select category_id, category, min(created_at) as created_at
from musicprojects_analytics_staging.Stage_Dim_Category 
group by category_id, category
