param (
    [Parameter(Position = 0)]
    [string] $Action,
    [Parameter(Position = 1)]
    [string] $Iface,
    [Parameter(Position = 2)]
    [string] $Options
)

$Profile = switch -Regex ( $Options ) {
    'trusted|work|domain' { 'DomainAuthenticated' }
    'private|home|internal' { 'Private' }
    default { 'Public' }
}

function Help() {
    Write-Host @"
Pro Custodibus Agent fw_zone script.

Adds the specified WireGuard interface to the specified firewall profile.
Run as administrator.

Usage:
  fw_zone.ps1 ACTION IFACE OPTIONS

Options:
  Profile name (eg 'public')

Examples:
  fw_zone.ps1 up wg0 trusted
"@
}

function Post-Up() {
    Write-Host "+ Get-NetConnectionProfile -InterfaceAlias $Iface"
    $Conn = Get-NetConnectionProfile -InterfaceAlias $Iface
    Write-Host "+ NetworkCategory : $($Conn.NetworkCategory)"
    if ( $Profile -ne $Conn.NetworkCategory ) {
        if ( $Profile -eq 'DomainAuthenticated' -or $Conn.NetworkCategory -eq 'DomainAuthenticated' ) {
            Write-Warning "cannot change firewall profile to or from DomainAuthenticated"
        } else {
            Write-Host "+ Set-NetConnectionProfile -InterfaceAlias $Iface -NetworkCategory $Profile"
            Set-NetConnectionProfile -InterfaceAlias $Iface -NetworkCategory $Profile
        }
    }
}

switch ( $Action ) {
    'pre_up' {}
    'post_up' { Post-Up }
    'up' { Post-Up }
    'down' {}
    'pre_down' {}
    'post_down' {}
    default { Help }
}
