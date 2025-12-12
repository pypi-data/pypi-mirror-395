#Requires -Module Ansible.ModuleUtils.Legacy
#AnsibleRequires -OSVersion 6.2
#AnsibleRequires -CSharpUtil Ansible.Basic
#
# Example Code for Windows Module win_certificate.ps1
#
$spec = @{
    options = @{
        dns_name = @{ type = "str" }
        validity_days = @{
            type = "int"
            default = 365
        }
        store_location_my = @{
            type = "str"
            default = "Cert:\LocalMachine\My"
        }
        store_location = @{
            type = "str"
            default = "Cert:\LocalMachine\My"
        }
        state = @{
            type = "str"
            default = "present"
            choices = @("present", "absent")
        }
        tmp_file_path = @{
            type = "str"
            default = "C:\Temp\ExportedCertificate.cer"
        }
        friendly_name = @{  # New parameter
            type = "str"
            default = "AnsibleCert"
        }
    }
}

$module = [Ansible.Basic.AnsibleModule]::Create($args, $spec)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version 2.0

function Get-CertificateCount($certificates) {
    if ($certificates -eq $null) {
        return 0
    } else {
        $certificates_type = $certificates.GetType()
        if ($certificates_type -is [System.Array]) {
            return $certificates.Count
        } else {
            return 1
        }
    }
}

function Create-Certificate() {
    $store_location_my = $module.Params.store_location_my
    $dns_name = $module.Params.dns_name
    $tmp_file_path = $module.Params.tmp_file_path
    $certificates_my = Get-ChildItem -Path $store_location_my -Recurse | Where-Object { $_.Subject -eq "CN=$dns_name" }
    $certificates_my_count = Get-CertificateCount $certificates_my
    if ($certificates_my_count -eq 0) {
        # No cert in store_location
        $validity_days = $module.Params.validity_days
        $expiration_date = (Get-Date).AddDays($validity_days)
        $certParams = @{
            DnsName = $dns_name
            CertStoreLocation = $store_location_my
            NotAfter = $expiration_date
            FriendlyName = $module.Params.friendly_name  # Use friendly name from parameters
        }
        try {
            $certificate_my = New-SelfSignedCertificate @certParams -ErrorAction Stop
        } catch {
            $module.FailJson("Failed to create the certificate $dns_name in $store_location_my. Error: $_")
        }
    } elseif ($certificates_my_count -eq 1) {
        $certificate_my = $certificates_my
    } else {
        $certificate_my = $certificates_my[0]
    }
    if ($module.Params.store_location -ne $store_location_my) {
        try {
            Export-Certificate -Cert $certificate_my -FilePath $module.Params.tmp_file_path -ErrorAction Stop
        } catch {
            $module.FailJson("Failed to export from store $store_location_my to $tmp_file_path. Error: $_")
        }
        Remove-Item -Path $certificate_my.PSPath -ErrorAction Stop
    }
    return $certificate_my
}

$dns_name = $module.Params.dns_name
$store_location = $module.Params.store_location
$store_location_my = $module.Params.store_location_my
$tmp_file_path = $module.Params.tmp_file_path

$certificates = Get-ChildItem -Path $store_location -Recurse | Where-Object { $_.Subject -eq "CN=$dns_name" }
$certificates_count = Get-CertificateCount $certificates

$module.Result.changed = $false

if ($module.Params.state -eq "absent") {
    # Remove the certificate
    if ($certificates_count -gt 0) {
        try {
            $certificate = $certificates[0]
            Remove-Item -Path $certificate.PSPath -ErrorAction Stop
            $module.Result.msg = "Certificate $dns_name removed"
            $module.Result.changed = $true
        } catch {
            $module.FailJson("Failed to remove the certificate $dns_name from $store_location. Error: $_")
        }
    } else {
        $module.Result.msg = "Certificate $dns_name is absent in $store_location"
    }
} else {
    if ($certificates_count -eq 0) {
        $certificate_my = Create-Certificate
        if ($module.Params.store_location -ne $store_location_my) {
            try {
                $certificate = Import-Certificate -FilePath $tmp_file_path -CertStoreLocation $store_location -ErrorAction Stop
                Remove-Item $tmp_file_path -ErrorAction Stop
                $module.Result.msg = "Certificate $dns_name created and imported to $store_location"
                $module.Result.changed = $true
            } catch {
                $module.FailJson("Failed to import $tmp_file_path to $store_location. Error: $_")
            }
        } else {
            $certificate = $certificate_my
        }
    }
    elseif ($certificates_count -eq 1) {
        $certificate = $certificates
    }
    else  {
        $certificate = $certificates[0]
    }
    $module.Result.thumbPrint = $certificate.thumbPrint
}

$module.ExitJson()
