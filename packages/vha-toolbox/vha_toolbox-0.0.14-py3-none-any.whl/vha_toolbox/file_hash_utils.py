import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Optional, Union


def compute_file_hash(
    file_path: Union[str, Path],
    extra_paths: Optional[Iterable[Union[str, Path]]] = None
) -> str:
    """
    Compute a stable SHA-256 hash for a file, optionally combined with other files.
    Only the first 8 hexadecimal characters of the hash are returned.

    Args:
        file_path (str | Path): The path to the primary file.
        extra_paths (list[str | Path] | None, optional): Additional file paths whose
            contents should contribute to the hash. Defaults to None.

    Returns:
        str: The first 8 characters of the resulting SHA-256 hash.

    Example:
        >>> compute_file_hash("image.jpg")
        'a94f2c1b'
        >>> compute_file_hash("image.jpg", ["frame.png"])
        'e12d99fa'

    Raises:
        FileNotFoundError: If the primary file does not exist.
        ValueError: If a provided path is invalid.
    """

    def _update_hasher(p: Path, hasher_obj: hashlib._hashlib.HASH):
        """Internal helper to update the hash with the content of a file."""
        if not p.exists() or not p.is_file():
            raise FileNotFoundError(f"Path '{p}' not found or not a file.")

        with p.open("rb") as f:
            while chunk := f.read(8192):
                hasher_obj.update(chunk)

    # Normalize main path
    main_path = Path(file_path)

    if not main_path.exists():
        raise FileNotFoundError(f"Path '{main_path}' not found.")

    hasher = hashlib.sha256()

    # Hash the primary file
    _update_hasher(main_path, hasher)

    # Hash extra files if provided
    if extra_paths:
        for ep in extra_paths:
            if ep is None:
                continue
            path = Path(ep)
            _update_hasher(path, hasher)

    # Return short hash
    return hasher.hexdigest()[:8]


def compute_stable_hash(
    values: Any,
    prefix: Optional[str] = None,
    length: int = 8
) -> str:
    """
    Compute a stable SHA-256 hash from any list of Python values.

    - Supporte : str, int, float, bool, None
    - Supporte : dicts (triés pour stabilité)
    - Supporte : listes, tuples, sets
    - Supporte : Path
    - Supporte : bytes / bytearray
    - Supporte : objets arbitraires en fallback repr()

    Args:
        values (Any): Single value or iterable of values.
        prefix (str | None): Optionnel, ajouté avant le hash final (ex.: "img_", "row_").
        length (int): Nombre de caractères du hash retourné (par défaut : 8).

    Returns:
        str: Short stable SHA-256 hash.

    Example:
        >>> compute_stable_hash(["image1.png", 3000, {"x": 12}])
        '9f3ac1d2'

        >>> compute_stable_hash("hello", prefix="p_")
        'p_a1b2c3d4'
    """

    def normalize(v):
        """Normalize a Python value into a deterministic JSON-serializable value."""
        if v is None:
            return None

        # Path → string
        if isinstance(v, Path):
            return str(v)

        # bytes → hex string
        if isinstance(v, (bytes, bytearray)):
            return v.hex()

        # dict → trié pour stabilité
        if isinstance(v, dict):
            return {k: normalize(v[k]) for k in sorted(v)}

        # list / tuple / set → liste triée si set
        if isinstance(v, (list, tuple)):
            return [normalize(x) for x in v]

        if isinstance(v, set):
            return sorted(normalize(x) for x in v)

        # primitive types
        if isinstance(v, (int, float, str, bool)):
            return v

        # fallback pour objets arbitraires
        return repr(v)

    # Si values n'est pas iterable → l’envelopper dans une liste
    if not isinstance(values, (list, tuple, set)):
        values = [values]

    # Normalisation profonde
    norm = normalize(values)

    # Conversion en JSON stable
    encoded = json.dumps(norm, sort_keys=True, separators=(",", ":")).encode("utf-8")

    # Hash
    digest = hashlib.sha256(encoded).hexdigest()[:length]

    return f"{prefix}{digest}" if prefix else digest
