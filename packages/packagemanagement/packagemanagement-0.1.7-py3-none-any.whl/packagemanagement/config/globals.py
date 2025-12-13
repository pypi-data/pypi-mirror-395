from packagemanagement.type.packages import PackageType, PackageManager

# _cli_rankings: list[RankedManager] = []
# _gui_rankings: list[RankedManager] = []
# _library_rankings: list[RankedManager] = []
#

# def get_ranked_managers(package_type: PackageType) -> list[RankedManager]:
#     rankings = []
#     match package_type:
#         case PackageType.CLI:
#             rankings = _cli_rankings
#         case PackageType.GUI_APP:
#             rankings = _gui_rankings
#         case PackageType.LIBRARY:
#             rankings = _library_rankings
#         case _:
#             raise RuntimeError(f"Didn't expect: {package_type}")
#     if len(rankings) == 0:
#         raise RuntimeError(f"For type {package_type}, there is no ranked managers.")
#     return rankings


# def _sorted_criteria_primary(package_type: PackageType, package_managers: set[RankedManager], allow_unranked: bool) -> list[RankedManager]:
#     has_ranking = []
#     no_ranking = []
#     # O(n)
#     for k in package_managers:
#         if package_type in k.ranking.keys():
#             has_ranking.append(k)
#         else:
#             no_ranking.append(k)
#
#     if not allow_unranked and len(no_ranking) > 0:
#         raise RuntimeError(f"The following have not been ranked for type {package_type}: {no_ranking}")
#
#     # On(logN)
#     has_ranking = sorted(has_ranking, key=lambda e: e.ranking[package_type]) # Numerical
#     no_ranking = sorted(no_ranking, key=lambda e: e.package_manager.name) # Alphabetical, requires sorting of unranked for expected behavior
#     return has_ranking + no_ranking
#
#
# def set_ranked_managers(package_managers: set[RankedManager], allow_unranked: bool):
#     global _cli_rankings
#     global _gui_rankings
#     global _library_rankings
#     _cli_rankings = _sorted_criteria_primary(package_type=PackageType.CLI, package_managers=package_managers, allow_unranked=allow_unranked)
#     _gui_rankings = _sorted_criteria_primary(package_type=PackageType.GUI_APP, package_managers=package_managers, allow_unranked=allow_unranked)
#     _library_rankings = _sorted_criteria_primary(package_type=PackageType.LIBRARY, package_managers=package_managers, allow_unranked=allow_unranked)
#

import logging
logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

_ordered_managers: dict[PackageType, list[PackageManager]] = {}
def set_ordered_managers(ordered_managers: dict[PackageType, list[PackageManager]]):
    global _ordered_managers
    for pt in PackageType:
        if pt not in ordered_managers.keys():
            raise KeyError(f"There is no entry for package type: {pt}. Your ordered managers are {ordered_managers}")
    _ordered_managers = ordered_managers

def get_ordered_managers() -> dict[PackageType, list[PackageManager]]:
    global _ordered_managers
    return _ordered_managers



