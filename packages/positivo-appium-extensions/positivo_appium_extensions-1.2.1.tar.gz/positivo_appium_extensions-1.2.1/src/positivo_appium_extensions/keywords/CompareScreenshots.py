import os.path
import cv2
import numpy as np
from robot.api.deco import keyword
from ._BaseKeyword import _BaseKeyword
from . import validators


class CompareScreenshots(_BaseKeyword):

    @keyword("Compare Screenshots")
    def compare_screenshots(self, img1, img2, expected="equal", tolerance=0.1):
        """Compares two saved images and validates if they are equal or different based on pixel difference.

        [Arguments]
        img1           Path to the first image file to compare
        img2           Path to the second image file to compare
        expected      Whether images should be 'equal' or 'different' (case-insensitive)
        tolerance     Maximum allowed difference ratio between images (0.0 to 1.0)

        [Return Values]
        None. Passes if comparison matches expectation, fails otherwise.

        [Raises]
        ValueError    If img1/img2 are not strings
                     If image files do not exist
                     If images are corrupt or in invalid format
                     If expected is not 'equal' or 'different'
                     If tolerance is not a number between 0 and 1
        AssertionError    If images are too different when expected='equal'
                         If images are too similar when expected='different'
        """
        # Validate tolerance parameter
        tolerance = float(tolerance)
        validators.validate_type(tolerance, "tolerance", float)
        validators.validate_range(tolerance, "tolerance", 0.0, 1.0)

        # Validate file paths
        validators.validate_type(img1, "img1", str)
        validators.validate_type(img2, "img2", str)

        # Check if files exist
        if not os.path.exists(img1):
            raise ValueError(f"Image file does not exist: {img1}")
        if not os.path.exists(img2):
            raise ValueError(f"Image file does not exist: {img2}")

        # Load images
        image1 = cv2.imread(img1)
        image2 = cv2.imread(img2)

        if image1 is None:
            raise ValueError(f"Could not read image (invalid format or corrupted): {img1}")
        if image2 is None:
            raise ValueError(f"Could not read image (invalid format or corrupted): {img2}")

        # Resize if images have different sizes
        if image1.shape != image2.shape:
            image2 = cv2.resize(image2, (image1.shape[1], image1.shape[0]))

        # Calculate absolute difference
        diff = cv2.absdiff(image1, image2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        non_zero = np.count_nonzero(gray)
        total_pixels = gray.size
        difference_percent = (non_zero / total_pixels) * 100

        # Set limit in %
        limit = tolerance * 100

        # Logging helper
        def log(msg, level="INFO"):
            self._builtin.log_to_console(msg)
            self._builtin.log(msg, level)

        # Validate expected parameter
        expected = expected.lower()
        validators.validate_string_choice(expected, "expected", ["equal", "different"])

        # Evaluate as expected
        if expected == "equal":
            if difference_percent > limit:
                log(f"❌ IMAGES ARE DIFFERENT. Difference: {difference_percent:.2f}% (limit {limit:.2f}%)", "ERROR")
                raise AssertionError(f"Images are different. Difference {difference_percent:.2f}% > limit {limit:.2f}%")
            else:
                log(f"✅ IMAGES ARE EQUAL. Difference: {difference_percent:.2f}% (<= {limit:.2f}%)")

        else:  # expected == "different"
            if difference_percent <= limit:
                log(f"❌ IMAGES ARE TOO SIMILAR. Difference: {difference_percent:.2f}% (limit {limit:.2f}%)", "ERROR")
                raise AssertionError(f"Images are too similar. Difference {difference_percent:.2f}% <= limit {limit:.2f}%")
            else:
                log(f"✅ IMAGES ARE DIFFERENT. Difference: {difference_percent:.2f}% (> {limit:.2f}%)")
