import resource
print(resource.getrlimit(resource.RLIMIT_AS))
resource.setrlimit(resource.RLIMIT_AS, (100,100))
print(resource.getrlimit(resource.RLIMIT_AS))
import pandas as pd