from packagemanagement.type.packages import PackageManager, CLIPackage
from sys import platform
import shutil
import datetime
import pathlib
from logging import getLogger

logger = getLogger(__name__)

class Htop(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.APT : "htop",
            PackageManager.BREW: "htop"
        }

class Bat(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.APT : "bat",
            PackageManager.BREW: "bat"
        }

# Fuzzy find in terminal, https://github.com/junegunn/fzf
class Fzf(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.APT : "fzf",
            PackageManager.BREW: "fzf"
        }

# Better ls, https://github.com/eza-community/eza
class Eza(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.BREW : "eza"
        }

# Better du, https://github.com/bootandy/dust
class DuDust(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.BREW : "dust"
        }

# Better df, https://github.com/muesli/duf
class Duf(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.APT : "duf",
            PackageManager.BREW: "duf"
        }

# Better find, https://github.com/sharkdp/fd
class FdFind(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.APT : "fd-find",
            PackageManager.BREW: "fd"
        }

# Better grep, https://github.com/BurntSushi/ripgrep
class Ripgrep(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.BREW : "ripgrep"
        }

# Better man pages, https://github.com/tldr-pages/tldr
class Tldr(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.BREW : "tlrc"
        }

class Yq(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.SNAP : "yq",
            PackageManager.BREW: "yq"
        }

# https://github.com/sst/opencode, CLI based code editor that is open source
class OpenCode(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.BREW  : "opencode"
        }

class DirEnv(CLIPackage):
    def __init__(self):
        self.package_dict: dict[PackageManager, str] = {
            PackageManager.BREW  : "direnv",
            PackageManager.APT: "direnv"
        }
    
    def configure(self):
        hook = ''
        shell_file = ''
        home = pathlib.Path.home()
        if 'linux' in platform:
            hook = 'eval "$(direnv hook bash)"'
            shell_file = f'{home}/.bashrc'
        elif 'darwin' in platform:
            hook = 'eval "$(direnv hook zsh)"'
            shell_file = f'{home}/.zshrc'
        else:
            raise RuntimeError(f"Config not support for os {platform}")

        with open(shell_file, "r") as f:
            bash_content = f.read()
        
        if hook not in bash_content:
            with open(shell_file, "a+") as f:
                logger.info(f"Configuring {shell_file} for direnv hook.")
                shutil.copy(shell_file, f'{shell_file}_{datetime.datetime.now()}')
                f.write(f'\n{hook}\n')



#!----- Interesting ---------!#
# Easier curl for APIs, # https://github.com/httpie/cli
# https://github.com/Aider-AI/aider
# AWS Stack Mock locally https://github.com/localstack/localstack
# Docker container for any distro, https://github.com/89luca89/distrobox
# Ubuntu VM easy, https://github.com/canonical/multipass
# AI auto tab assistant, https://github.com/TabbyML/tabby
# Create CLI's, https://github.com/spf13/cobra
# Better git diff, https://github.com/dandavison/delta

