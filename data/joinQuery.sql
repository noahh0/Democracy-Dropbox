SELECT
    "Distance from Poll".*,
    "Total Voting".*
FROM
    "Total Voting"
JOIN
    "Distance from Poll"
ON
    "Distance from Poll".geo_id = "Total Voting".geo_id;