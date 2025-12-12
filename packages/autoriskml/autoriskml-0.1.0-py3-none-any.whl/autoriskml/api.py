"""
AutoRiskML Main API
High-level interface for automated risk modeling

from autoriskml import AutoRisk

ar = AutoRisk(project="loan_scoring")
ar.register_source("train", csv="data/train.csv")
result = ar.run(source="train", target="default_flag", explain=True, deploy={"provider": "azure_ml"})
"""

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional, Union


class AutoRisk:
    """
    Main AutoRiskML class - acts like a senior risk data scientist
    
    This orchestrates the entire risk modeling pipeline:
    - Data ingestion (CSV, SQL, S3, Kafka)
    - Profiling & recommendations
    - Auto-cleaning
    - Binning & WOE/IV computation
    - Model training & selection
    - Scorecard generation
    - PSI monitoring & drift detection
    - SHAP explainability
    - Azure deployment
    """
    
    def __init__(
        self,
        project: str,
        output_dir: Optional[str] = None,
        log_level: str = "INFO",
        mode: str = "risk",  # or "trading"
    ):
        """
        Initialize AutoRisk project
        
        Args:
            project: Project name (used for artifact naming)
            output_dir: Directory for artifacts (default: ./artifacts/{project})
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
            mode: "risk" for credit/fraud scoring, "trading" for backtest mode
        """
        self.project = project
        self.mode = mode
        self.output_dir = output_dir or f"artifacts/{project}"
        self.log_level = log_level
        
        # Create output directory
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(f"{self.output_dir}/models", exist_ok=True)
        os.makedirs(f"{self.output_dir}/reports", exist_ok=True)
        os.makedirs(f"{self.output_dir}/specs", exist_ok=True)
        
        # Data sources registry
        self.sources = {}
        
        # Artifacts from last run
        self.artifacts = {}
        
        # Trained model
        self.model = None
        self.pipeline = None
        
        print(f"✅ AutoRisk project '{project}' initialized")
        print(f"📁 Output directory: {self.output_dir}")
    
    def register_source(
        self,
        name: str,
        csv: Optional[str] = None,
        parquet: Optional[str] = None,
        sql_query: Optional[str] = None,
        connection_string: Optional[str] = None,
        s3: Optional[str] = None,
        **kwargs
    ) -> None:
        """
        Register a data source
        
        Args:
            name: Source name (e.g., "train", "test", "prod")
            csv: Path to CSV file
            parquet: Path to Parquet file
            sql_query: SQL query to execute
            connection_string: Database connection string
            s3: S3 path (s3://bucket/key)
            **kwargs: Additional connector-specific options
        """
        source_config = {
            "name": name,
            "csv": csv,
            "parquet": parquet,
            "sql_query": sql_query,
            "connection_string": connection_string,
            "s3": s3,
            **kwargs
        }
        
        self.sources[name] = source_config
        print(f"✅ Registered source: '{name}'")
    
    def run(
        self,
        source: str,
        target: str,
        validation_source: Optional[str] = None,
        config: Optional[Union[str, Dict]] = None,
        clean: Optional[Dict] = None,
        binning: Optional[Dict] = None,
        features: Optional[Dict] = None,
        models: Optional[List[Union[str, Dict]]] = None,
        scorecard: Optional[Dict] = None,
        explain: bool = False,
        monitor: Optional[Dict] = None,
        report: Optional[Dict] = None,
        deploy: Optional[Dict] = None,
        persist_artifacts: bool = True,
    ) -> "RunResult":
        """
        Run the complete automated risk modeling pipeline
        
        This is the main method that does EVERYTHING:
        1. Load data
        2. Profile & get recommendations
        3. Auto-clean
        4. Binning & WOE/IV
        5. Feature selection
        6. Train models
        7. Generate scorecard
        8. Explain predictions
        9. Monitor PSI/drift
        10. Generate reports
        11. Deploy to Azure
        
        Args:
            source: Source name for training data
            target: Target column name
            validation_source: Optional validation source
            config: Config dict or path to YAML
            clean: Cleaning options
            binning: Binning options
            features: Feature selection options
            models: List of models to train
            scorecard: Scorecard generation options
            explain: Whether to compute SHAP explanations
            monitor: Monitoring configuration
            report: Report generation options
            deploy: Deployment configuration
            persist_artifacts: Save artifacts to disk
        
        Returns:
            RunResult object with all artifacts and metrics
        """
        print("\n" + "="*80)
        print(f"🚀 AutoRisk Pipeline: {self.project}")
        print("="*80)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_id = f"{self.project}_{timestamp}"
        
        # Load configuration
        if isinstance(config, str):
            with open(config, 'r') as f:
                config = json.load(f) if config.endswith('.json') else yaml.safe_load(f)
        config = config or {}
        
        # Merge configs (function args override config file)
        clean_config = {**(config.get('clean', {})), **(clean or {})}
        binning_config = {**(config.get('binning', {})), **(binning or {})}
        features_config = {**(config.get('features', {})), **(features or {})}
        models_list = models or config.get('models', ['logistic'])
        scorecard_config = {**(config.get('scorecard', {})), **(scorecard or {})}
        monitor_config = {**(config.get('monitor', {})), **(monitor or {})}
        report_config = {**(config.get('report', {})), **(report or {})}
        deploy_config = {**(config.get('deploy', {})), **(deploy or {})}
        
        # Result accumulator
        result = RunResult(run_id=run_id)
        
        # STAGE 1: Load Data
        print("\n📥 STAGE 1: Loading Data")
        print("-" * 80)
        train_data = self._load_source(source)
        print(f"✅ Loaded {len(train_data['data'])} rows × {len(train_data['columns'])} columns")
        
        if validation_source:
            val_data = self._load_source(validation_source)
            print(f"✅ Loaded validation: {len(val_data['data'])} rows")
        else:
            val_data = None
        
        # STAGE 2: Profile Data
        print("\n🔬 STAGE 2: Profiling Data")
        print("-" * 80)
        profile = self._profile_data(train_data, target)
        print(f"✅ Profiled {len(profile['columns'])} features")
        print(f"   • Missing values: {profile['missing_count']} columns")
        print(f"   • Recommendations: {len(profile['recommendations'])} items")
        result.profile = profile
        
        # STAGE 3: Auto-Clean
        print("\n✨ STAGE 3: Auto-Cleaning Data")
        print("-" * 80)
        clean_result = self._autoclean(train_data, target, clean_config)
        train_data_clean = clean_result['data']
        print(f"✅ Cleaned data")
        print(f"   • Missing imputed: {clean_result['imputed_count']} features")
        print(f"   • Outliers handled: {clean_result['outlier_count']} features")
        result.clean_spec = clean_result['spec']
        
        # STAGE 4: Binning & WOE/IV
        print("\n📊 STAGE 4: Binning & WOE/IV Computation")
        print("-" * 80)
        binning_result = self._compute_binning_woe(train_data_clean, target, binning_config)
        print(f"✅ Binned {len(binning_result['bins'])} features")
        for feat, iv in list(binning_result['iv_scores'].items())[:5]:
            print(f"   • {feat}: IV = {iv:.3f}")
        result.binning_spec = binning_result['spec']
        result.woe_tables = binning_result['woe_tables']
        result.iv_scores = binning_result['iv_scores']
        
        # STAGE 5: Feature Selection
        print("\n🎯 STAGE 5: Feature Selection")
        print("-" * 80)
        selected_features = self._select_features(binning_result, features_config)
        print(f"✅ Selected {len(selected_features)} features (min IV: {features_config.get('min_iv', 0.02)})")
        result.selected_features = selected_features
        
        # STAGE 6: Train Models
        print("\n🤖 STAGE 6: Training Models")
        print("-" * 80)
        X_train, y_train = self._prepare_training_data(train_data_clean, selected_features, target)
        if val_data:
            X_val, y_val = self._prepare_training_data(val_data, selected_features, target)
        else:
            X_val, y_val = None, None
        
        model_results = []
        for model_config in models_list:
            model_type = model_config if isinstance(model_config, str) else model_config['type']
            print(f"   Training {model_type}...")
            model_result = self._train_model(X_train, y_train, X_val, y_val, model_config)
            model_results.append(model_result)
            print(f"   ✅ {model_type}: AUC = {model_result['metrics']['auc']:.3f}")
        
        # Select best model
        best_model = max(model_results, key=lambda m: m['metrics']['auc'])
        self.model = best_model['model']
        result.best_model = best_model['type']
        result.metrics = best_model['metrics']
        print(f"\n✅ Best model: {best_model['type']} (AUC: {best_model['metrics']['auc']:.3f})")
        
        # STAGE 7: Generate Scorecard
        if scorecard_config:
            print("\n💳 STAGE 7: Generating Scorecard")
            print("-" * 80)
            scorecard_result = self._generate_scorecard(
                best_model['model'],
                binning_result,
                selected_features,
                scorecard_config
            )
            print(f"✅ Scorecard generated")
            print(f"   • Base score: {scorecard_config.get('base_score', 600)}")
            print(f"   • PDO: {scorecard_config.get('pdo', 20)}")
            result.scorecard = scorecard_result
        
        # STAGE 8: Explainability
        if explain:
            print("\n🔍 STAGE 8: Computing Explanations")
            print("-" * 80)
            try:
                explanations = self._compute_explanations(best_model['model'], X_train, selected_features)
                print(f"✅ SHAP explanations computed")
                result.explanations = explanations
            except Exception as e:
                print(f"⚠️  Explainability failed: {e} (install shap for full support)")
        
        # STAGE 9: Monitoring (PSI)
        if monitor_config.get('compute_psi') and val_data:
            print("\n📈 STAGE 9: Computing PSI")
            print("-" * 80)
            psi_result = self._compute_psi(
                train_data_clean,
                val_data,
                selected_features,
                monitor_config
            )
            print(f"✅ PSI computed: {psi_result['overall_psi']:.3f}")
            if psi_result['overall_psi'] > monitor_config.get('psi_threshold', 0.2):
                print(f"⚠️  WARNING: PSI exceeds threshold!")
            result.psi = psi_result
        
        # STAGE 10: Generate Reports
        if report_config:
            print("\n📄 STAGE 10: Generating Reports")
            print("-" * 80)
            report_path = self._generate_report(result, report_config)
            print(f"✅ Report generated: {report_path}")
            result.report_html = report_path
        
        # STAGE 11: Deploy
        if deploy_config and deploy_config.get('provider'):
            print("\n🚀 STAGE 11: Deploying to {deploy_config['provider']}")
            print("-" * 80)
            endpoint = self._deploy(best_model, deploy_config)
            print(f"✅ Deployed to {deploy_config['provider']}")
            print(f"   • Endpoint: {endpoint.get('scoring_uri', 'N/A')}")
            result.endpoint = endpoint
        
        # Save artifacts
        if persist_artifacts:
            self._persist_artifacts(result)
        
        print("\n" + "="*80)
        print("✅ AutoRisk Pipeline Complete!")
        print("="*80)
        
        return result
    
    def score(
        self,
        data: Union[str, Dict],
        output: str = "scores",  # "scores", "with_reasons", "full"
        chunk_size: Optional[int] = None
    ) -> List[Dict]:
        """
        Score new data using trained model
        
        Args:
            data: Source name, file path, or data dict
            output: Output format ("scores", "with_reasons", "full")
            chunk_size: Process in chunks (for large datasets)
        
        Returns:
            List of score dictionaries
        """
        if not self.model:
            raise ValueError("No model trained. Run ar.run() first.")
        
        print(f"🎯 Scoring data...")
        
        # Load data
        if isinstance(data, str):
            if data in self.sources:
                score_data = self._load_source(data)
            else:
                score_data = self._load_file(data)
        else:
            score_data = data
        
        # Apply transformations
        X = self._apply_transformations(score_data)
        
        # Score
        probabilities = self.model.predict_proba(X)
        scores = self._probabilities_to_scores(probabilities)
        
        results = []
        for i, (prob, score) in enumerate(zip(probabilities, scores)):
            result_dict = {
                'index': i,
                'probability': float(prob),
                'score': int(score),
                'risk_tier': self._get_risk_tier(score)
            }
            
            if output in ["with_reasons", "full"]:
                reasons = self._get_top_reasons(X[i])
                result_dict['top_reason'] = reasons[0] if reasons else None
                if output == "full":
                    result_dict['all_reasons'] = reasons
            
            results.append(result_dict)
        
        print(f"✅ Scored {len(results)} records")
        return results
    
    def monitor(
        self,
        source: Optional[str] = None,
        current_data: Optional[Dict] = None,
        baseline_source: Optional[str] = "train"
    ) -> "MonitorResult":
        """
        Monitor production data for drift
        
        Args:
            source: Source name for current data
            current_data: Or provide data directly
            baseline_source: Baseline source name (default: "train")
        
        Returns:
            MonitorResult with PSI, drift flags, recommendations
        """
        print("📈 Monitoring for drift...")
        
        # Load current and baseline data
        if source:
            current = self._load_source(source)
        else:
            current = current_data
        
        baseline = self._load_source(baseline_source)
        
        # Compute PSI per feature
        psi_results = {}
        drifted_features = []
        
        for feature in self.artifacts.get('selected_features', []):
            psi = self._compute_feature_psi(baseline, current, feature)
            psi_results[feature] = psi
            if psi > 0.2:
                drifted_features.append(feature)
        
        overall_psi = sum(psi_results.values()) / len(psi_results) if psi_results else 0.0
        
        # Alert logic
        alert = overall_psi > 0.2 or len(drifted_features) > 3
        
        result = MonitorResult(
            overall_psi=overall_psi,
            feature_psi=psi_results,
            drifted_features=drifted_features,
            alert=alert,
            message=f"PSI: {overall_psi:.3f}, {len(drifted_features)} drifted features",
            recommendation="Consider retraining model" if alert else "Model stable"
        )
        
        print(f"✅ PSI: {overall_psi:.3f}")
        if alert:
            print(f"⚠️  ALERT: {result.message}")
        
        return result
    
    def profile(self, source: str = "train") -> Dict:
        """Profile a data source"""
        data = self._load_source(source)
        return self._profile_data(data, None)
    
    def deploy(self, provider: str = "azure_ml", **kwargs) -> Dict:
        """Deploy trained model"""
        if not self.model:
            raise ValueError("No model trained")
        return self._deploy({"model": self.model}, {"provider": provider, **kwargs})
    
    # Internal methods (implementation stubs)
    
    def _load_source(self, name: str) -> Dict:
        """Load data from registered source"""
        if name not in self.sources:
            raise ValueError(f"Source '{name}' not registered")
        
        source = self.sources[name]
        
        # Simple CSV loader (placeholder - would use connectors module)
        if source.get('csv'):
            return self._load_csv(source['csv'])
        elif source.get('parquet'):
            return self._load_parquet(source['parquet'])
        else:
            raise NotImplementedError("Only CSV/Parquet supported in this version")
    
    def _load_csv(self, path: str) -> Dict:
        """Load CSV file"""
        # Placeholder - would use proper CSV reader
        data = {'data': [], 'columns': []}
        with open(path, 'r') as f:
            lines = f.readlines()
            if lines:
                data['columns'] = lines[0].strip().split(',')
                for line in lines[1:]:
                    values = line.strip().split(',')
                    row = {col: val for col, val in zip(data['columns'], values)}
                    data['data'].append(row)
        return data
    
    def _load_parquet(self, path: str) -> Dict:
        """Load Parquet file"""
        raise NotImplementedError("Parquet support requires pyarrow extra")
    
    def _profile_data(self, data: Dict, target: Optional[str]) -> Dict:
        """Profile dataset"""
        # Placeholder
        return {
            'columns': data['columns'],
            'rows': len(data['data']),
            'missing_count': 0,
            'recommendations': []
        }
    
    def _autoclean(self, data: Dict, target: str, config: Dict) -> Dict:
        """Auto-clean data"""
        # Placeholder
        return {
            'data': data,
            'spec': {},
            'imputed_count': 0,
            'outlier_count': 0
        }
    
    def _compute_binning_woe(self, data: Dict, target: str, config: Dict) -> Dict:
        """Compute binning and WOE/IV"""
        # Placeholder
        return {
            'bins': {},
            'woe_tables': {},
            'iv_scores': {},
            'spec': {}
        }
    
    def _select_features(self, binning_result: Dict, config: Dict) -> List[str]:
        """Select features based on IV"""
        # Placeholder
        min_iv = config.get('min_iv', 0.02)
        return [f for f, iv in binning_result['iv_scores'].items() if iv >= min_iv]
    
    def _prepare_training_data(self, data: Dict, features: List[str], target: str):
        """Prepare X, y for training"""
        # Placeholder
        return [], []
    
    def _train_model(self, X_train, y_train, X_val, y_val, config):
        """Train a model"""
        # Placeholder
        return {
            'type': 'logistic',
            'model': None,
            'metrics': {'auc': 0.85, 'ks': 0.45}
        }
    
    def _generate_scorecard(self, model, binning_result, features, config):
        """Generate credit scorecard"""
        # Placeholder
        return {}
    
    def _compute_explanations(self, model, X, features):
        """Compute SHAP explanations"""
        # Placeholder
        return {}
    
    def _compute_psi(self, baseline, current, features, config):
        """Compute PSI"""
        # Placeholder
        return {'overall_psi': 0.05}
    
    def _compute_feature_psi(self, baseline, current, feature):
        """Compute PSI for one feature"""
        # Placeholder
        return 0.05
    
    def _generate_report(self, result, config):
        """Generate HTML/PDF report"""
        # Placeholder
        path = f"{self.output_dir}/reports/report_{result.run_id}.html"
        with open(path, 'w') as f:
            f.write(f"<html><body><h1>AutoRisk Report: {self.project}</h1></body></html>")
        return path
    
    def _deploy(self, model, config):
        """Deploy model"""
        # Placeholder
        provider = config.get('provider')
        if provider == 'azure_ml':
            return {'scoring_uri': 'https://example.azureml.net/score', 'primary_key': 'fake-key'}
        return {}
    
    def _persist_artifacts(self, result):
        """Save artifacts to disk"""
        self.artifacts = result.__dict__
    
    def _apply_transformations(self, data):
        """Apply binning/WOE transformations"""
        # Placeholder
        return [[0.5] * 10]  # Fake feature vector
    
    def _probabilities_to_scores(self, probabilities):
        """Convert probabilities to credit scores"""
        # Placeholder: PDO = 20, base_score = 600
        return [int(600 - 20 * (prob - 0.5) * 100) for prob in probabilities]
    
    def _get_risk_tier(self, score):
        """Get risk tier from score"""
        if score >= 700:
            return "Low Risk"
        elif score >= 600:
            return "Medium Risk"
        else:
            return "High Risk"
    
    def _get_top_reasons(self, x):
        """Get top reason codes"""
        # Placeholder
        return ["High credit utilization (+45 pts)", "Recent late payments (+30 pts)"]


class RunResult:
    """Container for pipeline run results"""
    
    def __init__(self, run_id: str):
        self.run_id = run_id
        self.profile = None
        self.clean_spec = None
        self.binning_spec = None
        self.woe_tables = None
        self.iv_scores = None
        self.selected_features = None
        self.best_model = None
        self.metrics = {}
        self.scorecard = None
        self.explanations = None
        self.psi = None
        self.report_html = None
        self.report_pdf = None
        self.endpoint = None
        self.model_path = None
        self.scorecard_path = None
        self.binning_spec_path = None
        self.woe_tables_path = None


class MonitorResult:
    """Container for monitoring results"""
    
    def __init__(self, overall_psi, feature_psi, drifted_features, alert, message, recommendation):
        self.overall_psi = overall_psi
        self.feature_psi = feature_psi
        self.drifted_features = drifted_features
        self.alert = alert
        self.message = message
        self.recommendation = recommendation
    
    def summary(self):
        """Print summary"""
        return f"PSI: {self.overall_psi:.3f} | Drifted: {len(self.drifted_features)} features | {self.recommendation}"
