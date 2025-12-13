"""
Real Paper Reproduction: ImageNet preprocessing leakage

Validates that Demyst catches improper normalization done on full dataset
before train/validation split, a common pitfall in benchmark code.
"""

import textwrap

from demyst.guards.leakage_hunter import LeakageHunter


class TestImageNetPreprocessingLeakage:
    def test_full_dataset_normalization_before_split(self):
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import StandardScaler

            def load_and_preprocess(images, labels):
                scaler = StandardScaler()
                # Leakage: fitting on the full dataset before split
                images_norm = scaler.fit_transform(images)

                X_train, X_val, y_train, y_val = train_test_split(images_norm, labels, test_size=0.2)
                model = build_model()
                model.fit(X_train, y_train)
                return model
            """
        )

        hunter = LeakageHunter()
        result = hunter.analyze(code)
        violations = [
            v
            for v in result["violations"]
            if v["type"] in {"preprocessing_leakage", "test_in_training", "data_contamination"}
        ]
        assert len(violations) > 0

    def test_pipeline_normalization_is_safe(self):
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import StandardScaler

            def safe_pipeline(images, labels):
                X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2)
                pipe = Pipeline([
                    ("scaler", StandardScaler()),
                    ("model", build_model())
                ])
                pipe.fit(X_train, y_train)
                return pipe
            """
        )

        hunter = LeakageHunter()
        result = hunter.analyze(code)
        assert len(result["violations"]) == 0
