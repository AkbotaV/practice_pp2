CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id
    FROM   contacts
    WHERE  username = p_contact_name
    LIMIT  1;
 
    IF v_id IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;
 
    INSERT INTO phones (contact_id, phone, type)
    VALUES (v_id, p_phone, p_type)
    ON CONFLICT (contact_id, phone) DO NOTHING;
 
    RAISE NOTICE 'Phone % (%) added to "%".', p_phone, p_type, p_contact_name;
END;
$$;
 
 


CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql AS $$
DECLARE
    v_group_id INTEGER;
BEGIN
    -- Create group if it does not exist
    INSERT INTO groups (name)
    VALUES (p_group_name)
    ON CONFLICT (name) DO NOTHING;
 
    SELECT id INTO v_group_id
    FROM   groups
    WHERE  name = p_group_name;
 
    UPDATE contacts
    SET    group_id = v_group_id
    WHERE  username = p_contact_name;
 
    IF NOT FOUND THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
    ELSE
        RAISE NOTICE 'Contact "%" moved to group "%".', p_contact_name, p_group_name;
    END IF;
END;
$$;
 
 


CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id       INTEGER,
    username VARCHAR,
    email    VARCHAR,
    birthday DATE,
    grp      VARCHAR,
    phones   TEXT
)
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        g.name AS grp,
        STRING_AGG(p.phone || ' (' || COALESCE(p.type, '?') || ')', ', ') AS phones
    FROM   contacts c
    LEFT JOIN groups g ON g.id = c.group_id
    LEFT JOIN phones p ON p.contact_id = c.id
    WHERE  c.username ILIKE '%' || p_query || '%'
        OR c.email    ILIKE '%' || p_query || '%'
        OR p.phone    ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.username, c.email, c.birthday, g.name
    ORDER BY c.username;
END;
$$;
 

CREATE OR REPLACE FUNCTION get_contacts_page(p_limit INT, p_offset INT)
RETURNS TABLE(
    id INT,
    username VARCHAR,
    email VARCHAR,
    birthday DATE,
    phones TEXT
)
AS $$
BEGIN
    RETURN QUERY
    SELECT
        c.id,
        c.username,
        c.email,
        c.birthday,
        STRING_AGG(p.phone, ', ') AS phones
    FROM contacts c
    LEFT JOIN phones p ON p.contact_id = c.id
    GROUP BY c.id
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;