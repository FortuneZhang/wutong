#encoding=utf-8
s = 'UserVIP=1@CarCode=皖p38035@CarType=货车@CarLong=6.8@CarWeight=10@CarState=高栏@ContactMan=孙经理@ContactTel=15380004949@DriverCode=@Area= @Email=88599707@qq.com@OwnerName=孙经理@OwnerTel=15380004949@Source=中国物通网@ICQ=1@Rank=5@UserName=gyyn'
(pref,after) = s.split('@Email=')
print(pref, after)

info =  {x.split('=')[0]:x.split('=')[1] for x in pref.split('@')  if x != '' }
afterArray = after.split('@')
info['Email'] = afterArray[0] + afterArray[1]


