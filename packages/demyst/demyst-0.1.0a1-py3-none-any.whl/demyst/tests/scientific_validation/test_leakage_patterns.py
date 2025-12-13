"""
Scientific Validation Tests: Data Leakage Detection

Validates detection of common Machine Learning data leakage patterns.
"""

import textwrap

import pytest

from demyst.guards.leakage_hunter import LeakageHunter


class TestLeakagePatterns:

    def setup_method(self):
        self.hunter = LeakageHunter()

    def test_preprocessing_before_split(self):
        """Should detect fit_transform before train_test_split."""
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import StandardScaler
            
            def train_model(X, y):
                scaler = StandardScaler()
                # Leakage: Scaling on all data before splitting
                X_scaled = scaler.fit_transform(X)
                
                X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)
                return X_train
        """
        )

        result = self.hunter.analyze(code)
        violations = [v for v in result["violations"] if v["type"] == "preprocessing_leakage"]
        assert len(violations) > 0

    def test_target_encoding_before_cv(self):
        """Should detect target encoding before cross-validation."""
        code = textwrap.dedent(
            """
            from category_encoders import TargetEncoder
            from sklearn.model_selection import cross_val_score
            
            def evaluate_model(X, y):
                # Leakage: Target encoding on full dataset
                encoder = TargetEncoder()
                X_encoded = encoder.fit_transform(X, y)
                
                scores = cross_val_score(model, X_encoded, y, cv=5)
                return scores
        """
        )

        result = self.hunter.analyze(code)
        violations = [v for v in result["violations"] if v["type"] == "target_leakage"]
        assert len(violations) > 0

    def test_test_data_in_training(self):
        """Should detect test data used in training loop."""
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split
            
            def custom_training_loop(X, y):
                X_train, X_test, y_train, y_test = train_test_split(X, y)
                
                model = MyModel()
                # Leakage: Using X_test in fit
                model.fit(X_test, y_test) 
        """
        )

        result = self.hunter.analyze(code)
        # Violations might be 'test_in_training'
        violations = [v for v in result["violations"] if v["type"] == "test_in_training"]
        assert len(violations) > 0

    def test_test_data_in_tuning(self):
        """Should detect test data in hyperparameter tuning."""
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split, GridSearchCV
            
            def tune_model(X, y):
                X_train, X_test, y_train, y_test = train_test_split(X, y)
                
                # Leakage: Tuning on test set
                grid = GridSearchCV(model, param_grid)
                grid.fit(X_test, y_test)
        """
        )

        result = self.hunter.analyze(code)
        violations = [
            v for v in result["violations"] if v["type"] == "test_in_training"
        ]  # Or test_in_tuning
        assert len(violations) > 0

    def test_nlp_vocabulary_leakage(self):
        """Should detect fitting tokenizer on all data."""
        code = textwrap.dedent(
            """
            from keras.preprocessing.text import Tokenizer
            from sklearn.model_selection import train_test_split
            
            def process_text(texts, labels):
                tokenizer = Tokenizer()
                X_train, X_test, y_train, y_test = train_test_split(texts, labels)

                # Leakage: fitting vocab on the held-out test split
                tokenizer.fit_on_texts(X_test)

                # Sequences now inherit taint from X_test
                sequences = tokenizer.texts_to_sequences(X_train + X_test)

                # Using tainted sequences in training should be flagged
                model.fit(sequences, labels)
        """
        )

        result = self.hunter.analyze(code)
        violations = [
            v
            for v in result["violations"]
            if v["type"] in {"test_in_training", "data_contamination"}
        ]
        assert len(violations) > 0

    def test_tf_keras_leakage_using_test_split(self):
        """Should detect Keras model trained on the held-out test split."""
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split

            def train_keras(X, y):
                X_train, X_test, y_train, y_test = train_test_split(X, y)

                model = build_model()
                # Leakage: training on held-out test data
                model.fit(X_test, y_test, epochs=5)
        """
        )

        result = self.hunter.analyze(code)
        violations = [v for v in result["violations"] if v["type"] == "test_in_training"]
        assert len(violations) > 0

    def test_pytorch_dataloader_leakage(self):
        """Should detect DataLoader built on test data and used in training loop."""
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split
            from torch.utils.data import DataLoader, TensorDataset

            def train_with_loader(X, y):
                X_train, X_test, y_train, y_test = train_test_split(X, y)
                train_ds = TensorDataset(X_train, y_train)
                test_ds = TensorDataset(X_test, y_test)

                train_loader = DataLoader(train_ds, batch_size=32)
                test_loader = DataLoader(test_ds, batch_size=32)

                # Leakage: iterate over test_loader inside training function
                for batch in test_loader:
                    model.train_step(batch)
        """
        )

        result = self.hunter.analyze(code)
        violations = [
            v
            for v in result["violations"]
            if v["type"] in {"test_in_training", "data_contamination"}
        ]
        assert len(violations) > 0

    def test_time_series_future_data_leakage(self):
        """Should detect using future (test) data in training loop."""
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split

            def train_on_series(series):
                X_train, X_test = train_test_split(series)

                # Improperly train on held-out future segment
                model.fit(X_test)
        """
        )

        result = self.hunter.analyze(code)
        violations = [v for v in result["violations"] if v["type"] == "test_in_training"]
        assert len(violations) > 0

    def test_pytorch_dataset_leakage(self):
        """Should detect test split used inside training epoch."""
        code = textwrap.dedent(
            """
            from sklearn.model_selection import train_test_split

            def train_epoch(dataset):
                train_data, test_data = train_test_split(dataset)

                # Training loop consumes test_data
                for batch in test_data:
                    model.train_step(batch)
        """
        )

        result = self.hunter.analyze(code)
        violations = [
            v
            for v in result["violations"]
            if v["type"] in {"test_in_training", "data_contamination"}
        ]
        assert len(violations) > 0


class TestLegitimatePatterns:
    """Tests for patterns that should NOT be flagged."""

    def setup_method(self):
        self.hunter = LeakageHunter()

    def test_pipeline_usage(self):
        """Pipelines handle preprocessing correctly."""
        code = textwrap.dedent(
            """
            from sklearn.pipeline import Pipeline
            from sklearn.preprocessing import StandardScaler
            from sklearn.model_selection import train_test_split
            
            def correct_pipeline(X, y):
                X_train, X_test, y_train, y_test = train_test_split(X, y)
                
                pipe = Pipeline([
                    ('scaler', StandardScaler()),
                    ('model', MyModel())
                ])
                # Correct: Pipeline fits scaler only on training data during fit
                pipe.fit(X_train, y_train)
        """
        )

        result = self.hunter.analyze(code)
        assert len(result["violations"]) == 0
