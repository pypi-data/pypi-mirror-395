#!/bin/bash
# aptbox bash completion script
# 安装方法:
#   1. 将此文件复制到 /etc/bash_completion.d/aptbox
#   2. 或者 source 此文件到 ~/.bashrc

# 检查是否定义了_init_completion函数，如果没有则定义一个简单的
if ! type -t _init_completion >/dev/null 2>&1; then
    _init_completion() {
        cur=${COMP_WORDS[COMP_CWORD]}
        if [[ ${COMP_CWORD} -gt 1 ]]; then
            prev=${COMP_WORDS[COMP_CWORD-1]}
        else
            prev=""
        fi
        words=("${COMP_WORDS[@]}")
        cword=${COMP_CWORD}
        return 0
    }
fi

_aptbox_completion() {
    local cur prev words cword
    _init_completion || return

    # 获取当前命令的子命令
    local command=""
    if [[ ${cword} -gt 1 ]]; then
        for ((i=1; i<${cword}; i++)); do
            if [[ "${words[i]}" != -* ]]; then
                command="${words[i]}"
                break
            fi
        done
    fi

    # 基本的apt命令列表（用于穿透模式）
    local apt_commands="install remove update upgrade full-upgrade dist-upgrade purge autoremove autoclean clean search show list policy source depends rdepends changelog marks unmark deb dpkg-cache add-repository remove-repository"

    case "${command}" in
        update)
            case "${prev}" in
                --output|-o)
                    _filedir
                    return
                    ;;
                *)
                    COMPREPLY=($(compgen -W "--help -h --snapshot-dir --report-dir --verbose --temp-dir --force --dry-run" -- "${cur}"))
                    ;;
            esac
            ;;
        search)
            case "${prev}" in
                --output|-o)
                    _filedir
                    return
                    ;;
                --status)
                    COMPREPLY=($(compgen -W "installed not-installed" -- "${cur}"))
                    return
                    ;;
                --sort)
                    COMPREPLY=($(compgen -W "name size date" -- "${cur}"))
                    return
                    ;;
                --limit)
                    COMPREPLY=($(compgen -W "10 20 50 100" -- "${cur}"))
                    return
                    ;;
                *)
                    if [[ ${cur} == -* ]]; then
                        COMPREPLY=($(compgen -W "--help -h --snapshot-dir --report-dir --verbose --temp-dir --limit --status --exact --output -o --date -d --size -s --sort" -- "${cur}"))
                    else
                        # 如果当前位置是第一个非选项参数，提供包名补全（简单示例）
                        if [[ ${cword} -eq 2 ]]; then
                            COMPREPLY=($(compgen -W "python python3 vim curl wget git docker nginx mysql postgresql" -- "${cur}"))
                        fi
                    fi
                    ;;
            esac
            ;;
        report)
            case "${prev}" in
                --output|-o)
                    _filedir
                    return
                    ;;
                --type)
                    COMPREPLY=($(compgen -W "summary detail stats" -- "${cur}"))
                    return
                    ;;
                --id)
                    # 尝试从报告目录获取可用的报告ID
                    local report_dir="/var/lib/aptbox/reports"
                    if [[ -d "${report_dir}" ]]; then
                        local ids=$(find "${report_dir}" -name "*.json" -printf "%f\n" 2>/dev/null | sed 's/\.json$//' | head -20)
                        COMPREPLY=($(compgen -W "${ids}" -- "${cur}"))
                    fi
                    return
                    ;;
                --filter)
                    COMPREPLY=($(compgen -W "category:system category:development category:network category:database" -- "${cur}"))
                    return
                    ;;
                list|show|query)
                    if [[ ${cur} == -* ]]; then
                        COMPREPLY=($(compgen -W "--id --type --filter --output -o" -- "${cur}"))
                    fi
                    return
                    ;;
                *)
                    if [[ ${cur} == -* ]]; then
                        COMPREPLY=($(compgen -W "--help -h --snapshot-dir --report-dir --verbose --temp-dir" -- "${cur}"))
                    else
                        COMPREPLY=($(compgen -W "list show query" -- "${cur}"))
                    fi
                    ;;
            esac
            ;;
        "")
            # 没有子命令时，显示所有可用选项
            if [[ ${cur} == -* ]]; then
                COMPREPLY=($(compgen -W "--help -h --snapshot-dir --report-dir --verbose --temp-dir" -- "${cur}"))
            else
                # 提供aptbox子命令和apt穿透命令
                COMPREPLY=($(compgen -W "update search report ${apt_commands}" -- "${cur}"))
            fi
            ;;
        *)
            # APT穿透模式的补全
            case "${command}" in
                install|remove|purge)
                    # 软件包名补全（简化版本）
                    if [[ ${cur} == -* ]]; then
                        COMPREPLY=($(compgen -W "--dry-run --assume-no --assume-yes -y --show-progress --fix-broken --fix-missing --ignore-hold --force-yes --download-only --no-download --reinstall --no-install-recommends --install-suggests" -- "${cur}"))
                    else
                        # 这里可以集成apt-cache search的结果来提供更智能的包名补全
                        COMPREPLY=($(compgen -W "python3 python3-pip python3-venv git vim curl wget nginx apache2 mysql-server postgresql docker.io containerd" -- "${cur}"))
                    fi
                    ;;
                upgrade|full-upgrade|dist-upgrade)
                    COMPREPLY=($(compgen -W "--dry-run --assume-no --assume-yes -y --show-progress --with-new-pkgs --without-new-pkgs --no-install-recommends --install-suggests --fix-broken" -- "${cur}"))
                    ;;
                search)
                    if [[ ${cur} == -* ]]; then
                        COMPREPLY=($(compgen -W "--names-only --all --full --names-only --description --full" -- "${cur}"))
                    fi
                    ;;
                show)
                    if [[ ${cur} == -* ]]; then
                        COMPREPLY=($(compgen -W "--package --package --show --show --installed --installed --version --version --depends --depends --predepends --predepends --depends --depends --recommends --recommends --suggests --suggests --conflicts --conflicts --breaks --breaks --replaces --replaces --enhances --enhances" -- "${cur}"))
                    else
                        # 软件包名补全
                        COMPREPLY=($(compgen -W "python3 python3-pip git vim curl wget nginx" -- "${cur}"))
                    fi
                    ;;
                autoremove|autoclean|clean)
                    COMPREPLY=($(compgen -W "--dry-run --assume-no --assume-yes -y --show-progress --purge" -- "${cur}"))
                    ;;
                *)
                    # 默认apt选项补全
                    COMPREPLY=($(compgen -W "--help --help --help -h -h -v -v --version --version --version -q -q --quiet --quiet --quiet -qq -qq -s -s --simulate --simulate --simulate --dry-run --dry-run --dry-run --download-only --download-only --download-only -d -d -y -y --assume-yes --assume-yes --assume-yes --assume-no --assume-no --assume-no -u -u --show-upgraded --show-upgraded --show-upgraded -f -f --fix-broken --fix-broken --fix-broken -m -m --ignore-missing --ignore-missing --ignore-missing --ignore-hold --ignore-hold --ignore-hold --no-download --no-download --no-download -q -q --quiet --quiet --quiet -s -s --simulate --simulate --simulate -y -y --assume-yes --assume-yes --assume-yes -f -f --fix-broken --fix-broken --fix-broken" -- "${cur}"))
                    ;;
            esac
            ;;
    esac
}

# 注册补全函数
complete -F _aptbox_completion aptbox

# 如果需要动态加载包信息，可以添加以下函数（可选）
_aptbox_update_package_cache() {
    # 更新可用软件包缓存（用于更智能的包名补全）
    local cache_file="$HOME/.cache/aptbox_packages.cache"
    local cache_timeout=3600  # 1小时缓存

    if [[ -f "${cache_file}" && $(($(date +%s) - $(stat -c %Y "${cache_file}"))) -lt ${cache_timeout} ]]; then
        return 0
    fi

    mkdir -p "$(dirname "${cache_file}")"
    if command -v apt-cache >/dev/null 2>&1; then
        apt-cache pkgnames 2>/dev/null | head -1000 > "${cache_file}"
    fi
}

# 智能包名补全函数（可选增强）
_aptbox_complete_packages() {
    local cache_file="$HOME/.cache/aptbox_packages.cache"
    _aptbox_update_package_cache

    if [[ -f "${cache_file}" ]]; then
        local packages=$(grep "^${cur}" "${cache_file}" 2>/dev/null)
        COMPREPLY=($(compgen -W "${packages}" -- "${cur}"))
    fi
}