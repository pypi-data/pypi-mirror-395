#!/bin/sh -eu

# path to this script, eg '/usr/local/src/procustodibus-agent-1.0.0/install.sh'
install_script="$(readlink -f "$0")"
# path to /usr/local directory or equivalent
usr_local=${USR_LOCAL:-$(
    test -d /opt/homebrew && echo /opt/homebrew || echo /usr/local
)}
# path to agent source, eg '/usr/local/src/procustodibus-agent-1.0.0'
agent_src="${INSTALL_SRC:-$(dirname "$install_script")}"
# path to agent config directory, eg '/etc/wireguard'
cnf_dir="${INSTALL_CNF:-$(
    test -d $usr_local/etc/wireguard -a ! -d /etc/wireguard \
    && echo $usr_local/etc/wireguard \
    || echo /etc/wireguard
)}"
# path to installer log file
log_file="${INSTALL_LOG:-/var/log/procustodibus-install.log}"
# path to python executable
python_bin="${INSTALL_PYTHON:-python3}"
# path to Software Collections python 3.8 executable
python_scl_bin=/opt/rh/rh-python38/root/usr/bin/python3
# minimum required python version number
python_minimum_version="3.6"
# python packages required to create virtualenv
python_venv_packages="ensurepip venv"
# path to agent virtualenv
venv_path="${INSTALL_VENV:-/opt/venvs/procustodibus-agent}"
# path to install extra scripts for WireGuard pre/post/up/down
scripts_path="${INSTALL_SCRIPTS:-/usr/local/lib/procustodibus/agent/scripts}"
# base url for pro custodibus webapp
app_url=https://pro.custodib.us
# base url for pro custodibus documentation
doc_url=https://docs.procustodibus.com
# base url for RHEL EPEL RPM package download
epel_dl_url=https://dl.fedoraproject.org/pub/epel/epel-release-latest

# user-selected action: "help", "install", "remove", or "version"
action=help
# "yes" for dryrun (read-only) mode; else ""
dryrun=""
# "yes" for force (yes-to-all) mode; else ""
force=""
# "yes" if daemon restart required
requires_restart=""

while [ $# -gt 0 ]; do
    case $1 in
        --checkfns) dryrun=yes; force=yes; action=checkfns ;;
        -d|--dryrun)
            dryrun=yes
            force=yes
            test $action != help || action=install
            ;;
        -f|--force) force=yes ;;
        -h|--help) action=help ;;
        -i|--install) action=install ;;
        -r|--remove) action=remove ;;
        -v|--version) action=version ;;
    esac
    shift
done

# Outputs help text.
do_help() {
    local agent_src="$(dirname "$install_script")"
    cat << EOF
Pro Custodibus Agent installer.

Installs the Pro Custodibus Agent as a daemon in a python virtualenv.

Usage:
  install.sh --help
  install.sh --dryrun [--install | --remove]
  install.sh --install [--force]
  install.sh --remove [--force]
  install.sh --version

Options:
  -h --help     Show this help
  -d --dryrun   Run all installer checks without installing/removing anything
  -f --force    Automatically answer yes to all prompts
  -i --install  Install the agent
  -r --remove   Remove the agent
  -v --version  Show version number

Environment variables:
  INSTALL_CNF       Path to agent config directory ('$cnf_dir')
  INSTALL_LOG       Path to installer log ('/var/log/procustodibus-install.log')
  INSTALL_PYTHON    Path to python executable ('python3')
  INSTALL_SCRIPTS   Path to extra scripts ('/usr/local/lib/procustodibus/agent/scripts')
  INSTALL_SRC       Path to agent source code ('$agent_src')
  INSTALL_VENV      Path to agent virtualenv ('/opt/venvs/procustodibus-agent')
  USR_LOCAL         Path to /usr/local directory or equivalent
EOF
}

# Outputs agent version found in agent source, or "unknown-version".
#
# Examples
#
#   > get_agent_version
#   1.0.0
get_agent_version() {
    local version_file="$agent_src/PKG-INFO"
    local version_from_directory="$(
        echo "$(basename "$agent_src")" |
            sed -n 's/^procustodibus.agent.\([0-9].*\)/\1/p'
    )"
    if [ -f "$version_file" ]; then
        awk '$1=="Version:" { print $2 }' "$version_file"
    elif [ "$version_from_directory" ]; then
        echo "$version_from_directory"
    else
        echo unknown-version
    fi
}

# Outputs installer version string.
#
# Examples
#
#   > do_version
#   procustodibus-agent/install 1.0.0
do_version() {
    echo "procustodibus-agent/install $(get_agent_version)"
}

# Outputs agent version installed in virtualenv, or blank.
#
# Examples
#
#   > get_installed_agent_version
#   1.0.0
get_installed_agent_version() {
    if [ -f "$venv_path/bin/activate" ]; then
        . "$venv_path/bin/activate"
        pip list 2>/dev/null |
        awk '/procustodibus.agent/ { gsub(/[()]/, ""); print $2 }'
    else
        echo ""
    fi
}

# Outputs greatest version string from specified arguments.
#
# $* - Version strings.
#
# Examples
#
#   > calc_greater_version 1.23 12.3 1.2.3 1 12
#   12.3
calc_greater_version() {
    echo $* | tr ' ' '\n' | sort -V | tail -n1
}

# Logs specified arguments to log at info level.
#
# Also echos arguments to stdout.
#
# $* - Text to log.
#
# Examples
#
#   > log_info oh no!
#   oh no!
log_info() {
    echo "$*"
    log "$*"
}

# Logs specified arguments to log at warn level (eg a fixable problem).
#
# Also echos arguments to stderr.
#
# $* - Text to log.
#
# Examples
#
#   > log_warn oh no!
#   WARNING oh no!
log_warn() {
    echo "WARNING $*" 1>&2
    log "WARNING $*"
}

# Logs specified arguments to log at error level (eg a non-fixable problem).
#
# Also echos arguments to stderr.
#
# $* - Text to log.
#
# Examples
#
#   > log_error oh no!
#   ERROR oh no!
log_error() {
    echo "ERROR $*" 1>&2
    log "ERROR $*"
}

# Logs specified arguments to log (without echoing to stdout or stderr).
#
# Skips logging in "dryrun" mode.
#
# $* - Text to log.
#
# Examples
#
#   > log oh no!
log() {
    test ! "$dryrun" || return 0
    touch "$log_file"
    echo "$(date) $*" >> "$log_file"
}

# Continues to prompt user until she enters one of the options specified.
#
# Outputs the selected option (both to stdout and to the log). When in "force"
# mode, omits the prompt and automatically selects the first option.
#
# $1 - Prompt text.
# $* - Options.
#
# Examples
#
#   > prompt "do the thing?" yes no maybe
#   do the thing? ([y]es, [n]o, [m]aybe): _
#
# In the above example, if the user enters "y", "yes" would be output.
prompt() {
    local prompt options formatted_options selection
    prompt="$1"; shift
    log "$prompt"

    if [ "$force" ]; then
        selection=$1
        log "FORCED $selection"
    else
        options=" $* "
        formatted_options=$(echo "$*" | sed 's/^\([[:alnum:]]\)/[\1]/;s/ \([[:alnum:]]\)/, [\1]/g')
        selection=""

        while [ ! "$selection" -o "${options##* $selection*}" = "$options" ]; do
            read -p "$prompt ($formatted_options): " selection
            log "picked $selection"
        done
    fi

    echo $selection
}

# Exits with the specified code and log message.
#
# Also echos message to stdout.
#
# $1 - Exit code.
# $* - Text to log.
#
# Examples
#
#   > bye 1 oh no!
#   oh no!
bye() {
    local code=$1; shift
    log_info $*
    exit $code
}

# Outputs path to executable if specified executable is available on $PATH,
# or blank.
#
# $1 - Executable.
#
# Examples
#
#   > whichis python3
#   /usr/bin/python3
whichis() {
    command -v "$1" || true
}

# Outputs first executable from specified arguments that is available on $PATH,
# or blank.
#
# $@ - Executables.
#
# Examples
#
#   > whichof apk apt-get dnf pacman yum zypper
#   apt-get
whichof() {
    for option in "$@"; do
        if [ "$(whichis $option)" ]; then
            echo $option
            return 0
        fi
    done
}

get_regular_user_name() {
    ls -l $install_script | awk '{ print $3 }'
}

# Exits if not running as root user (unless in "dryrun" mode).
#
# Logs message indicating whether or not running as root.
#
# Examples
#
#   > require_root
#   running as root
require_root() {
    if [ $(id -u) -eq 0 ]; then
        log_info "running as root"
    else
        if [ "$dryrun" ]; then
            log_warn "not running as root: dryrun may be inaccurate"
        else
            log_error "must run as root"
            bye 1 FAIL
        fi
    fi
}

# Exits if configuration files are not present (unless in "dryrun" mode).
#
# Logs message indicating whether or not configuration was found.
#
# Examples
#
#   > require_cnf
#   agent configuration found at /etc/wireguard/procustodibus.conf
#   agent setup found at /etc/wireguard/procustodibus-setup.conf
require_cnf() {
    local base_path=$cnf_dir/procustodibus
    if [ -f $base_path.conf ]; then
        log_info "agent configuration found at $base_path.conf"
    else
        log_error "agent configuration not found at $base_path.conf"
        log_info $(echo "
            please download procustodibus.conf and procustodibus-setup.conf
            from the host's setup page on $app_url/, and then re-run this
            script; see $doc_url/guide/agents/install/ for more info
        " | paste -sd' ' -)
        test "$dryrun" || bye 1 FAIL
    fi

    if [ -f $base_path-credentials.conf ]; then
        log_info "agent credentials found at $base_path-credentials.conf"
    elif [ -f $base_path-setup.conf ]; then
        log_info "agent setup found at $base_path-setup.conf"
    else
        log_error "agent credentials not found"
        log_info $(echo "
            please download procustodibus-setup.conf from the host's setup page
            on $app_url/, and then re-run this script; see
            $doc_url/guide/agents/install/ for more info
        " | paste -sd' ' -)
        test "$dryrun" || bye 1 FAIL
    fi
}

# Sets the specified file's mode to the specified bits (unless in "dryrun" mode).
#
# Logs message indicating mode was fixed.
#
# $1 - File path.
# $2 - Mode bits.
#
# Examples
#
#   > fix_file_mode /etc/wireguard/procustodibus.conf 640
#   OK will fix mode
#   fixed mode
fix_file_mode() {
    log_info "OK will fix mode"
    test ! "$dryrun" || return 0
    chmod $2 "$1"
    log_info "fixed mode"
}

# Sets the specified file's owner to the specified user (unless in "dryrun" mode).
#
# Logs message indicating owner was fixed.
#
# $1 - File path.
# $2 - User name.
#
# Examples
#
#   > fix_file_mode /etc/wireguard/procustodibus.conf root
#   OK will fix owner
#   fixed owner
fix_file_owner() {
    log_info "OK will fix owner"
    test ! "$dryrun" || return 0
    chown $2 "$1"
    log_info "fixed owner"
}

# Sets the specified file's group to the specified group (unless in "dryrun" mode).
#
# Logs message indicating group was fixed.
#
# $1 - File path.
# $2 - User name.
#
# Examples
#
#   > fix_file_mode /etc/wireguard/procustodibus.conf root
#   OK will fix group
#   fixed group
fix_file_group() {
    log_info "OK will fix group"
    test ! "$dryrun" || return 0
    chgrp $2 "$1"
    log_info "fixed group"
}

# Restores the specified file's default SELinx context label (unless in "dryrun" mode).
#
# Logs message indicating label was fixed.
#
# $1 - File path.
#
# Examples
#
#   > fix_file_label /etc/wireguard/procustodibus.conf
#   OK will fix label
#   fixed label
fix_file_label() {
    log_info "OK will fix label"
    test ! "$dryrun" || return 0
    restorecon -F "$1"
    log_info "fixed label"
}

# Prompts to fix the specified configuration file's mode, group, and owner.
#
# Logs messages indicating the existing state, and any fixes made.
#
# $1 - File path.
# $2 - Expected file mode.
#
# Examples
#
#   > set_cnf_file_permissions /etc/wireguard/procustodibus.conf 644
#   /etc/wireguard/procustodibus.conf mode ok (-rw-r--r--.)
#   /etc/wireguard/procustodibus.conf owner is root
#   /etc/wireguard/procustodibus.conf group is root

#   > set_cnf_file_permissions /etc/wireguard/procustodibus-setup.conf 640
#   WARNING /etc/wireguard/procustodibus-setup.conf mode should be 640
#   fix mode? ([y]es, [n]no): _
#   OK will fix mode
#   fixed mode
#   /etc/wireguard/procustodibus-setup.conf owner is root
#   /etc/wireguard/procustodibus-setup.conf group is root
#   WARNING SELinux Would relabel /etc/wireguard/procustodibus-setup.conf from unconfined_u:object_r:user_home_t:s0 to unconfined_u:object_r:etc_t:s0
#   fix SELinux context label? ([y]es, [n]o): _
#   OK will fix label
#   fixed label
set_cnf_file_permissions() {
    local file_path="$1"
    local expected_mode="$2"
    local mode=$(ls -ln "$file_path" | awk '{ print $1 }')
    local owner=$(ls -ln "$file_path" | awk '{ print $3 }')
    local group=$(ls -ln "$file_path" | awk '{ print $4 }')
    local label=$(ls -Z "$file_path" 2>/dev/null | awk '/^-/ { print $4 } !/^-/ { print $1 }')

    if [ "$expected_mode" = 644 -a ! "${mode##-r?-??-?--*}" ]; then
        log_info "$file_path mode ok ($mode)"
    elif [ "$expected_mode" = 640 -a ! "${mode##-rw-??----*}" ]; then
        log_info "$file_path mode ok ($mode)"
    else
        log_warn "$file_path mode should be $expected_mode"
        case $(prompt "fix mode?" yes no) in
            y*) fix_file_mode "$file_path" $expected_mode ;;
            n*) ;;
        esac
    fi

    if [ "$owner" = 0 ]; then
        log_info "$file_path owner is root"
    else
        log_warn "$file_path owner should be root"
        case $(prompt "fix owner?" yes no) in
            y*) fix_file_owner "$file_path" 0 ;;
            n*) ;;
        esac
    fi

    if [ "$group" = 0 ]; then
        log_info "$file_path group is root"
    else
        log_warn "$file_path group should be root"
        case $(prompt "fix group?" yes no) in
            y*) fix_file_group "$file_path" 0 ;;
            n*) ;;
        esac
    fi

    if [ ! "${label##\?}" ]; then :
    elif [ ! "${label##system_u:object_r:etc_t:s0}" ]; then
        log_info "$file_path SELinux context label ok ($label)"
    elif [ "$(whichis restorecon)" ]; then
        log_warn "SELinux $(restorecon -Fnv "$file_path")"
        case $(prompt "fix SELinux context label?" yes no) in
            y*) fix_file_label "$file_path" ;;
            n*) ;;
        esac
    elif [ "$(uname)" = Linux ]; then
        log_error "$file_path SELinux context label should be system_u:object_r:etc_t:s0"
    fi
}

# Prompts to fix the mode, group, and owner of cnf and credential files.
#
# Logs messages indicating the existing state, and any fixes made.
#
# Examples
#
#   > set_cnf_permissions
#   WARNING /etc/wireguard/procustodibus.conf mode should be 644
#   fix mode? ([y]es, [n]no): _
#   OK will fix mode
#   fixed mode
#   /etc/wireguard/procustodibus.conf owner is root
#   /etc/wireguard/procustodibus.conf group is root
#   WARNING /etc/wireguard/procustodibus-credentials.conf mode should be 640
#   fix mode? ([y]es, [n]no): _
#   OK will fix mode
#   fixed mode
#   /etc/wireguard/procustodibus-credentials.conf owner is root
#   /etc/wireguard/procustodibus-credentials.conf group is root
set_cnf_permissions() {
    local base_path=$cnf_dir/procustodibus

    if [ -f $base_path.conf ]; then
        set_cnf_file_permissions $base_path.conf 644
    fi
    if [ -f $base_path-credentials.conf ]; then
        set_cnf_file_permissions $base_path-credentials.conf 640
    fi
    if [ -f $base_path-setup.conf ]; then
        set_cnf_file_permissions $base_path-setup.conf 640
    fi
}

# Deletes the specified file (unless in "dryrun" mode).
#
# Logs message indicating file was deleted.
#
# $1 - File path.
# $2 - File type.
#
# Examples
#
#   > do_delete_cnf /etc/wireguard/procustodibus.conf configuration
#   OK will delete configuration
#   deleted configuration
do_delete_cnf() {
    log_info "OK will delete $2"
    test ! "$dryrun" || return 0
    rm "$1"
    log_info "deleted $2"
}

# Prompts to delete the cnf and credential files.
#
# Logs messages indicating files that were deleted.
#
# Examples
#
#   > delete_cnf
#   WARNING agent configuration found at /etc/wireguard/procustodibus.conf
#   delete configuration? ([y]es, [n]no): _
#   OK will delete configuration
#   deleted configuration
#   WARNING agent setup found at /etc/wireguard/procustodibus-setup.conf
#   delete setup? ([y]es, [n]no): _
#   OK will delete setup
#   deleted setup
delete_cnf() {
    local base_path=$cnf_dir/procustodibus

    if [ -f $base_path.conf ]; then
        log_warn "agent configuration found at $base_path.conf"
        case $(prompt "delete configuration?" yes no) in
            y*) do_delete_cnf "$base_path.conf" configuration ;;
            n*) ;;
        esac
    else
        log_info "agent configuration not found at $base_path.conf"
    fi

    if [ -f $base_path-credentials.conf ]; then
        log_warn "agent credentials found at $base_path-credentials.conf"
        case $(prompt "delete credentials?" yes no) in
            y*) do_delete_cnf "$base_path-credentials.conf" credentials ;;
            n*) ;;
        esac
    else
        log_info "agent credentials not found at $base_path-credentials.conf"
    fi

    if [ -f $base_path-setup.conf ]; then
        log_warn "agent setup found at $base_path-setup.conf"
        case $(prompt "delete setup?" yes no) in
            y*) do_delete_cnf "$base_path-setup.conf" setup ;;
            n*) ;;
        esac
    else
        log_info "agent setup not found at $base_path-setup.conf"
    fi
}

# Outputs name of package-manager used by system, or blank.
#
# Examples
#
#   > get_package_manager
#   apt-get
get_package_manager() {
    whichof apk apt-get dnf pacman pkg yum zypper brew
}

# Outputs yes if wireguard can be installed via package manager.
#
# Ouputs blank if wireguard cannot be installed.
#
# Examples
#
#   > can_install_wireguard
#   yes
can_install_wireguard() {
    test "$(get_package_manager)" || return 0
    test "$(uname)" = "Linux" || echo "yes"
    test $(calc_greater_version 5.6 $(uname -r)) = "5.6" || echo "yes"
}

# Installs wireguard (unless in "dryrun" mode).
#
# Logs message indicating wireguard was installed.
#
# Examples
#
#   > do_install_wireguard
#   OK will install wireguard
#   installed wireguard
do_install_wireguard() {
    log_info "OK will install wireguard"
    test ! "$dryrun" || return 0

    case "$(get_package_manager)" in
        apk) apk add wireguard-tools ;;
        apt-get) apt-get install -y wireguard ;;
        brew) sudo -u $(get_regular_user_name) brew install wireguard-tools ;;
        dnf) dnf install -y wireguard-tools ;;
        pacman) pacman --noconfirm -Sy wireguard-tools ;;
        pkg) pkg install -y wireguard ;;
        yum) yum install -y wireguard-tools ;;
        zypper) zypper install -y wireguard-tools ;;
    esac
    log_info "installed wireguard"
}

# Prompts to install wireguard.
#
# Logs messages indicating wireguard was installed.
# May alternately output instructions to install wireguard manually,
# if it cannot be installed via package manager.
#
# Examples
#
#   > install_wireguard
#   WARNING wireguard not found
#   install wireguard? ([y]es, [q]uit): _
#   OK will install wireguard
#   installed wireguard
install_wireguard() {
    local where="$(whichis wg)"

    if [ ! "$where" ]; then
        log_warn "wireguard not found"
        if [ "$(can_install_wireguard)" ]; then
            case $(prompt "install wireguard?" yes quit) in
                y*) do_install_wireguard ;;
                q*) bye 1 QUIT ;;
            esac
        else
            log_error "unable to install wireguard automatically"
            log_info $(echo "
                please install wireguard, and then re-run this script;
                see $doc_url/guide/agents/install/ for more info
            " | paste -sd' ' -)
            test "$dryrun" || bye 1 FAIL
        fi
    else
        log_info "wireguard found at $where"
    fi
}

# Installs iptables (unless in "dryrun" mode).
#
# Logs message indicating iptables was installed.
#
# Examples
#
#   > do_install_iptables
#   OK will install iptables
#   installed iptables
do_install_iptables() {
    log_info "OK will install iptables"
    test ! "$dryrun" || return 0

    case "$(get_package_manager)" in
        apk) apk add iptables ;;
        apt-get) apt-get install -y iptables ;;
        dnf) dnf install -y iptables ;;
        pacman) pacman --noconfirm -Sy iptables ;;
        yum) yum install -y iptables ;;
        zypper) zypper install -y iptables ;;
    esac
    log_info "installed iptables"
}

# Prompts to install iptables on Linux.
#
# Logs messages indicating iptables was installed.
#
# Examples
#
#   > install_iptables
#   WARNING iptables not found
#   install iptables? ([y]es, [n]o): _
#   OK will install iptables
#   installed iptables
install_iptables() {
    local where="$(whichis iptables)"
    test "$(uname)" = "Linux" || return 0
    test "$(get_package_manager)" || return 0

    if [ ! "$where" ]; then
        log_warn "iptables not found"
        case $(prompt "install iptables?" yes no) in
            y*) do_install_iptables ;;
            n*) ;;
        esac
    else
        log_info "iptables found at $where"
    fi
}

# Outputs ID of linux distribution used by the system, or blank.
#
# Examples
#
#   > get_distro_name
#   rhel
#
# Known IDs
#
#   almalinux: AlmaLinux 8.5 (Arctic Sphynx)
#   amzn: Amazon Linux release 2 (Karoo)
#   centos: CentOS Linux release 8.2.2004 (Core)
#   fedora: Fedora release 32 (Thirty Two)
#   ol: Oracle Linux Server release 8.2
#   rhel: Red Hat Enterprise Linux release 8.2 (Ootpa)
#   rocky: Rocky Linux 8.5 (Green Obsidian)
get_distro_name() {
    if [ -f /etc/os-release ]; then
        sed 's/"//g' /etc/os-release | awk -F= '/^ID=/ { print $2 }'
    elif [ -f /etc/system-release ]; then
        awk '
            /CentOS/ { print "centos" }
            /Oracle/ { print "ol" }
            /Red Hat/ { print "rhel" }
        ' /etc/system-release
    else
        uname
    fi
}

# Outputs full version of linux distribution used by the system, or blank.
#
# Examples
#
#   > get_distro_version
#   8.2
get_distro_version() {
    if [ -f /etc/os-release ]; then
        sed 's/"//g' /etc/os-release | awk -F= '/VERSION_ID/ { print $2 }'
    elif [ -f /etc/system-release ]; then
        awk -vRS=' ' '/[[:digit:]]/ { print; nextfile }' /etc/system-release
    else
        uname -r
    fi
}

# Outputs major version of distro, or blank.
#
# Examples
#
#   > get_distro_major_version
#   8
get_distro_major_version() {
    local full_version=$(get_distro_version)
    case "$(get_distro_name)" in
        amzn)
            # align to corresponding rhel version
            case "$full_version" in
                2) echo 7 ;;
                2017.09) echo 6 ;;
                *) echo "$full_version" ;;
            esac
            ;;
        alpine|ubuntu) echo "$full_version" | sed 's/\([0-9]\.[0-9]*\)\..*/\1/' ;;
        *) echo "$full_version" | sed 's/\..*//' ;;
    esac
}

# Outputs yes if the linux distribution is a rhel-like distro, or blank.
#
# Examples
#
#   > get_redhat_distro
#   yes
get_redhat_distro() {
    case "$(get_distro_name)" in
        amzn)
            case "$(get_distro_version)" in
                2|2017.09) echo yes ;;
                *) exit 0
            esac
            ;;
        almalinux|centos|ol|rhel|rocky) echo yes ;;
    esac
}

# Outputs yes if Extra Packages for Enterprise Linux repo is installed, or blank.
#
# Examples
#
#   > get_redhat_epel_installed
#   yes
get_redhat_epel_installed() {
    local manager="$(get_package_manager)"
    test "$manager" = dnf -o "$manager" = yum || return 0
    $manager repolist | awk '/Extra Packages/ { print "yes"; nextfile }'
}

# Installs EPEL repo (unless in "dryrun" mode).
#
# Logs message indicating repo was installed.
#
# Examples
#
#   > do_add_redhat_epel_repo
#   OK will add epel repo
#   added epel repo
do_add_redhat_epel_repo() {
    local manager="$(get_package_manager)"

    log_info "OK will add epel repo"
    test ! "$dryrun" || return 0

    case "$(get_distro_name)" in
        centos) $manager install -y epel-release ;;
        *)
            local version=$(get_distro_major_version)
            $manager install -y $epel_dl_url-$version.noarch.rpm
            ;;
    esac
    log_info "added epel repo"
}

# Outputs yes if EPEL must be installed first before installing libsodium.
#
# Ouputs blank if EPEL doesn't need to be installed (because it is already
# installed, or because the distro doesn't need EPEL).
#
# Examples
#
#   > must_add_redhat_epel_to_install_libsodium
#   yes
must_add_redhat_epel_to_install_libsodium() {
    test "$(get_redhat_distro)" || return 0
    test ! "$(get_redhat_epel_installed)" || return 0
    echo "yes"
}

# Outputs yes if libsodium can be installed via package manager.
#
# Ouputs blank if libsodium cannot be installed.
#
# Examples
#
#   > can_install_libsodium
#   yes
can_install_libsodium() {
    test "$(get_package_manager)" || return 0
    case "$(get_distro_name)/$(get_distro_version)" in
        amzn/2022) return 0 ;;
        amzn/2023)
            awk '{
                split($4, a, ".");
                if (int(a[3]) >= 20230920) { print "yes" }
            }' /etc/amazon-linux-release
            ;;
        *) echo "yes" ;;
    esac
}

# Outputs path to libsodium, or blank.
#
# Examples
#
#   > get_libsodium_path
#   /lib/x86_64-linux-gnu/libsodium.so.23
get_libsodium_path() {
    if [ -f /etc/ld.so.conf ]; then
        ldconfig -p | awk '/libsodium/ { print $4 }'
    else
        find /lib /usr/lib $usr_local/lib -name 'libsodium.*' | sort -V | tail -n1
    fi
}

# Installs libsodium (unless in "dryrun" mode).
#
# Logs message indicating libsodium was installed.
#
# Examples
#
#   > do_install_libsodium
#   OK will install libsodium
#   installed libsodium
do_install_libsodium() {
    log_info "OK will install libsodium"
    test ! "$dryrun" || return 0

    case "$(get_package_manager)" in
        apk) apk add libsodium ;;
        apt-get) apt-get install -y libsodium23 ;;
        brew) sudo -u $(get_regular_user_name) brew install libsodium ;;
        dnf) dnf install -y libsodium ;;
        pacman) pacman --noconfirm -Sy libsodium ;;
        pkg) pkg install -y libsodium ;;
        yum) yum install -y libsodium ;;
        zypper) zypper install -y libsodium23 ;;
    esac
    log_info "installed libsodium"
}

# Prompts to install libsodium.
#
# Logs messages indicating libsodium was installed. May also prompt to install
# EPEL repo, if necessary. May alternately output instructions to install
# libsodium manually, if it cannot be installed via package manager.
#
# Examples
#
#   > install_libsodium
#   WARNING libsodium not found
#   install libsodium? ([y]es, [q]uit): _
#   OK will install libsodium
#   installed libsodium
install_libsodium() {
    local where="$(get_libsodium_path)"

    if [ ! "$where" ]; then
        log_warn "libsodium not found"
        if [ "$(must_add_redhat_epel_to_install_libsodium)" ]; then
            log_warn "epel repo (Extra Packages for Enterprise Linux) not added"
            case $(prompt "add epel repo and install libsodium?" yes quit) in
                y*) do_add_redhat_epel_repo; do_install_libsodium ;;
                q*) bye 1 QUIT ;;
            esac
        elif [ "$(can_install_libsodium)" ]; then
            case $(prompt "install libsodium?" yes quit) in
                y*) do_install_libsodium ;;
                q*) bye 1 QUIT ;;
            esac
        else
            log_error "unable to install libsodium automatically"
            log_info $(echo "
                please install libsodium, and then re-run this script;
                see $doc_url/guide/agents/install/ for more info
            " | paste -sd' ' -)
            test "$dryrun" || bye 1 FAIL
        fi
    else
        log_info "libsodium found at $where"
    fi
}

# Outputs yes if Software Collections repo is installed, or blank.
#
# Examples
#
#   > get_redhat_scl_installed
#   yes
get_redhat_scl_installed() {
    test "$(get_redhat_distro)" || return 0
    yum repolist | awk '/Software Collections|SCLo rh/ { print "yes"; nextfile }'
}

# Installs SCL repo (unless in "dryrun" mode).
#
# Logs message indicating repo was installed.
#
# Examples
#
#   > do_add_redhat_scl_repo
#   OK will add scl repo
#   added scl repo
do_add_redhat_scl_repo() {
    local version=$(get_distro_major_version)

    log_info "OK will add scl repo"
    test ! "$dryrun" || return 0

    case "$(get_distro_name)" in
        centos) yum install -y centos-release-scl ;;
        rhel) yum-config-manager --enable rhel-server-rhscl-$version-rpms ;;
    esac
    log_info "added scl repo"
}

# Outputs yes if distro needs SCL installed first before installing python.
#
# Ouputs blank if distro doesn't need SCL.
#
# Examples
#
#   > must_install_python_from_redhat_scl
#   yes
must_install_python_from_redhat_scl() {
    case "$(get_distro_name)" in
        centos) test "$(get_distro_major_version)" -gt 6 || echo "yes" ;;
        rhel) test "$(get_distro_major_version)" -gt 7 || echo "yes" ;;
    esac
}

# Outputs yes if this particular system needs SCL installed first before
# installing python.
#
# Ouputs blank if SCL doesn't need to be installed (because it is already
# installed, or because the distro doesn't need SCL).
#
# Examples
#
#   > must_add_redhat_scl_to_install_python
#   yes
must_add_redhat_scl_to_install_python() {
    test "$(must_install_python_from_redhat_scl)" || return 0
    test ! "$(get_redhat_scl_installed)" || return 0
    echo "yes"
}

# set $python_bin to $python_scl_bin if $python_bin doesn't already exist
# and we expect to install python from scl for this distro
if [ "$(must_install_python_from_redhat_scl)" -a ! "$(whichis "$python_bin")" ]; then
    python_bin="$python_scl_bin"
fi

# Outputs python version string, or blank.
#
# Examples
#
#   > get_python_version
#   3.6.11
get_python_version() {
    ("$python_bin" --version 2>/dev/null || echo "") | awk '{ print $2 }'
}

# Installs python (unless in "dryrun" mode).
#
# Logs message indicating python was installed.
#
# $1 - Label to output.
#
# Examples
#
#   > do_install_python python
#   OK will install python
#   installed python
do_install_python() {
    local what="$1"
    test "$what" || what="python"

    log_info "OK will install $what"
    test ! "$dryrun" || return 0

    case "$(get_package_manager)" in
        apk) apk add gcc libffi-dev make musl-dev python3-dev ;;
        apt-get) apt-get install -y gcc libffi-dev make python3-dev python3-venv ;;
        brew) sudo -u $(get_regular_user_name) brew install python3 ;;
        dnf) dnf install -y findutils gcc libffi-devel make python3-devel ;;
        pacman) pacman --noconfirm -Sy gcc libffi make python-virtualenv ;;
        pkg) pkg install -y python3 ;;
        yum)
            if [ "$(must_install_python_from_redhat_scl)" ]; then
                yum install -y rh-python38-python-cffi
            else
                yum install -y python3
            fi
            ;;
        zypper) zypper install -y python3-virtualenv ;;
    esac
    log_info "installed $what"
}

# Prompts to install python.
#
# Logs messages indicating python was installed. May also prompt to install
# SCL repo, if necessary. May alternately output instructions to install
# python manually, if it cannot be installed via package manager, or if an
# older version of python is currently installed.
#
# Examples
#
#   > install_python
#   WARNING python not found
#   install python? ([y]es, [q]uit): _
#   OK will install python
#   installed python
install_python() {
    local version minimum where instructions
    version=$(get_python_version)
    minimum="$python_minimum_version"
    where="$(whichis "$python_bin")"
    instructions=$(echo "
        please install python $minimum or newer, and then re-run this
        script with the INSTALL_PYTHON env var pointing to the new
        python executable; see $doc_url/guide/agents/install/ for more info
    " | paste -sd' ' -)

    if [ ! "$version" ]; then
        log_warn "python not found"
        if [ "$(must_add_redhat_scl_to_install_python)" ]; then
            log_warn "scl repo (Red Hat Software Collections) not added"
            case $(prompt "add scl repo and install python?" yes quit) in
                y*) do_add_redhat_scl_repo; do_install_python "" ;;
                q*) bye 1 QUIT ;;
            esac
        elif [ "$(get_package_manager)" ]; then
            case $(prompt "install python?" yes quit) in
                y*) do_install_python "" ;;
                q*) bye 1 QUIT ;;
            esac
        else
            log_error "unable to install python automatically"
            log_info $instructions
            test "$dryrun" || bye 1 FAIL
        fi
    elif [ $(calc_greater_version $minimum $version) != "$version" ]; then
        log_error "python $version found at $where but at least $minimum required"
        log_info $instructions
        test "$dryrun" || bye 1 FAIL
    else
        log_info "python $version found at $where"
    fi
}

# Outputs python packages missing that are needed to create virtualenv, or blank.
#
# Examples
#
#   > get_missing_venv_packages
#   ensurepip,venv
get_missing_venv_packages() {
    for package in $python_venv_packages; do
        "$python_bin" -m $package -h >/dev/null 2>&1 || echo $package
    done
}

# Prompts to install python packages missing that are needed to create
# virtualenv (unless in "dryrun" mode).
#
# Logs messages indicating packages were installed. May alternately output
# instructions to install packages manually, if they cannot be installed via
# package manager.
#
# Examples
#
#   > install_venv_packages
#   WARNING python missing these packages: ensurepip,venv
#   install missing packages? ([y]es, [q]uit): _
#   OK will install missing packages
#   installed missing packages
install_venv_packages() {
    local missing instructions
    missing="$(get_missing_venv_packages | paste -sd, -)"
    instructions=$(echo "
        please install these python packages: $missing;
        then re-run this script; see $doc_url/guide/agents/install/ for more info
    " | paste -sd' ' -)

    if [ "$missing" ]; then
        log_warn "python missing these packages: $missing"
        if [ "$(get_package_manager)" ]; then
            case $(prompt "install missing packages?" yes quit) in
                y*) do_install_python "missing packages" ;;
                q*) bye 1 QUIT ;;
            esac
        else
            log_error "unable to install misisng python packages automatically"
            log_info $instructions
            test "$dryrun" || bye 1 FAIL
        fi
    else
        log_info "python includes all packages needed for venv"
    fi
}

# Creates virtualenv for agent (unless in "dryrun" mode).
#
# Logs message indicating virtualenv was created.
#
# Examples
#
#   > do_create_venv
#   OK will create virtualenv
#   created virtualenv
do_create_venv() {
    log_info "OK will create virtualenv"
    test ! "$dryrun" || return 0

    "$python_bin" -m venv "$venv_path"
    log_info "created virtualenv"
}

# Deletes virtualenv for agent (unless in "dryrun" mode).
#
# Logs message indicating virtualenv was deleted.
#
# Examples
#
#   > do_delete_venv
#   OK will delete virtualenv
#   deleted virtualenv
do_delete_venv() {
    log_info "OK will delete virtualenv"
    test ! "$dryrun" || return 0

    rm -rf "$venv_path"
    log_info "deleted virtualenv"
}

# Prompts to create virtualenv for agent (unless in "dryrun" mode).
#
# Logs messages indicating virtualenv was created.
#
# Examples
#
#   > create_venv
#   WARNING python virtualenv not found at /opt/venv/procustodibus-agent
#   create virtualenv? ([y]es, [q]uit): _
#   OK will create virtualenv
#   created virtualenv
#
#   > create_venv
#   WARNING python virtualenv broken at /opt/venv/procustodibus-agent
#   recreate virtualenv? ([y]es, [q]uit): _
#   OK will delete virtualenv
#   deleted virtualenv
#   OK will create virtualenv
#   created virtualenv
create_venv() {
    if [ ! -f "$venv_path/bin/activate" ]; then
        log_warn "python virtualenv not found at $venv_path"
        case $(prompt "create virtualenv?" yes quit) in
            y*) do_create_venv ;;
            q*) bye 1 QUIT ;;
        esac
    elif ! $venv_path/bin/pip --version >/dev/null 2>&1; then
        log_warn "python virtualenv broken at $venv_path"
        case $(prompt "recreate virtualenv?" yes quit) in
            y*) do_delete_venv; do_create_venv ;;
            q*) bye 1 QUIT ;;
        esac
    else
        log_info "python virtualenv found at $venv_path"
    fi
}

# Prompts to delete virtualenv for agent (unless in "dryrun" mode).
#
# Logs messages indicating virtualenv was deleted.
#
# Examples
#
#   > delete_venv
#   WARNING python virtualenv found at /opt/venv/procustodibus-agent
#   delete virtualenv? ([y]es, [q]uit): _
#   OK will delete virtualenv
#   deleted virtualenv
delete_venv() {
    if [ -f "$venv_path/bin/activate" ]; then
        log_warn "python virtualenv found at $venv_path"
        case $(prompt "delete virtualenv?" yes quit) in
            y*) do_delete_venv ;;
            q*) bye 1 QUIT ;;
        esac
    else
        log_info "python virtualenv not found at $venv_path"
    fi
}

# Writes the agent version in its pyproject.toml file (unless in "dryrun" mode).
#
# Logs message indicating version was hardcoded.
# Skips if python version is 3.8 or newer.
#
# Examples
#
#   > write_agent_version
#   will hardcode agent version in pyproject.toml
write_agent_version() {
    local python_version=$(get_python_version)
    local agent_version=$(get_agent_version)
    test "$python_version" || return 0
    test $(calc_greater_version 3.8 $python_version) = 3.8 || return 0
    log_info "will hardcode agent version in pyproject.toml"
    test ! "$dryrun" || return 0
    mv pyproject.toml pyproject.original
    awk -v version="$agent_version" '
        /^dynamic = ."version"./ { $0 = "version = \"" version "\"" }
        { print }
    ' pyproject.original > pyproject.toml
}

# Install agent's python package (unless in "dryrun" mode).
#
# Logs message indicating package was installed/upgraded.
#
# $1 - Upgrade indicator.
#
# Examples
#
#   > do_install_agent_package
#   OK will install agent
#   installed agent
#
#   > do_install_agent_package upgrade
#   OK will upgrade agent
#   upgraded agent
do_install_agent_package() {
    local action=${1:-install}
    local available=$(get_agent_version)
    local opts=""
    local target=procustodibus-agent

    test $action = install || opts="--upgrade"
    test $available = unknown-version || target="$agent_src"

    log_info "OK will $action agent"
    requires_restart=yes
    test "$target" = procustodibus-agent || write_agent_version
    test ! "$dryrun" || return 0

    . "$venv_path/bin/activate"
    pip install --upgrade pip setuptools
    pip install $opts "$target"
    test ! -f pyproject.original || mv pyproject.original pyproject.toml

    if [ $action = upgrade ]; then
        log_info "upgraded agent"
    else
        log_info "${action}ed agent"
    fi
}

# Prompts to install agent's python package (unless in "dryrun" mode).
#
# Logs messages indicating package was installed/upgraded.
#
# Examples
#
#   > install_agent_package
#   WARNING agent package not installed
#   install agent from pypi? ([y]es, [q]uit): _
#   OK will install agent
#   installed agent
#
#   > install_agent_package
#   WARNING agent 1.0.0 package outdated (1.0.1 available)
#   upgrade agent from /usr/local/src/procustodibus-agent-1.0.1? ([y]es, [n]o): _
#   OK will upgrade agent
#   upgrade agent
install_agent_package() {
    local available=$(get_agent_version)
    local from=pypi
    local version=$(get_installed_agent_version)

    test $available = unknown-version || from="$agent_src"

    if [ ! "$version" ]; then
        log_warn "agent package not installed"
        case $(prompt "install agent from $from?" yes quit) in
            y*) do_install_agent_package ;;
            q*) bye 1 QUIT ;;
        esac
    elif [ $(calc_greater_version $available $version) != "$version" ]; then
        log_warn "agent $version package outdated ($available available)"
        case $(prompt "upgrade agent from $from?" yes no) in
            y*) do_install_agent_package upgrade ;;
            n*) ;;
        esac
    else
        log_info "agent $version package already installed"
    fi
}

# Outputs source directory for extra scripts.
#
# Examples
#
#   > get_scripts_src
#   /usr/local/src/procustodibus-agent-1.0.1/scripts/linux
get_scripts_src() {
    local src="$agent_src/scripts/$(uname | tr '[:upper:]' '[:lower:]')"
    test -d $src && echo $src || echo ""
}

# Installs extra scripts for WireGuard pre/post/up/down
#
# Logs messages indicating scripts were installed
#
# Examples
#
#   > install_scripts
#   OK will install scripts
#   installed scripts into /usr/local/lib/procustodibus/agent/scripts
install_scripts() {
    local src="$(get_scripts_src)"
    test "$src" || return 0
    log_info "OK will install scripts"
    test ! "$dryrun" || return 0

    mkdir -p $scripts_path
    cp -r $src/* $scripts_path/.
    log_info "installed scripts into $scripts_path"
}

# Removes extra scripts for WireGuard pre/post/up/down
#
# Logs messages indicating scripts were removed
#
# Examples
#
#   > remove_scripts
#   OK will remove scripts
#   removed scripts from /usr/local/lib/procustodibus/agent/scripts
remove_scripts() {
    test -d $scripts_path || return 0
    log_info "OK will remove scripts"
    test ! "$dryrun" || return 0

    rm -r $scripts_path
    log_info "removed scripts from $scripts_path"
}

# Outputs process supervisor name, or blank.
#
# Examples
#
#   > get_process_supervisor
#   systemd
get_process_supervisor() {
    if [ -x /lib/systemd/systemd -o -x /usr/lib/systemd/systemd ]; then
        echo systemd
    elif [ -d /Library/LaunchDaemons ]; then
        echo launchd
    elif [ -f /etc/rc.subr ]; then
        echo freebsdrc
    elif [ -f /etc/rc ]; then
        echo rc
    else
        whichof openrc
    fi
}

# Outputs expected path to agent's daemon script or service file, or blank.
#
# Examples
#
#   > get_daemon_path
#   /etc/systemd/system/procustodibus-agent.service
get_daemon_path() {
    case "$(get_process_supervisor)" in
        systemd) echo /etc/systemd/system/procustodibus-agent.service ;;
        launchd) echo /Library/LaunchDaemons/procustodibus-agent.plist ;;
        freebsdrc|rc) echo /etc/rc.d/procustodibus-agent ;;
        *) echo /etc/init.d/procustodibus-agent ;;
    esac
}

# Outputs state of agent's daemon, or blank.
#
# Examples
#
#   > get_daemon_state
#   running
get_daemon_state() {
    local where="$(get_daemon_path)"

    case "$(get_process_supervisor)" in
        launchd)
            launchctl print system/procustodibus-agent |
            awk -F' = ' '/state =/ { print $2 }'
            ;;
        openrc)
            rc-service procustodibus-agent status 2>/dev/null |
            awk '{ print $3 }'
            ;;
        systemd)
            systemctl show procustodibus-agent |
            awk -F= '/SubState/ { print $2 }'
            ;;
        *) test -x "$where" && "$where" status || echo "" ;;
    esac
}

# Install daemon script or service file for agent (unless in "dryrun" mode).
#
# Logs message indicating daemon was installed.
#
# Examples
#
#   > do_install_daemon
#   OK will install daemon
#   installed daemon
do_install_daemon() {
    local where="$(get_daemon_path)"

    log_info "OK will install daemon"
    requires_restart=yes
    test ! "$dryrun" || return 0

    case "$(get_process_supervisor)" in
        freebsdrc)
            awk -v venv_path="$venv_path" '
                /^program=/ { $0 = "program=" venv_path "/bin/procustodibus-agent" }
                { print }
            ' "$agent_src/etc/freebsd.service" > "$where"
            chmod +x "$where"
            ;;
        launchd)
            awk -v venv_path="$venv_path" '
                />ProgramArguments</ { program_arguments = 1; }
                /<string>/ {
                    if (program_arguments == 1) {
                        sub(">[^<]*<", ">" venv_path "/bin/procustodibus-agent<");
                        program_arguments = 0;
                    }
                }
                { print }
            ' "$agent_src/etc/launchd.plist" > "$where"
            launchctl bootstrap system "$where"
            ;;
        openrc)
            awk -v venv_path="$venv_path" '
                /^command=/ { $0 = "command=" venv_path "/bin/procustodibus-agent" }
                { print }
            ' "$agent_src/etc/openrc.service" > "$where"
            chmod +x "$where"
            ;;
        systemd)
            awk -v venv_path="$venv_path" '
                /^ExecStart=/ { $1 = "ExecStart=" venv_path "/bin/procustodibus-agent" }
                { print }
            ' "$agent_src/etc/systemd.service" > "$where"
            systemctl daemon-reload
            ;;
        *)
            awk -v venv_path="$venv_path" '
                /^command=/ { $0 = "command=" venv_path "/bin/procustodibus-agent" }
                { print }
            ' "$agent_src/etc/sysvinit.sh" > "$where"
            chmod +x "$where"
            ;;
    esac
    log_info "installed daemon"
}


# Removes daemon script or service file for agent (unless in "dryrun" mode).
#
# Logs message indicating daemon was removed.
#
# Examples
#
#   > do_remove_daemon
#   OK will remove daemon
#   removeed daemon
do_remove_daemon() {
    local supervisor="$(get_process_supervisor)"
    local where="$(get_daemon_path)"

    log_info "OK will remove daemon"
    test ! "$dryrun" || return 0

    case "$supervisor" in
        launchd) launchctl bootout system/procustodibus-agent || true ;;
    esac
    rm -f "$where"
    case "$supervisor" in
        systemd) systemctl daemon-reload ;;
    esac
    log_info "removed daemon"
}

# Prompts to install daemon for agent (unless in "dryrun" mode).
#
# Logs messages indicating daemon was installed.
#
# Examples
#
#   > install_daemon
#   WARNING systemd daemon not found at /etc/systemd/system/procustodibus-agent.service
#   install daemon? ([y]es, [q]uit): _
#   OK will install daemon
#   installed daemon
install_daemon() {
    local supervisor="$(get_process_supervisor)"
    local where="$(get_daemon_path)"

    test "$supervisor" || supervisor="sysvinit"

    if [ ! -f "$where" ]; then
        log_warn "$supervisor daemon not found at $where"
        case $(prompt "install daemon?" yes quit) in
            y*) do_install_daemon ;;
            q*) bye 0 QUIT ;;
        esac
    else
        log_info "$supervisor daemon found at $where"
    fi
}

# Prompts to remove daemon for agent (unless in "dryrun" mode).
#
# Logs messages indicating daemon was removed.
#
# Examples
#
#   > remove_daemon
#   WARNING systemd daemon found at /etc/systemd/system/procustodibus-agent.service
#   remove daemon? ([y]es, [q]uit): _
#   OK will remove daemon
#   removeed daemon
remove_daemon() {
    local supervisor="$(get_process_supervisor)"
    local where="$(get_daemon_path)"

    test "$supervisor" || supervisor="sysvinit"

    if [ -f "$where" ]; then
        log_warn "$supervisor daemon found at $where"
        case $(prompt "remove daemon?" yes quit) in
            y*) do_remove_daemon ;;
            q*) bye 0 QUIT ;;
        esac
    else
        log_info "$supervisor daemon not found at $where"
    fi
}

# Starts daemon for agent (unless in "dryrun" mode).
#
# Logs message indicating daemon was started. Also configures daemon to start
# automatically on system boot.
#
# $1 - Action (defaults to "start").
#
# Examples
#
#   > do_start_daemon
#   OK will start daemon
#   started daemon
#
#   > do_start_daemon restart
#   OK will restart daemon
#   restarted daemon
do_start_daemon() {
    local action=${1:-start}
    local where="$(get_daemon_path)"

    log_info "OK will $action daemon"
    test ! "$dryrun" || return 0

    case "$(get_process_supervisor)" in
        freebsdrc)
            "$where" enable
            "$where" $action
            ;;
        launchd)
            launchctl enable system/procustodibus-agent
            launchctl kickstart system/procustodibus-agent
            ;;
        openrc)
            rc-update add procustodibus-agent
            rc-service procustodibus-agent $action
            ;;
        rc)
            "$where" $action
            ;;
        systemd)
            systemctl enable procustodibus-agent
            systemctl $action procustodibus-agent
            ;;
        *)
            for runlevel in 0 1 6; do
                ln -fs "$where" /etc/rc$runlevel.d/K20procustodibus-agent
            done
            for runlevel in 2 3 4 5; do
                ln -fs "$where" /etc/rc$runlevel.d/S80procustodibus-agent
            done
            "$where" $action
            ;;
    esac
    log_info "${action}ed daemon"
}

# Stops daemon for agent (unless in "dryrun" mode).
#
# Logs message indicating daemon was stoped. Also removes configuration for
# daemon to start automatically on system boot.
#
# Examples
#
#   > do_stop_daemon
#   OK will stop daemon
#   stoped daemon
do_stop_daemon() {
    local where="$(get_daemon_path)"

    log_info "OK will stop daemon"
    test ! "$dryrun" || return 0

    case "$(get_process_supervisor)" in
        freebsdrc)
            "$where" stop
            "$where" disable
            ;;
        launchd)
            launchctl kill sighup system/procustodibus-agent
            ;;
        openrc)
            rc-service procustodibus-agent stop
            rc-update del procustodibus-agent
            ;;
        rc)
            "$where" stop
            ;;
        systemd)
            systemctl stop procustodibus-agent
            systemctl disable procustodibus-agent
            ;;
        *)
            "$where" stop
            for runlevel in 0 1 6; do
                rm -f /etc/rc$runlevel.d/K20procustodibus-agent
            done
            for runlevel in 2 3 4 5; do
                rm -f /etc/rc$runlevel.d/S80procustodibus-agent
            done
            ;;
    esac
    log_info "stopped daemon"
}

# Prompts to start daemon for agent (unless in "dryrun" mode).
#
# Logs messages indicating daemon was started.
#
# Examples
#
#   > start_daemon
#   WARNING daemon not running
#   start daemon? ([y]es, [q]uit): _
#   OK will start daemon
#   started daemon
start_daemon() {
    local state="$(get_daemon_state)"
    test "$state" || state="not running"

    case "$state" in
        *"is running"*|running|started)
            if [ "$requires_restart" ]; then
                log_warn "daemon requires restart"
                case $(prompt "restart daemon?" yes quit) in
                    y*) do_start_daemon restart ;;
                    q*) bye 0 QUIT ;;
                esac
            else
                log_info "daemon $state"
            fi
            ;;
        *)
            log_warn "daemon $state"
            case $(prompt "start daemon?" yes quit) in
                y*) do_start_daemon ;;
                q*) bye 0 QUIT ;;
            esac
            ;;
    esac
}

# Prompts to stop daemon for agent (unless in "dryrun" mode).
#
# Logs messages indicating daemon was stoped.
#
# Examples
#
#   > stop_daemon
#   WARNING daemon running
#   stop daemon? ([y]es, [q]uit): _
#   OK will stop daemon
#   stoped daemon
stop_daemon() {
    local state="$(get_daemon_state)"
    test "$state" || state="not running"

    case "$state" in
        *"is running"*|running|started)
            log_warn "daemon $state"
            case $(prompt "stop daemon?" yes quit) in
                y*) do_stop_daemon ;;
                q*) bye 0 QUIT ;;
            esac
            ;;
        *) log_info "daemon $state" ;;
    esac
}

# Outputs test results for all this script's helper functions.
do_checkfns() {
    echo get_agent_version: $(get_agent_version)
    echo get_installed_agent_version: $(get_installed_agent_version)
    echo calc_greater_version: $(calc_greater_version 1.23 12.3 1.2.3 1 12)
    echo log_info: $(log_info info message)
    echo log_warn: $(log_warn warn message)
    echo log_error: $(log_error error message)
    echo log: $(log log message)
    echo prompt: $(prompt "do it?" yes no)
    echo whichis true: $(whichis true)
    echo whichis nope: $(whichis nope)
    echo whichof: $(whichof nope also-nope true)
    echo get_regular_user_name: $(get_regular_user_name)
    echo get_package_manager: $(get_package_manager)
    echo can_install_wireguard: $(can_install_wireguard)
    echo get_distro_name: $(get_distro_name)
    echo get_distro_version: $(get_distro_version)
    echo get_distro_major_version: $(get_distro_major_version)
    echo get_redhat_distro: $(get_redhat_distro)
    echo get_redhat_epel_installed: $(get_redhat_epel_installed)
    echo must_add_redhat_epel_to_install_libsodium: $(must_add_redhat_epel_to_install_libsodium)
    echo can_install_libsodium: $(can_install_libsodium)
    echo get_libsodium_path: $(get_libsodium_path)
    echo get_redhat_scl_installed: $(get_redhat_scl_installed)
    echo must_install_python_from_redhat_scl: $(must_install_python_from_redhat_scl)
    echo must_add_redhat_scl_to_install_python: $(must_add_redhat_scl_to_install_python)
    echo python_bin: $python_bin
    echo get_python_version: $(get_python_version)
    echo get_missing_venv_packages: $(get_missing_venv_packages)
    echo get_scripts_src: $(get_scripts_src)
    echo get_process_supervisor: $(get_process_supervisor)
    echo get_daemon_path: $(get_daemon_path)
    echo get_daemon_state: $(get_daemon_state)
}

# Runs install process.
do_install() {
    require_root

    modifiers=""
    test ! "$force" || modifiers="force $modifiers"
    test ! "$dryrun" || modifiers="dryrun $modifiers"
    log_info "${modifiers}install $(get_agent_version)"

    require_cnf
    set_cnf_permissions
    install_wireguard
    install_iptables
    install_libsodium
    install_python
    install_venv_packages
    create_venv
    install_agent_package
    install_scripts
    install_daemon
    start_daemon

    test ! "$dryrun" && bye 0 install SUCCESS || bye 0 dryrun complete
}

# Runs remove process.
do_remove() {
    require_root

    modifiers=""
    test ! "$force" || modifiers="force $modifiers"
    test ! "$dryrun" || modifiers="dryrun $modifiers"
    log_info "${modifiers}remove $(get_agent_version)"

    stop_daemon
    remove_daemon
    remove_scripts
    delete_venv
    delete_cnf

    test ! "$dryrun" && bye 0 remove SUCCESS || bye 0 dryrun complete
}

case $action in
    checkfns) do_checkfns ;;
    help) do_help ;;
    install) do_install ;;
    remove) do_remove ;;
    version) do_version ;;
esac
