from enum import Enum


class PackageType(Enum):
    GUI_APP = "gui_app"
    CLI = "cli"
    LIBRARY = "library"

class PackageManager(Enum):
    NIX = "nix"
    APT = "apt"
    FLATPAK = "flatpak"
    SNAP = "snap"
    SNAP_CLASSIC = "snap_classic"
    BREW = "brew"

    @staticmethod
    def get_install_command(package_manger: "PackageManager", package: "Package") -> str:
        package_name = package.get_package_name(package_manger)
        match package_manger:
            case PackageManager.NIX:
                return f"nix-env -iA {package_name}"
            case PackageManager.APT:
                return f"apt-get install -y {package_name}"
            case PackageManager.FLATPAK:
                return f"flatpak install -y {package_name}"
            case PackageManager.SNAP:
                return f"snap install {package_name}"
            case PackageManager.SNAP_CLASSIC:
                return f"snap install {package_name} --classic"
            case PackageManager.BREW:
                args = ""
                if isinstance(package, GUIPackage):
                    args += "--cask "
                return f"brew install {args}{package_name}"
            case _:
                raise RuntimeError(f"Provided incorrect manager: {package_manger.name}")

    @staticmethod
    def get_check_command(package_manger: "PackageManager", package: "Package") -> str:
        package_name = package.get_package_name(package_manger)
        match package_manger:
            case PackageManager.NIX:
                return f"nix-env --query --installed | grep {package_name.split('.')[1]}" # This is because pacs are formatted nix.{actual name}
            case PackageManager.APT:
                return f"dpkg -l | grep {package_name}"
            case PackageManager.FLATPAK:
                return f"flatpak list | grep {package_name}"
            case PackageManager.SNAP:
                return f"snap list | grep {package_name}"
            case PackageManager.SNAP_CLASSIC:
                return f"snap list | grep {package_name}"
            case PackageManager.BREW:
                return f"brew list | grep {package_name}"
            case _:
                raise RuntimeError(f"Provided incorrect manager: {package_manger.name}")


class RankedManager:
    package_manager: PackageManager
    ranking: dict[PackageType, int]

    def __init__(self, manager: PackageManager, ranking: dict[PackageType, int]):
        self.package_manager = manager
        self.ranking = ranking

# Package type should have it's own ranking for which manager
# Modules should themselves have a global preference
#

class Package:

    def __init__(self):
        self.package_dict: dict = {}
        self.p_type: PackageType
    
    def which_package_manager(self, ordered_managers: dict[PackageType, list[PackageManager]]) -> PackageManager:
        keys = self.package_dict.keys()
        my_managers = ordered_managers[self.p_type]
        if len(keys) == 1:
            for i in keys:
                return i
        else:
            for r in my_managers:
                if r in keys:
                    return r
            raise RuntimeError(f"No managers available {my_managers} could be found for package {self}")
    
    def get_package_name(self, manager: PackageManager) -> str:
        return self.package_dict[manager]

    def allow_sudo(self):
        return True
    
    def configure(self):
        pass


class GUIPackage(Package):
    p_type = PackageType.GUI_APP

class CLIPackage(Package):
    p_type = PackageType.CLI

class LibraryPackage(Package):
    p_type = PackageType.LIBRARY


