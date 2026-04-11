CREATE OR REPLACE PROCEDURE insert_or_update(p_username VARCHAR, p_phone VARCHAR) as $$
BEGIN
IF EXISTS(
  SELECT 1 FROM phonebook WHERE username=p_username
) THEN  
    UPDATE phonebook 
    SET  phone=p_phone 
    WHERE username=p_username;
ELSE 
  INSERT INTO phonebook(username,phone) 
  VALUES(p_username,p_phone);
END IF;
END;
$$ LANGUAGE plpgsql;



CREATE or REPLACE PROCEDURE insert_many_users(p_username text[],p_phone text[]) as $$
DECLARE i INT;
BEGIN
FOR i IN 1 .. array_length(p_username,1) LOOP
IF p_phone[i] ~ '^\+?[0-9]{10,15}$' THEN
IF EXISTS(SELECT 1 FROM phonebook WHERE username=p_username[i]) 
  THEN 
  UPDATE phonebook 
  SET phone=p_phone[i] 
  WHERE username=p_username[i];
ELSE 
  INSERT INTO phonebook(username,phone) 
  VALUES(p_username[i],p_phone[i]);
END IF;
ELSE RAISE NOTICE 'Incorrect data: %, %',
                p_username[i], p_phone[i];
END IF;
END LOOP;

END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE PROCEDURE delete_contact(p_value text) as $$
BEGIN
  DELETE FROM phonebook 
    WHERE username=p_value OR phone=p_value;
END;
$$ LANGUAGE plpgsql;