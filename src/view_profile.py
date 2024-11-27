import pstats
from pstats import SortKey


p = pstats.Stats('profile')
p.strip_dirs().sort_stats(-1).print_stats()
p.sort_stats(SortKey.TIME).print_stats(10)
