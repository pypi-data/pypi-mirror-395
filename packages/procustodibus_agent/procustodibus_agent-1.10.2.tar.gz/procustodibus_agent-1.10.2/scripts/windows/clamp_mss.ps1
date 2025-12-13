param (
    [Parameter(Position = 0)]
    [string] $Action,
    [Parameter(Position = 1)]
    [string] $Iface,
    [Parameter(Position = 2)]
    [string] $Options
)

function Help() {
    Write-Host @"
Pro Custodibus Agent clamp_mss script.

Enables/disables MSS-clamping of forwarded connections in the specified
WireGuard interface. Run as administrator.

Usage:
  clamp_mss.ps1 ACTION IFACE OPTIONS

Options:
  outbound|true  Clamps MSS of connections outbound to the WireGuard network
  clean|false    Cleans MSS-clamping

Examples:
  clamp_mss.ps1 up wg0 outbound
"@
}

function Set-ClampMss( $Iface, $Enabled ) {
    Write-Host "+ Set-NetIPInterface -InterfaceAlias $Iface -ClampMss $Enabled"
    Set-NetIPInterface -InterfaceAlias $Iface -ClampMss $Enabled
}

function Post-Up() {
    switch -Regex ( $Options ) {
        'outbound|true' { Set-ClampMss $Iface 'Enabled' }
        default { Pre-Down }
    }
}

function Pre-Down() {
    Set-ClampMss $Iface 'Disabled'
}

switch ( $Action ) {
    'pre_up' {}
    'post_up' { Post-Up }
    'up' { Post-Up }
    'down' { Pre-Down }
    'pre_down' { Pre-Down }
    'post_down' {}
    default { Help }
}
