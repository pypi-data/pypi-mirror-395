import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
from veox.plotting import plot_evolution

class TestPlotting(unittest.TestCase):
    def setUp(self):
        self.history_data = {
            "generations": [
                {"gen": 0, "min_fitness": 0.5, "avg_fitness": 0.6, "max_fitness": 0.7},
                {"gen": 1, "min_fitness": 0.6, "avg_fitness": 0.7, "max_fitness": 0.8},
                {"gen": 2, "min_fitness": 0.7, "avg_fitness": 0.8, "max_fitness": 0.9},
            ],
            "individuals": [
                {"generation": 0, "fitness": 0.6},
                {"generation": 0, "fitness": 0.7},
                {"generation": 1, "fitness": 0.8},
            ]
        }
        
    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.savefig")
    def test_plot_evolution(self, mock_savefig, mock_show):
        """Test that plot_evolution runs without error."""
        plot_evolution(self.history_data, title="Test Plot")
        mock_show.assert_called_once()
        
    @patch("matplotlib.pyplot.show")
    @patch("matplotlib.pyplot.savefig")
    def test_plot_evolution_save(self, mock_savefig, mock_show):
        """Test sending plot to file."""
        plot_evolution(self.history_data, save_path="test_plot.png")
        mock_savefig.assert_called_with("test_plot.png")
        
    def test_empty_history(self):
        """Test handling of empty history."""
        # Should just return/log warning, no exception
        plot_evolution({})
        plot_evolution({"generations": []})

if __name__ == "__main__":
    unittest.main()
