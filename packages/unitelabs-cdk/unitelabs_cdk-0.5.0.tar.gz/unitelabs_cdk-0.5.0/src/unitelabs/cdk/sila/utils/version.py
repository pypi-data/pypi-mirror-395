import packaging.version


def parse_version(version: str) -> str:
    """Parse a PEP 440-compatible version into a valid SiLA 2 version."""

    try:
        v = packaging.version.parse(version)
        parts = [str(v.major), str(v.minor)]
        if v.micro != 0:
            parts.append(str(v.micro))
        sila_version = ".".join(parts)

        suffix_parts = []
        if v.pre:
            suffix_parts.append(f"{v.pre[0]}{v.pre[1]}")
        if v.post:
            suffix_parts.append(f"post{v.post}")
        if v.dev:
            suffix_parts.append(f"dev{v.dev}")
        if v.local:
            suffix_parts.append(v.local.replace(".", "_"))

        if suffix_parts:
            sila_version += "_" + "_".join(suffix_parts)

        return sila_version
    except packaging.version.InvalidVersion:
        msg = f"Invalid version format: '{version}'."
        raise ValueError(msg) from None
