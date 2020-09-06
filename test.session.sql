SELECT t1.name,
    t2.type,
    t1.year
FROM Building t1
    LEFT JOIN Type t2 ON (t2.id = t1.type_id) WHERE t1.type_id = 1