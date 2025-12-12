"""
* `Organization`:  InsightSolver Solutions Inc.
* `Project Name`:  InsightSolver
* `Module Name`:   insightsolver
* `File Name`:     __init__.py
* `Author`:        Noé Aubin-Cadot
* `Email`:         noe.aubin-cadot@insightsolver.com

Description
-----------
The Python module `insightsolver` is an API client of the InsightSolver SaaS which is designed to generate advanced rule mining and data insights.

License
-------
Exclusive Use License - see `LICENSE <license.html>`_ for details.

----------------------------

"""

# Import the version of the module
from .version import __version__

__all__ = [
	"InsightSolver",
	"get_credits_available",
]

def __getattr__(name):
	"""
	Deferred imports to avoid triggering dependencies during the pip install.
	Without it, the pip install tries to import Pandas earlier than it is installed.
	"""
	if name == "InsightSolver":
		from .insightsolver import InsightSolver
		return InsightSolver
	elif name == "get_credits_available":
		from .insightsolver import get_credits_available
		return get_credits_available
	raise AttributeError(f"module {__name__} has no attribute {name}")