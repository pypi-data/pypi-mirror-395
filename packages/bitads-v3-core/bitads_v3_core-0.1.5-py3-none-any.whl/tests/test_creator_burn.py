"""
Test cases for creator emissions burning mechanism.
"""
import unittest
import math

from bitads_v3_core.domain.creator_burn import apply_creator_burn


TOLERANCE = 1e-9


class TestCreatorBurn(unittest.TestCase):
    """Test cases for apply_creator_burn function."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Creator UID for testing
        self.creator_uid = 99  # Creator UID (different from miners)
    
    def test_no_burn_burn_percentage_zero(self):
        """
        Test case: burn_percentage = 0.0 (no burn).
        Expected: All weight goes to miners, normalized.
        """
        uids = [0, 1, 2]
        miner_scores = [0.5, 0.3, 0.2]
        
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=None,
            burn_percentage=0.0
        )
        
        # Should return original uids
        self.assertEqual(final_uids, uids)
        
        # Weights should be normalized (sum to 1.0)
        self.assertAlmostEqual(sum(final_weights), 1.0, delta=TOLERANCE)
        
        # Weights should match normalized scores
        total = sum(miner_scores)
        expected_weights = [s / total for s in miner_scores]
        for i, (actual, expected) in enumerate(zip(final_weights, expected_weights)):
            self.assertAlmostEqual(actual, expected, delta=TOLERANCE, 
                                 msg=f"Weight {i} mismatch")
    
    def test_burn_50_percent(self):
        """
        Test case: burn_percentage = 50.0 (half burn, half miners).
        Expected: 50% to creator, 50% distributed among miners.
        """
        uids = [0, 1, 2]
        miner_scores = [0.5, 0.3, 0.2]
        total_score = sum(miner_scores)
        
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=self.creator_uid,
            burn_percentage=50.0
        )
        
        # Should include creator UID
        self.assertIn(self.creator_uid, final_uids)
        
        # Weights should sum to 1.0
        self.assertAlmostEqual(sum(final_weights), 1.0, delta=TOLERANCE)
        
        # Creator should have 0.5 weight
        creator_index = final_uids.index(self.creator_uid)
        self.assertAlmostEqual(final_weights[creator_index], 0.5, delta=TOLERANCE)
        
        # Miners should share the remaining 0.5 proportionally
        miner_weights = [w for i, w in enumerate(final_weights) if final_uids[i] != self.creator_uid]
        miner_weights_sum = sum(miner_weights)
        self.assertAlmostEqual(miner_weights_sum, 0.5, delta=TOLERANCE)
        
        # Check proportional distribution
        base_weights = [s / total_score for s in miner_scores]
        for i, uid in enumerate(uids):
            miner_index = final_uids.index(uid)
            expected_weight = base_weights[i] * 0.5  # Scaled by miner_prop
            self.assertAlmostEqual(final_weights[miner_index], expected_weight, 
                                 delta=TOLERANCE, msg=f"Miner {uid} weight mismatch")
    
    def test_creator_uid_already_in_list(self):
        """
        Test case: Creator UID is already in the uids list.
        Expected: Creator's weight is overwritten with burn weight.
        """
        uids = [0, 1, self.creator_uid]  # Creator UID already present
        miner_scores = [0.5, 0.3, 0.2]  # Last score is for creator (will be overwritten)
        
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=self.creator_uid,
            burn_percentage=30.0
        )
        
        # UIDs should remain the same (no new UID added)
        self.assertEqual(len(final_uids), len(uids))
        self.assertEqual(set(final_uids), set(uids))
        
        # Creator's weight should be burn weight (0.3), not based on its score
        creator_index = final_uids.index(self.creator_uid)
        self.assertAlmostEqual(final_weights[creator_index], 0.3, delta=TOLERANCE)
        
        # Weights should sum to 1.0
        self.assertAlmostEqual(sum(final_weights), 1.0, delta=TOLERANCE)
        
        # Miners should share 70% proportionally
        miner_indices = [i for i, uid in enumerate(final_uids) if uid != self.creator_uid]
        miner_weights_sum = sum(final_weights[i] for i in miner_indices)
        self.assertAlmostEqual(miner_weights_sum, 0.7, delta=TOLERANCE)
    
    def test_creator_not_found_skip_burn(self):
        """
        Test case: Creator hotkey not found in metagraph.
        Expected: Burn is skipped gracefully, returns normalized miner weights.
        """
        uids = [0, 1, 2]
        miner_scores = [0.5, 0.3, 0.2]
        
        # Creator not found (pass None)
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=None,  # Creator not found
            burn_percentage=50.0  # Even with burn enabled, should skip
        )
        
        # Should return original uids (no creator added)
        self.assertEqual(final_uids, uids)
        
        # Weights should be normalized miner weights (no burn)
        self.assertAlmostEqual(sum(final_weights), 1.0, delta=TOLERANCE)
        total = sum(miner_scores)
        expected_weights = [s / total for s in miner_scores]
        for i, (actual, expected) in enumerate(zip(final_weights, expected_weights)):
            self.assertAlmostEqual(actual, expected, delta=TOLERANCE)
    
    def test_all_miner_scores_zero(self):
        """
        Test case: All miner scores are zero or invalid.
        Expected: All weights are 0.0.
        """
        uids = [0, 1, 2]
        miner_scores = [0.0, 0.0, 0.0]
        
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=self.creator_uid,
            burn_percentage=50.0
        )
        
        # All weights should be 0.0
        self.assertEqual(final_weights, [0.0] * len(final_weights))
        
        # Creator UID should be included if found
        if self.creator_uid in final_uids:
            creator_index = final_uids.index(self.creator_uid)
            self.assertEqual(final_weights[creator_index], 0.0)
    
    def test_invalid_scores_nan_inf(self):
        """
        Test case: Miner scores contain NaN or inf values.
        Expected: Invalid values are replaced with 0.0, then normalized.
        """
        uids = [0, 1, 2]
        miner_scores = [0.5, float('nan'), float('inf')]
        
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=None,
            burn_percentage=0.0
        )
        
        # Only first miner should have weight (others are 0.0)
        self.assertAlmostEqual(final_weights[0], 1.0, delta=TOLERANCE)
        self.assertAlmostEqual(final_weights[1], 0.0, delta=TOLERANCE)
        self.assertAlmostEqual(final_weights[2], 0.0, delta=TOLERANCE)
        self.assertAlmostEqual(sum(final_weights), 1.0, delta=TOLERANCE)
    
    def test_negative_scores_clamped(self):
        """
        Test case: Negative scores are clamped to 0.0.
        Expected: Negative values become 0.0, then normalized.
        """
        uids = [0, 1, 2]
        miner_scores = [0.5, -0.1, 0.3]
        
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=None,
            burn_percentage=0.0
        )
        
        # Negative score should be treated as 0.0
        # Only miners 0 and 2 should have weight
        total = 0.5 + 0.3  # Sum of valid scores
        self.assertAlmostEqual(final_weights[0], 0.5 / total, delta=TOLERANCE)
        self.assertAlmostEqual(final_weights[1], 0.0, delta=TOLERANCE)
        self.assertAlmostEqual(final_weights[2], 0.3 / total, delta=TOLERANCE)
        self.assertAlmostEqual(sum(final_weights), 1.0, delta=TOLERANCE)
    
    def test_burn_percentage_clamped(self):
        """
        Test case: burn_percentage outside [0, 100] is clamped.
        Expected: Values are clamped to valid range.
        """
        uids = [0, 1]
        miner_scores = [0.5, 0.5]
        
        # Test negative value
        _, weights_neg = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=None,
            burn_percentage=-10.0
        )
        self.assertAlmostEqual(sum(weights_neg), 1.0, delta=TOLERANCE)
        
        # Test value > 100
        _, weights_over = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=self.creator_uid,
            burn_percentage=150.0
        )
        # Should be clamped to 100%, so all weight to creator
        self.assertIn(self.creator_uid, _)
        creator_index = _.index(self.creator_uid)
        self.assertAlmostEqual(weights_over[creator_index], 1.0, delta=TOLERANCE)
    
    def test_empty_uids_list(self):
        """
        Test case: Empty uids list.
        Expected: Returns empty lists.
        """
        final_uids, final_weights = apply_creator_burn(
            uids=[],
            miner_scores=[],
            creator_uid=self.creator_uid,
            burn_percentage=50.0
        )
        
        self.assertEqual(final_uids, [])
        self.assertEqual(final_weights, [])
    
    def test_burn_100_percent(self):
        """
        Test case: burn_percentage = 100.0 (all burn).
        Expected: All weight to creator, zero to miners.
        """
        uids = [0, 1, 2]
        miner_scores = [0.5, 0.3, 0.2]
        
        final_uids, final_weights = apply_creator_burn(
            uids=uids,
            miner_scores=miner_scores,
            creator_uid=self.creator_uid,
            burn_percentage=100.0
        )
        
        # Creator should have all weight
        creator_index = final_uids.index(self.creator_uid)
        self.assertAlmostEqual(final_weights[creator_index], 1.0, delta=TOLERANCE)
        
        # All miners should have zero weight
        for i, uid in enumerate(final_uids):
            if uid != self.creator_uid:
                self.assertAlmostEqual(final_weights[i], 0.0, delta=TOLERANCE)
        
        self.assertAlmostEqual(sum(final_weights), 1.0, delta=TOLERANCE)
    
    def test_length_mismatch_raises_error(self):
        """
        Test case: uids and miner_scores have different lengths.
        Expected: Raises ValueError.
        """
        uids = [0, 1, 2]
        miner_scores = [0.5, 0.3]  # Different length
        
        with self.assertRaises(ValueError):
            apply_creator_burn(
                uids=uids,
                miner_scores=miner_scores,
                creator_uid=None,
                burn_percentage=0.0
            )


if __name__ == "__main__":
    unittest.main()

