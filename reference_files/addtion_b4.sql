UPDATE canal_status SET `on`=0;
COMMIT;

# need move .z2

UPDATE `user` SET email1 = TRIM(LEFT(email1,LENGTH(email1)-3)) WHERE email1 LIKE "%.z2";
UPDATE `user` SET email2 = TRIM(LEFT(email2,LENGTH(email2)-3)) WHERE email2 LIKE "%.z2";
UPDATE `user` SET email3 = TRIM(LEFT(email3,LENGTH(email3)-3)) WHERE email3 LIKE "%.z2";
UPDATE company_contact set email = TRIM(LEFT(email,LENGTH(email)-3)) WHERE email LIKE "%.z2";
UPDATE email_hold_list set email = TRIM(LEFT(email,LENGTH(email)-3)) WHERE email LIKE "%.z2";
UPDATE email_list set email = TRIM(LEFT(email,LENGTH(email)-3)) WHERE email LIKE "%.z2";
COMMIT;
