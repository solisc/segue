BEGIN TRANSACTION;

  DELETE FROM slot WHERE room_id IN (SELECT id FROM room WHERE name = 'PMPA');
  DELETE FROM room WHERE name = 'PMPA';

COMMIT;
