# One late observation, two branches

[Download the offline explorer ZIP](https://raw.githubusercontent.com/DannyExperiments/strong-extension-posterior-smoothing/v1.0.0/visualization/strong-extension-posterior-smoothing-explorer.zip). Extract it and open index.html. Choose a formula, set the two literal emission probabilities, and rotate the diagram. For each fixed pair of endpoints the explorer routes every positive unit to the larger available value and every negative unit to the smaller. The readouts are exact fractions.

The diagrams use the prior one quarter and the original unsmoothed rows. The two worked formulas each have one variable and two clauses. For x AND x the branch likelihoods can be 3/4 and 1/4, giving posterior 1/2. For x AND NOT x the best likelihoods yield posterior 7/16. Teal marks the positive branch, orange marks the negative branch, and gold marks literal emissions. The diagram shows selected routes. Section 4 of the paper proves the general strict-positive comparison.

To regenerate the animation, run the following with Python 3 and Pillow already installed.

    python3 visualization/render.py

Arial is the local default. Set Q432_FONT and Q432_BOLD_FONT to paths to suitable fonts on other systems.
