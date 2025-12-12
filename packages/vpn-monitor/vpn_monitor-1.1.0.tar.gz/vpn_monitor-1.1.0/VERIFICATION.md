# Verifying Releases

To ensure the security and integrity of the `vpn-monitor.exe` executable, we sign our releases using [Sigstore](https://sigstore.dev) and generate build provenance using [SLSA](https://slsa.dev).

You can verify the executable using one of the following methods.

## Method 1: GitHub CLI (Recommended)

If you have the [GitHub CLI](https://cli.github.com/) installed, you can verify the artifact attestation directly.

```powershell
gh attestation verify vpn-monitor.exe --owner henrykp
```

**Expected Output:**

```text
✓ Verification successful!

Subject: vpn-monitor.exe
Predicate Type: https://slsa.dev/provenance/v1
...
```

## Method 2: Cosign (Manual Verification)

If you prefer to use [Cosign](https://docs.sigstore.dev/system_config/installation/), you can verify the blob signature using the `.sig` and `.pem` files included in the release.

1. Download `vpn-monitor.exe`, `vpn-monitor.exe.sig`, and `vpn-monitor.exe.pem` from the release page.
2. Run the following command:

```powershell
cosign verify-blob vpn-monitor.exe `
  --certificate vpn-monitor.exe.pem `
  --signature vpn-monitor.exe.sig `
  --certificate-identity "https://github.com/henrykp/vpn_status_monitor/.github/workflows/release.yml@refs/tags/v*" `
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"
```

**Expected Output:**

```text
Verified OK
```

## Method 3: SHA256 Checksum

You can also verify the file integrity by checking its SHA256 hash.

```powershell
Get-FileHash vpn-monitor.exe -Algorithm SHA256
```

Compare the output hash with the one provided in the release notes or the provenance attestation.
