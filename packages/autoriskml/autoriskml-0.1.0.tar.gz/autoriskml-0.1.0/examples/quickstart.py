"""
AutoRiskML Example: Credit Scoring
Demonstrates the revolutionary automated risk modeling pipeline
"""

print("=" * 80)
print("🚀 AutoRiskML Demo: Credit Scoring")
print("=" * 80)
print()

# Example 1: Basic Credit Scoring
print("📊 Example 1: Basic Credit Scoring Pipeline")
print("-" * 80)

from autoriskml import AutoRisk

# Initialize project
ar = AutoRisk(project="credit_scoring_demo")

# Create sample data (in production, you'd load from CSV/SQL/S3)
import os
sample_csv = "sample_loans.csv"
if not os.path.exists(sample_csv):
    # Create minimal sample data
    with open(sample_csv, 'w') as f:
        f.write("customer_id,age,income,credit_util,loan_amount,default_flag\n")
        f.write("1,25,45000,0.75,5000,1\n")
        f.write("2,35,65000,0.25,10000,0\n")
        f.write("3,45,85000,0.15,15000,0\n")
        f.write("4,28,35000,0.85,3000,1\n")
        f.write("5,52,95000,0.10,20000,0\n")
        f.write("6,33,55000,0.45,8000,0\n")
        f.write("7,41,75000,0.20,12000,0\n")
        f.write("8,29,42000,0.80,6000,1\n")
    print(f"✅ Created sample data: {sample_csv}")

# Register data source
ar.register_source("train", csv=sample_csv)

print("\n🎯 Running automated pipeline...")
print("   This will:")
print("   1. Profile the data")
print("   2. Auto-clean")
print("   3. Compute WOE/IV")
print("   4. Train model")
print("   5. Generate scorecard")
print("   6. Create report")
print()

# Run the full pipeline (THIS IS WHERE THE MAGIC HAPPENS!)
try:
    result = ar.run(
        source="train",
        target="default_flag",
        explain=False,  # Set to True if shap is installed
        persist_artifacts=True
    )
    
    print("\n" + "=" * 80)
    print("✅ PIPELINE COMPLETE!")
    print("=" * 80)
    print(f"📊 Model Performance:")
    print(f"   • Best Model: {result.best_model}")
    print(f"   • AUC: {result.metrics.get('auc', 'N/A')}")
    print(f"   • KS: {result.metrics.get('ks', 'N/A')}")
    print()
    print(f"📁 Artifacts Saved:")
    print(f"   • Output Dir: artifacts/credit_scoring_demo/")
    print(f"   • Report: {result.report_html}")
    print()
    
    # Example 2: Score new customers
    print("=" * 80)
    print("💳 Example 2: Scoring New Customers")
    print("=" * 80)
    
    # Create new customers file
    new_customers_csv = "new_customers.csv"
    with open(new_customers_csv, 'w') as f:
        f.write("customer_id,age,income,credit_util,loan_amount\n")
        f.write("101,30,50000,0.60,7000\n")
        f.write("102,40,80000,0.18,14000\n")
        f.write("103,26,38000,0.90,4000\n")
    
    print(f"✅ Created new customers file: {new_customers_csv}")
    print("\n🎯 Scoring...")
    
    scores = ar.score(new_customers_csv, output="with_reasons")
    
    print("\n📋 Scores:")
    print("-" * 80)
    for score in scores:
        print(f"Customer {score['index']+1}:")
        print(f"   Score: {score['score']}")
        print(f"   Probability: {score['probability']:.2%}")
        print(f"   Risk Tier: {score['risk_tier']}")
        print(f"   Top Reason: {score.get('top_reason', 'N/A')}")
        print()
    
    # Example 3: Monitoring
    print("=" * 80)
    print("📈 Example 3: Drift Monitoring")
    print("=" * 80)
    
    monitor_result = ar.monitor(
        source="train",  # In production, this would be new production data
        baseline_source="train"
    )
    
    print(f"✅ Monitoring Summary:")
    print(f"   {monitor_result.summary()}")
    print()
    
    print("=" * 80)
    print("🎉 AutoRiskML Demo Complete!")
    print("=" * 80)
    print()
    print("🚀 What just happened:")
    print("   ✅ Automated data profiling")
    print("   ✅ Smart data cleaning")
    print("   ✅ WOE/IV computation")
    print("   ✅ Model training & selection")
    print("   ✅ Scorecard generation")
    print("   ✅ Real-time scoring")
    print("   ✅ Drift monitoring")
    print()
    print("📦 This is what a SENIOR RISK DATA SCIENTIST does - automated in ONE command!")
    print()
    print("💡 Next steps:")
    print("   • Load your own data: ar.register_source('mydata', csv='path/to/data.csv')")
    print("   • Deploy to Azure: ar.run(..., deploy={'provider': 'azure_ml'})")
    print("   • Add explainability: pip install autoriskml[explain]")
    print("   • Scale to big data: pip install autoriskml[distributed]")
    print()

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("This is a minimal demo. Full functionality requires implementation of all modules.")
    print("The core API is complete - modules are stubs in this v0.1.0 release.")
    print()
    print("Coming in next releases:")
    print("   • Full binning & WOE/IV engine")
    print("   • PSI/CSI monitoring")
    print("   • SHAP explainability")
    print("   • Azure ML deployment")
    print("   • XGBoost/LightGBM models")
    print()
    print("Star the repo to follow development: https://github.com/idrissbado/AutoRiskML")
