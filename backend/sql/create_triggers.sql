DROP TRIGGER IF EXISTS before_pilot_insert;
CREATE TRIGGER before_pilot_insert
BEFORE INSERT ON pilots
FOR EACH ROW
BEGIN
    -- Check if the mech assigned to the pilot is in the same roster
    SELECT CASE
        WHEN NEW.mech_id IS NOT NULL AND 
             (SELECT roster_id FROM mechs WHERE mech_id = NEW.mech_id) != NEW.roster_id
        THEN
            RAISE(ABORT, 'Pilot and Mech must belong to the same roster')
    END;
END;

DROP TRIGGER IF EXISTS before_pilot_update;
CREATE TRIGGER before_pilot_update
BEFORE UPDATE OF mech_id ON pilots
FOR EACH ROW
BEGIN
    -- Check if the mech assigned to the pilot is in the same roster
    SELECT CASE
        WHEN NEW.mech_id IS NOT NULL AND 
             (SELECT roster_id FROM mechs WHERE mech_id = NEW.mech_id) != NEW.roster_id
        THEN
            RAISE(ABORT, 'Pilot and Mech must belong to the same roster')
    END;
END;

DROP TRIGGER IF EXISTS before_mech_insert;
CREATE TRIGGER before_mech_insert
BEFORE INSERT ON mechs
FOR EACH ROW
BEGIN
    -- Check if the pilot assigned to the mech is in the same roster
    SELECT CASE
        WHEN NEW.mech_pilot_id IS NOT NULL AND 
             (SELECT roster_id FROM pilots WHERE pilot_id = NEW.mech_pilot_id) != NEW.roster_id
        THEN
            RAISE(ABORT, 'Mech and Pilot must belong to the same roster')
    END;
END;

DROP TRIGGER IF EXISTS before_mech_update;
CREATE TRIGGER before_mech_update
BEFORE UPDATE OF mech_pilot_id ON mechs
FOR EACH ROW
BEGIN
    -- Check if the pilot assigned to the mech is in the same roster
    SELECT CASE
        WHEN NEW.mech_pilot_id IS NOT NULL AND 
             (SELECT roster_id FROM pilots WHERE pilot_id = NEW.mech_pilot_id) != NEW.roster_id
        THEN
            RAISE(ABORT, 'Mech and Pilot must belong to the same roster')
    END;
END;