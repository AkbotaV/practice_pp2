CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR)  
AS $$ 
BEGIN
RETURN QUERY
SELECT c.id, c.username, c.phone 
FROM phonebook c 
WHERE c.username ILIKE '%' || p ||'%' 
or c.phone ILIKE '%'|| p ||'%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT,p_offset INT) 
RETURNS TABLE(id INT, username VARCHAR, phone VARCHAR) as $$

BEGIN
RETURN QUERY
SELECT  p.id, p.username, p.phone FROM phonebook p ORDER BY p.id LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;