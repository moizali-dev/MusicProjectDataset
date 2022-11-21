select category_id , category, min(created_at) as created_at
from musicprojects.musicprojects_staging.{{ set_table() }}
where category_id is not null and category is not null
group by category_id , category