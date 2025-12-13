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
Pro Custodibus Agent masquerade script.

Enables/disables masquerading of forwarded connections in/out of the specified
WireGuard interface. Run as administrator.

Usage:
  masquerade.ps1 ACTION IFACE OPTIONS

Options:
  all|true      Masquerades inbound and outbound connections
  inbound       Masquerades connections inbound from the WireGuard network
  outbound      Masquerades connections outbound to the WireGuard network
  clean|false   Cleans up masquerading

Examples:
  masquerade.ps1 up wg0 outbound
"@
}

function Set-Masquerading( $Iface, $Handle ) {
    $Index = 0
    Get-NetIPAddress -InterfaceAlias $Iface -AddressFamily IPv4 | % {
        $Name = "${Handle}${Index}"
        $Address = "$($_.IPAddress)/$($_.PrefixLength)"
        Write-Host "+ New-NetNat -Name $Name -InternalIPInterfaceAddressPrefix $Address"
        New-NetNat -Name $Name -InternalIPInterfaceAddressPrefix $Address
        $Index++
    }
}

function Post-Up-Inbound() {
    Set-Masquerading $Iface "${Iface}natin"
}

function Post-Up-Outbound() {
    Get-NetAdapter -Physical `
        | Where-Object { $_.Status -eq 'Up' } `
        | Sort -Unique InterfaceAlias `
        | % { Set-Masquerading $_.InterfaceAlias "${Iface}natout" }
}

function Post-Up() {
    Pre-Down
    switch -Regex ( $Options ) {
        'all|true' { Post-Up-Inbound; Post-Up-Outbound }
        'inbound' { Post-Up-Inbound }
        'outbound' { Post-Up-Outbound }
    }
}

function Pre-Down() {
    Get-NetNat | Where-Object { $_.Name -like "${Iface}nat*" } | % {
        Write-Host "+ Remove-NetNat -Name $($_.Name) -Confirm:$false"
        Remove-NetNat -Name $_.Name -Confirm:$false
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
