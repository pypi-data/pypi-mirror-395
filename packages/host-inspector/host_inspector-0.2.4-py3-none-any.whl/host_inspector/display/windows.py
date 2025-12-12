"""
Get-CimInstance -Namespace root\\wmi -ClassName WmiMonitorID | ForEach-Object {
    [PSCustomObject]@{
        Name                 = ([System.Text.Encoding]::ASCII.GetString($_.UserFriendlyName) -replace '\0','').Trim()
        InstanceName         = $_.InstanceName
        Manufacturer         = ([System.Text.Encoding]::ASCII.GetString($_.ManufacturerName) -replace '\0','').Trim()
        SerialNumber         = ([System.Text.Encoding]::ASCII.GetString($_.SerialNumberID) -replace '\0','').Trim()
    }
} | ConvertTo-Json


Get-PnpDevice -Class Monitor | Where-Object Status -eq 'OK' | Select-Object FriendlyName, InstanceId
"""


def get_display_info() -> list[dict]:
    # TODO: Implement Windows display detection
    return [
        {
            "name": "--",
            "display_id": 1,
            "resolution_actual": "--",
            "resolution": "--",
            "refresh_rate": "--",
        }
    ]
