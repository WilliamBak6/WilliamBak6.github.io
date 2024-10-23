import os as os
import sys 
from pip import main   

package_requirement = [
    'seaborn',
    'requests',
    'pandas',
    'scrapy',
    'mysql-connector-python',
    'mysqlclient',
    'apache-airflow',
    'python-dotenv'

]

# type(sys.path)
# for path in sys.path:
#     print(sys.path)

[x for x in package_requirement if main(['install', x])]