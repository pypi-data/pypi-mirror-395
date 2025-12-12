import subprocess

from zalando_kubectl.utils import Environment, ExternalBinary


_ENCRYPT_ROLES = (
    "ReadOnly",
    "Deployer",
    "Manual",
    "Emergency",
    "Administrator",
    "PowerUser",
)
_DECRYPT_ROLES = ("Manual", "Emergency", "Administrator", "PowerUser")


def zalando_aws_cli_run(zalando_aws_cli: ExternalBinary, *cmd):
    return zalando_aws_cli.run(
        cmd,
        check=True,
        stdout=subprocess.PIPE,
        forward_context=False,
        forward_namespace=False,
    ).stdout


def encrypt_with_okta(
    env: Environment, account_metadata, kms_keyid, role, strip, plain_text
):
    cmdline = [
        f"--target-account={account_metadata['name']}",
        "encrypt",
    ]
    if not strip:
        cmdline.append("--strip=false")
    if kms_keyid:
        cmdline.append(f"--kms-keyid={kms_keyid}")
    if role:
        cmdline.append(f"--roles={role}")
    cmdline.extend(
        [
            "--",
            plain_text,
        ]
    )

    return zalando_aws_cli_run(env.zalando_aws_cli, *cmdline)


def decrypt_with_okta(env: Environment, role, encrypted_value):
    cmdline = [
        "decrypt",
    ]
    if role:
        cmdline.append(f"--roles={role}")
    cmdline.extend(
        [
            "--",
            encrypted_value,
        ]
    )

    return zalando_aws_cli_run(env.zalando_aws_cli, *cmdline)
