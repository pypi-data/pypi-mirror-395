import math

RATIO_TOL = 0.05  # tolérance par défaut


def _ratio(w, h):
    return w / h if h else 0.0


def should_rotate_by_ratio(
    img,
    frame_img,
    frame_target_ratio: float,
    img_target_ratio: float,
    tol: float = RATIO_TOL,
    require_orientation_flip: bool = True,
):
    """
    Détermine si l'on doit tourner le cadre en fonction :

    - du ratio réel du cadre
    - du ratio réel de l'image
    - des ratios cibles souhaités (ex.: 2/3, 3/2, carré, etc.)
    - d'une tolérance
    - et éventuellement d'un changement de sens (portrait -> paysage)

    Args:
        img (PIL.Image.Image): L'image originale.
        frame_img (PIL.Image.Image): L'image du cadre.
        frame_target_ratio (float): Le ratio attendu pour le cadre (ex.: 2/3).
        img_target_ratio (float): Le ratio attendu pour l'image (ex.: 3/2).
        tol (float): Tolérance relative pour comparer les ratios.
        require_orientation_flip (bool): Si True, impose que l'un soit portrait et l'autre paysage.

    Returns:
        bool: True si le cadre doit être tourné, False sinon.
    """
    pw, ph = img.size
    fw, fh = frame_img.size

    img_r = _ratio(pw, ph)
    frame_r = _ratio(fw, fh)

    # cadre carré → jamais de rotation
    if math.isclose(frame_r, 1.0, rel_tol=tol):
        return False

    # vérifier le ratio du cadre
    frame_match = math.isclose(frame_r, frame_target_ratio, rel_tol=tol)

    # vérifier le ratio de l’image
    img_match = math.isclose(img_r, img_target_ratio, rel_tol=tol)

    if not (frame_match and img_match):
        return False

    # si orientation doit changer (portrait → paysage ou inverse)
    if require_orientation_flip:
        frame_is_portrait = fh > fw
        img_is_landscape = pw > ph
        orientation_ok = frame_is_portrait and img_is_landscape
        return orientation_ok

    return True
