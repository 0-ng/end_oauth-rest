"""
@FileName   : Config.py
@Author     : Chen Wang
@Version    : Python3.8 、Windows or Linux
@Description: 相关配置文件数据库和后端session、密钥、email设置等
@Time       : 2020/1/28 18:37
@Software   : PyCharm
@Contact    : 1416825008@qq.com
@Github     : https://github.com/JackMin1314/Python_Study
@Gitee      : https://gitee.com/JackMin1314/Python_Study
代 码 仅 限 学 习 ，严 禁 商 业 用 途，转 载 请 注 明 出 处~

"""
# import lib
from datetime import timedelta
# MySQL数据库名称
mysql_base = 'spider'
# MySQL数据库中表名称
mysql_table = 'userinfo'
# 下面是docker使用时候的配置
mysql_host = 'spider-mysql'
# MySQL数据库root对应的密码
mysql_passwd = '5201020116'
# session 生存时间
session_lifeTime = timedelta(days=3)
# cookie 生存时间(秒)
max_ageTime = 60*60*6    # 6hour
# 生成token的密钥,修改下面的值会导致之前的token不能使用
my_secretKey = "biubiubiu"

# 配置保存mysql数据库的文件、日志文件、用户文件的根目录
db_backup_dir = 'folders'

# 保存用户产生的文件的主文件夹名
user_backup_dir = 'userfiles'

# errlog日志记录配置
# 配置输出日志格式
LOG_FORMAT = "%(asctime)s %(levelname)s %(funcName)s() ==> %(message)s "
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '      # 配置输出时间的格式，
serverlogs_name = 'errlogs.txt'
