from testAUC import faux_normal_predictions, dashboard

# Simulate a model, evaluated on a Validation set and a Test set:
y_true_val, y_score_val = faux_normal_predictions(neg_mu=0.3, pos_mu=0.8, seed=2023)
y_true_tst, y_score_tst = faux_normal_predictions(std=0.5, neg_mu=0.4, pos_mu=0.9, seed=2023)

# All in one Dashboard to evaluate the Validation vs. Test sets performance
dashboard(y_true_val, y_score_val, y_true_tst, y_score_tst)