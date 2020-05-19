update gateway set login = null,password = null,testMode = 1,trialMode = 1;

update organization_bio set orgCode = DATABASE(),email = 'info@z2systems.com' ,contactEmail = 'info@z2systems.com';

update system_settings set value = '1' where name = 'fakeEmailRecipient';

update account set loginPassword = 'DesGp43VxrlZhXAhTIaG6A==' where id = 1;
commit;

