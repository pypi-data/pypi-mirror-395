param (
    [Parameter(Position = 0)]
    [string] $Action,
    [Parameter(Position = 1)]
    [string] $Iface,
    [Parameter(Position = 2)]
    [string] $Options
)

$LogDir = 'C:\Program Files\Pro Custodibus Agent\log'
$ForwardingEnabledFile = "$LogDir\forwarding-enabled.txt"

function Help() {
    Write-Host @"
Pro Custodibus Agent forward script.

Allows/disallows forwarding connections in/out of the specified WireGuard
interface. Run as administrator.

Usage:
  forward.ps1 ACTION IFACE OPTIONS

Options:
  all|true      Allows forwarding inbound and outbound connections
  inbound       Allows forwarding connections inbound from the WireGuard network
  outbound      Allows forwarding connections outbound to the WireGuard network
  internal      Allows forwarding connections within the WireGuard network
  clean|false   Cleans up forwarding

Examples:
  forward.ps1 up wg0 outbound
"@
}

function Set-Forwarding( $Iface, $Enabled ) {
    if ( $Iface -match '^\w[\w .-]+$' ) {
        Write-Host "+ Set-NetIPInterface -InterfaceAlias $Iface -Forwarding $Enabled"
        Set-NetIPInterface -InterfaceAlias $Iface -Forwarding $Enabled
    } else {
        Write-Warning "cannot change forwarding on invalid interface alias"
    }
}

function Post-Up() {
    switch -Regex ( $Options ) {
        'internal' {
            Set-Forwarding $Iface 'Enabled'
        }
        'all|true|inbound|outbound' {
            Set-Forwarding $Iface 'Enabled'
            $Adapters = Get-NetAdapter -Physical `
                | Where-Object { $_.Status -eq 'Up' } `
                | % { Get-NetIPInterface -InterfaceAlias $_.Name -Forwarding 'Disabled' } `
                | Sort -Unique InterfaceAlias `
                | % { $_.InterfaceAlias }
            $Adapters | Out-File -Append $ForwardingEnabledFile
            $Adapters | % { Set-Forwarding $_ 'Enabled' }
        }
        default {
            Pre-Down
        }
    }
}

function Pre-Down() {
    Set-Forwarding $Iface 'Disabled'
    if ( Test-Path -Path $ForwardingEnabledFile ) {
        Get-Content $ForwardingEnabledFile `
            | Sort -Unique `
            | % { Set-Forwarding $_ 'Disabled' }
        Remove-Item -Path $ForwardingEnabledFile
    }
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
