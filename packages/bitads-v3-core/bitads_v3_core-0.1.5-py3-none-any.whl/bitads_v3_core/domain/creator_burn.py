import math
from typing import List, Tuple, Optional

def apply_creator_burn(
    uids: List[int],
    miner_scores: List[float],
    creator_uid: Optional[int],
    burn_percentage: float,
) -> Tuple[List[int], List[float]]:
    """
    Apply creator emissions burning to miner scores.
    
    This function injects creator emissions burning into the scoring process by:
    1. Normalizing miner scores (handling invalid values)
    2. Applying burn percentage to split weight between creator and miners
    3. Returning final UIDs and weights that sum approximately to 1.0
    
    Args:
        uids: List of miner UIDs (ints) currently considered by the subnet
        miner_scores: List of floats (same length as uids) representing miner scores
        creator_uid: Creator/owner UID (None if not found or burn disabled)
        burn_percentage: Float in [0.0, 100.0], desired fraction of emissions to burn
    
    Returns:
        Tuple of (final_uids, final_weights), where:
            - final_uids: List of UIDs including the creator UID (if found and burn enabled)
            - final_weights: List[float] in [0.0, 1.0], same length as final_uids
            - sum(final_weights) ≈ 1.0 (or 0.0 if all scores invalid)
    
    Behavior:
        - If creator_uid is None: burn is skipped, returns normalized miner weights
        - If all miner scores are invalid (zero/NaN/inf): returns zero weights
        - If burn_percentage == 0.0: no burn applied, all weight goes to miners
        - If creator UID already in uids: overwrites its weight with burn weight
        - If creator UID not in uids: appends it with burn weight
    """
    # Validate inputs
    if len(uids) != len(miner_scores):
        raise ValueError(f"uids and miner_scores must have same length, got {len(uids)} and {len(miner_scores)}")
    
    if not uids:
        return ([], [])
    
    # Clamp burn_percentage to valid range
    burn_percentage = max(0.0, min(100.0, burn_percentage))
    burn_prop = burn_percentage / 100.0
    miner_prop = 1.0 - burn_prop
    
    # Check if creator UID is in the list (needed to exclude it from normalization if present)
    creator_in_list = creator_uid is not None and creator_uid in uids
    
    # Clean miner scores
    cleaned_scores = []
    for score in miner_scores:
        # Replace NaN or non-finite entries with 0.0
        if not math.isfinite(score):
            cleaned_scores.append(0.0)
        # Clamp negative values to 0.0
        elif score < 0.0:
            cleaned_scores.append(0.0)
        else:
            cleaned_scores.append(score)
    
    # If creator is in the list, exclude its score from normalization
    # (we want creator weight to represent burn only, not its miner score)
    if creator_in_list:
        creator_index = uids.index(creator_uid)
        # Compute total score excluding creator
        total_score = sum(score for i, score in enumerate(cleaned_scores) if i != creator_index)
    else:
        # Compute total score from all scores
        total_score = sum(cleaned_scores)
    
    # Handle case where all scores are invalid
    if total_score <= 0.0:
        # No valid miner signal - return zero weights
        if burn_prop > 0.0 and creator_uid is not None:
            # Creator found: return zeros for all miners, zero for creator
            final_uids = list(uids)
            final_weights = [0.0] * len(uids)
            if creator_uid not in final_uids:
                final_uids.append(creator_uid)
                final_weights.append(0.0)
            return (final_uids, final_weights)
        # No burn or creator not found: return zeros
        return (list(uids), [0.0] * len(uids))
    
    # Normalize miner scores to get base weights (sum to 1.0)
    # If creator is in list, exclude its score from normalization
    if creator_in_list:
        creator_index = uids.index(creator_uid)
        base_miner_weights = []
        for i, score in enumerate(cleaned_scores):
            if i == creator_index:
                # Creator's base weight is 0 (will be overwritten with burn weight)
                base_miner_weights.append(0.0)
            else:
                base_miner_weights.append(score / total_score)
    else:
        base_miner_weights = [score / total_score for score in cleaned_scores]
    
    # If burn is disabled, return normalized miner weights
    if burn_prop == 0.0:
        return (list(uids), base_miner_weights)
    
    # Burn is enabled - if creator not found, skip burn and return normalized miner weights
    if creator_uid is None:
        return (list(uids), base_miner_weights)
    
    # Apply burn: scale miner weights by miner_prop
    miner_weights_final = [w * miner_prop for w in base_miner_weights]
    creator_weight_final = burn_prop
    
    # Construct final vectors
    final_uids = list(uids)
    final_weights = list(miner_weights_final)
    
    if creator_in_list:
        # Creator UID already present - overwrite its weight with burn weight
        creator_index = final_uids.index(creator_uid)
        final_weights[creator_index] = creator_weight_final
    else:
        # Creator UID not present - append it
        final_uids.append(creator_uid)
        final_weights.append(creator_weight_final)
    
    # Normalize to ensure sum ≈ 1.0 (handle floating-point issues)
    total = sum(final_weights)
    if total > 0.0 and abs(total - 1.0) > 1e-9:
        final_weights = [w / total for w in final_weights]
    
    # Ensure all weights are in [0.0, 1.0] (defensive clamp)
    final_weights = [max(0.0, min(1.0, w)) for w in final_weights]
    
    return (final_uids, final_weights)

