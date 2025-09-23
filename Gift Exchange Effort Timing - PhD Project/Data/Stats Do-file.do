scatter effort wage
bysort wage: egen avg_effort_level = mean(effort)
scatter avg_effort_level wage
