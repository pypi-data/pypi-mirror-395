from packagemanagement.type.packages import PackageManager, GUIPackage


class VSCodium(GUIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.NIX : "nixpkgs.vscodium",
            PackageManager.BREW: "vscodium"
        }

# class Lens(Package):
#     package_dict: dict[PackageManager, str] = {
#         PackageManager.NIX : "nixpkgs.lens"
#     }

class Gitkraken(GUIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.FLATPAK : "com.axosoft.GitKraken",
            PackageManager.BREW: "gitkraken"
        }

class IntelliJ(GUIPackage):

    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.FLATPAK : "com.jetbrains.IntelliJ-IDEA-Community",
            PackageManager.BREW: "intellij-idea"
        }


class Ghostty(GUIPackage):

    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.SNAP_CLASSIC : "ghostty",
            PackageManager.BREW: "ghostty"
        }

    def configure():
        # So that when ssh into various nodes, the XTerm is known
        inserted_into_bash = """
        if [[ "$TERM_PROGRAM" == "ghostty" ]]; then
            export TERM=xterm-256color
        fi"""


#!----- Interesting ---------!#
# Remote IDE tool, https://github.com/loft-sh/devpod
# Wordpress for backend admin panels, https://github.com/appsmithorg/appsmith?tab=readme-ov-file
# React framework close to no-code, https://github.com/refinedev/refine
# API Interactive GUI, https://github.com/hoppscotch/hoppscotch

